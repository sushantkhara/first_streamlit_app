import streamlit
import snowflake.connector
import pandas as pd

streamlit.title("Zena's Amazing Athleisure Catalog")

try:
    # Check if running in Streamlit environment
    streamlit.secrets

    # Connect to Snowflake
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()

    # Run a Snowflake query and put it all in a variable called my_catalog
    my_cur.execute("SELECT color_or_style FROM catalog_for_website")
    my_catalog = my_cur.fetchall()

    # Put the data into a DataFrame
    df = pd.DataFrame(my_catalog)

    # Temporarily write the DataFrame to the page so I can see what I am working with
    # streamlit.write(df)

    # Put the first column into a list
    color_list = df[0].values.tolist()

    # Let's put a pick list here so they can pick the color
    option = streamlit.selectbox('Pick a sweatsuit color or style:', color_list)

    # We'll build the image caption now since we can
    product_caption = f'Our warm, comfortable, {option} sweatsuit!'

    # Use the selected option to retrieve all the info from the database using a parameterized query
    my_cur.execute(
        "SELECT direct_url, price, size_list, upsell_product_desc FROM catalog_for_website WHERE color_or_style = %s",
        (option,),
    )
    df2 = my_cur.fetchone()

    # Check if df2 is not None before using its values
    if df2:
        streamlit.image(df2[0], width=400, caption=product_caption)
        streamlit.write('Price: ', df2[1])
        streamlit.write('Sizes Available: ', df2[2])
        streamlit.write(df2[3])

    # Close the Snowflake cursor and connection
    my_cur.close()
    my_cnx.close()

except AttributeError:
    streamlit.warning("This script is not running in a Streamlit environment.")

except snowflake.connector.errors.ProgrammingError as e:
    streamlit.error(f"Snowflake ProgrammingError: {e}")

except snowflake.connector.errors.DatabaseError as e:
    streamlit.error(f"Snowflake DatabaseError: {e}")
