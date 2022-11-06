from pycaret.classification import predict_model,load_model
import streamlit as st


@st.cache(allow_output_mutation=True)
def model():
	model=load_model('../Models/models-v1-11-06-2022')
	return model


def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    if predictions == 0:
        st.success('No Cardiovascular disease detected')
        st.write('✨Keep it up!✨')
        st.balloons()
    else:
        st.warning('Cardiovascular diseas detected')
        st.write('Please consult doctor for further information.')
    
    return predictions