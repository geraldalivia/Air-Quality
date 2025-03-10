# Air Quality Analysis Dashboard

## Project Overview
This dashboard analyzes air pollution data from Dongsi and Wanliu stations from 2013 to 2017, focusing on PM10 by examining daily patterns and correlations with meteorological factors.

## Live Dashboard
[Streamlit-Geralda Livia](https://air-quality-geraldalivia.streamlit.app/)

## Data Source
Raw Dataset air quality from [Dicoding Air Quality](https://air-quality-geraldalivia.streamlit.app/). For the analysis and development dashboard use the cleaned data version from [Cleaned Data](https://air-quality-geraldalivia.streamlit.app/). Analysis focus on PM10 levels and other meteorological related data.

## library
- Streamlit
- Pandas
- Numpy
- Matplotlib
- Seaborn
- Gdown
- OS
- Scipy
- Plotly

## Research Questions
1. What is the daily pattern of PM10 concentrations at Dongsi and Wanliu stations for the period 2013-2017?
2. Is there a correlation between meteorological factors (TEMP, DEWP and PRES) and PM10 concentration levels at the two stations?        

## Installation and Setup
### Create virtual environment use pipeenv
   To install pipenv
   ```
   pip install pipenv
   ```
   To create virtual environment
   ```
   pipenv install
   ```
   To activate virtual environment
   ```
   pipenv shell
   ```
   ```
   pip install -r requirements.txt
   ```
### Install the required packages
   The packages needed to run the analysis on both Colab and the dashboard
   ```
   pip install pandas numpy matplotlib gdown os plotly scipy seaborn streamlit
   ```
   or by the following command
   ```
   pip install -r requirements.txt
   ```
### Run the Dashboard 
   Navigate to the  `air-quality-dashboard.py` and runn the streamlit App
    ```
    streamlit run air-quality-dashboard.py
    ```
## About Dashboard
- **Overview**: Basic information and statistics about the dataset
- **Daily Patterns**: Visualization of hourly PM10 concentrations throughout the day
- **Correlation Analysis**: Relationship between PM10 and meteorological parameters
- **Annual Trends**: Show the annual trend for further investigation
- **Distribution Analysis**: Reveals data distribution, the max-min point, and outlier
- **Further Analysis**: To understand the different factors contributing to PM10 variations over time.
- **Summary**: Project Conclusion

## About me
- **Name**: Geralda Livia Nugraha
- **Email Address**: mc299d5x1168@student.devacademy.id
- **Dicoding ID**: [MC299D5X1168](https://www.dicoding.com/users/alddar/)
