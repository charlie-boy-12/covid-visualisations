import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import streamlit as st

st.title('Covid Cases, Deaths & Vaccinations')

st.set_option('deprecation.showPyplotGlobalUse', False)

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

# latest_df = pd.read_csv("https://covid.ourworldindata.org/data/latest/owid-covid-latest.csv")

full_df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

# full_df.columns

selected_col_df = full_df \
[ 
    [
        'continent', 
        'location', 
        'date', 
        'total_cases', 
        'new_cases', 
        'new_cases_smoothed',
        'total_deaths', 
        'new_deaths', 
        'new_deaths_smoothed', 
        'total_cases_per_million', 
        'new_cases_per_million', 
        'new_cases_smoothed_per_million',
        'total_deaths_per_million', 
        'new_deaths_per_million',
        'new_deaths_smoothed_per_million', 
        'reproduction_rate', 
        'icu_patients', 
        'icu_patients_per_million', 
        'hosp_patients', 
        'hosp_patients_per_million', 
        'weekly_icu_admissions',
        'weekly_icu_admissions_per_million', 
        'weekly_hosp_admissions',
        'weekly_hosp_admissions_per_million', 
        'total_vaccinations',
        'people_vaccinated', 
        'people_fully_vaccinated', 
        'total_boosters',
        'new_vaccinations', 
        'new_vaccinations_smoothed',
        'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
        'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
        'new_vaccinations_smoothed_per_million',
        'new_people_vaccinated_smoothed',
        'new_people_vaccinated_smoothed_per_hundred', 
        'population'
    ] 
]

continent_list = selected_col_df['continent'].unique().tolist()
country_list = selected_col_df['location'].unique().tolist()

# removing continents from country list
for element in continent_list:
    if element in country_list:
        country_list.remove(element)

continent_list.remove(np.nan)

# SELECT WHICH COUNTRY OR CONTINET TO PLOT

country_or_continent = st.radio(
    'Country or Continent',
    ('Country', 'Continent')
)

if country_or_continent == 'Continent':
    
    selection = st.selectbox(
        'Select a continent to plot',
        continent_list
    )

elif country_or_continent == 'Country':
    
    selection = st.selectbox(
        'Select a country to plot',
        country_list
    )
    
country_mask = selected_col_df['location'] == selection
country_df = selected_col_df[country_mask]

country_df["date"] = country_df["date"].astype("datetime64")
country_df["date"] = country_df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
country_df["date"] = country_df["date"].astype("datetime64")

# SELECT WHICH VALUES TO PLOT

columns_to_plot_primary = [
    'new_cases_smoothed_per_million',
    'new_deaths_smoothed_per_million',
    'hosp_patients_per_million'
]

columns_to_plot_secondary = [
    'people_fully_vaccinated_per_hundred'
]

col1, col2 = st.columns(2)
with col1:
    columns_to_plot_primary_selected = st.multiselect(
    'Select values to plot on primary axis (standardised/scaled)',
    columns_to_plot_primary)
with col2:
    columns_to_plot_secondary_selected = st.multiselect(
    'Select values to plot on secondary axis (%)',
    columns_to_plot_secondary)


if st.button('Generate Plot'):
    
    with st.spinner(text="Generating plot for " + selection):
        
        # CANVAS
        fig, ax_primary = plt.subplots(figsize=(16, 8))

        x = country_df['date']

        # PRIMARY AXIS
        i = 0

        for col in columns_to_plot_primary_selected:
            y = country_df[col]
            y_scaled = NormalizeData(y)
            ax_primary.plot(
                x, 
                y_scaled,
                label = col + " (1 = " + str(np.max(y)) + ")",
                color = plt.cm.tab10(i)
            )
            i += 1

        # SECONDARY AXIS
        ax_secondary = ax_primary.twinx()
        ax_secondary.set_ylim(0, 100)

        for col in columns_to_plot_secondary_selected:
            y = country_df[col]
            # y_scaled = NormalizeData(y)
            ax_secondary.plot(
                x, 
                y,
                label = col,
                color = plt.cm.tab10(i)
            )
            i += 1

        # SET AXIS LABELS
        ax_primary.set_ylabel("Standardised Scale (see legend for value)")
        ax_secondary.set_ylabel("Percentage")
        
        # SETTING LEGENDS
        ax_primary.legend(
            loc='upper center', 
            bbox_to_anchor=(0.2, -0.1),
            fancybox=True, 
            shadow=True, 
            ncol=1
        )
        ax_secondary.legend(
            loc='upper center', 
            bbox_to_anchor=(0.7, -0.1),
            fancybox=True, 
            shadow=True, 
            ncol=1
        )

        # SETTING MARGINS
        ax_primary.margins(x=0, y=0)
        ax_secondary.margins(x=0, y=0)

        # SETTING SPINES
        ax_primary.spines['top'].set_visible(False)
        ax_secondary.spines['top'].set_visible(False)
        
        # SETTING SIZING
        params = {
            'legend.fontsize': 'x-large',
            # 'figure.figsize': (16, 8),
            'axes.labelsize': 'x-large',
            # 'axes.titlesize':'x-large',
            'xtick.labelsize':'large',
            'ytick.labelsize':'large'
        }
        
        plt.rcParams.update(params)
        
        st.subheader(selection)
        st.pyplot(plt)

with st.expander("Data Source"):
    st.write("https://covid.ourworldindata.org/")
    
# -------------------------------------------------
# TO DO LIST
# -------------------------------------------------

# - Add hospitalisations
# - Vaxed vs non-vaxed that are hospitalised or deaths