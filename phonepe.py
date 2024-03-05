import streamlit as st
from streamlit_option_menu import option_menu
import PIL 
from PIL import Image
import base64
import plotly.express as px
import mysql.connector
import json
import pandas as pd
import os

#DATAFRAME CREATION
#sql connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="phonepe")
print(mydb)
mycursor = mydb.cursor(buffered=True)

#Agg_insu_df
mycursor.execute("select * from aggregated_insurance" )
table1=mycursor.fetchall()
Aggregated_insurance=pd.DataFrame(table1,columns=("States", "Year", "Quarter", "Transaction_name",
                                                  "Transaction_Amount", "Transaction_Count"))



#Agg_trans_df
mycursor.execute("select * from aggregated_transaction" )
table2=mycursor.fetchall()
Aggregated_transaction=pd.DataFrame(table2,columns=("States", "Year", "Quarter", "Transaction_type", 
                                                  "Transaction_Count", "Transaction_Amount"))

#Agg_user_df
mycursor.execute("select * from aggregated_user" )
table3=mycursor.fetchall()
Aggregated_user=pd.DataFrame(table3,columns=("States", "Year", "Quarter", "Brand", "Count", "Percentage"))

#Map_insu_df
mycursor.execute("select * from map_insurance" )
table4=mycursor.fetchall()
Map_insurance=pd.DataFrame(table4,columns=("States", "Year", "Quarter", "District", "Transaction_Amount", 
                                             "Transaction_Count"))


#Map_trans_df
mycursor.execute("select * from map_transaction" )
table5=mycursor.fetchall()
Map_transaction=pd.DataFrame(table5,columns=("States", "Year", "Quarter", "District", "Transaction_Amount", 
                                             "Transaction_Count"))


#Map_user_df
mycursor.execute("select * from map_user" )
table6=mycursor.fetchall()
Map_user=pd.DataFrame(table6,columns=("States", "Year", "Quarter", "District", "Registered_user", "App_opens"))


#top_insu_district_df
mycursor.execute("select * from top_insu_district" )
table7=mycursor.fetchall()
Top_insu_district=pd.DataFrame(table7,columns=("States", "Year", "Quarter", "Districts", "Transaction_Amount", 
                                               "Transaction_Count"))

#top_insu_pincode_df
mycursor.execute("select * from top_insu_pincode" )
table8=mycursor.fetchall()
Top_insu_pincode=pd.DataFrame(table8,columns=("States", "Year", "Quarter", "Pincode", "Transaction_Amount", 
                                               "Transaction_Count"))



#top_trans_district_df
mycursor.execute("select * from top_transaction_districts" )
table9=mycursor.fetchall()
Top_transaction_district=pd.DataFrame(table9,columns=("States", "Year", "Quarter","Districts", "Transaction_Amount", 
                                                      "Transaction_Count"))

#top_trans_pincode_df
mycursor.execute("select * from top_transaction_pincode" )
table10=mycursor.fetchall()
Top_transaction_pincode=pd.DataFrame(table10,columns=("States", "Year", "Quarter", "Pincode", "Transaction_Amount", 
                                                      "Transaction_Count")) 

#top_user_district_df
mycursor.execute("select * from top_user_district" )
table11=mycursor.fetchall()
Top_user_district=pd.DataFrame(table11,columns=("States", "Year", "Quarter","District", "Registered_users"))

#top_user_pincode_df
mycursor.execute("select * from top_user_pincode" )
table12=mycursor.fetchall()
Top_user_pincode=pd.DataFrame(table12,columns=("States", "Year", "Quarter","Pincode", "Registered_users"))


st.set_page_config(page_title="Phonepe",layout="wide")
with st.sidebar:
    st.sidebar.header(":violet[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]")   
    select=option_menu("Main menu",["HOME","DATA EXPLORATION","INSIGHTS","ABOUT"])
    default_option="HOME"
