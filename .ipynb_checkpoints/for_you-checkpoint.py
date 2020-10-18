# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 16:00:45 2020

@author: gopic
"""

import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import streamlit as st

raw = pd.read_csv('applicants.csv')
data= pd.read_csv('test.csv')

areas = ('None','other','education', 'insurance', 'energy','technology', 'healthcare', 'consulting', 'public_policy', 'aerospace','retail', 'sports', 'finance', 'transportation')
universities = ('None','University of Waterloo','University of Florida','Texas A&M University','Harvard')
year = ('None','Fr', 'Ma', 'PhD', 'Sr', 'O', 'So', 'Jr')
applications = pd.read_csv('intermediate_applications.csv')
sk = pd.read_csv('skills.csv')


aoi = st.sidebar.selectbox("SELCET BY AREA OF INTEREST",areas)
uni = st.sidebar.selectbox("SELCET BY UNIVERSITY",universities)
grade = st.sidebar.selectbox("SELCET BY YEAR",year)
ml = st.sidebar.slider('ML_Level', 0, 7, (1, 7),1)
data = st.sidebar.slider('Data_Level', 0, 7, (1, 7),1)
dev = st.sidebar.slider('Development_Level', 0, 7, (1, 7),1)
exp = st.sidebar.checkbox('PREVIOUS HACKATHON EXPERIENCE',['YES'])
DS_EXP =  st.sidebar.selectbox("SELCET BY DS Exp",(0,1,2,3,4))
#button = st.sidebar.button('Submit')
skills = st.sidebar.multiselect('Select Skills', ('Pandas','full_stack','cloud','NumPy','Excel','Pytorch','TensorFlow','SQL','Keras','Tableau','dev_ops','Scikit-learn','Python','MATLAB','R'))


raw.fillna('None',inplace=True)
if st.sidebar.button('submit'):
    sample = raw
    
    if aoi!='None':
        sample = sample[sample['relavent_industries'].str.contains(aoi)]
    if uni!='None':
        sample = sample[sample['school'].str.contains(uni)]
    if grade!='None':
        sample = sample[sample['classification'].str.contains(grade)]
    tsk = sk[(sk['ML']>=ml[0]) & (sk['ML']<=ml[1]) & (sk['Data']>=data[0]) & (sk['Data']<=data[1]) & (sk['Dev']>=dev[0]) & (sk['Dev']<=dev[1])]
    sample = sample[sample.index.isin(list(tsk.index))]
    if exp:
        #sample['num_hackathons_attended'] = sample['num_hackathons_attended'].apply(int)
        sample = sample[sample['num_hackathons_attended']!='0']
    if skills!=[]:
        li = []
        for x in skills:
            li+=list(sample[sample['technology_experience'].str.contains(x)].index)
        li = list(set(li))
        sample = sample[sample.index.isin(li)]
    sample = sample[sample['datascience_experience']==DS_EXP]
    
    sample = sample.drop(['other_school','minors', 'age_bin','first_generation','workshop_suggestions'],axis= 1)
    index = list(sample.index)
    i = 0
    cols = ["primary","secondary","success","danger","warning","info","dark"]
    c = len(cols)
    ci = 0
    st.markdown(f'''  <h2   style="text-align:center">Found {len(sample)} Participants</h2>''', unsafe_allow_html=True)
    while i+1 <len(index):
        
        p,q = index[i],index[i+1]
        st.markdown(f'''
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    
    <div class = "row">
            <div class = "col">
                <div class="card text-white bg-{cols[ci]} mb-3" style="width: 18rem">
                  <div class="card-body">
                    <h3 class="card-title">{sample.loc[p,'userid']}</h5>
                    <h4 class="card-text-right">{sample.loc[p,'school']}</p>
                    <h4 class="card-text">{sample.loc[p,'classification']}</p>
                    <h4 class="card-text">{sample.loc[p,'technology_experience']}</p>
                    <a href="#" class="btn btn-light">Request</a>
                  </div>
                 </div>
            </div>
            <div class = "col">
                 <div class="card text-white bg-{cols[(ci+1)%c]} mb-3" style="width: 18rem">
                   <div class="card-body">
                     <h3 class="card-title">{sample.loc[q,'userid']}</h5>
                     <h4 class="card-text-right">{sample.loc[q,'school']}</p>
                     <h4 class="card-text">{sample.loc[q,'classification']}</p>
                     <h4 class="card-text">{sample.loc[p,'technology_experience']}</p>
                     <a href="#" class="btn btn-light">Request</a>
                   </div>
                  </div>
             </div>
        </div>
    </div>
''', unsafe_allow_html=True)
        i+=2
        ci = (ci+2)%c
