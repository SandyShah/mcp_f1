"""FastF1 cache management utilities"""

import os
import fastf1


def init_cache(cache_dir: str = "/tmp/fastf1_cache") -> None:
    """
    Initialize FastF1 cache directory.
    
    This enables caching of FastF1 API responses to speed up repeated requests
    and reduce load on the F1 timing data servers.
    
    Args:
        cache_dir: Directory path for cache storage (default: /tmp/fastf1_cache)
    """
    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)
    
    # Enable FastF1 caching
    fastf1.Cache.enable_cache(cache_dir)
    
    print(f"FastF1 cache enabled at: {cache_dir}")