if select=="HOME":
    col1,col2 = st.columns([3,2.5],gap="medium")
    with col1:
        st.image(Image.open("C:\\Users\\NANDHINI\\Downloads\\Phonepelogo.png"),width = 300)
       
        st.markdown('''PhonePe  is an Indian digital payments and financial technology company headquartered in 
                    Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, 
                    Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI),
                    went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.
                    The Indian digital payments story has truly captured the world’s imagination.
                     From the largest towns to the remotest villages, there is a payments revolution being 
                    driven by the penetration of mobile phones, mobile internet and state-of-art payments infrastructure
                    built as Public Goods championed by the central bank and the government.''')
        
        st.image(Image.open("C:\\Users\\NANDHINI\\Downloads\\phonepe.jpg"),width = 400) 
        if st.button("Go to Link"):
            st.markdown("[Visit the Link](https://github.com/PhonePe/pulse/blob/master/README.md)")
    with col2:
       st.video("C:\\Users\\NANDHINI\\Downloads\\pulse-video.mp4")
       st.video("C:\\Users\\NANDHINI\\Downloads\\upi.mp4")
      

elif select=="DATA EXPLORATION":
    tab1, tab2, tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        method=st.radio("select the method",["Aggregated Insurance","Aggregated Transaction","Aggregated User"])
        Year = st.sidebar.slider("Select the Year", min_value=2020, max_value=2023)
        Quarter = st.sidebar.slider("Select the quarter", min_value=1, max_value=4) 
        if method=="Aggregated Insurance":
            amount=Aggregated_insurance[(Aggregated_insurance["Year"]==Year) & (Aggregated_insurance["Quarter"]==Quarter)]
            #amount.reset_index(drop=True, inplace=True)
            transaction=amount.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
            transaction.reset_index(inplace=True)
            col1,col2=st.columns([3,2.5],gap="medium")
            with col1:
                fig_amount=px.bar(transaction,x="States",y="Transaction_Amount",title=f"{Year} TRANSACTION AMOUNT Quarter {Quarter} ",
                          height=650,width=600)
                st.plotly_chart(fig_amount)
            with col2:
                fig_count=px.bar(transaction,x="States",y="Transaction_Count",title=f"{Year} TRANSACTION COUNT Quarter {Quarter} ",
                         height=650,width=600)
                st.plotly_chart(fig_count)
            
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.choropleth(Aggregated_insurance,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',locations='States',color='Transaction_Amount',color_continuous_scale='twilight',
                    hover_name="States",title=f"{Year} TRANSACTION AMOUNT Quarter {Quarter} ",
                    height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            with col2:
                fig = px.choropleth(Aggregated_insurance,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',locations='States',color='Transaction_Count',color_continuous_scale='twilight',
                    hover_name="States",title=f"{Year} Transaction_Count Quarter {Quarter} ",
                    height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
        if method=="Aggregated Transaction":
            amount=Aggregated_transaction[(Aggregated_transaction["Year"]==Year) & (Aggregated_transaction["Quarter"]==Quarter)]
            #amount.reset_index(drop= True, inplace=True)
            transaction=amount.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
            transaction.reset_index(inplace=True)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.bar(transaction,x="States",y="Transaction_Amount",title=f"{Year} TRANSACTION AMOUNT Quarter {Quarter} ",
                            height=650,width=600)
                st.plotly_chart(fig_amount)
            with col2:
                fig_count=px.bar(transaction,x="States",y="Transaction_Count",title=f"{Year} TRANSACTION COUNT Quarter {Quarter} ",
                            height=650,width=600)
                st.plotly_chart(fig_count)
            states=st.selectbox("select the state",Aggregated_transaction["States"].unique())
            amount=Aggregated_transaction[(Aggregated_transaction["Year"]==Year) & (Aggregated_transaction["Quarter"]==Quarter) & (Aggregated_transaction["States"]==states)]
            transaction=amount.groupby("Transaction_type")[["Transaction_Amount","Transaction_Count"]].sum()
            transaction.reset_index(inplace=True)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.pie(transaction,names="Transaction_type",values="Transaction_Amount",title=f"{Year} {states.upper()} TRANSACTION AMOUNT Quarter {Quarter} ",
                            width=600)
                st.plotly_chart(fig_amount)
            with col2:
                fig_count=px.pie(transaction,names="Transaction_type",values="Transaction_Count",title=f"{Year} {states.upper()} TRANSACTION COUNT Quarter {Quarter} ",
                            width=600)
                st.plotly_chart(fig_count)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.choropleth(Aggregated_transaction,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',locations='States',color='Transaction_Amount',color_continuous_scale='twilight',
                    hover_name="States",title=f"{Year} TRANSACTION AMOUNT Quarter {Quarter} ",
                    height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            with col2:
                fig = px.choropleth(Aggregated_transaction,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',locations='States',color='Transaction_Count',color_continuous_scale='twilight',
                    hover_name="States",title=f"{Year} Transaction_Count Quarter {Quarter} ",
                    height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            
        if method=="Aggregated User":
            states=st.selectbox("select the state",Aggregated_user["States"].unique())
            amount=Aggregated_user[(Aggregated_user["Year"]==Year) & (Aggregated_user["Quarter"]==Quarter) & (Aggregated_user["States"]==states)]
            transaction=amount.groupby("Brand")[["Percentage","Count"]].sum()
            transaction.reset_index(inplace=True)            
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.bar(transaction,x="Brand",y="Percentage",title=f"{Year} Percentage Quarter {Quarter} ",
                            height=650,width=600)
                st.plotly_chart(fig_amount)
            with col2:
                fig_count=px.bar(transaction,x="Brand",y="Count",title=f"{Year} Count Quarter {Quarter} ",
                            height=650,width=600)
                st.plotly_chart(fig_count)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.choropleth(Aggregated_user,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',locations='States',color='Percentage',color_continuous_scale='twilight',
                    hover_name="States",title=f"{Year} Percentage Quarter {Quarter} ",
                    height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            with col2:
                
                fig = px.choropleth(Aggregated_user,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',locations='States',color='Count',color_continuous_scale='twilight',
                    hover_name="States",title=f"{Year} Count Quarter {Quarter} ",
                    height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)

    with tab2:
        method=st.radio("select the method",["Map Insurance","Map Transaction","Map User"])
        if method=="Map Insurance":

            amount=Map_insurance[(Map_insurance["Year"]==Year) & (Map_insurance["Quarter"]==Quarter)]
            transaction=amount.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
            transaction.reset_index(inplace=True)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.bar(transaction,x="States",y="Transaction_Amount",title=f"{Year} TRANSACTION AMOUNT Quarter {Quarter} ",
                            )
                st.plotly_chart(fig_amount)
            with col2:
                fig_count=px.bar(transaction,x="States",y="Transaction_Count",title=f"{Year} TRANSACTION COUNT Quarter {Quarter} ",
                            )
                st.plotly_chart(fig_count)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.choropleth(Map_insurance,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Transaction_Amount',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Transaction_Amount Quarter {Quarter} ",
                        height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            with col2:
                fig = px.choropleth(Map_insurance,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Transaction_Count',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Transaction_Count Quarter {Quarter} ",
                        height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            states=st.selectbox("select the state for map_insu",Map_insurance["States"].unique())
            amount=Map_insurance[(Map_insurance["Year"]==Year) & (Map_insurance["Quarter"]==Quarter) & (Map_insurance["States"]==states)]
            transaction=amount.groupby("District")[["Transaction_Amount","Transaction_Count"]].sum()
            transaction.reset_index(inplace=True)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.bar(transaction,x="District",y="Transaction_Amount",title=f"{Year} {states.upper()} TRANSACTION AMOUNT Quarter {Quarter} ",
                            height=650,width=600)
                st.plotly_chart(fig_amount)
            with col2:
                fig_count=px.bar(transaction,x="District",y="Transaction_Count",title=f"{Year} {states.upper()} TRANSACTION COUNT Quarter {Quarter} ",
                            height=650,width=600)
                st.plotly_chart(fig_count)
            
        if method=="Map Transaction":
            amount=Map_transaction[(Map_transaction["Year"]==Year) & (Map_transaction["Quarter"]==Quarter)]
            transaction=amount.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
            transaction.reset_index(inplace=True)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.bar(transaction,x="States",y="Transaction_Amount",title=f"{Year} TRANSACTION AMOUNT Quarter {Quarter} ",
                            )
                st.plotly_chart(fig_amount)
            with col2:
                fig_count=px.bar(transaction,x="States",y="Transaction_Count",title=f"{Year} TRANSACTION COUNT Quarter {Quarter} ",
                            )
                st.plotly_chart(fig_count)
            
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.choropleth(Map_transaction,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Transaction_Amount',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Transaction_Amount Quarter {Quarter} ",
                        height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            with col2:
                fig = px.choropleth(Map_transaction,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Transaction_Count',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Transaction_Count Quarter {Quarter} ",
                        height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            states=st.selectbox("select the state for map_insu",Map_transaction["States"].unique())
            amount=Map_transaction[(Map_transaction["Year"]==Year) & (Map_transaction["Quarter"]==Quarter) & (Map_transaction["States"]==states)]
            transaction=amount.groupby("District")[["Transaction_Amount","Transaction_Count"]].sum()
            transaction.reset_index(inplace=True)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.bar(transaction,x="District",y="Transaction_Amount",title=f"{Year} {states.upper()} TRANSACTION AMOUNT Quarter {Quarter} ",
                            height=650,width=600)
                st.plotly_chart(fig_amount)
            with col2:
                fig_count=px.bar(transaction,x="District",y="Transaction_Count",title=f"{Year} {states.upper()} TRANSACTION COUNT Quarter {Quarter} ",
                            height=650,width=600)
                st.plotly_chart(fig_count)

        if method=="Map User":
            amount=Map_user[(Map_user["Year"]==Year) & (Map_user["Quarter"]==Quarter)]
            transaction=amount.groupby("States")[["Registered_user","App_opens"]].sum()
            transaction.reset_index(inplace=True)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.line(transaction,x="States",y=["Registered_user","App_opens"],title=f"{Year} REGISTERED USER & APP OPENS Quarter {Quarter} ",
                            markers=True,width=1000,height=800)
                st.plotly_chart(fig_amount)
            
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.choropleth(Map_user,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Registered_user',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Registered_user Quarter {Quarter} ",
                        height=500,width=500)               
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            with col2:
                fig = px.choropleth(Map_user,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='App_opens',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} App_opens Quarter {Quarter} ",
                        height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            states=st.selectbox("select the state for map_user",Map_user["States"].unique())
            amount=Map_user[(Map_user["Year"]==Year) & (Map_user["Quarter"]==Quarter) & (Map_user["States"]==states)]
            transaction=amount.groupby("District")[["Registered_user","App_opens"]].sum()
            transaction.reset_index(inplace=True)
            
            fig_amount=px.line(transaction,x="District",y=["Registered_user","App_opens"],title=f"{Year} REGISTERED USER & APP OPENS Quarter {Quarter} ",
                            markers=True,width=1000,height=800)
            st.plotly_chart(fig_amount)
            

    with tab3:
        method=st.radio("select the method",["Top Insurance","Top Transaction","Top User"])

        if method=="Top Insurance":
            amount=Top_insu_pincode[(Top_insu_pincode["Year"]==Year) & (Top_insu_pincode["Quarter"]==Quarter)]
            transaction=amount.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
            transaction.reset_index(inplace=True)

            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.bar(transaction,x="States",y="Transaction_Amount",title=f"{Year} Transaction_Amount Quarter {Quarter} ",
                            )
                st.plotly_chart(fig_amount)

            with col2:
            
                fig_count=px.bar(transaction,x="States",y="Transaction_Count",title=f"{Year} Transaction_Count Quarter {Quarter} ",
                            )
                st.plotly_chart(fig_count)

            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.choropleth(Top_insu_pincode,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Transaction_Amount',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Transaction_Amount Quarter {Quarter} ",
                        height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            with col2:
                fig = px.choropleth(Top_insu_pincode,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Transaction_Count',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Transaction_Count Quarter {Quarter} ",
                        height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            states=st.selectbox("select the state for top_insu_pincode",Top_insu_pincode["States"].unique())
            amount=Top_insu_pincode[(Top_insu_pincode["Year"]==Year) & (Top_insu_pincode["States"]==states)]
            amount.reset_index(drop=True, inplace=True)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.bar(amount,x="Quarter",y="Transaction_Amount",hover_data='Pincode',title="Transaction Amount",
                    height=800)
                st.plotly_chart(fig)
            with col2:
                fig = px.bar(amount,x="Quarter",y="Transaction_Count",hover_data='Pincode',title="Transaction Count",
                    height=800)
                st.plotly_chart(fig)

            

        if method=="Top Transaction":
            amount=Top_transaction_pincode[(Top_transaction_pincode["Year"]==Year) & (Top_transaction_pincode["Quarter"]==Quarter)]
            transaction=amount.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
            transaction.reset_index(inplace=True)

            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig_amount=px.bar(transaction,x="States",y="Transaction_Amount",title=f"{Year} Transaction_Amount Quarter {Quarter} ",
                            )
                st.plotly_chart(fig_amount)

            with col2:
            
                fig_count=px.bar(transaction,x="States",y="Transaction_Count",title=f"{Year} Transaction_Count Quarter {Quarter} ",
                            )
                st.plotly_chart(fig_count)
            
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.choropleth(Top_transaction_pincode,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Transaction_Amount',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Transaction_Amount Quarter {Quarter} ",
                        height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
            with col2:
                fig = px.choropleth(Top_transaction_pincode,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Transaction_Count',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Transaction_Count Quarter {Quarter} ",
                        height=500,width=500)                
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)

            states=st.selectbox("select the state for top_insu_pincode",Top_transaction_pincode["States"].unique())
            amount=Top_transaction_pincode[(Top_transaction_pincode["Year"]==Year) & (Top_transaction_pincode["States"]==states)]
            amount.reset_index(drop=True, inplace=True)
            col1,col2=st.columns([2.5,2.5],gap="medium")
            with col1:
                fig = px.bar(amount,x="Quarter",y="Transaction_Amount",hover_data='Pincode',title="Transaction Amount",
                    height=800)
                st.plotly_chart(fig)
            with col2:
                fig = px.bar(amount,x="Quarter",y="Transaction_Count",hover_data='Pincode',title="Transaction Count",
                    height=800)
                st.plotly_chart(fig)

            

        if method=="Top User":
            amount=Top_user_pincode[(Top_user_pincode["Year"]==Year) & (Top_user_pincode["Quarter"]==Quarter)]
            amount.reset_index(drop=True, inplace=True)

            
            fig_amount=px.bar(amount,x="States",y="Registered_users",hover_data='Pincode',title=f"{Year} Registered_users Quarter {Quarter} ",
                            width=1000)
            st.plotly_chart(fig_amount)
            
            fig = px.choropleth(Top_user_pincode,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',locations='States',color='Registered_users',color_continuous_scale='twilight',
                        hover_name="States",title=f"{Year} Registered_users Quarter {Quarter} ",
                        height=1000,width=1000)                
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
           


if select=="INSIGHTS":
    question=st.selectbox("select your question",("1. What are the Top 10 states based on amount of transaction?",
                                                "2. What are the Top 10 states based on transaction of count?",
                                                "3. What are the types of Transaction and their Transaction amount & count?",
                                                "4. What are the types of Brand and their count & Percentage?",
                                                "5. Which district have the highest number of Registered user and their corresponding states?",
                                                "6. What are the Top 10 pincodes based on amount of transaction and their respective states?",
                                                "7. What are the Top 10 pincodes based on transaction count and their respective states?",
                                                "8. What are the Top 10 pincodes based on registered user and their respective states?",
                                                "9. Which district have the highest number of app opens and their respective states?",
                                                ))

    if question=="1. What are the Top 10 states based on amount of transaction?":
            method=st.radio("select the method",["Aggregated Transaction","Map Transaction","Top Transaction"])
            if method=="Aggregated Transaction":        
                mycursor.execute("SELECT States as STATES,Transaction_Amount as TRANSACTION_AMOUNT from aggregated_transaction GROUP BY States ORDER BY TRANSACTION_AMOUNT DESC LIMIT 10  ")
                t1=mycursor.fetchall()
                df1=pd.DataFrame(t1,columns=["STATES","TRANSACTION AMOUNT"])
                
                col1,col2=st.columns([2.5,2.5],gap="medium")
                with col1:
                    st.write(df1)
                with col2:
                    fig_count=px.pie(df1,names="STATES",values="TRANSACTION AMOUNT",title="TOP 10 TRANSACTION AMOUNT ",
                            width=600)
                    st.plotly_chart(fig_count)
            if method=="Map Transaction":        
                mycursor.execute("SELECT States as STATES,Transaction_Amount as TRANSACTION_AMOUNT from map_transaction GROUP BY States ORDER BY TRANSACTION_AMOUNT DESC LIMIT 10  ")
                t2=mycursor.fetchall()
                df2=pd.DataFrame(t2,columns=["STATES","TRANSACTION AMOUNT"])
                
                col1,col2=st.columns([2.5,2.5],gap="medium")
                with col1:
                    st.write(df2)
                with col2:
                    fig_count=px.pie(df2,names="STATES",values="TRANSACTION AMOUNT",title="TOP 10 TRANSACTION AMOUNT ",
                            width=600)
                    st.plotly_chart(fig_count)
            if method=="Top Transaction":        
                mycursor.execute("SELECT States as STATES,Transaction_Amount as TRANSACTION_AMOUNT from top_transaction_pincode GROUP BY States ORDER BY TRANSACTION_AMOUNT DESC LIMIT 10  ")
                t3=mycursor.fetchall()
                df3=pd.DataFrame(t3,columns=["STATES","TRANSACTION AMOUNT"])
                
                col1,col2=st.columns([2.5,2.5],gap="medium")
                with col1:
                    st.write(df3)
                with col2:
                    fig_count=px.pie(df3,names="STATES",values="TRANSACTION AMOUNT",title="TOP 10 TRANSACTION AMOUNT ",
                            width=600)
                    st.plotly_chart(fig_count)

    if question=="2. What are the Top 10 states based on transaction of count?":
            method=st.radio("select the method",["Aggregated Transaction","Map Transaction","Top Transaction"])
            if method=="Aggregated Transaction":        
                mycursor.execute("SELECT States as STATES,Transaction_count as TRANSACTION_COUNT from aggregated_transaction GROUP BY States ORDER BY TRANSACTION_COUNT DESC LIMIT 10  ")
                t1=mycursor.fetchall()
                df1=pd.DataFrame(t1,columns=["STATES","TRANSACTION COUNT"])
                
                col1,col2=st.columns([2.5,2.5],gap="medium")
                with col1:
                    st.write(df1)
                with col2:
                    fig_count=px.pie(df1,names="STATES",values="TRANSACTION COUNT",title="TOP 10 TRANSACTION COUNT",
                            width=600)
                    st.plotly_chart(fig_count)
            if method=="Map Transaction":        
                mycursor.execute("SELECT States as STATES,Transaction_count as TRANSACTION_COUNT from map_transaction GROUP BY States ORDER BY TRANSACTION_COUNT DESC LIMIT 10  ")
                t2=mycursor.fetchall()
                df2=pd.DataFrame(t2,columns=["STATES","TRANSACTION COUNT"])
                
                col1,col2=st.columns([2.5,2.5],gap="medium")
                with col1:
                    st.write(df2)
                with col2:
                    fig_count=px.pie(df2,names="STATES",values="TRANSACTION COUNT",title="TOP 10 TRANSACTION COUNT",
                            width=600)
                    st.plotly_chart(fig_count)
            if method=="Top Transaction":        
                mycursor.execute("SELECT States as STATES,Transaction_count as TRANSACTION_COUNT from top_transaction_pincode GROUP BY States ORDER BY TRANSACTION_COUNT DESC LIMIT 10  ")
                t3=mycursor.fetchall()
                df3=pd.DataFrame(t3,columns=["STATES","TRANSACTION COUNT"])
                
                col1,col2=st.columns([2.5,2.5],gap="medium")
                with col1:
                    st.write(df3)
                with col2:
                    fig_count=px.pie(df3,names="STATES",values="TRANSACTION COUNT",title="TOP 10 TRANSACTION COUNT",
                            width=600)
                    st.plotly_chart(fig_count)

    if question== "3. What are the types of Transaction and their Transaction amount & count?":
        mycursor.execute("SELECT Transaction_type as Transaction_type,Transaction_Count as Transaction_count,Transaction_Amount as Transaction_amount from aggregated_transaction group by Transaction_type" )
        t3=mycursor.fetchall()
        df3=pd.DataFrame(t3,columns=["Transaction Type","Transaction Count","Transaction Amount"])
        col1,col2=st.columns([2.5,2.5],gap="medium")
        with col1:
            st.write(df3)
        with col2:
            fig = px.line(df3, x="Transaction Type", y=["Transaction Amount","Transaction Count"],title="Transaction types",
                          markers=True)
            st.plotly_chart(fig)

    if question== "4. What are the types of Brand and their count & Percentage?":
        mycursor.execute("SELECT Brand as Brand, Count as Count, Percentage as Percentage from aggregated_user group by Brand")
        t4=mycursor.fetchall()
        df4=pd.DataFrame(t4,columns=["Brand","Count","Percentage"])
        col1,col2=st.columns([2.5,2.5],gap="medium")
        with col1:
            st.write(df4)
        with col2:
            fig = px.line(df4, x="Brand", y=["Count","Percentage"],title="Brands",
                          markers=True)
            st.plotly_chart(fig)

    if question== "5. Which district have the highest number of Registered user and their corresponding states?":
        mycursor.execute("SELECT District as District, States as States, Registered_user as Reg_user from map_user group by District order by Reg_user DESC LIMIT 10")
        t5=mycursor.fetchall()
        df5=pd.DataFrame(t5,columns=["Districts","States","Reg_user"])
        col1,col2=st.columns([2.5,2.5],gap="medium")
        with col1:
            st.write(df5)
        with col2:
            fig = px.pie(df5, names="Districts",values="Reg_user",title="Registered users",
                          )
            st.plotly_chart(fig) 

    if question== "6. What are the Top 10 pincodes based on amount of transaction and their respective states?":
        mycursor.execute("SELECT States as States, Pincode as pincode,Transaction_Amount as Transaction_amount from top_transaction_pincode group by Pincode order by Transaction_amount DESC LIMIT 10")
        t6=mycursor.fetchall()
        df6=pd.DataFrame(t6,columns=["States","pincode","Transaction Amount"])
        col1,col2=st.columns([2.5,2.5],gap="medium")
        with col1:
            st.write(df6)
        with col2:
            fig = px.bar(df6, x="States",y="Transaction Amount",hover_data='pincode',title="Transaction amount")
            st.plotly_chart(fig)

    if question== "7. What are the Top 10 pincodes based on transaction count and their respective states?":
        mycursor.execute("SELECT States as States, Pincode as pincode,Transaction_Count as Transaction_Count from top_transaction_pincode group by Pincode order by Transaction_Count DESC LIMIT 10")
        t7=mycursor.fetchall()
        df7=pd.DataFrame(t7,columns=["States","pincode","Transaction Count"])
        col1,col2=st.columns([2.5,2.5],gap="medium")
        with col1:
            st.write(df7)
        with col2:
            fig = px.bar(df7, x="States",y="Transaction Count",hover_data='pincode',title="Transaction Count")
            st.plotly_chart(fig)  

    if question== "8. What are the Top 10 pincodes based on registered user and their respective states?":
        mycursor.execute("SELECT States as States, Pincode as pincode,Registered_users as Registered_users from top_user_pincode group by Pincode order by Registered_users DESC LIMIT 10")
        t8=mycursor.fetchall()
        df8=pd.DataFrame(t8,columns=["States","pincode","Reg Users"])
        col1,col2=st.columns([2.5,2.5],gap="medium")
        with col1:
            st.write(df8)
        with col2:
            fig = px.bar(df8, x="States",y="Reg Users",hover_data='pincode',title="Reg users")
            st.plotly_chart(fig)  

    if question== "9. Which district have the highest number of app opens and their respective states?":
        mycursor.execute('''SELECT District as District,States as States, SUM(App_opens) as Total_App_opens FROM map_user GROUP BY District order by App_opens 
                 DESC LIMIT 10''')
        t9=mycursor.fetchall()
        df9=pd.DataFrame(t9,columns=["District","States","App opens"])
        col1,col2=st.columns([2.5,2.5],gap="medium")
        with col1:
            st.write(df9)
        with col2:
            fig = px.bar(df9, x="District",y="App opens",hover_data="States",title="App opens")
                          
            st.plotly_chart(fig)
                 
                

if select=="ABOUT":
    
    st.header(":violet[ABOUT PHONEPE PULSE]")
    st.write('''BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, 
                 announced the launch of PhonePe Pulse, India's first interactive website with data, 
                 insights and trends on digital payments in the country. The PhonePe Pulse website showcases 
                 more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 
                 45% market share, PhonePe's data is representative of the country's digital payment habits.''')
        
    st.write('''The insights on the website and in the report have been drawn from two key sources - the 
                 entirety of PhonePe's transaction data combined with merchant and customer interviews. The report
                  is available as a free download on the PhonePe Pulse website and GitHub.''')
    st.header(":violet[ABOUT PHONEPE]")
    st.write("PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
    st.write("My Project GitHub link ⬇️") 
    st.write("https://github.com/sgopika1999/Phonepe-Pulse-Data-Visualization-and-Exploration")
    st.write("MAIL: gopika.sivabalan@gmail.com")
    
   

            

    





    
       