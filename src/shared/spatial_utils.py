import h3
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Any

class SpatialUtils:
    @staticmethod
    def latlng_to_h3(lat: float, lng: float, resolution: int = 9) -> str:
        """Convert latitude/longitude to an H3 index."""
        return h3.latlng_to_h3(lat, lng, resolution)

    @staticmethod
    def h3_to_latlng(h3_index: str) -> Tuple[float, float]:
        """Convert an H3 index to latitude/longitude."""
        return h3.h3_to_latlng(h3_index)

    @staticmethod
    def get_h3_polygons(bbox: List[float], resolution: int = 7) -> List[str]:
        """
        Get all H3 indices covering a bounding box.
        :param bbox: [min_lon, min_lat, max_lon, max_lat]
        :param resolution: H3 resolution level
        :return: List of H3 hex indices
        """
        min_lon, min_lat, max_lon, max_lat = bbox
        
        # Define the bounding box polygon
        geojson_poly = {
            "type": "Polygon",
            "coordinates": [[
                [min_lon, min_lat],
                [max_lon, min_lat],
                [max_lon, max_lat],
                [min_lon, max_lat],
                [min_lon, min_lat]
            ]]
        }
        
        # h3.polyfill takes (GeoJSON, resolution)
        # Note: h3-py version differences might affect this, but standard version is:
        return list(h3.polyfill(geojson_poly, resolution))

    @staticmethod
    def aggregate_by_h3(df: pd.DataFrame, lat_col: str, lng_col: str, resolution: int = 7) -> pd.DataFrame:
        """
        Aggregate a flat dataframe by H3 resolution.
        """
        df['h3_index'] = df.apply(lambda x: h3.latlng_to_h3(x[lat_col], x[lng_col], resolution), axis=1)
        return df.groupby('h3_index').mean()

if __name__ == "__main__":
    utils = SpatialUtils()
    # print(utils.latlng_to_h3(18.975, 72.825))
