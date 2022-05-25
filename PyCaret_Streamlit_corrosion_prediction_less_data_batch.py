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


# In[7]:


def run():
    
    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Individual", "Batch"))

    st.sidebar.info('This is a web app to predict corrosion rates of oil wells based on         several features that you can see in the sidebar. Please adjust the         value of each feature. After that, click on the Predict button at the bottom to         see the prediction of the model.')
    
    st.sidebar.success('https://www.pungoapp.com')
    
    st.title("Corrosion Prediction Web App")

    if add_selectbox == 'Individual':

        BPPD = st.slider(label = 'BPPD', min_value = 0,
                          max_value = 2000 ,
                          value = 500,step=1)
        
        BAPD = st.slider(label = 'BAPD', min_value = 0,
                          max_value = 5000 ,
                          value = 1000,step=1)
                          
        Caudal_gas = st.slider(label = 'Caudal_gas_MSCFD', min_value = 0,
                          max_value = 1000 ,
                          value = 100,step=1)
   
        Presion_cabeza = st.slider(label = 'Presion_cabeza_psi', min_value = 0,
                          max_value = 500,
                          value = 150,step=1)

        Temperatura_cabeza = st.slider(label = 'Temperatura_cabeza_F', min_value = 0,
                          max_value = 300 ,
                          value = 150,step=1)

        Salinidad = st.slider(label = 'Salinidad_ppm', min_value = 0,
                          max_value = 100000 ,
                          value = 50000,step=100)

        CO2_gas = st.slider(label = 'CO2_gas %', min_value = 0,
                          max_value = 100 ,
                          value = 20,step=1)
                          
        Bicarbonatos = st.slider(label = 'bicarbonatos_ppm', min_value = 0,
                          max_value = 3000,
                          value = 500,step=1)

        Dosis_IC = st.slider(label = 'dosis_IC_ppm', min_value = 0,
                          max_value = 300,
                          value = 100,step=1)

        Fe = st.slider(label = 'Fe_ppm', min_value = 0,
                          max_value = 200,
                          value = 50,step=1)
        
        output=""

        features = {'BPPD': BPPD, 'BAPD': BAPD,
            'Caudal_gas_MSCFD': Caudal_gas, 'Presion_cabeza_psi': Presion_cabeza,
            'Temperatura_cabeza_F': Temperatura_cabeza, 'Salinidad_ppm': Salinidad,
            'CO2_gas': CO2_gas, 'bicarbonatos_ppm': Bicarbonatos,
            'dosis_IC_ppm': Dosis_IC, 'Fe_ppm': Fe}
        
        features_df  = pd.DataFrame([features])
        
        st.table(features_df) 

        if st.button('Predict corrosion rate'):
            output = predict_corrosion(model, features_df)
                    
            output1=str('%f' % output) + ' mpy'
            
        st.success('Based on your input variables, the corrosion rate is {}'.format(output1))
        
        if output < 1:
            st.sucess("Corrosion risk: Low")
        if output>=1 and output<5:
            st.sucess("Corrosion risk: Moderate")
        if output>=5 and output<10:
            st.sucess("Corrosion risk: High")
        if output >= 10:
            st.sucess("Corrosion risk: Severe")
        
    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)


# In[8]:


if __name__ == '__main__':
    run()

