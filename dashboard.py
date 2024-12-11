import streamlit as st
import pandas as pd
import plotly.express as px
import random
import numpy as np
from datetime import datetime

# Gerando dados fictícios com valores grandes
def generate_data(num_records=5000):
    categories = ['Travel', 'Commissions', 'Suppliers']
    data = {
        'Date': [datetime.now().strftime('%Y-%m-%d')] * num_records,
        'Amount': [random.randint(500, 5000) for _ in range(num_records)],
        'Category': [random.choice(categories) for _ in range(num_records)],
        'Description': [f'Transaction {i}' for i in range(num_records)],
        'Method': [random.choice(['Credit Card', 'Debit Card', 'Transfer', 'Boleto']) for _ in range(num_records)],
        'Transaction_ID': [f'ID_{i}' for i in range(num_records)],
    }
    df = pd.DataFrame(data)
    return df

# Carregando dados
df = generate_data()

# Calculando KPIs
total_spent = df['Amount'].sum()
total_travel = df[df['Category'] == 'Travel']['Amount'].sum()
total_commissions = df[df['Category'] == 'Commissions']['Amount'].sum()
total_suppliers = df[df['Category'] == 'Suppliers']['Amount'].sum()

# Layout do Dashboard
st.set_page_config(page_title="Corporate Reconciliation Dashboard", page_icon="💼", layout="wide")

# Cabeçalho do Dashboard
st.title("Corporate Reconciliation Dashboard")
st.markdown("""
    This dashboard provides insights into corporate reconciliation data, highlighting key expenses across various categories.
    Use the visualizations below to gain an overview of financial transactions.
""")

# Exibindo KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Spent", f"€{total_spent:,.2f}", delta=f"€{total_spent - total_travel - total_commissions - total_suppliers:,.2f}")
    
with col2:
    st.metric("Total Travel", f"€{total_travel:,.2f}", delta=f"€{total_travel - total_commissions:,.2f}")
    
with col3:
    st.metric("Total Commissions", f"€{total_commissions:,.2f}", delta=f"€{total_commissions - total_suppliers:,.2f}")

# Gráfico de Dispersão de Gastos por Categoria
fig = px.bar(df.groupby('Category')['Amount'].sum().reset_index(), 
             x='Category', y='Amount', 
             color='Category', 
             labels={'Amount': 'Total Amount Spent', 'Category': 'Expense Category'},
             title="Total Amount Spent by Category",
             color_discrete_map={"Travel": "royalblue", "Commissions": "darkorange", "Suppliers": "green"})

st.plotly_chart(fig, use_container_width=True)

# Gráfico de Evolução de Gastos ao Longo do Tempo
df['Date'] = pd.to_datetime(df['Date'])
df_monthly = df.groupby([df['Date'].dt.to_period('M'), 'Category'])['Amount'].sum().reset_index()
df_monthly['Date'] = df_monthly['Date'].dt.strftime('%Y-%m')

fig2 = px.line(df_monthly, x='Date', y='Amount', color='Category', markers=True, 
               title="Monthly Spend Trend by Category", 
               labels={'Amount': 'Monthly Spend', 'Date': 'Month'},
               color_discrete_map={"Travel": "royalblue", "Commissions": "darkorange", "Suppliers": "green"})

st.plotly_chart(fig2, use_container_width=True)

# Gráfico de
