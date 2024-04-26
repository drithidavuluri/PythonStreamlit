import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Set the page configuration for the dashboard
st.set_page_config(page_title="Instagram Influencer Analysis", layout="wide")

# Function to load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("instagram.csv", encoding='utf-8', skipinitialspace=True)
    df.columns = df.columns.str.strip().str.replace("\n", " ").str.replace("  ", " ")
    
    # Convert 'K' and 'M' in numerical fields to thousands and millions
    def convert_k_m_to_number(x):
        if isinstance(x, str):
            if 'K' in x:
                return float(x.replace('K', '')) * 1e3
            elif 'M' in x:
                return float(x.replace('M', '')) * 1e6
        return float(x)

    df['Followers'] = df['Followers'].apply(convert_k_m_to_number)
    df['Authentic engagement'] = df['Authentic engagement'].apply(convert_k_m_to_number)
    df['Engagement avg'] = df['Engagement avg'].apply(convert_k_m_to_number)
    
    return df

df = load_data()

# Title of the dashboard
#st.title("Instagram Influencer Dashboard")

# Display the raw data as a table
# st.subheader("Data Overview")
# if st.checkbox("Show raw data"):
#     st.write(df)

# Layout for plots
col1, col2, col3 = st.columns(3)
with col1:
    # Histogram of followers distribution
    #st.subheader("Distribution of Followers")
    fig = px.histogram(df, x='Followers', nbins=50, title="Distribution of Followers")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Box plot for authentic engagement by category
    #st.subheader("Authentic Engagement by Category")
    fig = px.box(df, x='category_1', y='Authentic engagement', color='category_1',
                 title="Authentic Engagement by Category")
    st.plotly_chart(fig, use_container_width=True)

with col3:
    # Box plot for average engagement by category
    #st.subheader("Average Engagement by Category")
    fig2 = px.box(df, x='category_1', y='Engagement avg', color='category_1',
                  title="Average Engagement by Category")
    st.plotly_chart(fig2, use_container_width=True)

col4, col5, col6 = st.columns(3)
with col4:
    # Pie chart for audience country distribution
    #st.subheader("Audience Country Distribution")
    country_counts = df['Audience country(mostly)'].value_counts()
    fig = px.pie(values=country_counts, names=country_counts.index, title="Audience Country Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col5:
    # Scatter plot with regression line for engagement vs followers
    #st.subheader("Authentic Engagement vs. Followers")
    fig = px.scatter(df, x='Followers', y='Authentic engagement', trendline="ols",
                     title="Authentic Engagement vs. Followers with Regression Line")
    st.plotly_chart(fig, use_container_width=True)

with col6:
    # Correlation heatmap
    #st.subheader("Correlation Heatmap")
    corr = df[['Followers', 'Authentic engagement', 'Engagement avg']].corr()
    plt.figure(figsize=(7, 4))  # Adjust size to fit within the column
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    st.pyplot(plt)

# Using an additional row for the bar chart
#st.subheader("Top Influencers by Authentic Engagement")
top_engagement = df.nlargest(10, 'Authentic engagement')[['instagram name', 'Authentic engagement']]
fig = px.bar(top_engagement, x='instagram name', y='Authentic engagement', title="Top Influencers by Authentic Engagement")
st.plotly_chart(fig, use_container_width=True)
