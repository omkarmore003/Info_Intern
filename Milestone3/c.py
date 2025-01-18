import mysql.connector
import pandas as pd

# Connect to MySQL database (update credentials as needed)
conn = mysql.connector.connect(
    host="127.0.0.1",  # Change to your database host
    user="root",       # Your MySQL username
    password="Omkar@003",  # Your MySQL password
    database="inventory_management"  # Database name
)
cursor = conn.cursor()

# Create a new table for adjusted inventory if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS adjusted_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(255),
    product VARCHAR(255),
    original_stock INT,
    adjusted_stock INT,
    adjustment FLOAT,
    risk_level VARCHAR(50)
)
""")

# Create the risk_data table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS risk_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    risk_level VARCHAR(50),
    stock_adjustment FLOAT
)
""")

# Load risk data
risk_data_path = "sentiment_and_risk_analysis_results.csv"
risk_data = pd.read_csv(risk_data_path)

# Adjust stock based on risk levels
def adjust_stock_db(title, risk_level):
    cursor.execute("SELECT country_name, product, stock_level FROM inventory")
    inventory_data = cursor.fetchall()

    for country_name, product, stock_level in inventory_data:
        # Check if both country_name and product match (product is fixed as 'coffee')
        if country_name.lower() in title.lower() and "coffee" in product.lower():  # Ensure product is coffee
            # Adjust stock
            if risk_level == 'High':
                stock_adjustment = stock_level * -0.20  # Decrease by 20%
            elif risk_level == 'Medium':
                stock_adjustment = 0  # No change
            elif risk_level == 'Low':
                stock_adjustment = stock_level * 0.05  # Increase by 5%
            else:
                stock_adjustment = 0

            adjusted_stock = stock_level + stock_adjustment

            # Insert adjusted stock into the new adjusted_inventory table
            cursor.execute("""
                INSERT INTO adjusted_inventory (country_name, product, original_stock, adjusted_stock, adjustment, risk_level)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (country_name, "coffee", stock_level, adjusted_stock, stock_adjustment, risk_level))
            conn.commit()

            # Insert risk data into the risk_data table
            cursor.execute("""
                INSERT INTO risk_data (title, risk_level, stock_adjustment)
                VALUES (%s, %s, %s)
            """, (title, risk_level, stock_adjustment))
            conn.commit()

# Apply adjustments and store data in the new table
for _, row in risk_data.iterrows():
    adjust_stock_db(row['Title'], row['Risk Level'])

# Fetch adjusted inventory for review
cursor.execute("SELECT * FROM adjusted_inventory")
adjusted_inventory = cursor.fetchall()

# Convert to DataFrame and display the adjusted inventory
adjusted_inventory_df = pd.DataFrame(adjusted_inventory, columns=["ID", "Country Name", "Product", "Original Stock", "Adjusted Stock", "Adjustment", "Risk Level"])
print(adjusted_inventory_df)

# Save the adjusted inventory to a CSV file
adjusted_inventory_df.to_csv('adjusted_inventory.csv', index=False)

# Fetch risk data for review
cursor.execute("SELECT * FROM risk_data")
risk_data_fetched = cursor.fetchall()

# Display the risk data
risk_data_df = pd.DataFrame(risk_data_fetched, columns=["ID", "Title", "Risk Level", "Stock Adjustment"])
print(risk_data_df)

# Close the database connection
conn.close()
