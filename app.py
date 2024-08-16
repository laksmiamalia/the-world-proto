import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Set page title and favicon
st.set_page_config(page_title="Know The World", page_icon="🌍")

# Display the title
st.markdown('<div class="main-title">Know The World</div>', unsafe_allow_html=True)

# Fetch the list of all countries for autocomplete
countries_url = "https://restcountries.com/v3.1/all"
countries_response = requests.get(countries_url)
if countries_response.status_code == 200:
    countries_data = countries_response.json()
    country_list = [country['name']['common'] for country in countries_data]
else:
    country_list = []

# Input field with suggestions for country name
country_name = st.selectbox("Enter a country name:", country_list)

# Display country information
if country_name:
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]
        country = data['name']['common']
        capital_city = data['capital'][0]
        continent = data['continents'][0]
        flag_url = data['flags']['png']
        area = data.get('area', 'N/A')
        languages = ', '.join(data['languages'].values()) if 'languages' in data else 'N/A'
        currencies = ', '.join([currency['name'] for currency in data['currencies'].values()]) if 'currencies' in data else 'N/A'

        st.write(f"**Country:** {country}")

        # Display capital city, continent, and flag side by side
        col1, col2 = st.columns([1, 3])
        with col1:
            # Display the flag normally
            st.image(flag_url, caption=f"{country} Flag", width=100)
        with col2:
            st.write(f"**Capital City:** {capital_city}")
            st.write(f"**Continent:** {continent}")
            st.write(f"**Area:** {area} km²")
            st.write(f"**Languages:** {languages}")
            st.write(f"**Currencies:** {currencies}")
    else:
        st.error("Country not found.")
