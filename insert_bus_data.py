import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",  # Replace with your MySQL username
    password="your_password",  # Replace with your MySQL password
    database="your_database"  # Replace with your database name
)
cursor = conn.cursor()

# Create table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS bus_routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(255),
    busname VARCHAR(255),
    arrival_time DATETIME,
    duration VARCHAR(255),
    fare DECIMAL(10, 2),
    seats_available VARCHAR(255),
    rating VARCHAR(10),
    departure_location VARCHAR(255),
    arrival_location VARCHAR(255)
);
'''
cursor.execute(create_table_query)

# Function to insert data
def insert_data(data):
    insert_query = '''
    INSERT INTO bus_routes (
        route_name, busname, arrival_time, duration, fare,
        seats_available, rating, departure_location, arrival_location
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (
        data.get('route-collected'),
        data.get('name'),
        data.get('arrival_time'),
        data.get('duration'),
        data.get('fare'),
        data.get('seats_available'),
        data.get('rating'),
        data.get('departure_location'),
        data.get('arrival_location')
    ))
    conn.commit()

# Insert the scraped data
for bus in kerala_bus_details:  # Assuming kerala_bus_details is your list of dictionaries
    insert_data(bus)

# Close the connection
cursor.close()
conn.close()
