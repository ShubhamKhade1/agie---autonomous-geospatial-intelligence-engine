import copernicusmarine
import os
from typing import List, Dict, Any, Optional

class CopernicusDataPuller:
    def __init__(self):
        # Authentication is handled via copernicusmarine.login()
        pass

    def authenticate(self):
        """Log in to Copernicus Marine Service."""
        # Use COPERNICUS_USERNAME and COPERNICUS_PASSWORD environment variables
        pass

    def subset_and_download(
        self, 
        dataset_id: str, 
        bbox: tuple, 
        temporal: tuple, 
        output_dir: str,
        variables: Optional[List[str]] = None
    ) -> str:
        """
        Subset and download Copernicus CMEMS data.
        :param dataset_id: Dataset ID (e.g., 'cmems_mod_glo_phy_my_0.083deg_P1D-m')
        :param bbox: (West, South, East, North) -> (min_lon, min_lat, max_lon, max_lat)
        :param temporal: (Start DateTime, End DateTime)
        :param output_dir: Local path to save files
        :param variables: List of variables to extract (e.g., ["thetao"])
        :return: Path to the downloaded file
        """
        min_lon, min_lat, max_lon, max_lat = bbox
        start_datetime, end_datetime = temporal

        print(f"Subsetting Copernicus CMEMS data: {dataset_id}...")
        
        output_file = f"{dataset_id.replace('.', '_')}_subset.nc"
        
        # copernicusmarine.subset downloads the data to a file
        copernicusmarine.subset(
            dataset_id=dataset_id,
            variables=variables,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            minimum_longitude=min_lon,
            maximum_longitude=max_lon,
            minimum_latitude=min_lat,
            maximum_latitude=max_lat,
            output_directory=output_dir,
            output_filename=output_file,
            force_download=True
        )
        
        return os.path.join(output_dir, output_file)

if __name__ == "__main__":
    # Test example
    puller = CopernicusDataPuller()
    # puller.subset_and_download(
    #     'cmems_mod_glo_phy_my_0.083deg_P1D-m', 
    #     (-26, 14, -22, 18), 
    #     ("2020-01-01T00:00:00", "2020-01-02T00:00:00"), 
    #     "./data/raw"
    # )
