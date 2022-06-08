import pandas as pd
import plotly_express as px
import streamlit as st

st.set_page_config(page_title = 'Sale Dashboard',
                   page_icon = ':bar_chart:',
                   layout = 'wide'
                   )

@st.cache

def get_data_from_excel():
    df = pd.read_excel(r'supermarkt_sales.xlsx', skiprows = 3, usecols = 'B:R')
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    df.columns = df.columns.str.title()
    return df
df = get_data_from_excel()

print(df.head())

st.sidebar.header('Please, filter here:')
city = st.sidebar.multiselect(
    'Select the city',
    options = df['City'].unique(),
    default = df['City'].unique()
)

customer = st.sidebar.multiselect(
    'Select the Customer type',
    options = df['Customer_Type'].unique(),
    default = df['Customer_Type'].unique()
)

gender = st.sidebar.multiselect(
    'Select the Gender',
    options = df['Gender'].unique(),
    default = df['Gender'].unique()
)

df_selection = df.query(
    'City == @city & Customer_Type == @customer & Gender == @gender'
)

st.title(':bar_chart: Sales Dashboard')
st.markdown('---')

total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating = ':star:' * int(round(average_rating, 0))
average_sales_by_transaction = round(df_selection['Total'].mean(), 2)


left_column, middle_column,right_column = st.columns(3)
with left_column:
    st.subheader('Total Sales')
    st.subheader(f'U$ {total_sales:,}')
with middle_column:
    st.subheader('Average Rating')
    st.subheader(f'{average_rating} {star_rating}')
with right_column:
    st.subheader('Average sales by transaction')
    st.subheader(f'U$ {average_sales_by_transaction:,}')

st.markdown('---')

sales_by_product_line = (
    df_selection.groupby('Product Line').sum()[['Total']].sort_values('Total', ascending=True)
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x = 'Total',
    y = sales_by_product_line.index,
    orientation= 'h',
    title= '<b>Total sales per product</b>',
    color_discrete_sequence= ['#0083B8'] * len(sales_by_product_line),
    template= 'plotly_white'
)

fig_product_sales.update_layout(
    plot_bgcolor = 'rgba(0,0,0,0)',   #remove o fundo (coloca ele como transparente)
    xaxis = (dict(showgrid = False))  #remove  as barras
)


sales_by_hour = df_selection.groupby('Hour').sum()[['Total']].sort_values('Total', ascending=True)
fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = 'Total',
    title = '<b> Sales by Hour</b>',
    color_discrete_sequence= ['#0083B8'] * len(sales_by_hour),
    template= 'plotly_white'
)

fig_hourly_sales.update_layout(
    plot_bgcolor = 'rgba(0,0,0,0)',   #remove o fundo (coloca ele como transparente)
    yaxis = (dict(showgrid = False))  #remove  as barras
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width = True)
right_column.plotly_chart(fig_hourly_sales, use_container_width = True)  

hide_st_style = '''
                <style>
                #MainMenu {visibility:hidden;}
                footer {visibility:hidden;}
                header {visibility:hidden;}
                </style>'''
st.markdown(hide_st_style, unsafe_allow_html = True)
