# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import json

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

# Add ORDER_FILLED toggle
order_filled = st.checkbox("Mark order as filled", value=False)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    # Display order preview
    st.subheader("Order Preview:")
    st.write(f"**Smoothie Name:** {smoothie_name}")
    st.write(f"**Ingredients:** {ingredients_string}")
    st.write(f"**Order Filled:** {'✅ Yes' if order_filled else '❌ No'}")

    # Prepare insert statement safely
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (NAME_ON_ORDER, ingredients, ORDER_FILLED)
        VALUES ('{smoothie_name}', '{ingredients_string}', {str(order_filled).upper()})
    """

    # Submit button
    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        if order_filled:
            st.success("✅ Order submitted and marked as FILLED!")
        else:
            st.success("✅ Order submitted successfully!")

# API call to SmoothieFroot
try:
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon", timeout=10)
    if smoothiefroot_response.status_code == 200:
        st.subheader("🍉 SmoothieFroot API Response:")
        st.json(smoothiefroot_response.json())
    else:
        st.warning(f"API returned status code: {smoothiefroot_response.status_code}")
except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch data from SmoothieFroot API: {str(e)}")