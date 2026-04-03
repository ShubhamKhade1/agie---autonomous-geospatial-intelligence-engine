import earthaccess
import os
from typing import List, Dict, Any, Optional

class NASADataPuller:
    def __init__(self):
        # Authentication is handled via earthaccess.login() 
        # which reads from .netrc or environment variables
        pass

    def authenticate(self):
        """Log in to NASA Earthdata."""
        auth = earthaccess.login()
        return auth

    def search_and_download(
        self, 
        short_name: str, 
        bbox: tuple, 
        temporal: tuple, 
        output_dir: str,
        count: int = 10
    ) -> List[str]:
        """
        Search for NASA datasets and download granules.
        :param short_name: Dataset ID (e.g., 'ATL06' for ICESat-2)
        :param bbox: (West, South, East, North)
        :param temporal: (Start Date, End Date)
        :param output_dir: Local path to save files
        :param count: Max number of granules to download
        :return: List of downloaded file paths
        """
        print(f"Searching NASA Earthdata: {short_name}...")
        results = earthaccess.search_data(
            short_name=short_name,
            bounding_box=bbox,
            temporal=temporal,
            count=count
        )
        
        if not results:
            print(f"No results found for {short_name}")
            return []

        print(f"Found {len(results)} granules. Downloading to {output_dir}...")
        downloaded_files = earthaccess.download(results, output_dir)
        return downloaded_files

if __name__ == "__main__":
    # Test example (requires credentials)
    puller = NASADataPuller()
    # puller.authenticate()
    # puller.search_and_download('MOD11A1', (-10, 20, 10, 50), ("2024-01-01", "2024-01-02"), "./data/raw")
