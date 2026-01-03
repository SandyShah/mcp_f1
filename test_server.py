"""Test script for FastF1 MCP Server - Direct Function Test"""

import os
import tempfile
import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt

# Initialize cache
cache_dir = '/tmp/fastf1_cache'
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)
print(f"FastF1 cache enabled at: {cache_dir}")

def compare_qualifying_laps(year: int, race: str, session: str = "Q") -> str:
    """Test version of compare_qualifying_laps"""
    try:
        print(f"\nLoading {year} {race} {session} session...")
        quali = fastf1.get_session(year, race, session)
        quali.load(telemetry=True)
        
        print("Session loaded successfully!")
        print(f"Total drivers: {len(quali.results)}")
        
        # Get top 3 drivers from results
        top3 = quali.results.head(3)
        
        # Extract telemetry for each top 3 driver
        telemetry_data = []
        for idx, driver_result in top3.iterrows():
            driver_abbr = driver_result['Abbreviation']
            print(f"Processing {driver_abbr}...")
            
            # Get all laps for this driver
            driver_laps = quali.laps.pick_driver(driver_abbr)
            
            if len(driver_laps) == 0:
                continue
            
            # Get the fastest lap
            fastest_lap = driver_laps.pick_fastest()
            
            # Get telemetry
            telemetry = fastest_lap.get_telemetry()
            
            # Get team color for visualization
            try:
                team_color = plotting.get_team_color(driver_result['TeamName'], session=quali)
            except (AttributeError, TypeError, KeyError):
                colors = ['#3671C6', '#27F4D2', '#FF8700']
                team_color = colors[len(telemetry_data) % 3]
            
            telemetry_data.append({
                'driver': driver_abbr,
                'name': driver_result['FullName'],
                'team': driver_result['TeamName'],
                'lap_time': fastest_lap['LapTime'],
                'telemetry': telemetry,
                'color': team_color
            })
        
        print(f"\nSuccessfully extracted telemetry for {len(telemetry_data)} drivers")
        
        # Create visualization with 3 plots
        print("Creating visualizations...")
        fig, axes = plt.subplots(3, 1, figsize=(16, 12))
        
        # Plot 1: Speed Comparison
        ax_speed = axes[0]
        for data in telemetry_data:
            tel = data['telemetry']
            ax_speed.plot(tel['Distance'], tel['Speed'], 
                        color=data['color'], 
                        label=f"{data['driver']} - {data['lap_time']}", 
                        linewidth=2.5)
        
        ax_speed.set_ylabel('Speed (km/h)', fontsize=12, fontweight='bold')
        ax_speed.set_title(f'{year} {race} - Top 3 Qualifying Laps Speed Comparison', 
                         fontsize=14, fontweight='bold')
        ax_speed.legend(loc='upper right', fontsize=10)
        ax_speed.grid(True, alpha=0.3)
        
        # Plot 2: Throttle/Brake Combined (Dual Y-axis)
        ax_throttle = axes[1]
        ax_brake = ax_throttle.twinx()
        
        for i, data in enumerate(telemetry_data):
            tel = data['telemetry']
            # Throttle
            if i == 0:
                ax_throttle.plot(tel['Distance'], tel['Throttle'], 
                               color=data['color'], 
                               label=f"{data['driver']} - Throttle", 
                               linewidth=2, 
                               alpha=0.7,
                               linestyle='-')
            
            # Brake
            ax_brake.plot(tel['Distance'], tel['Brake'], 
                        color=data['color'], 
                        label=f"{data['driver']} - Brake", 
                        linewidth=2, 
                        alpha=0.9,
                        linestyle='--')
        
        ax_throttle.set_ylabel('Throttle (%)', fontsize=12, fontweight='bold', color='green')
        ax_brake.set_ylabel('Brake', fontsize=12, fontweight='bold', color='red')
        ax_throttle.set_title('Throttle (solid) and Brake (dashed) Application', 
                            fontsize=14, fontweight='bold')
        ax_throttle.tick_params(axis='y', labelcolor='green')
        ax_brake.tick_params(axis='y', labelcolor='red')
        ax_throttle.grid(True, alpha=0.3)
        
        lines1, labels1 = ax_throttle.get_legend_handles_labels()
        lines2, labels2 = ax_brake.get_legend_handles_labels()
        ax_throttle.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=9)
        
        # Plot 3: Speed with all 3 drivers (detailed)
        ax_detail = axes[2]
        for data in telemetry_data:
            tel = data['telemetry']
            ax_detail.plot(tel['Distance'], tel['Speed'], 
                         color=data['color'], 
                         label=data['driver'], 
                         linewidth=2.5,
                         alpha=0.8)
        
        ax_detail.set_ylabel('Speed (km/h)', fontsize=12, fontweight='bold')
        ax_detail.set_xlabel('Distance (m)', fontsize=12, fontweight='bold')
        ax_detail.set_title('Detailed Speed Trace Comparison', 
                          fontsize=14, fontweight='bold')
        ax_detail.legend(loc='upper right', fontsize=10)
        ax_detail.grid(True, alpha=0.3)
        ax_detail.fill_between(telemetry_data[0]['telemetry']['Distance'], 
                              0, 
                              telemetry_data[0]['telemetry']['Speed'], 
                              alpha=0.1, 
                              color=telemetry_data[0]['color'])
        
        plt.tight_layout()
        
        # Save to file
        output_dir = tempfile.gettempdir()
        filename = f"f1_qualifying_{year}_{race}_{session}_top3_comparison.png"
        output_path = os.path.join(output_dir, filename)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Visualization saved to: {output_path}")
        
        # Build summary
        summary = f"""
╔══════════════════════════════════════════════════════════════════╗
║  {year} {race} - Qualifying Top 3 Comparison
╚══════════════════════════════════════════════════════════════════╝

Top 3 Fastest Lap Times:
"""
        
        for i, data in enumerate(telemetry_data, 1):
            summary += f"  {i}. {data['name']:25s} ({data['team']:20s}): {data['lap_time']}\n"
        
        summary += f"""
Visualization Details:
  📊 Plot 1: Speed comparison across all 3 drivers
  📊 Plot 2: Throttle (solid) and Brake (dashed) - Dual Y-axis
  📊 Plot 3: Detailed speed trace with shaded area

📁 Visualization saved to: {output_path}
"""
        
        return summary
        
    except Exception as e:
        return f"Error: {str(e)}"


# Run test
print("="*80)
print("Testing FastF1 MCP Server - compare_qualifying_laps tool")
print("="*80)

result = compare_qualifying_laps(year=2024, race='Monaco', session='Q')
print(result)

print("="*80)
print("Test completed!")
