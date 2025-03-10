import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gdown
import os
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

# Title page
st.set_page_config(page_title=" Air Quality Analysis by Geralda Livia")

# Load dataset (local)
#data = pd.read_csv(r"D:\ML Engineer DBS Foundation X Dicoding\latihan_python\all_data_air_quality.csv", encoding='utf-8', engine='python')

# Title of the dashboard
st.title('Data Analysis Project: Air Quality Dashboard')

# Description
st.write('This is a dashboard that show analyzes air pollution data from Dongsi and Wanliu stations from 2013-2017, focusing on PM10 concentrations and meteorological factors')

# About me
st.markdown("""
### About Me
- **Name**: Geralda Livia Nugraha
- **Email Address**: mc299d5x1168@student.devacademy.id
- **Dicoding ID**: [MC299D5X1168](https://www.dicoding.com/users/alddar/)

### Project Overview
This project aims to analyze air quality data from Dongsi and Wanliu stations in China from 2013 to 2017, focusing on PM10 concentrations by examining daily patterns and investigating correlations with meteorological factors. The insights gained will enhance the understanding of pollution patterns and their driving factors, contributing to more effective air quality management strategies. The findings can guide policy decisions on traffic management and emission controls, help residents plan outdoor activities to avoid peak pollution hours, provide scientific evidence for environmental protection measures, support urban planning that considers air quality factors, and contribute to public health initiatives by identifying high-risk pollution periods.

### Define Question  
1. What is the daily pattern of PM10 concentrations at Dongsi and Wanliu stations for the period 2013-2017?
2. Is there a correlation between meteorological factors (TEMP, DEWP and PRES) and PM10 concentration levels at the two stations?        
""")

# ID GDrive
file_id = "11MUFnACVg1Lxh05u7RRb7bEaK-RJTJYh"
output = "data.csv"
url = f'https://drive.google.com/uc?id={file_id}'
# Download data
@st.cache_data
def load_data():
    # Download file
    gdown.download(url, output, quiet=False)
    data = pd.read_csv(output)
    return data
try:
    data = load_data()
    st.write(f"Success Load The Data {data.shape[0]} baris")
    st.dataframe(data.head())
except Exception as e:
    st.error(f"Error: {e}")
# Display raw data sample
with st.expander("Dataset Overview"):
    st.dataframe(data.head())
    st.write(f"Dataset shape: {data.shape}")

# Data preprocessing
@st.cache_data
def preprocess_data(df):
    # Create datetime column
    if 'date' not in df.columns:
        df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    
    # Extract time components
    df['day_of_week'] = df['date'].dt.day_name()
    df['hour_of_day'] = df['date'].dt.hour
    df['month_name'] = df['date'].dt.month_name()
    df['year_month'] = df['date'].dt.strftime('%Y-%m')
    
    # Filter for stations of interest
    dongsi_data = df[df['station'] == 'Dongsi'].copy()
    wanliu_data = df[df['station'] == 'Wanliu'].copy()
    
    return df, dongsi_data, wanliu_data

# Preprocess data
data, dongsi_data, wanliu_data = preprocess_data(data)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Analysis", 
                         ["Overview", 
                          "Daily PM10 Patterns", 
                          "Meteorological Correlations", 
                          "Annual Trends", 
                          "Distribution Analysis",
                          "Further Analysis",
                          "Summary"])



# Overview page
if page == "Overview":
    st.header("Dataset Overview")
    
    # Display basic statistics
    st.subheader("Basic Statistics")
    st.dataframe(data.describe())
    
    # Station information
    st.subheader("Station Information")
    station_counts = data['station'].value_counts()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Records per Station:")
        st.dataframe(station_counts)
    
    with col2:
        fig = px.pie(values=station_counts.values, names=station_counts.index, 
                     title="Data Distribution by Station")
        st.plotly_chart(fig)
    
    # Year and month distribution
    st.subheader("Temporal Distribution")
    
    year_counts = data['year'].value_counts().sort_index()
    month_counts = data['month'].value_counts().sort_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(x=year_counts.index, y=year_counts.values, 
                     labels={'x': 'Year', 'y': 'Count'}, title="Records by Year")
        st.plotly_chart(fig)
    
    with col2:
        fig = px.bar(x=month_counts.index, y=month_counts.values, 
                     labels={'x': 'Month', 'y': 'Count'}, title="Records by Month")
        st.plotly_chart(fig)



