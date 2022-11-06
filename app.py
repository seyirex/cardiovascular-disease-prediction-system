import codecs
import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
from datetime import datetime
from PIL import Image
# from utils.helper import predict
from pycaret.classification import load_model,predict_model
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning)

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_option("deprecation.showfileUploaderEncoding", False)

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(page_title='cardiovascular-disease-prediction-system',
    layout='wide')
#---------------------------------#
# PATH = "../models/"
@st.cache(allow_output_mutation=True)
def model():
	model=load_model('models-v1-11-06-2022')
	return model


# image1 = Image.open('images/24315644_2202_w037_n003_186a_p1_186.jpg')
# filedoc = codecs.open("markdown/documentation.md", "r", "utf-8")

def run(): 
    tab1, tab2, tab3 = st.tabs(["Home", "Prediction Form", "About"])
    with tab1:
        stc.html("""
                <div style="background-color:#31333F;padding:10px;border-radius:10px">
                <h1 style="color:white;text-align:center;">Cardiovascular Disease Prediction System</h1>
                </div>""")
        
        with st.form(key='mlform'):
            col1, col2 = st.columns(2)
            with col1:
                age=st.number_input("Age",0,65)
                gender=st.number_input("gender (0: 'Male', 1: 'Female')",0,1)
                ap_hi=st.number_input("Systolic blood pressure ",100,180)
                ap_lo =st.number_input("Diastolic blood pressure",60,100) 
                cholesterol= st.selectbox("Cholesterol level",('normal','above normal','well above normal'))   
            with col2:
                glucose= st.selectbox("glucose level",('normal','above normal','well above normal')) 
                smoke=st.number_input("Smoker(0: 'No', 1: 'Yes')",0,1)
                alco=st.number_input("Alcohol intake(0: 'No', 1: 'Yes')",0,1) 
                active=st.number_input("Physical activity (0: 'No', 1: 'Yes')",0,1)
                bmi=st.number_input("BMI")     
                
            submit_message = st.form_submit_button(label='Prdict')

            input_dict = {
                'gender':gender,
                'age':age,
                'ap_hi':ap_hi,
                'ap_lo':ap_lo,
                'cholesterol':cholesterol,
                'glucose':glucose,
                'smoke':smoke,
                'alco':alco,
                'active':active,
                'bmi':bmi,
                        }
            df = pd.DataFrame([input_dict])
        
        if submit_message:
            with st.spinner('Prediction in Progress. Please Wait...'):
                predictions_df = predict_model(estimator=model(), data=df)
                predictions = predictions_df['Label'][0]
                if predictions == 0:
                    st.success('No Cardiovascular disease detected')
                    st.write('✨Keep it up!✨')
                    st.balloons()
                else:
                    st.warning('Cardiovascular diseas detected')
                    st.write('Please consult doctor for further information.')
    
        
    with tab2:
        pass
        
    with tab3:
        pass
             
if __name__ == '__main__':
    run()