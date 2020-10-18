import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import streamlit as st
import sklearn.model_selection as sk_model
from sklearn.linear_model import LogisticRegression as lr
import random, math

raw = pd.read_csv('applicants.csv')
workshops = pd.read_csv('workshops.csv')
query_features = pd.read_csv("query_features_2.csv")
user_index = None

data= pd.read_csv('test.csv')
my_expander = st.beta_expander("Resources")
link = '[Kaggle for Datasets and NoteBooks](http://kaggle.com)'
my_expander.markdown(link, unsafe_allow_html=True)
link = '[Google Colab for editing and model building](https://colab.research.google.com/)'
my_expander.markdown(link, unsafe_allow_html=True)
link = '[Streamlit to build WebApps](http://streamlit.io)'
my_expander.markdown(link, unsafe_allow_html=True)
clicked = my_expander.button('Get Resources')

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

def find_word_substrings(tag_list, query):
    count = 0
    for tag in tag_list:

        if tag.lower() in query.lower():
            count += 1
            
    return count

def create_feature_df(df, is_queries=False):
    for i in range(len(workshops.index)):
        col = []
        if is_queries:
            for j in range(len(queries.index)):
                col.append(find_word_substrings(tags_dict[workshops.iloc[i]["workshop_short"]], df.iloc[j]["query"]))
            df.insert(len(df.query)-1, (workshops.iloc[i]["workshop_short"]+"_count"), col)
            
        else:
            for j in range(len(df.index)):
                col.append(find_word_substrings(tags_dict[workshops.iloc[i]["workshop_short"]], df.iloc[j]["workshop_suggestions"]))
            df.insert(len(df.columns), (workshops.iloc[i]["workshop_short"]+"_count"), col)
            
    return df

def get_classifier():
    x = query_features[query_features.columns[2:23]]
    y = query_features[query_features.columns[-1]]
    x_train, x_test, y_train, y_test = sk_model.train_test_split(x, y, test_size=0.2)

    clf = lr(max_iter=1000).fit(x_train, y_train)
    
    return clf

def get_app_workshop_data(index):
    applicant = raw.iloc[index].to_frame().transpose()
    applicant = applicant[["workshop_suggestions"]]
    
    app_df = create_feature_df(applicant)
    
    clf = get_classifier()
    return clf.predict(applicant[applicant.columns[1:22]])

def get_workshops(track, experience, include_difficult):
    workshop_list = []
    for i in range(len(workshops["track"])):
        if not include_difficult:
            if workshops.iloc[i]["track"] == track and workshops.iloc[i]["difficulty"] <= experience:
                workshop_list.append(workshops.iloc[i]["workshop_name"])
        else:
            workshop_list.append(workshops.iloc[i]["workshop_name"])
            
    random.Random(4).shuffle(workshop_list)
            
    if len(workshop_list) < 3: return workshop_list
    else: return workshop_list[0:3]
    
def get_display_text(app):
    if type(raw.iloc[user_index]["workshop_suggestions"]) == float:
        return "Hm... It doesn't look like you've given us any info as to what kind of workshops you'd like to see. Feel free to search up a topic of interest in the search bar above and see what you get!"
    
    else:
        return ("Because you suggested that you were interested in workshops about  \"*%s*\"  and your experience with data science is \n  *%s*, here are a couple of workshops that you might find pretty awesome:" % (raw.at[user_index, "workshop_suggestions"], experience[applicant["datascience_experience"]]))

    
    
    
experience = ["beginner", "amateur", "advanced", "expert"]

tags_dict = {}
for i in range(len(workshops.index)):
    tags_dict[str(workshops.iloc[i]["workshop_short"])] = (workshops.iloc[i]["tags"]).split(", ")




try:
    user_index = int(st.text_input("Enter user index"))
except:
    print("Bad.")

if user_index != None:
    applicant = raw.iloc[user_index]

    st.title("Welcome, user " + applicant["userid"] + "!")
    st.markdown("""
    ## Workshop Recommendations""")
    
    workshop_query = st.text_input("What workshops do you want to attend?")
    advanced_diff = st.checkbox("Include workshops above your experience level?")
    if workshop_query != "":
        raw.at[user_index, "workshop_suggestions"] = workshop_query
    
    st.markdown("Not sure where to start? How about you kick things off right by attending some awesome workshops you might be interested in! :eyes:")
    
    st.markdown("%s" % get_display_text(applicant))
    
    if type(raw.iloc[user_index]["workshop_suggestions"]) != float:
        workshops = get_workshops(get_app_workshop_data(user_index), applicant["datascience_experience"], advanced_diff)
        
        for i in range(len(workshops)):
            st.markdown("### • %s" % (workshops[i]))

st.markdown("""## Cluster Connections""")
st.markdown("Trying to find a partner to group up with or just a friend who has similar interests that you can chat with? We've got you covered! Using the filter tools in the sidebar to your left, choose which options you want to filter by (age, school, experience, interests, etc). When you hit \"submit\", a bunch of fellow TAMU Datathon applicants will pop up below, most of whom probably have the same desire to connect as you do. Why not say hi? :smile:")

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