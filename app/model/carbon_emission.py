import os

import pandas as pd

dirname = os.path.dirname(__file__)
# classification csv
food_carbon_classification_datasets_path = os.path.join(dirname, 'BREEZE_Food_Carbon_Emission_Classification.csv')
classification_df = pd.read_csv(food_carbon_classification_datasets_path)
# segmentation csv
food_carbon_segmentation_datasets_path = os.path.join(dirname, 'BREEZE_Food_Carbon_Emission_Segmentation.csv')
segmentation_df = pd.read_csv(food_carbon_segmentation_datasets_path)

def getCarbonEmission(name: str):
  """Get Food Recipe and Emission"""
  # Filter the dataframe by name
  filtered_df = classification_df[classification_df['MAKANAN'] == name]

  # Filter columns
  filtered_df = filtered_df[['BAHAN', 'BERAT (kg)', 'Carbon Footprint']]

  ingredients = []
  for _, row in filtered_df.iterrows():
    ingredients.append({
      "bahan": row['BAHAN'],
      "berat": row['BERAT (kg)'],
      "carbon_footprint": row['Carbon Footprint']
    })

  # Calculate total emissions
  total_emissions = filtered_df['Carbon Footprint'].sum()

  return ingredients, total_emissions

def getCarbonEmissionSegmentation(ingredients_list: list):
  """Get Ingredients Segmentation and Emission"""
  ingredients = []
  total_emission = 0

  for _, row in segmentation_df.iterrows():
    name = row['Food Product'].lower()
    name = row['Food Product'].strip()
    if (name in ingredients_list):
      total_emission += row['Carbon Footprint']
      ingredients.append({
        "bahan": row['Food Product'],
        "berat": row['Weight (kg)'],
        "carbon_footprint": row['Carbon Footprint']
      })

  return ingredients, total_emission