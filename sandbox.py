import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

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

country_mask = selected_col_df['location'] == "United Kingdom"
country_df = selected_col_df[country_mask]
        
country_df["date"] = country_df["date"].astype("datetime64")
country_df["date"] = country_df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
country_df["date"] = country_df["date"].astype("datetime64")

# country_df[["date",'new_cases_smoothed_per_million','icu_patients', 
#         'icu_patients_per_million', 
#         'hosp_patients', 
#         'hosp_patients_per_million', 
#         'weekly_icu_admissions',
#         'weekly_icu_admissions_per_million', 
#         'weekly_hosp_admissions',
#         'weekly_hosp_admissions_per_million']]




columns_to_plot_primary = [
    'new_cases_smoothed_per_million',
    'new_deaths_smoothed_per_million',
    'hosp_patients_per_million'
]

columns_to_plot_secondary = [
    'people_fully_vaccinated_per_hundred'
]

fig, ax_primary = plt.subplots(figsize=(16, 8))

x = country_df['date']

i = 0

for col in columns_to_plot_primary:
    y = country_df[col]
    y_scaled = NormalizeData(y)
    
    ax_primary.plot(
        x, 
        y_scaled,
        label = col,
        color = plt.cm.tab10(i)
    )
    
    i += 1

# list(plt.cm.tab10(1))
# ax_primary.set_prop_cycle(cmap='tab10')

ax_secondary = ax_primary.twinx()
ax_secondary.set_ylim(0, 100)

for col in columns_to_plot_secondary:
    y = country_df[col]
    # y_scaled = NormalizeData(y)
    
    ax_secondary.plot(
        x, 
        y,
        label = col,
        color = plt.cm.tab10(i)
    )
    
    i += 1

ax_primary.legend(
    loc='upper center', 
    bbox_to_anchor=(0.1, -0.1),
    fancybox=True, 
    shadow=True, 
    ncol=1
)

ax_secondary.legend(
    loc='upper center', 
    bbox_to_anchor=(0.4, -0.1),
    fancybox=True, 
    shadow=True, 
    ncol=1
)

plt.show()

# plt.colormaps()
# cmap=plt.cm.coolwarm

# print(plt.cm.keys())






# Set data

# - x-axis
x = country_df['date']
# - primary axis
y_cases = country_df['new_cases_smoothed_per_million'] 
y_deaths = country_df['new_deaths_smoothed_per_million']
# - secondary axis
y_total_vaxed = country_df['people_fully_vaccinated_per_hundred']

# Create blank canvas
fig, ax1 = plt.subplots(figsize=(16, 8))

# Scale data for cases and deaths
y_cases_scaled = NormalizeData(y_cases)
y_deaths_scaled = NormalizeData(y_deaths)

# Set axis
ax1.plot(
    x, 
    y_cases_scaled,
    label = "New Cases Standardised (7 day average)",
    color = "tab:blue"
)

ax1.plot(
    x, 
    y_deaths_scaled,
    label = "New Deaths Standardised (7 day average)",
    color = "tab:red"
)

# Create 2ndary axis for vax
ax2 = ax1.twinx()

ax2.plot(
    x, 
    y_total_vaxed,
    label = "% Fully Vaxed",
    color = "tab:green"
)

ax2.set_ylim(0, 100)

# ax.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

ax1.margins(x=0, y=0)
ax2.margins(x=0, y=0)

ax1.legend(
    loc='upper center', 
    bbox_to_anchor=(0, -0.1),
    fancybox=True, 
    shadow=True, 
    ncol=2
)
ax2.legend(
    loc='upper center', 
    bbox_to_anchor=(0.2, -0.1),
    fancybox=True, 
    shadow=True, 
    ncol=1
)

plt.show()