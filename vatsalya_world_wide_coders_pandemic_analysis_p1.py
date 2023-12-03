# -*- coding: utf-8 -*-
"""Vatsalya_World_Wide Coders Pandemic Analysis P1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uiCrwfoXbcTJpNDnwZaHqyTFdKPHtlZf

# COVID-19 Outbreak Analysis

### World Health Organisation A1



We all know that coronavirus is spreading on a daily basis in India. So, let's try to visualise how fast it is spreading.

First, let's look at the dashboard created by Johns Hopkins University. You can look at the following live dashboard to see the real-time trend.

[COVID-19 Live Dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)

Now, let's create a similar map for India using Python to visualise the most affected states in India due to coronavirus. After the class, you can share it with your parents, relatives and friends by sending them the link to the map.

---

---

#### Activity 1: Retrieve and Analyze Code from Database

This is the source code for the map to be created. You will learn to write it after signing up for the applied tech course. Right now, you just have to execute the code.
"""

#  Action: Run the code below.
# Download data
!git clone https://github.com/CSSEGISandData/COVID-19.git

# Install 'geocoder'
!pip install geocoder

# Importing modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import geocoder
import folium
from folium import plugins

# DataFrame for the world
conf_csv = '/content/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
conf_df = pd.read_csv(conf_csv)
grouped_conf_df = conf_df.groupby(by = ['Country/Region'], as_index = False).sum()

# DataFrame for India
india_df = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
india_df = india_df.iloc[1:36, :]
# state_latitudes = []
# state_longitudes = []
# for i in india_df.index:
#     state = india_df['State'][i]
#     state_lat = geocoder.osm(state).lat
#     state_lng = geocoder.osm(state).lng
#     state_latitudes.append(state_lat)
#     state_longitudes.append(state_lng)

# state_latitudes = pd.Series(data = state_latitudes, index = india_df.index)
# state_longitudes = pd.Series(data = state_longitudes, index = india_df.index)
# india_df['Latitude'] = state_latitudes
# india_df['Longitude'] = state_longitudes

state_coordinates = [(19.7515, 75.7139), # Maharashtra
                    (11.1271, 78.6569), # Tamil Nadu
                    (15.9129, 79.7400), # Andhra Pradesh
                    (15.317, 75.7139), # Karnataka
                    (28.7041, 77.1025), # Delhi
                    (26.8467, 80.9462), # UP
                    (22.9868, 87.8550), # WB
                    (25.0961, 85.3131), # Bihar
                    (18.1124, 79.0193), # Telangana
                    (22.2587, 71.1924), # Gujarat
                    (26.2006, 92.9376), # Assam
                    (27.0238, 74.2179), # Rajasthan
                    (20.9517, 85.0985), # Odisha
                    (29.0588, 76.0856), # Haryana
                    (22.9734, 78.6569), # Madhya Pradesh
                    (10.8505, 76.2711), # Kerala
                    (31.1471, 75.3412), # Punjab
                    (33.7782, 76.5762), # Jammu and Kashmir
                    (23.6102, 85.2799), # Jharkhand
                    (21.2787, 81.8661), # Chattisgarh
                    (30.0668, 79.0193), # Uttarakhand
                    (15.2993, 74.1240), # Goa
                    (23.9408, 91.9882), # Tripura
                    (11.9416, 79.8083), # Puducherry
                    (24.6637, 93.9063), # Manipur
                    (31.1048, 77.1734), # Himachal Pradesh
                    (26.1584, 94.5624), # Nagaland
                    (28.2180, 94.7278), # Arunachal Pradesh
                    (11.7401, 92.6586), # Andaman and Nicobar
                    (34.1700, 77.5800), # Ladakh
                    (30.7333, 76.7794), # Chandigarh
                    (20.1809, 73.0169), # Dadra and Nagar Haveli
                    (25.4670, 91.3662), # Meghalaya
                    (27.5330, 88.5122), # Sikkim
                    (23.1645, 92.9376), # Mizoram
                     ]

ind_state_lat = pd.Series([s[0] for s in state_coordinates], index = india_df.index)
ind_state_lng = pd.Series([s[1] for s in state_coordinates], index = india_df.index)

india_df['Latitude'] = ind_state_lat
india_df['Longitude'] = ind_state_lng

# DataFrame for the US
us_conf_csv = '/content/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
us_conf_df = pd.read_csv(us_conf_csv)
us_conf_df = us_conf_df.dropna()
grouped_us_conf_df = us_conf_df.groupby(by = ['Combined_Key'], as_index = False).sum()

