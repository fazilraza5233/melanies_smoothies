# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Streamlit App Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
    Choose the fruits you want to add to your custom smoothie!
    """
)

# Create a Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).to_pandas()

smoothie_name = st.text_input("Give your smoothie a name:", placeholder="e.g., Tropical Paradise, Berry Blast...")

# Multiselect for fruit ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe["FRUIT_NAME"].tolist())

if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)

    # Prepare insert statement safely
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients)
        VALUES ('{ingredients_string}')
    """

    # Submit button
    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("✅ Order submitted successfully!")

