from typing import Sized
import streamlit as st
import plotly.express as px
import pandas as pd

# This is our title in the main page
st.title("125 Years of Summer Olympics")
# Title in the sidebar
st.sidebar.title("125 Years of Summer Olympics")

medal = "./data/Olympics.csv"

# ---------------------------
# TASK 1: load in data
@st.cache(persist = True)

def load_data(data):
    data = pd.read_csv(data)
    data = data.sort_values(by=['Year'])
    return data

data = load_data(medal)
# we need to cache the output of load_data if the input doesn't change
# so that the CPU cycle is not jammed every time you move the slider/ re-run app in any way
# essentially, we don't want to reload the data every time when we perform an interaction

# at this point, you are not going to see anything after you rerun the app
# because we haven't had any output yet

# let's try to show the data here
#st.write(data)

# -----------------------
# TASK 2: Create bar chart to view performance by Olympic Year (top 10)
# Widget: radio buttons for selecting order and bar chart mode
st.sidebar.header("Ranking of Top 10 Country Medals by Olympic year")
# Clean up "Year" column for use: .unique() and .sort()
year_list = data['Year'].unique()
year_list.sort()
choice = st.sidebar.selectbox("Select Olympic Year",year_list, key='0')
chosen_data = data[data['Year']==choice]
# process selected data for caption
host_city = chosen_data['Host_city'].unique()
host_city=str(host_city).strip("['']")
host_country = chosen_data['Host_country'].unique()
host_country=str(host_country).strip("['']")

st.subheader("Ranking of Top 10 Country Medals in %i" %choice)
st.caption('Host location: %s, %s' %(host_city,host_country))

# Add radio buttons for descending/ ascending order
order = st.sidebar.radio('Order',["descending",'ascending'])

# Add radio buttons for grouped/ stacked barmode
barmode = st.sidebar.radio('Bar Chart Mode',['group', "stack"])

bar = px.bar(chosen_data, x="Country_Name", y=["Gold","Silver","Bronze"], labels = {'Country_Name': "Country Name", 'Total_Medals': "Total Medals"}, barmode=barmode)

if order == 'descending':
  bar.update_xaxes(range =[-0.5,9.5])
  bar.update_xaxes(categoryorder = 'total descending')
else:
  bar.update_xaxes(categoryorder = 'total ascending')
st.write(bar)

# -----------------------
# Task 3: Create scatter plot to view country's performance over time
# Widget: selectbox to let user select countries
st.sidebar.subheader("Country's performance over time")
st.subheader("Country's performance over time")
# We also have to get unique values from data["Country_Name"] beforehand
country_list = data['Country_Name'].unique()
country_list.sort()

choice_country = st.sidebar.multiselect("Pick a country/ countries", country_list)

if len(choice_country) == 0:
  st.write("Please select a country/ countries to view performance (Data of all countries is shown by default)")
else:
  choice_data = data[data.Country_Name.isin(choice_country)]
  choice_data=choice_data.sort_values(by=['Year'])
  fig_years = px.scatter(choice_data, x='Year', y="Total_Medals", color='Country_Name', facet_col ='Continent')
  st.write(fig_years)

# create checkbox to hide graph
hide = st.sidebar.checkbox('Hide all country data')
if not hide:
  fig_years = px.scatter(data, x='Year', y="Total_Medals",color='Continent', hover_name='Country_Name')
  st.write(fig_years)

# -----------------------
# Task 4: Create animation of all countries
# Widget: radio buttons to change projection view, and regular buttons to change chart type
st.sidebar.subheader("Mapping animation of medals by country")
st.subheader("Mapping animation of medals by country")

# Create radio buttons to select projection type
view = st.sidebar.radio('View',['natural earth', "orthographic","equirectangular"])
# Create buttons to change chart type
chart_type = st.sidebar.radio("Change graph type",['Choropleth','Bubble map'])

# Write if-else statement to pass in selection of chart type, and directly pass in selection of view into the parameter of graph function
if chart_type =='Choropleth':
  fig2 = px.choropleth(data, locations = 'Country_Code', animation_frame = 'Year', hover_name='Country_Name', projection=view, color='Total_Medals')
  st.write(fig2)
else:
  fig2 = px.scatter_geo(data, locations = 'Country_Code', animation_frame = 'Year', hover_name='Country_Name', projection=view, color='Total_Medals', size='Total_Medals')
  st.write(fig2)