# Function to get total confirmed cases in a country
def get_total_confirmed_cases_for_country(country_name):
    total_cases_country = conf_df[conf_df['Country/Region'] == country_name].iloc[:, 4:].apply(sum, axis = 0)
    total_cases_country.index = pd.to_datetime(total_cases_country.index)
    return total_cases_country

# Function to get total confirmed cases in the world
def get_total_confirmed_global_cases():
    global_cases = conf_df.iloc[:, 4:].apply(sum, axis=0)
    global_cases.index = pd.to_datetime(global_cases.index)
    return global_cases

# Function to create a line plot
def line_plot(your_name, plot_background, fig_width, fig_height, country_name, colour, linewidth, markertype):
    dt_series = None
    if country_name != 'global':
        dt_series = get_total_confirmed_cases_for_country(country_name)
    else:
        dt_series = get_total_confirmed_global_cases()
    plt.style.use(plot_background)
    plt.figure(figsize = (fig_width, fig_height))
    plt.title(f'{country_name.upper()}: Total Coronavirus Cases Reported\nCreated by {your_name.upper()}\nPowered by WHO', fontsize = 16)
    plt.plot(dt_series.index, dt_series, c = colour, lw = linewidth, marker = markertype, markersize = 7)
    plt.xticks(rotation = 45)
    plt.ylabel("Total Cases")
    plt.grid(linestyle='--', c='grey')
    plt.show()

# Add minimap
def add_minimap(map_name):
    # Plugin for mini map
    minimap = plugins.MiniMap(toggle_display = True)
    map_name.add_child(minimap) # Add minimap
    plugins.ScrollZoomToggler().add_to(map_name) # Add scroll zoom toggler to map
    plugins.Fullscreen(position='topright').add_to(map_name) # Add full screen button to map

# Add title to map
def add_title(map_name, country, your_name):
    title_html = '''
        <h2 align="center" style="font-size:20px"><b>Coronavirus Total Confirmed Cases in {}</b></h2>
        <h4 align="center" style="font-size:16px"><i>Created by</i> {}</h4>
        <h4 align="center" style="font-size:16px"><i>Powered by</i>
            <a href="https://covid19.who.int/">WHO</a>
        </h4>
             '''.format(country, your_name.upper())
    return map_name.get_root().html.add_child(folium.Element(title_html))

# Function to create folium maps using for India, US, Argnetina and the world
def folium_map_with_circles(your_name, country, map_width, map_height, left_margin, top_margin, map_tile, zoom, circle_color, minimap):
    last_col = conf_df.columns[-1]
    if country == 'India':
        india_map = folium.Map(location = [22.3511148, 78.6677428],
                               width = map_width, height = map_height,
                               left = f"{left_margin}%", top = f"{top_margin}%",
                               tiles = map_tile, zoom_start = zoom)

        if minimap == True:
            add_minimap(india_map)

        add_title(india_map, country, your_name)
        for i in india_df.index:
            folium.Circle(radius = float(india_df.loc[i, 'Confirmed']) / 2,
                          location = [india_df.loc[i, 'Latitude'], india_df.loc[i, 'Longitude']],
                          popup = "{}\n {}\n on {}".format(india_df.loc[i, 'State'],
                                                          india_df.loc[i, 'Confirmed'],
                                                          india_df.loc[i, 'Last_Updated_Time']),

                          color = circle_color,
                          fill = True).add_to(india_map)
        return india_map

    elif country == 'US':
        us_map = folium.Map(location = [39.381266, -97.922211],
                            width = map_width, height = map_height,
                            left = f"{left_margin}%", top = f"{top_margin}%",
                            tiles = map_tile, zoom_start = zoom)
        if minimap == True:
            add_minimap(us_map)

        add_title(us_map, country, your_name)
        for i in grouped_us_conf_df.index:
            folium.Circle(location = [grouped_us_conf_df.loc[i, 'Lat'], grouped_us_conf_df.loc[i, 'Long_']],
                          radius = int(grouped_us_conf_df.loc[i, last_col]),
                          popup = "{}\n {}\n on {}".format(grouped_us_conf_df.loc[i, 'Combined_Key'],
                                                          grouped_us_conf_df.loc[i, last_col],
                                                          last_col),
                          color = circle_color,
                          fill = True).add_to(us_map)
        return us_map


    elif country == 'World':
        world_map = folium.Map(location = [0, 0],
                            width = map_width, height = map_height,
                            left = f"{left_margin}%", top = f"{top_margin}%",
                            tiles = map_tile, zoom_start = zoom)
        if minimap == True:
            add_minimap(world_map)

        add_title(world_map, country, your_name)
        for i in grouped_conf_df.index:
            folium.Circle(location = [grouped_conf_df.loc[i, 'Lat'], grouped_conf_df.loc[i, 'Long']],
                          radius = int(grouped_conf_df.loc[i, last_col]) / 2,
                          popup = "{}\n {}\n on {}".format(grouped_conf_df.loc[i, 'Country/Region'],
                                                          grouped_conf_df.loc[i, last_col],
                                                          last_col),
                          color = circle_color,
                          fill = True).add_to(world_map)
        return world_map
    else:
        print("\nWrong input! Enter either India, US or World.\n")

