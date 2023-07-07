import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')
def create_daily_rentbike_df(df):
    daily_rentbike_df = df.resample(rule='D', on='dteday').agg({
        'cnt' : 'sum'
    })
    daily_rentbike_df = daily_rentbike_df.reset_index()
    daily_rentbike_df.rename(columns={
        'cnt' : 'jumlah_rent_bike'
    }, inplace = True)

    return daily_rentbike_df

def create_workingday_df(df):
    workingday_df = df.groupby(by='workingday').cnt.sum().reset_index()
    workingday_df.rename(columns={
        'cnt' : 'jumlah_rent_bike'
    }, inplace=True)

    return workingday_df

def create_weathersit_df(df):
    weathersit_df = df.groupby(by='weathersit').cnt.sum().reset_index()
    weathersit_df.rename(columns={
        'cnt' : 'jumlah_rent_bike'
    }, inplace=True)

    return weathersit_df

main_data = pd.read_csv('main_data.csv')
main_data['dteday'] = pd.to_datetime(main_data['dteday'])

min_date = main_data['dteday'].min()
max_date = main_data['dteday'].max()

with st.sidebar:
    st.image('https://cdn.pixabay.com/photo/2017/01/31/14/44/bicycle-2024675_1280.png')

    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = main_data[(main_data['dteday'] >= str(start_date)) &
                  (main_data['dteday'] <= str(end_date))]

daily_rentbike_df = create_daily_rentbike_df(main_df)
workingday_df = create_workingday_df(main_df)
weathersit_df = create_weathersit_df(main_df)

st.header('Rent Bike :sparkles:')

st.subheader('Daily Rent')

col1, col2 = st.columns(2)

with col1:
    total_rent = daily_rentbike_df.jumlah_rent_bike.sum()
    st.metric('Total rent', value=total_rent)

fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    daily_rentbike_df['dteday'],
    daily_rentbike_df['jumlah_rent_bike'],
    marker = 'o',
    linewidth = 2,
)

st.pyplot(fig)

st.subheader('Working Day Rent')
fig, ax = plt.subplots(figsize=(16,8))
sns.barplot(x='workingday', y='jumlah_rent_bike', data=workingday_df)

st.pyplot(fig)

st.subheader('Weather Rent')
fig, ax = plt.subplots(figsize=(16,8))
colors = ['blue','grey','grey','grey']
sns.barplot(x='weathersit', y='jumlah_rent_bike', data=weathersit_df, palette=colors)

st.pyplot(fig)