# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """
    Choose the fruit you want in your custom smoothie!
    """
)

name_box=st.text_input('Name of the Smoothie')
st.write('The Name of the Smoothie will be',name_box)
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe,use_container_width=True)

ingredients_list=st.multiselect('Select 5 Ingredients:',my_dataframe,max_selections=5)

if ingredients_list:
    ingredients=''
    for fruit in ingredients_list:
        ingredients+=fruit+' '
        st.subheader(fruit+"Nutritional Information")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
        fruits_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    st.write(ingredients)

    my_insert_sql="""insert into smoothies.public.orders(ingredients,name_on_order) 
        values('"""+ingredients+"""','"""+name_box+"""')"""

    time_to_insert=st.button('Place Order')

    if time_to_insert:
        session.sql(my_insert_sql).collect()
        st.success('Your Smoothie is Ordered!'+name_box,icon='✅')

