import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

hour_df = pd.read_csv("dashboard/hour_df.csv")
hour_df['date'] = pd.to_datetime(hour_df['date'])

def performa_persewaan_sepeda(df):
    performa_df = df.resample(rule='M', on='date').agg({
        'count': 'sum'
    })
    performa_df = performa_df.reset_index()
    performa_df.rename(columns={
        'count': 'total_penyewa_sepeda'
    }, inplace=True)

    return performa_df

def perbandingan_persewaan_sepeda(df):
    perbandingan_sewa_df = df.groupby("workingday").agg({
        'count' : 'sum'})
    perbandingan_sewa_df = perbandingan_sewa_df.reset_index()
    perbandingan_sewa_df.rename(columns={
        'count' : 'perbandingan_sewa'
    }, inplace=True)

    return perbandingan_sewa_df

#filter tanggal
min_date = hour_df['date'].min()
max_date = hour_df['date'].max()

with st.sidebar:
    st.image("dashboard/bike-sharing.jpg")

    start_date, end_date = st.date_input(
        label='Jangka Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = hour_df[(hour_df["date"] >= str(start_date)) & (hour_df["date"] <= str(end_date))]

performa_df = performa_persewaan_sepeda(main_df)
perbandingan_sewa_df = perbandingan_persewaan_sepeda(main_df)

st.header(':bike: Dashboard Persewaan Sepeda :bike:')

#Pertanyaan 1: Performa persewaan sepeda
st.subheader('Performa Persewaan Sepeda')
fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    performa_df["date"],
    performa_df['total_penyewa_sepeda'],
    marker='o',
    linewidth=2,
    color='#90CAF9'
)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

#Pertanyaan 2: Perbandingan Persewaan di weekdays dan weekend
st.subheader('Perbandingan Persewaan Sepeda: Weekdays vs Weekend')
labels = 'Weekdays', 'Weekend'
sizes = perbandingan_sewa_df['perbandingan_sewa'].tolist()
explode = (0.1, 0)
    
fig2, ax2 =plt.subplots()
ax2.pie(sizes, 
        explode=explode, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90
        )
ax2.axis('equal')
st.pyplot(fig2)


st.subheader('Rata-rata Persewaan Sepeda')
col1, col2, col3 = st.columns(3)

#Pertanyaan 3: Rata-rata sewa sepeda berdasarkan musim
with col1:
    col1.markdown('Berdasarkan Musim')
    by_season = hour_df.groupby('season')[['casual','registered']].mean().reset_index()
    
    st.bar_chart(
        by_season,
        x = 'season',
        y = ['casual', 'registered']
        )

#Pertanyaan 4: Rata-rata sewa sepeda berdasarkan kondisi cuaca
with col2:
    col2.markdown('Berdasarkan Cuaca')
    by_weather = hour_df.groupby('weathersit')[['casual','registered']].mean().reset_index()
    
    st.bar_chart(
        by_weather,
        x = 'weathersit',
        y = ['casual', 'registered']
        )

#Pertanyaan 5: Rata-rata sewa sepeda berdasarkan hari
with col3:
    col3.markdown('Berdasarkan Hari')
    by_day = hour_df.groupby('weekday')[['casual','registered']].mean().reset_index()

    st.bar_chart(
        by_day,
        x = 'weekday',
        y = ['casual', 'registered']
        )


#Analisis Lanjutan
def bagi_waktu(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 15:
        return 'Afternoon'
    elif 15 <= hour < 20:
        return 'Evening'
    else:
        return 'Night'

hour_df['rentang_waktu'] = hour_df['hour'].apply(bagi_waktu)

def rentang_persewaan_sepeda(df):
    rentang_sewa_df = df.groupby('rentang_waktu').agg({
        'count' : 'sum'})
    rentang_sewa_df = rentang_sewa_df.reset_index()
    rentang_sewa_df.rename(columns={
        'count' : 'rentang_sewa'
    }, inplace=True)

    return rentang_sewa_df

rentang_sewa_df = rentang_persewaan_sepeda(main_df)

#Rentang waktu persewaan sepeda
st.subheader('Rentang Waktu Persewaan Sepeda')
st.bar_chart(
        data = rentang_sewa_df,
        x = 'rentang_waktu',
        y = 'rentang_sewa'
        )
