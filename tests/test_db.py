import sys
import os

# Ensure the src directory is in the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from db_manager import DBManager

def test_db_connection():
    """Test MongoDB connection and data retrieval."""
    db = DBManager()
    sample_plant = "Comptonia peregrina"  # Replace with an actual plant in your database

    # Fetch care instructions for the sample plant
    care_instructions = db.get_care_instructions(sample_plant)

    # Check if the care instructions were retrieved and print the result
    if care_instructions:
        print("✅ Successfully retrieved care instructions:")
        print(care_instructions)
    else:
        print("❌ No care instructions found for:", sample_plant)

if __name__ == "__main__":
    test_db_connection()

