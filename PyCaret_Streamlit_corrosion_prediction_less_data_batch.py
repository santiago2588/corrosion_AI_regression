#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pycaret.regression import load_model, predict_model

# In[2]:


import streamlit as st


# In[3]:


import pandas as pd
import numpy as np


# In[4]:


model = load_model('corrosion_regressor_less_data')


# In[5]:


def predict_corrosion(model, df):
    predictions_data = predict_model(estimator = model, data = df)
    predictions=predictions_data['Label'][0]
    return predictions

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# In[7]:


def run():
    
    st.image("C:/Users/saint/Code examples/Corrosion AI/logo_pungo.png")
    
    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict corrosion rate?",
    ("Individual", "Batch"))

    st.sidebar.info('This is a web app to predict corrosion rates of oil wells based on         several features that you can see in the main body. Please adjust the         value of each feature. After that, click on the Predict button at the bottom to         see the prediction of the model.')
    
    st.sidebar.success('https://www.pungoapp.com')
    
    st.title("Corrosion Prediction Web App")
    st.subheader("Please adjust the value of each feature")

    if add_selectbox == 'Individual':

        BPPD = st.slider(label = 'Barrels of oil per day (BOPD)', min_value = 0,
                          max_value = 2000 ,
                          value = 500,step=1)
        
        BAPD = st.slider(label = 'Barrels of water per day (BWPD)', min_value = 0,
                          max_value = 5000 ,
                          value = 1000,step=1)
                          
        Caudal_gas = st.slider(label = 'Gas flow rate (MSCFD)', min_value = 0,
                          max_value = 1000 ,
                          value = 100,step=1)
   
        Presion_cabeza = st.slider(label = 'Head pressure (psi)', min_value = 0,
                          max_value = 500,
                          value = 150,step=1)

        Temperatura_cabeza = st.slider(label = 'Head temperature (F)', min_value = 0,
                          max_value = 300 ,
                          value = 150,step=1)

        Salinidad = st.slider(label = 'Salinity (ppm)', min_value = 0,
                          max_value = 100000 ,
                          value = 50000,step=100)

        CO2_gas = st.slider(label = 'CO2 content in gas (%)', min_value = 0,
                          max_value = 100 ,
                          value = 20,step=1)
                          
        Bicarbonatos = st.slider(label = 'Bicarbonates (ppm)', min_value = 0,
                          max_value = 3000,
                          value = 500,step=1)

        Dosis_IC = st.slider(label = 'Corrosion inhibitor dosis (ppm)', min_value = 0,
                          max_value = 300,
                          value = 100,step=1)

        Fe = st.slider(label = 'Fe (ppm)', min_value = 0,
                          max_value = 200,
                          value = 50,step=1)
        
        output=""

        features = {'BPPD': BPPD, 'BAPD': BAPD,
            'Caudal_gas_MSCFD': Caudal_gas, 'Presion_cabeza_psi': Presion_cabeza,
            'Temperatura_cabeza_F': Temperatura_cabeza, 'Salinidad_ppm': Salinidad,
            'CO2_gas': CO2_gas, 'bicarbonatos_ppm': Bicarbonatos,
            'dosis_IC_ppm': Dosis_IC, 'Fe_ppm': Fe}
        
        features_df  = pd.DataFrame([features])
        
        #st.table(features_df) 

        if st.button('Predict corrosion rate'):
            output = predict_corrosion(model, features_df)
                  
            output1=str("%.2f" % output) + ' mpy'
            
            st.success('Based on your input variables, the corrosion rate is {}'.format(output1))
 
            if output < 1:
                st.success("Corrosion risk: Low")
            if output>=1 and output<5:
                st.success("Corrosion risk: Moderate")
            if output>=5 and output<10:
                st.success("Corrosion risk: High")
            if output >= 10:
                st.success("Corrosion risk: Severe")         
    
    
    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            predictions=predictions.rename({'Label':'Corrosion_rate_mpy'},axis='columns')
            st.write(predictions)
            
            def convert_df(df):
                return df.to_csv().encode('utf-8')

            csv = convert_df(predictions)

            st.download_button("📥Press to Download",csv,"file.csv","text/csv",key='download-csv')

# In[8]:

if __name__ == '__main__':
    run()

