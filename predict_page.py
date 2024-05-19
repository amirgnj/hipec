import pickle
import numpy as np
import pandas as pd
import streamlit as st


def load_model():
    with open('saved_x.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

model = data["model"]
sample = data["sample"]
new_attrs = ['grow_policy', 'max_bin', 'eval_metric', 'callbacks', 'early_stopping_rounds', 'max_cat_to_onehot', 'max_leaves', 'sampling_method']

['Age', 'BMIkgm2', 'AlbumingdL', 'CreatininemgdL', 'PCI', 'WBCCount',
       'Plateletcount', 'CCI', 'ASAClass_2', 'ECOGPerformanceStatus_00',
       'ECOGPerformanceStatus_10', 'histology_2_Appendiceal',
       'histology_2_Other', 'Symptomatic_Yes', 'FormalLiverResection_Yes',
       'DistalPancreatectomy_Yes', 'smallbowelresection_Yes',
       'PartialColectomy_Yes', 'proctectomy_Yes', 'subtotal_gastrectomy_Yes']

for attr in new_attrs:
    setattr(model, attr, None)
def show_predict_page():
    st.title("Severe Complications Following CRS-HIPEC")

    #st.info("###### 📚 This risk calculator was developed and validated using data from a cohort of 1,954 adult patients who underwent CRS-HIPEC between 2001 and 2020. (AUC: 0.71)")
    st.info("###### 💡 Tip: The variables have set ranges determined by our dataset. Should there be a need to enter a value beyond these ranges, please use the maximum or minimum value available.")

    st.write("""### Please  provide the following information:""")
    
    Age = st.slider("Age", 18, 90, 55)
    BMIkgm2 = st.slider("BMI", 14, 40, 25)

    CCI = st.slider("Charlson comorbidity index (CCI)", 0, 24, 0)
    PCI = st.slider("Peritoneal cancer index (PCI)", 0, 39, 10, 1)

    cols2 = st.columns(2)
    WBCCount = cols2[0].number_input("WBC", 1, 45, 7)
    Plateletcount = cols2[1].number_input("Platelet", 10, 1000, 250, 10)

    #cols = st.columns(1)
    
    #CreatininemgdL = cols[1].number_input("Creatinine", 0, 12, 1)
    


    cols5 = st.columns(2)
    AlbumingdL = cols5[0].number_input("Albumin", 0, 10, 3)
    Symptomatic_ = cols5[1].selectbox('Symptomatic', ("No", "Yes"))


    cols6 = st.columns(3)
    FormalLiverResection_ = cols6[0].selectbox('Liver Resection', ("No", "Yes"))
    DistalPancreatectomy_ = cols6[1].selectbox('Distal Pancreatectomy', ("No", "Yes"))
    smallbowelresection_ = cols6[2].selectbox('Small Bowel Resection', ("No", "Yes"))

    cols7 = st.columns(3)
    PartialColectomy_ = cols7[0].selectbox('Partial Colectomy', ("No", "Yes"))
    proctectomy_ = cols7[1].selectbox('Proctectomy', ("No", "Yes"))
    subtotal_gastrectomy_ = cols7[2].selectbox('Subtotal Gastrectomy', ("No", "Yes"))

 



    ok = st.button("Predict the probability of severe complications")

    if ok:
        sample["Age"] = Age
        sample["BMIkgm2"] = BMIkgm2

        
        sample["AlbumingdL"] = AlbumingdL
        sample["PCI"] = PCI
        sample["CCI"] = CCI
        sample["CreatininemgdL"] = 1
        sample["WBCCount"] = WBCCount
        sample["Plateletcount"] = Plateletcount
        


        if  Symptomatic_ == "Yes":
            sample["Symptomatic_Yes"] = 1
       
        if  FormalLiverResection_ == "Yes":
            sample["FormalLiverResection_Yes"] = 1
        if  DistalPancreatectomy_ == "Yes":
            sample["DistalPancreatectomy_Yes"] = 1
        if  smallbowelresection_ == "Yes":
            sample["smallbowelresection_Yes"] = 1
        if  PartialColectomy_ == "Yes":
            sample["PartialColectomy_Yes"] = 1
        if  proctectomy_ == "Yes":
            sample["proctectomy_Yes"] = 1
        if  subtotal_gastrectomy_ == "Yes":
            sample["subtotal_gastrectomy_Yes"] = 1




        chance = model.predict_proba(sample)
        #sample = data["sample"]
        st.subheader(f"Estimated probability of severe complications: {chance[0][1]*100:.2f}%")
    reset = st.button("Reset")
    if reset:
        sample.loc[:,:] = 0

    st.error("###### ❗ Disclaimer: Please note that this tool does not reflect causal relationships between input variables and the outcome, and therefore it should not be used in isolation to dictate surgical planning.")






        

