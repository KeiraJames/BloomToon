import sys
import os

# Add the src directory to the Python path (so we can import plantnet_api from src)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Now, import the class from the src/plantnet_api.py
from plantnet_api import PlantNetAPI

def test_identify_plant():
    # Use an absolute or correctly relative path to the image
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/images/monstera.jpg'))
    
    plantnet_api = PlantNetAPI(api_key="2b10X3YLMd8PNAuKOCVPt7MeUe")
    plant = plantnet_api.identify_plant(image_path)
    
    # Print to verify the plant is identified
    print(f"Identified plant: {plant}")

if __name__ == "__main__":
    test_identify_plant()

