# Air Quality Analysis Dashboard

## Author
- **Name**: Geralda Livia Nugraha
- **Email Address**: mc299d5x1168@student.devacademy.id
- **Dicoding ID**: [MC299D5X1168](https://www.dicoding.com/users/alddar/)

## Project Overview
This dashboard analyzes air pollution data from Dongsi and Wanliu stations from 2013 to 2017, focusing on PM10 concentrations by examining daily patterns and investigating correlations with meteorological factors. The insights gained enhance understanding of pollution patterns and their driving factors, contributing to more effective air quality management strategies.

## Features
- Interactive dashboard built with Streamlit
- Time series analysis of PM10 concentrations
- Comparison between two stations (Dongsi and Wanliu)
- Correlation analysis with meteorological parameters (TEMP, DEWP, PRES)
- Advanced statistical analysis time series decomposition

## Research Questions
1. What is the daily pattern of PM10 concentrations at Dongsi and Wanliu stations for the period 2013-2017?
2. Is there a correlation between meteorological factors (TEMP, DEWP and PRES) and PM10 concentration levels at the two stations?        

## Installation and Setup
1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run dashboard-air-quality.py
   ```

## Data Source
Raw Data from 'https://drive.google.com/file/d/1RhU3gJlkteaAQfyn9XOVAz7a5o1-etgr/view'.
For dashboard uses a clean data of air quality data, stored in the file `all_data_air_quality.csv`.

## Dashboard Structure
- **Overview**: Basic information and statistics about the dataset
- **Daily Patterns**: Visualization of hourly PM10 concentrations throughout the day
- **Correlation Analysis**: Relationship between PM10 and meteorological parameters
- **Annual Trends**: Show the annual trend for further investigation
- **Distribution Analysis**: Reveals data distribution, the max-min point, and outlier
- **Further Analysis**: To understand the different factors contributing to PM10 variations over time.
- **Summary**: Project Conclusion
