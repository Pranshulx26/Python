import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 

st.set_page_config(layout='wide', page_title='Startup Funding Dashboard', page_icon=':bar_chart:')
df = pd.read_csv(r'C:\Users\yashs\Python\week8\startup-dashboard\cleaned_startup_funding_2.csv')
df.rename(columns={'Industry Vertical': 'Vertical', 'City  Location': 'City', 'InvestmentnType': 'Investment Type'}, inplace=True)
print(df.info())

def load_investor_details(investor_name):
    st.header(f"Details for Investor: {investor_name}")
    # load the recent 5 investments made by this investor
    investor_df = df[df['Investors Name'].str.contains(investor_name, case=False, na=False)]
    st.subheader('Recent Investments')
    st.dataframe(investor_df.head()[['Date', 'Startup Name', 'Vertical', 'City', 'Investment Type', 'Amount in INR (Cr)']])


    col1, col2 = st.columns(2)
    # biggest investments 
    with col1:
        st.subheader('Biggest Investments')
        biggest_investments = df[df['Investors Name'].str.contains(investor_name, case=False, na=False)].groupby('Startup Name')['Amount in INR (Cr)'].sum().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots()
        ax.bar(biggest_investments.index, biggest_investments.values)
        ax.set_xlabel('Amount in INR (Cr)')
        ax.set_title(f'Biggest Investments by {investor_name}')
        st.pyplot(fig)

    with col2:
        st.subheader('Investment by Vertical')
        investment_by_vertical = df[df['Investors Name'].str.contains(investor_name, case=False, na=False)].groupby('Vertical')['Amount in INR (Cr)'].sum().sort_values(ascending=True).head(5)
        fig2, ax2 = plt.subplots()
        ax2.pie(investment_by_vertical.values, labels=investment_by_vertical.index, autopct='%1.1f%%')
        ax2.set_title(f'Investment by Vertical for {investor_name}')
        st.pyplot(fig2)
    
    st.subheader('Investment by City')
    investment_by_city = df[df['Investors Name'].str.contains(investor_name, case=False, na=False)].groupby('City')['Amount in INR (Cr)'].sum().sort_values(ascending=True).head(5)
    fig3, ax3 = plt.subplots()
    ax3.pie(investment_by_city.values, labels=investment_by_city.index, autopct='%1.1f%%')
    ax3.set_title(f'Investment by City for {investor_name}')
    st.pyplot(fig3)

    # investment over the years.
    st.subheader('Investment Over the Years')
    investment_over_years = df[df['Investors Name'].str.contains(investor_name, case=False, na=False)].groupby('year')['Amount in INR (Cr)'].sum().sort_index()
    fig4, ax4 = plt.subplots()
    ax4.plot(investment_over_years.index, investment_over_years.values, marker='o')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Amount in INR (Cr)')
    ax4.set_title(f'Investment Over the Years for {investor_name}')
    st.pyplot(fig4)

def load_overall_analysis():
    st.title('Overall Analysis of Startup Funding')

    # total invested amount
    total_invested = df['Amount in INR (Cr)'].sum()
    st.metric(label='Total Invested Amount (in Cr)', value=f"{total_invested:,.2f}")

    # maximum invested amount in a single startup
    max_investment = df.groupby('Startup Name')['Amount in INR (Cr)'].sum().max()
    st.metric(label='Maximum Investment in a Single Startup (in Cr)', value=f"{max_investment:,.2f}")

    # average investment amount
    avg_investment = df.groupby('Startup Name')['Amount in INR (Cr)'].sum().mean()
    st.metric(label='Average Investment per Startup (in Cr)', value=f"{avg_investment:,.2f}")

    # MOM graph
    st.subheader('Month on Month Investment')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        mom_investment = df.groupby(['year', 'month'])['Amount in INR (Cr)'].sum().reset_index()
        mom_investment['month_year'] = mom_investment.apply(lambda x: f"{x['month']}/{x['year']}", axis=1)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(mom_investment['month_year'], mom_investment['Amount in INR (Cr)'], marker='o')
        ax.set_xlabel('Month/Year')
        ax.set_ylabel('Amount in INR (Cr)')
        ax.set_title('Month on Month Investment')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        mom_investment = df.groupby(['year', 'month'])['Startup Name'].count().reset_index()
        mom_investment['month_year'] = mom_investment.apply(lambda x: f"{x['month']}/{x['year']}", axis=1)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(mom_investment['month_year'], mom_investment['Startup Name'], marker='o')
        ax.set_xlabel('Month/Year')
        ax.set_ylabel('Number of Startups')
        ax.set_title('Month on Month Investment')
        plt.xticks(rotation=45)
        st.pyplot(fig)




st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(df['Startup Name'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')

else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['Investors Name'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
