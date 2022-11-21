# importing core lib
import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
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


# Removing streamlit water mark
hide_streamlit_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#Loadind the dataset
@st.cache(allow_output_mutation=True)
def model():
	model=load_model('./Models/models-v3-11-18-2022')
	return model

def run(): 
    tab1, tab2, tab3 = st.tabs(["Home", "Resources ", "Changelog"])
    with tab1:
        stc.html("""
                <div style="background-color:#31333F;padding:10px;border-radius:10px">
                <h1 style="color:white;text-align:center;">Cardiovascular Disease Prediction System</h1>
                </div>""")
        st.write("This application is meant to assist doctors in diagnosing, if a patient has cardiovascular Disease or not using few details about their health")
        st.write("Please Enter the below details to know the results")
         
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
                predictions_label = predictions_df['Label'][0]
                predictions_score = predictions_df['Score'][0]
                print(predictions_score)
                if predictions_label == 0:
                    st.success(f'No Cardiovascular disease detected, confidence Score {predictions_score}')
                    st.write('✨Keep it up!✨')
                else:
                    st.warning(f'Cardiovascular disease detected,confidence Score {predictions_score}')
                    st.write('Please consult doctor for further information.')
    
        
    with tab2:
        col1, col2= st.columns(2)
        with col1:
            st.video("https://www.youtube.com/watch?v=lTCF8y7e1Bw")
            st.subheader("Cardiovascular Disease Overview")

        with col2:
            st.video("https://www.youtube.com/watch?v=Sc3IN99sRrI")
            st.subheader("Cardiovascular System Anatomy")
        col3,col4= st.columns(2)
        with col3:
            st.video("https://www.youtube.com/watch?v=frUxLyipCJY")
            st.subheader("Common Symptoms of Cardiovascular Disease ")

        with col4:
            st.video("https://www.youtube.com/watch?v=vqaja_LD1Kk")
            st.subheader("Coronary Artery Disease, Causes, Signs and Symptoms, Diagnosis and Treatment")
             
    with tab3:
        st.subheader("Your Appliction and AI model is up to date, Admin would let you know when new model is out ")
        
             
if __name__ == '__main__':
    run()