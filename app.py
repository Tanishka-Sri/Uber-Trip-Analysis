import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="UberRide", layout="wide")
st.title("🚕 UberRide 🚕")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("uber-raw-data-sep14.csv")
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    df['Day'] = df['Date/Time'].dt.day
    df['Weekday'] = df['Date/Time'].dt.weekday
    df['Hour'] = df['Date/Time'].dt.hour
    df['Month'] = df['Date/Time'].dt.month_name()
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("📊 Filters")
selected_hour = st.sidebar.slider("Select Hour", 0, 23, (0, 23))
selected_day = st.sidebar.slider("Select Day", int(df.Day.min()), int(df.Day.max()), (int(df.Day.min()), int(df.Day.max())))

filtered_df = df[(df['Hour'] >= selected_hour[0]) & (df['Hour'] <= selected_hour[1]) &
                 (df['Day'] >= selected_day[0]) & (df['Day'] <= selected_day[1])]

# Show metrics
st.markdown(f"### 📈 Total Trips: {len(filtered_df):,}")

# Trips per Hour
st.subheader("Trips per Hour")
fig1, ax1 = plt.subplots()
sns.countplot(x='Hour', data=filtered_df, palette='viridis', ax=ax1)
ax1.set_title('Number of Trips by Hour')
st.pyplot(fig1)

# Trips per Weekday
st.subheader("Trips per Weekday")
fig2, ax2 = plt.subplots()
sns.countplot(x='Weekday', data=filtered_df, palette='coolwarm', ax=ax2)
ax2.set_title('Number of Trips by Weekday')
st.pyplot(fig2)

# Heatmap
st.subheader("📊 Heatmap: Day vs Hour")
heatmap_data = filtered_df.groupby(['Day','Hour']).size().unstack(fill_value=0)
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax3)
st.pyplot(fig3)

# Pickup location scatter plot
st.subheader("🗺️ Pickup Locations")
fig4, ax4 = plt.subplots(figsize=(10, 10))
ax4.scatter(filtered_df['Lon'], filtered_df['Lat'], s=1, alpha=0.5)
ax4.set_title("Pickup Locations in NYC")
ax4.set_xlabel("Longitude")
ax4.set_ylabel("Latitude")
st.pyplot(fig4)
