from plantnet_api import PlantNetAPI

def main():
    # Set up PlantNet API
    plantnet_api = PlantNetAPI(api_key="2b10X3YLMd8PNAuKOCVPt7MeUe")
    
    # Example usage of PlantNetAPI
    plant = plantnet_api.identify_plant("monstera.jpg")
    print(plant)

if __name__ == "__main__":
    main()

