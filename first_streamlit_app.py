import streamlit
import snowflake.connector

# Check if running in Streamlit environment
if streamlit._is_running_with_streamlit:

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

    finally:
        # Close the cursor and connection in a finally block
        if my_cur:
            my_cur.close()
        if my_cnx:
            my_cnx.close()

else:
    streamlit.warning("This script is not running in a Streamlit environment.")
