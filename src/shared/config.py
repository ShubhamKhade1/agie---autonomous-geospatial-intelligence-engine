from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import yaml
import os

class ROI(BaseModel):
    id: str
    name: str
    bbox: List[float] = Field(..., min_items=4, max_items=4) # [min_lon, min_lat, max_lon, max_lat]
    description: Optional[str] = None
    priority: int = 1

class ROIConfig(BaseModel):
    rois: List[ROI]

def load_rois(config_path: str = "config/rois.yaml") -> List[ROI]:
    """Load ROIs from a YAML file."""
    if not os.path.exists(config_path):
        # Default fallback
        return [ROI(id="default", name="Default Region", bbox=[-10.0, 20.0, 10.0, 50.0])]
    
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)
        config = ROIConfig(**config_data)
        return config.rois

if __name__ == "__main__":
    # Test ROI creation
    roi = ROI(id="india_coast", name="West Coast of India", bbox=[68.0, 8.0, 77.0, 20.0])
    print(roi.model_dump_json())