# Total confirmed cases in the descending order.
grouped_conf_df = conf_df.groupby(by='Country/Region', as_index=False).sum()
desc_grp_conf_df = grouped_conf_df.sort_values(by=conf_df.columns[-1], ascending=False)

# Function to create a bar plot displaying the top 10 countries having the most number of coronavirus confirmed cases.
def bar_plot(your_name, num_countries, width, height):
    last_col = conf_df.columns[-1]
    latest_date = datetime.datetime.strptime(last_col, '%m/%d/%y').strftime('%B %d, %Y') # Modify the latest date in the 'Month DD, YYYY' format.
    plt.figure(figsize = (width, height))
    plt.title(f'Top {num_countries} Countries with Highest COVID-19 Confirmed Cases\nCreated by {your_name.upper()}\nPowered by WHO',
              fontsize = 16)
    sns.barplot(desc_grp_conf_df[last_col].head(num_countries), desc_grp_conf_df['Country/Region'].head(num_countries), orient = 'h')
    plt.xlabel(f'Total Confirmed Cases (in millions) as of {latest_date}')
    plt.show()

# Non-cumulative Confirmed Cases.
non_cum_conf_df = desc_grp_conf_df.iloc[:, :4]
for i in range(len(desc_grp_conf_df.columns[3:]) - 1):
    series = desc_grp_conf_df[desc_grp_conf_df.columns[3 + (i + 1) ]] - desc_grp_conf_df[desc_grp_conf_df.columns[3 + i]]
    non_cum_conf_df[desc_grp_conf_df.columns[3 + (i + 1)]] = series

# Function to get the total non-cumulative confirmed cases in a country.
def get_total_daily_confirmed_cases_for_country(country_name):
    total_daily_cases = non_cum_conf_df[non_cum_conf_df['Country/Region'] == country_name].iloc[:, 4:].apply(sum, axis = 0)
    total_daily_cases.index = pd.to_datetime(total_daily_cases.index)
    return total_daily_cases

# Line plot for the daily (non-cumulative) confirmed cases in various countries.
def daily_cases_line_plot(your_name, num_countries, width, height):
    plt.figure(figsize=(width, height))
    plt.title(f'Non-Cumulative COVID-19 Confirmed Cases\nCreated by {your_name.upper()}\nPowered by WHO', fontsize = 16)
    for region in non_cum_conf_df.iloc[:num_countries, :]['Country/Region']:
        total_conf_cases = get_total_daily_confirmed_cases_for_country(region)
        plt.plot(total_conf_cases.index[53:], total_conf_cases[53:], lw=2.5, label=region)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid('major', linestyle='--', c='grey')
    plt.show()

# Download data
!git clone https://github.com/CSSEGISandData/COVID-19.git

"""---

#### Activity 2: Line Plot^

Let's create a line plot to visualise the total number of confirmed cases in India till yesterday. For the line plot, the dataset that we have on coronavirus is maintained at Johns Hopkins University which gets according to the US time. Hence, we have data updated till yesterday.

To view this dataset, write `conf_df[conf_df['Country/Region'] == 'India']` in the code cell below.
"""

#  Action: Write conf_df[conf_df['Country/Region'] == 'India'] to view the dataset for India that will be used to create a line plot.
conf_df[conf_df['Country/Region'] == 'India']

"""So, in this dataset, we have data for the total confirmed cases in India starting from January 22, 2020. The date given here is in the `MM/DD/YY` format where

- `MM` stands for month

- `DD` stands for day

- `YY` stands for year

Now, let's create a line plot. To create a line plot, you need to use the `line_plot()` function which takes the following inputs:

- Name of the person who is creating the line plot which should be a text value enclosed within single-quotes (`''`) or double-quotes (`""`).

- The background style of the line plot which should be a text value enclosed within single-quotes (`''`) or double-quotes (`""`).. Here is the list of most commonly used background styles:

  1. `'dark_background'` (most preferred)

  2. `'ggplot'`

  3. `'seaborn'`

  4. `'fivethirtyeight'`

  and many more.

- Width of the line plot (numeric value).

- Height of the line plot (numeric value).

- Name of the country which should be a text value enclosed within single-quotes (`''`) or double-quotes (`""`).

- Colour of the lines which should be a text value enclosed within single-quotes (`''`) or double-quotes (`""`). Here's the list of most commonly used colours:

  1. `'red'`
  
  2. `'cyan'`
  
  3. `'magenta'`

  4. `'yellow'`

  5. `'green'`

- The width of the line (numeric value)

- The marker style on the line plot which should be a text value enclosed within single-quotes (`''`) or double-quotes (`""`). Here is the list of the most commonly used marker styles:

  1. `'o'` for a circular marker

  2. `'*'` for a starred marker

  3. `'^'` for a upper triangular marker

"""

