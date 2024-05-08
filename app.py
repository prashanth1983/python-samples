import aiohttp
from aiohttp import ClientSession, ClientTimeout
import asyncio
import json
import streamlit as st

class ApiService:
    def __init__(self):
        self.base_url = "https://datapipeline-admin-prod.shop.dell.com"
        self.timeout = ClientTimeout(total=3000)
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE5ODA3NTUxMDAsImlzcyI6IkRhdGEgUGlwZWxpbmUiLCJhdWQiOiJQcm9kdWN0In0.Hl0HpqVn5lJJLJJ8jL71ULPR5CA4P390x0qiBagfRX8'
        }

    async def get_data_from_api_async(self, endpoint):
        try:
            async with ClientSession(timeout=self.timeout, headers=self.headers) as session:
                async with session.get(f"{self.base_url}{endpoint}") as response:
                    # Ensure success status code
                    response.raise_for_status()

                    # Read response content asynchronously
                    responseData = await response.json()
                    return responseData
        except aiohttp.ClientError as ex:
            # Log or handle the exception appropriately
            print(f"Aiohttp ClientError: {ex}")
            raise

async def main():
    try:
        load_ui()
        country= st.text_input("Country: ", key="input1")
        language= st.text_input("Language: ", key="input2")
        segment= st.text_input("Segment: ", key="input3")
        customerset= st.text_input("Customerset: ", key="input4")
        category= st.text_input("Category: ", key="input5")
        submit = st.button('Generate')  
        if submit:
            await generate(country, language, segment,customerset,category)

        
    except Exception as ex:
        # Log or handle the exception appropriately
        print(f"Exception: {ex}")

def load_ui():
    #App UI starts here
    st.set_page_config(page_title="Read Ordercode from Sales catalog", page_icon=":robot:")
    st.header("Retrieve Ordercodes and Variant codes from Sales catalog for the given category")

async def generate(country, language, segment,customerset,category):
    try:
        api_service = ApiService()
        endpoint = "/csbapi/datapipeline/catalog/retrieve/{}/{}/{}/{}".format(language, country, segment, customerset)
        json_data = await api_service.get_data_from_api_async(endpoint)

        if json_data is None:
            print("Error: Failed to retrieve JSON data from the API")
            return

        # print("Received JSON data:", json_data)  # Print the JSON data for inspection

        data = json.loads(json_data)        
        
        #Get all the order code under laptop catagory       
        if not category:
            orderCodes3 = [
                a['id'] for variant in data['productvariants'].values()
                for variant in variant['variants']
                for a in variant['ordercodes']
            ]
        else:
            categoryPath = "all-products/{}/".format(category)
            orderCodes3 = [
                a['id'] for key, value in data['productvariants'].items()
                if categoryPath in key
                for variant in value['variants']
                for a in variant['ordercodes']
            ]
        
        order_codes3 = list(set(orderCodes3))

        st.write("Order codes")
        st.write(order_codes3) 
     

        order_code_string = ','.join(order_codes3)
        #st.write(order_code_string) 

        ## Get all variants
        if not category:
            variants = [
                variant['id'] for variant in data['productvariants'].values()
                for variant in variant['variants']
            ]
        else:
            categoryPath = "all-products/{}/".format(category)
            variants = [
                variant['id'] for key, value in data['productvariants'].items()
                if categoryPath in key
                for variant in value['variants']
            ]          
        
        variants = list(set(variants))

        st.write("variants")
        st.write(variants)           

        # print("Order Codes:", order_code_string)
        # print("Variants:", variants)
        # st.subheader("Answer:")
        # st.write(variants)
    except Exception as ex:
        print(f"Exception: {ex}")


asyncio.run(main())