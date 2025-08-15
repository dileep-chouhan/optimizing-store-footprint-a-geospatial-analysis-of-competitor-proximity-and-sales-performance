import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
# --- 1. Synthetic Data Generation ---
# Generate synthetic data for store locations, competitor density, demographics, and sales
np.random.seed(42)  # for reproducibility
num_stores = 100
data = {
    'StoreID': range(1, num_stores + 1),
    'Latitude': np.random.uniform(34, 35, num_stores),
    'Longitude': np.random.uniform(-118, -117, num_stores),
    'CompetitorDensity': np.random.randint(1, 10, num_stores), # Density score (1-10)
    'AvgIncome': np.random.randint(40000, 120000, num_stores),
    'Sales': np.random.randint(50000, 500000, num_stores)
}
df = pd.DataFrame(data)
# Create geometry column for geospatial analysis
df['geometry'] = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326") #WGS84
# --- 2. Analysis ---
# Calculate correlation between sales and competitor density
correlation = df['Sales'].corr(df['CompetitorDensity'])
print(f"Correlation between Sales and Competitor Density: {correlation}")
# Calculate average sales by income bracket (example: high, medium, low)
df['IncomeBracket'] = pd.qcut(df['AvgIncome'], 3, labels=['Low', 'Medium', 'High'])
average_sales_by_income = df.groupby('IncomeBracket')['Sales'].mean()
print("\nAverage Sales by Income Bracket:")
print(average_sales_by_income)
# --- 3. Visualization ---
# Create a scatter plot of store locations, colored by sales
plt.figure(figsize=(10, 6))
plt.scatter(gdf['Longitude'], gdf['Latitude'], c=gdf['Sales'], cmap='viridis', s=50)
plt.colorbar(label='Sales')
plt.title('Store Locations and Sales')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('store_locations.png')
print("Plot saved to store_locations.png")
# Create a bar chart of average sales by income bracket
plt.figure(figsize=(8, 6))
average_sales_by_income.plot(kind='bar')
plt.title('Average Sales by Income Bracket')
plt.xlabel('Income Bracket')
plt.ylabel('Average Sales')
plt.savefig('sales_by_income.png')
print("Plot saved to sales_by_income.png")
#Handle potential errors during file saving
try:
    plt.savefig('sales_by_income.png')
    print("Plot saved to sales_by_income.png")
except Exception as e:
    print(f"Error saving plot: {e}")