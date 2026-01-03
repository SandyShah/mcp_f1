"""Analysis tools for FastF1 MCP Server"""

import os
import tempfile
import subprocess
import platform
from typing import Any
import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt
import numpy as np


def register_analysis_tools(mcp: Any) -> None:
    """
    Register analysis tools with the MCP server.
    
    Args:
        mcp: FastMCP server instance
    """
    
    @mcp.tool()
    def compare_qualifying_laps(year: int, race: str, session: str = "Q") -> str:
        """
        Compare qualifying laps for top 3 drivers with telemetry visualization.
        
        Analyzes the fastest qualifying laps of the top 3 drivers and generates
        detailed telemetry comparisons including speed maps, throttle, and brake data.
        Automatically opens the visualization and displays top 10 qualifiers.
        
        Args:
            year: Season year (e.g., 2024)
            race: Race name or round number (e.g., 'Monaco', 'Monza', or '1')
            session: Session type (default: 'Q' for qualifying)
        
        Returns:
            Summary text with top 10 driver lap times and visualization file path
        """
        try:
            # Load the qualifying session
            quali = fastf1.get_session(year, race, session)
            quali.load(telemetry=True)
            
            # Get top 3 drivers from results for telemetry comparison
            if not hasattr(quali, 'results') or quali.results is None or len(quali.results) == 0:
                return f"Error: No results found for {year} {race} {session}"
            
            if len(quali.results) < 3:
                return f"Error: Insufficient drivers in session. Found {len(quali.results)}, need at least 3."
            
            # Get top 10 for results display
            top10 = quali.results.head(10)
            top3 = quali.results.head(3)
            
            # Extract telemetry for each top 3 driver
            telemetry_data = []
            for idx, driver_result in top3.iterrows():
                driver_abbr = driver_result['Abbreviation']
                
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
                    # Fallback colors
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
            
            if len(telemetry_data) < 3:
                return f"Error: Could not extract telemetry for 3 drivers. Found {len(telemetry_data)}."
            
            # Create visualization with 3 plots
            fig, axes = plt.subplots(3, 1, figsize=(16, 12))
            
            # Helper function to format lap time
            def format_lap_time(lap_time):
                if hasattr(lap_time, 'total_seconds'):
                    total_ms = lap_time.total_seconds() * 1000
                    minutes = int(total_ms // 60000)
                    seconds = int((total_ms % 60000) // 1000)
                    milliseconds = int(total_ms % 1000)
                    return f"{minutes}:{seconds:02d}.{milliseconds:03d}"
                return str(lap_time)
            
            # Plot 1: Speed Comparison
            ax_speed = axes[0]
            for data in telemetry_data:
                tel = data['telemetry']
                formatted_time = format_lap_time(data['lap_time'])
                ax_speed.plot(tel['Distance'], tel['Speed'], 
                            color=data['color'], 
                            label=f"{data['driver']} - {formatted_time}", 
                            linewidth=2.5)
            
            ax_speed.set_ylabel('Speed (km/h)', fontsize=12, fontweight='bold')
            ax_speed.set_title(f'{year} {race} - Top 3 Qualifying Laps Speed Comparison', 
                             fontsize=14, fontweight='bold')
            ax_speed.legend(loc='upper right', fontsize=10)
            ax_speed.grid(True, alpha=0.3)
            
            # Plot 2: Throttle Only - All 3 drivers
            ax_throttle = axes[1]
            
            for i, data in enumerate(telemetry_data):
                tel = data['telemetry']
                # Throttle - show all 3 drivers with different line styles
                line_styles = ['-', '--', '-.']
                ax_throttle.plot(tel['Distance'], tel['Throttle'], 
                               color=data['color'], 
                               label=f"{data['driver']}", 
                               linewidth=2.5, 
                               alpha=0.85,
                               linestyle=line_styles[i])
            
            ax_throttle.set_ylabel('Throttle (%)', fontsize=12, fontweight='bold')
            ax_throttle.set_xlabel('Distance (m)', fontsize=12, fontweight='bold')
            ax_throttle.set_title('Throttle Application Comparison', 
                                fontsize=14, fontweight='bold')
            ax_throttle.legend(loc='upper right', fontsize=10)
            ax_throttle.grid(True, alpha=0.3)
            ax_throttle.set_ylim(0, 105)
            
            # Plot 3: Brake Only - All 3 drivers
            ax_brake = axes[2]
            
            for i, data in enumerate(telemetry_data):
                tel = data['telemetry']
                # Brake - show all 3 drivers with different line styles
                brake_styles = ['-', '--', '-.']
                ax_brake.plot(tel['Distance'], tel['Brake'] * 100,  # Scale brake to 0-100
                            color=data['color'], 
                            label=f"{data['driver']}", 
                            linewidth=2.5, 
                            alpha=0.85,
                            linestyle=brake_styles[i])
            
            ax_brake.set_ylabel('Brake (%)', fontsize=12, fontweight='bold')
            ax_brake.set_xlabel('Distance (m)', fontsize=12, fontweight='bold')
            ax_brake.set_title('Brake Application Comparison', 
                              fontsize=14, fontweight='bold')
            ax_brake.legend(loc='upper right', fontsize=10)
            ax_brake.grid(True, alpha=0.3)
            ax_brake.set_ylim(0, 105)
            
            plt.tight_layout()
            
            # Save to workspace directory for VS Code preview
            # Get the workspace root (go up from server directory)
            workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            output_dir = os.path.join(workspace_root, 'f1_visualizations')
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"f1_qualifying_{year}_{race}_{session}_top3_comparison.png"
            output_path = os.path.join(output_dir, filename)
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            # Open the image in VS Code
            try:
                subprocess.run(['code', output_path], check=False)
            except Exception:
                pass  # Silently ignore if VS Code command is not available
            
            # Build summary text with top 10 results
            summary = f"""
╔══════════════════════════════════════════════════════════════════╗
║  {year} {race} - Qualifying Results
╚══════════════════════════════════════════════════════════════════╝

🏆 TOP 10 QUALIFYING TIMES:
┌──────┬─────────────────────────────┬──────────────────────┬──────────────┐
│ Pos  │ Driver                      │ Team                 │ Best Lap     │
├──────┼─────────────────────────────┼──────────────────────┼──────────────┤
"""
            
            for idx, driver_result in top10.iterrows():
                # Use direct indexing instead of .get() for pandas Series
                pos = driver_result['Position'] if 'Position' in driver_result else idx + 1
                name = driver_result['FullName'] if 'FullName' in driver_result else 'Unknown'
                team = driver_result['TeamName'] if 'TeamName' in driver_result else 'Unknown'
                
                # Get the best lap time
                driver_abbr = driver_result['Abbreviation'] if 'Abbreviation' in driver_result else ''
                driver_laps = quali.laps.pick_driver(driver_abbr)
                if len(driver_laps) > 0:
                    best_lap = driver_laps.pick_fastest()
                    lap_time = best_lap['LapTime']
                else:
                    # Try Q3, then Q2, then Q1
                    lap_time = None
                    for q_session in ['Q3', 'Q2', 'Q1']:
                        if q_session in driver_result and driver_result[q_session] is not None:
                            lap_time = driver_result[q_session]
                            break
                    if lap_time is None:
                        lap_time = 'No Time'
                
                # Format lap time nicely
                if hasattr(lap_time, 'total_seconds') and lap_time is not None:
                    try:
                        total_ms = lap_time.total_seconds() * 1000
                        minutes = int(total_ms // 60000)
                        seconds = int((total_ms % 60000) // 1000)
                        milliseconds = int(total_ms % 1000)
                        time_str = f"{minutes}:{seconds:02d}.{milliseconds:03d}"
                    except:
                        time_str = str(lap_time)
                else:
                    time_str = str(lap_time) if lap_time is not None else 'No Time'
                
                # Convert pos to string for formatting - handle NaN/None
                try:
                    if pos is None or (isinstance(pos, float) and np.isnan(pos)):
                        pos_str = str(idx + 1)
                    else:
                        pos_str = str(int(float(pos)))
                except:
                    pos_str = str(idx + 1)
                
                summary += f"│ {pos_str:^4} │ {name:27s} │ {team:20s} │ {time_str:12s} │\n"
            
            summary += f"""└──────┴─────────────────────────────┴──────────────────────┴──────────────┘

📊 TELEMETRY VISUALIZATION (Top 3):
  • Plot 1: Speed comparison across all 3 drivers
  • Plot 2: Throttle application only - All 3 drivers
  • Plot 3: Brake application only - All 3 drivers

📁 Visualization saved to: {output_path}
📂 Open the image in VS Code to view the telemetry comparison

Analysis complete! The visualization shows:
- Speed differences across the lap
- Throttle application patterns for each driver
- Brake application patterns for each driver
"""
            
            return summary
            
        except Exception as e:
            return f"Error analyzing qualifying laps: {str(e)}\n\nPlease check:\n- Year and race name are correct\n- Session type is valid (Q, Q1, Q2, Q3)\n- Telemetry data is available for this session"
    
    @mcp.tool()
    def visualize_tyre_strategy(year: int, race: str, session: str = "R") -> str:
        """
        Create an enhanced tyre strategy visualization for a race.
        
        Generates a horizontal stacked bar chart showing each driver's tyre strategy
        throughout the race, including compound types, stint lengths, and pit stops.
        Drivers are ordered by race results (points).
        
        Args:
            year: Season year (e.g., 2024)
            race: Race name or round number (e.g., 'Monaco', 'Abu Dhabi', or '1')
            session: Session type (default: 'R' for race)
        
        Returns:
            Summary text with tyre strategy stats and visualization file path
        """
        try:
            # Load the race session
            race_session = fastf1.get_session(year, race, session)
            race_session.load()
            
            # Get all laps with tyre information
            laps_tyre = race_session.laps
            
            if len(laps_tyre) == 0:
                return f"Error: No lap data found for {year} {race} {session}"
            
            # Check if tyre data is available
            if 'Compound' not in laps_tyre.columns:
                return f"Error: Tyre compound data not available for this session"
            
            # Create visualization
            fig, ax = plt.subplots(figsize=(18, 12))
            
            # Set background color
            ax.set_facecolor('#f0f0f0')
            fig.patch.set_facecolor('white')
            
            # Get race results to order drivers
            results = race_session.results.sort_values('Points', ascending=False)
            driver_order = results['Abbreviation'].tolist()
            
            # Filter to only drivers who finished
            finished_drivers = [d for d in driver_order if d in laps_tyre['Driver'].unique()]
            
            # Define tyre colors
            tyre_colors = {
                'SOFT': '#E8002D',      # Red
                'MEDIUM': '#FFED00',    # Yellow
                'HARD': '#FFFFFF',      # White
                'INTERMEDIATE': '#00AA00',  # Green
                'WET': '#0080FF'        # Blue
            }
            
            # Get unique compounds used in the race
            compounds_used = laps_tyre['Compound'].unique()
            
            # Process data for each driver
            driver_data = []
            for driver in finished_drivers:
                driver_laps = laps_tyre.pick_driver(driver).sort_values('LapNumber')
                
                stint_info = []
                for stint in sorted(driver_laps['Stint'].unique()):
                    stint_laps = driver_laps[driver_laps['Stint'] == stint]
                    compound = stint_laps['Compound'].iloc[0]
                    start_lap = stint_laps['LapNumber'].min()
                    end_lap = stint_laps['LapNumber'].max()
                    laps_count = int(end_lap - start_lap + 1)
                    
                    stint_info.append({
                        'start_lap': start_lap,
                        'laps_count': laps_count,
                        'compound': compound,
                        'color': tyre_colors.get(compound, '#808080')
                    })
                
                driver_data.append({
                    'driver': driver,
                    'stints': stint_info
                })
            
            # Plot bars
            y_pos = np.arange(len(driver_data))
            for idx, data in enumerate(driver_data):
                left_pos = 0
                for stint in data['stints']:
                    # Draw bar with black edge
                    ax.barh(idx, stint['laps_count'], left=left_pos, 
                            color=stint['color'], edgecolor='black', linewidth=1.5,
                            height=0.7)
                    
                    # Add lap count text in the middle of each stint bar
                    text_color = 'black' if stint['compound'] not in ['SOFT', 'INTERMEDIATE', 'WET'] else 'white'
                    ax.text(left_pos + stint['laps_count']/2, idx, 
                           f"{stint['laps_count']}", 
                           va='center', ha='center', fontsize=14, fontweight='bold',
                           color=text_color)
                    
                    left_pos += stint['laps_count']
                
                # Add total laps at the end of the bar
                ax.text(left_pos + 2, idx, f"({int(left_pos)})", 
                       va='center', ha='left', fontsize=9, fontweight='bold', color='#333333')
            
            # Customize plot
            ax.set_yticks(y_pos)
            ax.set_yticklabels([d['driver'] for d in driver_data], fontsize=12, fontweight='bold')
            ax.set_xlabel('Lap Number', fontsize=13, fontweight='bold')
            ax.set_title(f'{year} {race} - Tyre Strategy by Driver\n(Ordered by Race Results)', 
                        fontsize=15, fontweight='bold', pad=20)
            ax.invert_yaxis()
            ax.grid(axis='x', alpha=0.4, linestyle='--', linewidth=0.8)
            ax.set_axisbelow(True)
            
            # Set x-axis limits with padding
            max_laps = max(sum(s['laps_count'] for s in d['stints']) for d in driver_data)
            ax.set_xlim(0, max_laps + 5)
            
            # Create custom legend
            legend_labels = []
            for compound in ['SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET']:
                if compound in compounds_used:
                    legend_labels.append(compound)
            
            legend_elements = [plt.Rectangle((0,0),1,1, facecolor=tyre_colors[compound], 
                                              edgecolor='black', linewidth=1.5, label=compound)
                               for compound in legend_labels]
            
            ax.legend(handles=legend_elements, loc='upper right', fontsize=14, 
                     title='Tyre Compound', title_fontsize=15, framealpha=0.95,
                     edgecolor='black', fancybox=True)
            
            # Adjust layout
            plt.tight_layout()
            
            # Save to workspace directory for VS Code preview
            workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            output_dir = os.path.join(workspace_root, 'f1_visualizations')
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"f1_tyre_strategy_{year}_{race}_{session}.png"
            output_path = os.path.join(output_dir, filename)
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            # Open the image in VS Code
            try:
                subprocess.run(['code', output_path], check=False)
            except Exception:
                pass  # Silently ignore if VS Code command is not available
            
            # Calculate summary statistics
            total_drivers = len(finished_drivers)
            compound_stats = {}
            for compound in compounds_used:
                drivers_using = len(laps_tyre[laps_tyre['Compound'] == compound]['Driver'].unique())
                compound_stats[compound] = drivers_using
            
            # Build summary text
            summary = f"""
╔══════════════════════════════════════════════════════════════════╗
║  {year} {race} - Tyre Strategy Analysis
╚══════════════════════════════════════════════════════════════════╝

🏁 RACE OVERVIEW:
  • Total drivers shown: {total_drivers}
  • Total laps in race: {max_laps}
  • Tyre compounds used: {', '.join(sorted(compounds_used))}

📊 COMPOUND USAGE:
"""
            
            for compound in sorted(compounds_used):
                count = compound_stats.get(compound, 0)
                emoji = {'SOFT': '🔴', 'MEDIUM': '🟡', 'HARD': '⚪', 
                        'INTERMEDIATE': '🟢', 'WET': '🔵'}.get(compound, '⚫')
                summary += f"  {emoji} {compound:12s} - {count:2d} drivers used this compound\n"
            
            summary += f"""
🏎️  TYRE STRATEGY INSIGHTS:
  • Each bar represents one driver (ordered by points)
  • Bar segments show different stints with tyre compounds
  • Numbers in segments indicate stint length in laps
  • Numbers in parentheses show total laps completed

📁 Visualization saved to: {output_path}
📂 Open the image in VS Code to view the detailed strategy chart

Color Legend:
  🔴 SOFT (Red) - Softest compound, highest grip, fastest degradation
  🟡 MEDIUM (Yellow) - Medium compound, balanced performance
  ⚪ HARD (White) - Hardest compound, lowest grip, slowest degradation
  🟢 INTERMEDIATE (Green) - Wet weather, medium grip
  🔵 WET (Blue) - Full wet weather conditions
"""
            
            return summary
            
        except Exception as e:
            return f"Error creating tyre strategy visualization: {str(e)}\n\nPlease check:\n- Year and race name are correct\n- Session type is valid (R for race)\n- Tyre data is available for this session"
