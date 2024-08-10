import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Function to connect to MySQL database and fetch data
def fetch_data_from_db(database, table):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Iloveall@12345",  # Replace with your MySQL password
            database=database
        )
        query = f"SELECT * FROM {table};"
        df = pd.read_sql(query, conn)
        conn.close()
        if df.empty:
            st.warning(f"No data found in the table '{table}'.")
        return df
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# Streamlit application
def main():
    st.title("Red Bus Dashboard")

    # Sidebar for selecting database
    database_option = st.sidebar.selectbox(
        "Select Database",
        ["kerala_bus_routes", "kadamba_bus_routes", "rajasthan_bus_routes", "bengal_bus_routes","himachal_bus_routes","assam_bus_routes","uttra_bus_routes","bihar_bus_routes","punjab__bus_routes","chandigar_bus_routes"]
    )

    # Define table name based on database choice
    table_name = database_option

    st.header(f"Bus Details from {table_name}")

    # Fetch data
    df = fetch_data_from_db("bus_routes", table_name)

    # Display data
    if not df.empty:
        # Sidebar Filters
        st.sidebar.header("Filter Options")

        # Filter by route name
        unique_routes = df['route_name'].unique()
        selected_route = st.sidebar.selectbox("Select Route", ["All"] + list(unique_routes))

        # Apply filter based on route selection
        if selected_route != "All":
            df = df[df['route_name'] == selected_route]

        # Display the filtered data
        st.dataframe(df)

        # Graphical Representations
        st.sidebar.header("Graphical Representations")

        # Bar Chart
        if st.sidebar.checkbox("Show Bar Chart of Fares"):
            st.subheader("Bar Chart of Fares")
            if 'fare' in df.columns:
                df['fare'] = df['fare'].replace("Not listed", "0").astype(float)  # Ensure fare is numeric
                fig, ax = plt.subplots()
                df.groupby('route_name')['fare'].mean().plot(kind='bar', ax=ax)
                ax.set_title('Average Fare by Route')
                ax.set_xlabel('Route Name')
                ax.set_ylabel('Average Fare')
                st.pyplot(fig)
            else:
                st.write("Fare data is not available for graphical representation.")

        # Line Chart
        if st.sidebar.checkbox("Show Line Chart of Ratings"):
            st.subheader("Line Chart of Ratings")
            if 'rating' in df.columns:
                df['rating'] = df['rating'].replace("No rating", "0").astype(float)  # Ensure rating is numeric
                fig = px.line(df, x='route_name', y='rating', title='Ratings by Route')
                st.plotly_chart(fig)
            else:
                st.write("Rating data is not available for graphical representation.")

        # Histogram
        if st.sidebar.checkbox("Show Histogram of Duration"):
            st.subheader("Histogram of Duration")
            if 'duration' in df.columns:
                df['duration'] = df['duration'].str.extract('(\d+)').astype(float)  # Extract numeric values
                fig, ax = plt.subplots()
                df['duration'].dropna().plot(kind='hist', bins=20, ax=ax)
                ax.set_title('Histogram of Duration')
                ax.set_xlabel('Duration')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)
            else:
                st.write("Duration data is not available for graphical representation.")

        # Option to download data as CSV
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name=f"{table_name}_details.csv",
            mime="text/csv"
        )
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()
