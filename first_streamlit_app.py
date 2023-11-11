import streamlit
import snowflake.connector

# Connect to Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# Execute Snowflake query
my_cur.execute(
    "SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()"
)

# Fetch the result
my_data_row = my_cur.fetchone()

# Display result
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

# Close the cursor and connection
my_cur.close()
my_cnx.close()
