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

def get_workshops(track, experience):
    workshop_list = []
    for i in range(len(workshops["track"])):
        if workshops.iloc[i]["track"] == track and workshops.iloc[i]["difficulty"] <= experience:
            workshop_list.append(workshops.iloc[i]["workshop_name"])
            
    random.shuffle(workshop_list)
            
    if len(workshop_list) < 3: return workshop_list
    else: return workshop_list[0:3]
    
def get_display_text(app):
    if type(app["workshop_suggestions"]) == float:
        return "Hm... It doesn't look like you've given us any info as to what kind of workshops you'd like to see. Feel free to search up a topic of interest in the search bar above and see what you get!"
    
    else:
        return ("Because you suggested that you were interested in workshops about  \"*%s*\"  and your experience with data science is \n  *%s*:" % (applicant["workshop_suggestions"], experience[applicant["datascience_experience"]]))

    
    
    
experience = ["beginner", "amateur", "advanced", "expert"]

tags_dict = {}
for i in range(len(workshops.index)):
    tags_dict[str(workshops.iloc[i]["workshop_short"])] = (workshops.iloc[i]["tags"]).split(", ")


user_index = None




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
    
    st.markdown("Not sure where to start? How about you kick things off right by attending some awesome workshops you might be interested in! :eyes:")
    
    st.markdown("%s" % get_display_text(applicant))
    
    if type(applicant["workshop_suggestions"]) != float:
        st.write(get_workshops(get_app_workshop_data(user_index), applicant["datascience_experience"]))