# Daily PM10 patterns page
elif page == "Daily PM10 Patterns":
    st.header("Question 1: Daily Pattern of PM10 Concentrations")
    
    # Calculate hourly averages
    dongsi_hourly = dongsi_data.groupby('hour_of_day')['PM10'].mean().reset_index()
    wanliu_hourly = wanliu_data.groupby('hour_of_day')['PM10'].mean().reset_index()
    
    # Combined hourly averages plot
    st.subheader("Average PM10 by Hour of Day")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dongsi_hourly['hour_of_day'], y=dongsi_hourly['PM10'],
                             mode='lines+markers', name='Dongsi Station',
                             line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=wanliu_hourly['hour_of_day'], y=wanliu_hourly['PM10'],
                             mode='lines+markers', name='Wanliu Station',
                             line=dict(color='red', width=2)))
    
    fig.update_layout(
        title='Daily Pattern of PM10 (2013-2017)',
        xaxis_title='Hour of Day',
        yaxis_title='Average PM10',
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        legend=dict(y=0.99, x=0.99, xanchor='right', yanchor='top'),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight about the daily pattern
    st.info("""
    **Insight:** The daily pattern shows two distinct peaks:
    - Morning (7:00-9:00 AM): Likely corresponds to morning rush hour traffic
    - Afternoon (14:00-16:00 PM): Lower concentrations during midday
    - Evening (19:00-22:00 PM): Corresponds to evening activities and reduced atmospheric mixing
    
    Wanliu station shows higher PM10 concentrations than Dongsi station during morning and evening peak hours, 
    while Dongsi station tends to maintain higher concentrations during midday hours. This suggests location-specific 
    differences in pollution sources, daily human activities, and atmospheric conditions throughout the day.
    """)
    
    # Yearly patterns
    st.subheader("Daily Patterns by Year")
    
    years = sorted(data['year'].unique())
    selected_year = st.selectbox("Select Year for Detailed View", years)
    
    dongsi_year = dongsi_data[dongsi_data['year'] == selected_year]
    wanliu_year = wanliu_data[wanliu_data['year'] == selected_year]
    
    dongsi_year_hourly = dongsi_year.groupby('hour_of_day')['PM10'].mean().reset_index()
    wanliu_year_hourly = wanliu_year.groupby('hour_of_day')['PM10'].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dongsi_year_hourly['hour_of_day'], y=dongsi_year_hourly['PM10'],
                             mode='lines+markers', name='Dongsi Station',
                             line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=wanliu_year_hourly['hour_of_day'], y=wanliu_year_hourly['PM10'],
                             mode='lines+markers', name='Wanliu Station',
                             line=dict(color='red', width=2)))
    
    fig.update_layout(
        title=f'Daily Pattern of PM10 Concentrations in {selected_year}',
        xaxis_title='Hour of Day',
        yaxis_title='Average PM10 Concentration',
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        legend=dict(y=0.99, x=0.99, xanchor='right', yanchor='top'),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

# Meteorological Correlations page
elif page == "Meteorological Correlations":
    st.header("Question 2: Correlation Between Meteorological Factors and PM10")
    
    # Overall correlations 
    st.subheader("Overall Correlation Analysis")
    
    # Calculate correlations Between PM10 and Meteorology Parameter 
    # Meteorology Parameter(TEMP, DEWP, PRES)
    corr_features = ['PM10', 'TEMP', 'DEWP', 'PRES']
    correlation = data[corr_features].corr()
    
    # Display correlation matrix
    fig = px.imshow(correlation, 
                    text_auto=True, 
                    color_continuous_scale='RdBu_r',
                    labels=dict(color="Correlation"),
                    zmin=-1, zmax=1)
    fig.update_layout(title='Correlation Between PM10 and Meteorological Factors')
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    st.info("""
    **Insight:** The correlation analysis reveals:
    - Temperature (TEMP) has a weak negative correlation with PM10, suggesting higher temperatures are associated with lower PM10 levels
    - Dew point (DEWP) shows a similar but slightly weaker negative correlation
    - Pressure (PRES) has a very weak positive correlation with PM10
    
    These correlations suggest meteorological factors influence PM10 concentrations, but the relationship is not very strong, indicating other factors (like emissions) likely play more significant roles.
    """)
    
    # Station-specific correlations
    st.subheader("Station-Specific Correlation Analysis")
    
    tab1, tab2 = st.tabs(["Dongsi Station", "Wanliu Station"])
    
    with tab1:
        dongsi_corr = dongsi_data[corr_features].corr()
        fig = px.imshow(dongsi_corr, 
                        text_auto=True, 
                        color_continuous_scale='RdBu_r',
                        labels=dict(color="Correlation"),
                        zmin=-1, zmax=1)
        fig.update_layout(title='Dongsi Station: Correlation Between PM10 and Meteorological Factors')
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        wanliu_corr = wanliu_data[corr_features].corr()
        fig = px.imshow(wanliu_corr, 
                        text_auto=True, 
                        color_continuous_scale='RdBu_r',
                        labels=dict(color="Correlation"),
                        zmin=-1, zmax=1)
        fig.update_layout(title='Wanliu Station: Correlation Between PM10 and Meteorological Factors')
        st.plotly_chart(fig, use_container_width=True)

    # Scatter plots
    st.subheader("Scatter Plots: PM10 vs Meteorological Factors")
    
    meteo_factor = st.selectbox("Select Meteorological Factor", ["TEMP", "DEWP", "PRES"])
    
    fig = px.scatter(data, x=meteo_factor, y='PM10', color='station', opacity=0.5,
                     trendline='ols', trendline_scope='overall',
                     title=f'PM10 vs {meteo_factor} by Station',
                     labels={'PM10': 'PM10'})
    
    st.plotly_chart(fig, use_container_width=True)
    

# Annual Trends page
elif page == "Annual Trends":
    st.header("Annual Trends Analysis")
    
    # Calculate yearly averages
    yearly_avg = data.groupby(['year', 'station'])['PM10'].mean().reset_index()
    
    # Plot yearly trends
    st.subheader("Yearly Average PM10")
    
    fig = px.line(yearly_avg, x='year', y='PM10', color='station',
                  markers=True, line_shape='linear',
                  title='Yearly Average PM10 (2013-2017)',
                  labels={'PM10': 'Average PM10', 'year': 'Year'})
    
    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=min(data['year']), dtick=1),
        legend=dict(y=0.99, x=0.01, xanchor='left', yanchor='top'),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate monthly averages by year
    monthly_avg = data.groupby(['year', 'month', 'station'])['PM10'].mean().reset_index()
    
    # Plot monthly trends
    st.subheader("Monthly Average PM10 by Year")
    
    selected_year = st.selectbox("Select Year", sorted(data['year'].unique()), key="monthly_trends")
    year_data = monthly_avg[monthly_avg['year'] == selected_year]
    
    fig = px.line(year_data, x='month', y='PM10', color='station',
                  markers=True, line_shape='linear',
                  title=f'Monthly Average PM10 in {selected_year}',
                  labels={'PM10': 'Average PM10', 'month': 'Month'})
    
    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        legend=dict(y=0.99, x=0.01, xanchor='left', yanchor='top'),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Annual statistics table
    st.subheader("Annual PM10 Statistics by Station")
    
    # Calculate yearly statistics
    yearly_stats = data.groupby(['year', 'station'])['PM10'].agg([
        'mean', 'median', 'std', 'min', 'max'
    ]).reset_index()
    
    # Format table for display
    yearly_stats = yearly_stats.round(2)
    yearly_stats.columns = ['Year', 'Station', 'Mean', 'Median', 'Std Dev', 'Min', 'Max']
    
    # Display table
    st.dataframe(yearly_stats, use_container_width=True)
    
    # Insight
    st.info("""
    **Insight:** The annual trend analysis shows:
    - A decreasing trend in PM10 concentrations from 2013 to 2016, followed by a significant increase in 2017 for most stations
    - Consistent relative differences between stations across years, with some stations (like Aotizhongxin) consistently lower than others
    - Notable U-shaped pattern across the 5-year period, with 2016 showing the lowest concentrations for almost all stations

    This suggests initial improvement in air quality possibly due to pollution control measures, but a concerning reversal of this 
    trend in 2017 that requires further investigation.
    """)


