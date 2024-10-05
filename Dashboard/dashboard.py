import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set seaborn style
sns.set(style='dark')

def create_weekday_analysis(df):
    # Create weekday descriptions
    df['workingday_desc'] = df['workingday'].map({0: 'Weekend', 1: 'Weekday'})
    weekday_rentals = df.groupby('workingday_desc')['cnt'].sum()
    weekday_rentals_casual = df.groupby('workingday_desc')['casual'].sum()
    weekday_rentals_registered = df.groupby('workingday_desc')['registered'].sum()
    
    return weekday_rentals, weekday_rentals_casual, weekday_rentals_registered

def create_daily_analysis(df):
    weekday_name = {
        0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
        4: 'Thursday', 5: 'Friday', 6: 'Saturday'
    }
    df['weekday_name'] = df['weekday'].map(weekday_name)
    weekday_avg_cnt = df.groupby('weekday')['cnt'].mean()
    weekday_avg_casual = df.groupby('weekday_name')['casual'].mean()
    weekday_avg_registered = df.groupby('weekday')['registered'].mean()
    
    return weekday_avg_cnt, weekday_avg_casual, weekday_avg_registered, weekday_name

def create_seasonal_analysis(df):
    df['season_desc'] = df['season'].map({
        1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
    })
    season_cnt = df.groupby('season_desc')['cnt'].sum()
    return season_cnt

# Sidebar
with st.sidebar:
    # Add Image
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Add Title
    st.title("Bike Rental Analysis")
    
    # Add information
    st.markdown("Created by:")
    st.markdown("A. Kafaby Syairozie")  

# Load your data
day_df = pd.read_csv("day.csv")  # Adjust the path as needed


# Create Streamlit app
st.header('Bike Rental Analysis Dashboard :bike:')

# Create all analysis dataframes
weekday_rentals, weekday_rentals_casual, weekday_rentals_registered = create_weekday_analysis(day_df)
weekday_avg_cnt, weekday_avg_casual, weekday_avg_registered, weekday_name = create_daily_analysis(day_df)
season_cnt = create_seasonal_analysis(day_df)

# Add metrics
st.subheader('Key Metrics')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = day_df['cnt'].sum()
    st.metric("Total Rentals", f"{total_rentals:,}")

with col2:
    avg_daily_rentals = day_df['cnt'].mean()
    st.metric("Average Daily Rentals", f"{avg_daily_rentals:,.0f}")

with col3:
    peak_rentals = day_df['cnt'].max()
    st.metric("Peak Daily Rentals", f"{peak_rentals:,}")

# Weekday vs Weekend Analysis
st.subheader('Weekday vs Weekend Analysis')

col1, col2 = st.columns(2)

with col1:
    # Pie chart for weekday/weekend distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.pie(weekday_rentals, 
            labels=weekday_rentals.index, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=['#90CAF9', '#D3D3D3'])
    plt.title('Proportion of Bike Rentals between Weekdays and Weekends')
    plt.axis('equal')
    st.pyplot(fig)

with col2:
    # Bar chart for casual vs registered users
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    x = np.arange(len(weekday_rentals_casual))
    
    plt.bar(x - width/2, weekday_rentals_casual.values / 1000, 
            width, label='Casual', color='#90CAF9')
    plt.bar(x + width/2, weekday_rentals_registered.values / 1000, 
            width, label='Registered', color='#D3D3D3')
    
    plt.xlabel(None)
    plt.ylabel('Total Rental Count (in thousands)')
    plt.title('Comparison of Bike Rentals (Casual & Registered)')
    plt.xticks(x, weekday_rentals_casual.index)
    plt.legend()
    st.pyplot(fig)

# Daily Analysis
st.subheader('Daily Rental Patterns')

col1, col2 = st.columns(2)

with col1:
    # Pie chart for daily distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.pie(weekday_avg_cnt, 
            labels=[weekday_name[i] for i in weekday_avg_cnt.index],
            autopct='%1.1f%%', 
            startangle=140, 
            counterclock=False,
            colors=sns.color_palette("pastel"))
    plt.title('Proportion of Average Bike Rentals in a Week')
    plt.axis('equal')
    st.pyplot(fig)

with col2:
    # Bar chart for daily casual vs registered
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(7)
    width = 0.35
    
    plt.bar(x - width/2, weekday_avg_casual, 
            width, label='Casual', color='#90CAF9')
    plt.bar(x + width/2, weekday_avg_registered, 
            width, label='Registered', color='#D3D3D3')
    
    plt.xlabel(None)
    plt.ylabel('Average Rental Count')
    plt.title('Average Bike Rentals by Day of Week')
    plt.xticks(x, weekday_name.values(), rotation=45)
    plt.legend()
    st.pyplot(fig)

# Seasonal Analysis
st.subheader('Percentage Total Rental in Any Seasons')

fig, ax = plt.subplots(figsize=(10, 6))
plt.pie(season_cnt, 
        labels=season_cnt.index, 
        autopct='%1.1f%%', 
        startangle=200, 
        counterclock=False,
        colors=sns.color_palette("pastel"))
plt.title('Distribution of Bike Rentals by Season')
st.pyplot(fig)

# Correlation
st.subheader('Correlation Temperature and Total Rental')

# Temperature correlation scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
plt.scatter(day_df['temp'], day_df['cnt'], 
            alpha=0.5, color='#90CAF9')
plt.xlabel('Temperature (°C)')
plt.ylabel('Total Rental Count')
plt.title('Temperature vs Rental Count')
    
# Calculate and display correlation
correlation = day_df['temp'].corr(day_df['cnt'])
plt.text(0.05, 0.95, f'Correlation: {correlation:.2f}', 
         transform=ax.transAxes, 
         bbox=dict(facecolor='white', alpha=0.8))
    
st.pyplot(fig)


st.caption('Copyright © 2024 A. Kafaby Syairozie')
