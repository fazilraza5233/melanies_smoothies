# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruites you want to add in your custom smoothie!
  
  """
)

# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
#     index=None,
#     placeholder="Select favourite fruit...",
# )

# st.write("You selected:", option)

from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingediants_list = st.multiselect('Choose upto 5 ingrediants: ', my_dataframe)
if ingediants_list:
    # st.write(ingediants_list);
    # st.text(ingediants_list);
    ingredients_string = ''
    for fruit_chosen in ingediants_list:
        ingredients_string += fruit_chosen + ' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""
    # st.write(ingredients_string)
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Ordered Successfully!')

# st.write(my_insert_stmt)

