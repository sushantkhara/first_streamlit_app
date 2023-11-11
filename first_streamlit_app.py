import streamlit
import snowflake.connector
import secrets

# Load Snowflake secrets
snowflake_secrets = streamlit.secrets["snowflake"]

# Establish Snowflake connection
try:
    my_cnx = snowflake.connector.connect(
        user=snowflake_secrets["user"],
        password=snowflake_secrets["password"],
        account=snowflake_secrets["account"],
        warehouse=snowflake_secrets["warehouse"],
        database=snowflake_secrets["database"],
        schema=snowflake_secrets["schema"],
    )

    my_cur = my_cnx.cursor()

    # Execute Snowflake query
    my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    my_data_row = my_cur.fetchone()

    # Display result
    streamlit.text("Hello from Snowflake:")
    streamlit.text(my_data_row)

except snowflake.connector.errors.ProgrammingError as e:
    streamlit.error(f"Snowflake error: {e}")

# Close the cursor and connection in a finally block
finally:
    if my_cur:
        my_cur.close()
    if my_cnx:
        my_cnx.close()
