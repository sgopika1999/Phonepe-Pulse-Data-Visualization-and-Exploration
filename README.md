# PHONEPE-PULSE-DATA-VISUALIZATION AND EXPLORATION

# What is PhonePe Pulse?
The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With over 45% market share, PhonePe's data is representative of the country's digital payment habits. The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.

# Libraries/Modules needed for the project!
1.Plotly - (To plot and visualize the data)

2.Pandas - (To Create a DataFrame with the scraped data)

3.mysql.connector - (To store and retrieve the data)

4.Streamlit - (To Create Graphical user Interface)

5.json - (To load the json files)

6.git.repo.base - (To clone the GitHub repository)

# Key Technologies and Skills

Python

Git

Pandas

PostgreSQL

Streamlit

Plotly

# Workflow

![Alt Text](https://github.com/sgopika1999/flowchart/blob/main/phonepe%20overflow.png?raw=true)


## Step 1:
## Importing the Libraries:
Importing the libraries. As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. If the libraries are not installed already use the below piece of code to install.

    !pip install ["Name of the library"]

If the libraries are already installed then we have to import those into our script by mentioning the below codes.
    
    
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

# Step 2:

## Data transformation:

In this step the JSON files that are available in the folders are converted into the readeable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created. In order to perform this step I've used os, json and pandas packages.

path1 = "Path of the JSON files"
agg_trans_list = os.listdir(path1)

# Give any column names that you want
columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],'Transaction_amount': []}

Looping through each and every folder and opening the json files appending only the required key and values and creating the dataframe.


for states in agg_insu_list:
    cur_state=path0+states+"/"
    agg_year_list=os.listdir(cur_state)

    for year in agg_year_list:
        cur_year=cur_state+year+"/"
        agg_file_list=os.listdir(cur_year)

        for file in agg_file_list:
            cur_file=cur_year+file
            data=open(cur_file,"r")
            A=json.load(data)
          

            for i in A["data"]["transactionData"]:
                payment_name=i["name"]
                payment_amount=i["paymentInstruments"][0]["amount"]
                payment_count=i["paymentInstruments"][0]["count"]                   
                column0['Transaction_name'].append(payment_name)
                column0['Transaction_amount'].append(payment_amount)
                column0['Transaction_count'].append(payment_count)
                column0['States'].append(states)
                column0['Year'].append(year)
                column0['Quarter'].append(int(file.strip('.json')))
      Agg_insu=pd.DataFrame(column0)
      Agg_insu["States"]=Agg_insu["States"].replace("andaman-&-nicobar-islands","Andaman & Nicobar island")
      Agg_insu["States"]=Agg_insu["States"].replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra & Nagar Haveli and Daman & Diu")
      Agg_insu["States"]=Agg_insu["States"].str.replace("-"," ")
      Agg_insu["States"]=Agg_insu["States"].str.title()
      Agg_insu

# Step 4:
## Database insertion:

To insert the datadrame into SQL first I've created a new database and tables using "mysql-connector-python" library in Python to connect to a MySQL database and insert the transformed data using SQL commands.

# Creating the connection between python and mysql


    mydb = sql.connect(host="localhost",
               user="username",
               password="password",
               database= "phonepe_pulse"
              )
    mycursor = mydb.cursor(buffered=True)


# Creating tables



                    create_query1 = '''
                          CREATE TABLE IF NOT EXISTS phonepe.aggregated_insurance (
                              States varchar(100),
                              Year int,
                              Quarter int,
                              Transaction_name varchar(100),
                              Transaction_amount float,
                              Transaction_count int
                          )
                      '''
                    mycursor.execute(create_query1)
                    
                    insert_query1 = '''
                        INSERT INTO phonepe.aggregated_insurance 
                        (States, Year, Quarter, Transaction_name, Transaction_amount, Transaction_count)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    '''
                    mydb.commit()
                    
                    data=Agg_insu.values.tolist()
                    mycursor.executemany(insert_query1,data))


## Step 5:

## Dashboard creation:

To create colourful and insightful dashboard I've used Plotly libraries in Python to create an interactive and visually appealing dashboard. Plotly's built-in Pie, Bar, Geo map functions are used to display the data on a charts and map and Streamlit is used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.

## Step 6:

## Data retrieval:

Finally if needed Using the "mysql-connector-python" library to connect to the MySQL database and fetch the data into a Pandas dataframe.

## Contact:

📧 Email: gopika.sivabalan@gmail.com