#  Action: Create a line plot for the total confirmed cases in India using the 'line_plot()' function.
line_plot('anmol akshat tripathi','fivethirtyeight', 23,10,'India','red',3,'^')

"""**Note:** The `line_plot()` function is NOT a standard Python function. It is a user-defined function created at WHOython to simplify the line plot creation process. You will learn to create your own user-defined function in the subsequent classes in this course.

---

#### Activity 3: Map^^

Let's create a map for India. For this, we are going to use a dataset showing state-wise data for India. To view the first five rows for the total confirmed cases in India, call the `head()` function on the `india_df` variable which stores the data.
"""

#  Action: List the first five rows of the dataset containing the total number of confirmed cases in India.
india_df.head(20)

"""Let's now create a map for India to show the state-wise total confirmed cases of coronavirus. Using the latitude and longitude values (which are numeric values with decimal), we can create circular markers on a map. For this, you need to use the `folium_map_with_circles()` function which takes the following inputs:

- Name of the person who is creating the map which should be a text value enclosed within single-quotes (`''`) or double-quotes (`""`).

- Name of the country for which a map needs to be created. It should be a text value enclosed within single-quotes (`''`) or double-quotes (`""`). For the map only three values are supported:

  1. `'India'`

  2. `'US'`

  3. `'World'`

- Width of the map (numeric value).

- Height of the map (numeric value).

- Left margin for the map (numeric value).

- Top margin for the map (numeric value).

- The background style of the line plot which should be a text value enclosed within single-quotes (`''`) or double-quotes (`""`). Here is the list of most commonly used background styles:

  1. `'OpenStreetMap'`

  2. `'Stamen Terrain'`

  3. `'Stamen Toner'`

- Initial zoom in value (a numeric value)

- Colour of the circles on the map should be a text value enclosed within single-quotes (`''`) or double-quotes (`""`). Here's the list of most commonly used colours:

  1. `'red'`
  
  2. `'blue'`
  
  3. `'magenta'`

  4. `'yellow'`

  5. `'green'`

- Whether you want the map to have a minimap or not; `True` for **yes** and `False` for **no**.

"""



#  Action: Create a map for India to show the state-wise total confirmed cases of coronavirus.
folium_map_with_circles("anmol akshat tripathi","US",1017,700,7,5,'OpenStreetMap',2,'blue', True)

"""**Note:** The `folium_map_with_circles()` function is NOT a standard Python function. It is a user-defined function created at WHO using Python to simplify the map creation process. You will learn to create your own user-defined function in the subsequent classes in this course.

Let's export the above map as an HTML file. You can make it a web page like a website and share it with your parents or friends. To do this, you need to use the `save()` function which is a standard Python function. The input to this function should be a path (or location) of the directory where you want to store the HTML file. Also, name the file as `index.html`. This is very important.
"""

#  Action: Export the world map as an HTML file.
World_map = folium_map_with_circles("anmol akshat tripathi","World",1017,700,7,5,'OpenStreetMap',2,'blue', True)
World_map.save('/content/index.html')

"""---

Activity 4: Bar Plot
Let’s create a bar chart displaying the top 10 countries having the most
number of coronavirus confirmed cases. For this, you need to use the bar_plot() function. It
takes four inputs:
1. Name of the person who is creating the bar plot which should be a text value enclosed within
single-quotes ('') or double-quotes ("").
2. Number of countries to be listed in the bar plot (numeric value)
3. Width of the bar plot (numeric value)
4. Height of the bar plot (numeric value)
"""

bar_plot("anmol", 17,10,7)

"""Activity 5: Daily (Non-Cumulative) Confirmed Cases Line Plot
Let’s create line plots
for daily confirmed cases for the top 4 worst affected countries. For this, you need to use the
daily_cases_line_plot() function. It takes four inputs:
1. Name of the person who is creating the line plot which should be a text value enclosed within
single-quotes ('') or double-quotes ("").
2. Number of countries (numeric value) for which the line plot needs to be created.
3. Width of the plot (numeric value)
4. Height of the plot (numeric value)

"""

daily_cases_line_plot("anmol",3,10,12)