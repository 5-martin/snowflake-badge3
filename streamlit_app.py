# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

name_on_order = st.text_input('Name on Order')
st.write('The name on your Smoothie well be:', name_on_order)

# Get the current credentials
cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    for fruit in ingredients_list:
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit}")
        st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
    #st.write(ingredients_string)
    my_insert_stmt = f"INSERT INTO smoothies.public.orders(name_on_order,ingredients) VALUES ('{name_on_order}','{ingredients_string}')"
    #st.write(my_insert_stmt)
    do_order = st.button('Submit Order')
    
    if do_order:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered: {ingredients_string}', icon="✅")