# Distribution Analysis page
elif page == "Distribution Analysis":
    st.header("Distribution Analysis")
    
    # PM10 distribution
    st.subheader("PM10 Distribution")
    
    tab1, tab2 = st.tabs(["Overall Distribution", "By Station"])
    
    with tab1:
        fig = px.histogram(data, x='PM10', nbins=50,
                          title='Distribution of PM10 ',
                          labels={'PM10': 'PM10', 'count': 'Frequency'})
        
        # Add a vertical line for the mean
        mean_pm10 = data['PM10'].mean()
        fig.add_vline(x=mean_pm10, line_dash="dash", line_color="red")
        fig.add_annotation(x=mean_pm10, y=0.9, yref="paper",
                          text=f"Mean: {mean_pm10:.2f}",
                          showarrow=True, arrowhead=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.histogram(data, x='PM10', color='station', nbins=50,
                          barmode='overlay', opacity=0.7,
                          title='Distribution of PM10 Concentrations by Station',
                          labels={'PM10': 'PM10 Concentration', 'count': 'Frequency'})
        
        # Add vertical lines for the means
        dongsi_mean = dongsi_data['PM10'].mean()
        wanliu_mean = wanliu_data['PM10'].mean()
        
        fig.add_vline(x=dongsi_mean, line_dash="dash", line_color="blue")
        fig.add_vline(x=wanliu_mean, line_dash="dash", line_color="red")
        
        fig.add_annotation(x=dongsi_mean, y=0.95, yref="paper",
                          text=f"Dongsi Mean: {dongsi_mean:.2f}",
                          showarrow=True, arrowhead=1, font=dict(color="blue"))
        
        fig.add_annotation(x=wanliu_mean, y=0.85, yref="paper",
                          text=f"Wanliu Mean: {wanliu_mean:.2f}",
                          showarrow=True, arrowhead=1, font=dict(color="red"))
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Box plots by station and year
    st.subheader("PM10 Distribution by Year and Station")
    
    fig = px.box(data, x='year', y='PM10', color='station',
                title='PM10 Distribution by Year and Station',
                labels={'PM10': 'PM10 Concentration', 'year': 'Year'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Meteorological factors distribution
    st.subheader("Distribution of Meteorological Factors")
    
    meteo_factor = st.selectbox(
        "Select Meteorological Factor", 
        ["TEMP", "DEWP", "PRES"],
        key="meteo_dist"
    )
    
    fig = px.histogram(data, x=meteo_factor, color='station', nbins=50,
                      barmode='overlay', opacity=0.7,
                      title=f'Distribution of {meteo_factor} by Station',
                      labels={meteo_factor: meteo_factor, 'count': 'Frequency'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    st.info(f"""
    **Insight:** The distribution analysis reveals:
    - PM10 concentrations show a right-skewed distribution, indicating occasional high pollution episodes
    - Wanliu station has a higher average PM10 concentration (110.23) compared to Dongsi (104.23), contradicting the statement about Dongsi having higher concentrations
    - Box plots by year and station show varying distributions across years, with extreme values (>800 μg/m³) present in all years
    - Meteorological factors (TEMP, DEWP, PRES) show similar distributions across stations, suggesting regional meteorological conditions
    - Temperature (TEMP) shows a bimodal distribution, reflecting seasonal variations
    """)

# Further Analysis page
elif page == "Further Analysis":
    st.header("Further Analysis")
    
    # Time Series Decomposition
    st.subheader("Time Series Decomposition of PM10")
    
    st.write("""
    This analysis decomposes the PM10 time series into trend, seasonal, and residual components
    to better understand the temporal patterns.
    """)
    
    # Create daily aggregated data
    @st.cache_data
    def create_daily_data(station_data):
        daily_data = station_data.groupby(pd.Grouper(key='date', freq='D'))['PM10'].mean().reset_index()
        # Fill missing values using interpolation
        daily_data['PM10'] = daily_data['PM10'].interpolate(method='linear')
        return daily_data
    
    # Select station for decomposition
    station = st.selectbox("Select Station for Decomposition", ["Dongsi", "Wanliu"])
    station_data = dongsi_data if station == "Dongsi" else wanliu_data
    
    daily_station_data = create_daily_data(station_data)
    
    # Plot the daily data
    fig = px.line(daily_station_data, x='date', y='PM10',
                 title=f'{station} Station: Daily Average PM10 Concentrations',
                 labels={'PM10': 'PM10 Concentration', 'date': 'Date'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Perform decomposition if data is sufficient
    if len(daily_station_data) > 365:
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        # Set date as index for decomposition
        daily_station_data = daily_station_data.set_index('date')
        
        # Perform decomposition
        decomposition = seasonal_decompose(daily_station_data['PM10'], model='additive', period=365)
        
        # Create dataframe from decomposition results
        decomp_data = pd.DataFrame({
            'original': daily_station_data['PM10'],
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid
        }).reset_index()
        
        # Plot decomposition components
        components = ['original', 'trend', 'seasonal', 'residual']
        titles = ['Original Data', 'Trend Component', 'Seasonal Component', 'Residual Component']
        
        for component, title in zip(components, titles):
            fig = px.line(decomp_data, x='date', y=component,
                         title=f'{title}',
                         labels={component: 'Value', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Interpretation
        st.info("""
        **Decomposition Interpretation:**
        - **Trend Component:** Shows the long-term progression of PM10 concentrations over time, revealing whether pollution is generally increasing or decreasing.
        - **Seasonal Component:** Captures the repeating annual pattern, showing how PM10 levels fluctuate throughout the year.
        - **Residual Component:** Represents the irregular fluctuations not explained by trend or seasonality, which could be related to special events or measurement errors.
        
        This decomposition helps us understand the different factors contributing to PM10 variations over time.
        """)
    else:
        st.error("Insufficient data for meaningful decomposition. Need at least 365 days of data.")
    
# Distribution Analysis page
elif page == "Summary":
    st.header("Project Summary")
    st.subheader("Conclusion: Air Quality Analysis Dashboard")
    st.markdown("""         
    ### Summary of Findings
    #### Daily Patterns of PM10 Concentrations
    Result: identified clear daily patterns in PM10 concentrations at both monitoring stations
    - A bimodal pattern emerged with distinct morning peaks (7:00-9:00 AM) coinciding with morning rush hour traffic
    - Evening peaks (19:00-22:00 PM) aligned with evening activities and traffic
    - Mid-afternoon troughs (14:00-16:00 PM) showed the lowest pollution levels
    - Dongsi station consistently recorded higher PM10 concentrations than Wanliu, suggesting greater pollution in the urban center

    #### Correlation with Meteorological Factors
    Result: revealed relationships between PM10 and meteorological parameters
    - Temperature (TEMP): Weak negative correlation at both stations, slightly stronger at Dongsi
    - Dew Point (DEWP): Similar weak negative correlation pattern
    - Atmospheric Pressure (PRES): Very weak positive correlation
    - The correlations were generally stronger at Dongsi station, suggesting meteorological factors may have more influence in urban center locations

    #### Anual Trends
    Result: know the anual trend for further investigation
    - A decreasing trend in PM10 concentrations from 2013 to 2016, followed by a significant increase in 2017 for most stations
    - Consistent relative differences between stations across years, with some stations (like Aotizhongxin) consistently lower than others
    - Notable U-shaped pattern across the 5-year period, with 2016 showing the lowest concentrations for almost all stations
    
    #### Distribution Analysis
    Result: reveals some information like the type of data distribution, the max-min point, and outlier.
    - PM10 concentrations show a right-skewed distribution, indicating occasional high pollution episodes
    - Wanliu station has a higher average PM10 concentration (110.23) compared to Dongsi (104.23), contradicting the statement about Dongsi having higher concentrations
    - Box plots by year and station show varying distributions across years, with extreme values (>800 μg/m³) present in all years
    - Meteorological factors (TEMP, DEWP, PRES) show similar distributions across stations, suggesting regional meteorological conditions
    - Temperature (TEMP) shows a bimodal distribution, reflecting seasonal variations
    
    #### Futher Analysis
    Result: from decomposition interpretation helps us to understand the different factors contributing to PM10 variations over time.
    - Trend Component: Shows the long-term progression of PM10 concentrations over time, revealing whether pollution is generally increasing or decreasing.
    - Seasonal Component: Captures the repeating annual pattern, showing how PM10 levels fluctuate throughout the year.
    - Residual Component: Represents the irregular fluctuations not explained by trend or seasonality, which could be related to special events or measurement errors.
    
    ### Addressing the Research Questions
    The dashboard successfully addressed all the research questions defined in the project overview:
    1. **What are the daily patterns of PM10 concentrations?**  
    The analysis clearly identified and visualized the bimodal daily pattern, showing morning and evening peaks with afternoon troughs.
    2. **How do meteorological factors correlate with PM10 concentrations?**  
    The correlation analysis quantified the relationships between PM10 and temperature, dew point, and pressure, finding weak but consistent patterns.    
""")
        
