from pymongo import MongoClient

class DBManager:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://keirajames2003:SP3P4kpkCQYnW8wS@cluster0.i7fqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client['plants']
        self.collection = self.db['c1']

    def get_care_instructions(self, genus_species):
        genus, species = genus_species.split()  # Split genus and species

        # Query MongoDB for care instructions
        plant = self.collection.find_one({
            f"Genus.{genus}.{species}": {"$exists": True}  # Check if the species exists under the genus
        })

        if plant:
            # Extract care instructions from the right path
            care_instructions = plant["Genus"][genus].get(species, {})
            if care_instructions:
                formatted_care_instructions = (
                    f"Care Instructions for {genus_species}:\n"
                    f"Water: {care_instructions.get('water', 'N/A')}\n"
                    f"Sunlight: {care_instructions.get('sunlight', 'N/A')}\n"
                    f"Soil: {care_instructions.get('soil', 'N/A')}\n"
                )
                return formatted_care_instructions
            else:
                return "Care instructions not available for this species."
        else:
            return "Care instructions not found for this plant."

