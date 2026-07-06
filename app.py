import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Business KPI Dashboard", page_icon="📈", layout="wide")

st.markdown("""
<style>
.main{background:#f5f7fb;}
.block-container{padding-top:1rem;}
div[data-testid="metric-container"]{
background:linear-gradient(135deg,#4facfe,#00f2fe);
padding:20px;border-radius:15px;color:white;
box-shadow:0px 10px 25px rgba(0,0,0,.15);}
section[data-testid="stSidebar"]{background:#111827;}
section[data-testid="stSidebar"] *{color:white;}
</style>
""", unsafe_allow_html=True)

np.random.seed(42)
months=pd.date_range("2025-01-01",periods=12,freq="ME")
regions=["North","South","East","West"]
categories=["Technology","Furniture","Office Supplies"]
rows=[]
for m in months:
    for r in regions:
        for c in categories:
            rev=np.random.randint(40000,120000)
            prof=rev*np.random.uniform(.18,.35)
            cust=np.random.randint(200,900)
            rows.append([m.strftime("%b"),r,c,rev,prof,cust])
df=pd.DataFrame(rows,columns=["Month","Region","Category","Revenue","Profit","Customers"])

up=st.sidebar.file_uploader("Upload CSV",type=["csv"])
if up:
    df=pd.read_csv(up)

region=st.sidebar.multiselect("Region",df.Region.unique(),default=list(df.Region.unique()))
category=st.sidebar.multiselect("Category",df.Category.unique(),default=list(df.Category.unique()))
filtered=df[df.Region.isin(region)&df.Category.isin(category)]

st.title("📊 Modern Business KPI Dashboard")
c1,c2,c3,c4=st.columns(4)
c1.metric("Revenue",f"${filtered.Revenue.sum():,.0f}")
c2.metric("Profit",f"${filtered.Profit.sum():,.0f}")
c3.metric("Customers",f"{filtered.Customers.sum():,}")
growth=filtered.Customers.sum()/df.Customers.sum()*100
c4.metric("Customer Growth",f"{growth:.1f}%")

monthly=filtered.groupby("Month",sort=False)[["Revenue","Profit"]].sum().reset_index()
st.plotly_chart(px.line(monthly,x="Month",y=["Revenue","Profit"],markers=True,template="plotly_dark"),use_container_width=True)
col1,col2=st.columns(2)
with col1:
    st.plotly_chart(px.bar(filtered.groupby("Region")["Revenue"].sum().reset_index(),x="Region",y="Revenue",color="Revenue"),use_container_width=True)
with col2:
    st.plotly_chart(px.pie(filtered,names="Category",values="Profit",hole=.55),use_container_width=True)
st.plotly_chart(px.scatter(filtered,x="Revenue",y="Customers",color="Category",size="Profit",hover_name="Region"),use_container_width=True)
st.dataframe(filtered,use_container_width=True)
st.download_button("Download Filtered Data",filtered.to_csv(index=False),"business_data.csv")
