import numpy as np
import pandas as pd

def processData(excelFilePath, pastExp, corpusString):
    #data read from a .xlsx file in the system
    data = pd.read_excel(excelFilePath)
    
    #Job Profile Description (#user defined)
    preferable_past_experience = 4 # Default value
    if pastExp and pastExp != '':
        preferable_past_experience = int(pastExp)
    corpus = [corpusString]

    #NaNs dropped
    data = data.dropna(axis = 0)
    
    candidate_data = pd.DataFrame({'First Name':data['First Name'], 'Last Name':data['Last Name'], 'Company':data['Company'], 'Job Title':data['Job Title'], 'Past Experience':data['Past Experience']})
    
    #Also use endorsements as a scoring parameter, here it's a simulated normal distribution
    candidate_data['Endorsements'] = np.round(np.random.normal(8, 2, len(candidate_data)), 2)
    #Count Vectorizer imported for NLP
    from sklearn.feature_extraction.text import CountVectorizer

    #Bag of words deployed to create a word dictionary 
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(corpus)

    #Categories given on the basis of closeness to the job description
    match_score_category = []
    for i in range (0, len(candidate_data)):
        match_array = vectorizer.transform([candidate_data.loc[i, 'Job Title']]).toarray()
        score = 0
        for j in range(0, x.toarray().size):
            if match_array[:, j] == 0:
                score+=0
            else:
                score+=1
        if score>=2:
            match_score_category+= [1]
        elif score == 1 :
            match_score_category+= [2]
        else:
            match_score_category+= [3]
        i+=1
            
        
    candidate_data['Match Score Category jp']= pd.DataFrame({'Match Score Category jp': match_score_category})

    candidate_match_score = []

    for i in range(0, len(candidate_data)):
        if candidate_data.loc[i, 'Match Score Category jp'] == 1:
            candidate_match_score+= [5]
        elif candidate_data.loc[i, 'Match Score Category jp'] == 2:
            candidate_match_score+= [3]
        else:
            candidate_match_score+= [1]
        i+=1
        
    candidate_data['Candidate Match Score jp']= pd.DataFrame({'Candidate Match Score jp': candidate_match_score})

    #Another score parameter on the basis of the past experience of respective candidates    
    candidate_match_score_n = []

    for i in range(0, len(candidate_data)):
        if candidate_data.loc[i, 'Past Experience']>=1 and candidate_data.loc[i, 'Past Experience']<=(preferable_past_experience - 1):
            candidate_match_score_n+=[2]
        elif candidate_data.loc[i, 'Past Experience']>(preferable_past_experience - 1) and candidate_data.loc[i, 'Past Experience']<=(preferable_past_experience + 1):
            candidate_match_score_n+=[3]
        elif candidate_data.loc[i, 'Past Experience']>(preferable_past_experience + 1) and candidate_data.loc[i, 'Past Experience']<=(preferable_past_experience + 3):
            candidate_match_score_n+=[4]
        elif candidate_data.loc[i, 'Past Experience']>(preferable_past_experience + 3):
            candidate_match_score_n+=[5]
        else:
            candidate_match_score_n+=[1]
        i+=1
        
    candidate_data['Candidate Match Score pe']= pd.DataFrame({'Candidate Match Score pe': candidate_match_score_n})
    
    #Score on the basis of Endorsements
    candidate_match_score_m = []
    for i in range(0, len(candidate_data)):
        if candidate_data.loc[i, 'Endorsements'] < (np.mean(candidate_data['Endorsements'])-2):
            candidate_match_score_m+=[1]
        elif candidate_data.loc[i, 'Endorsements']>=(np.mean(candidate_data['Endorsements'])-2) and candidate_data.loc[i, 'Endorsements']<=(np.mean(candidate_data['Endorsements'])+2):
            candidate_match_score_m+=[3]
        else:
            candidate_match_score_m+=[5]
        i+=1
        
    candidate_data['Candidate Match Score ed']= pd.DataFrame({'Candidate Match Score ed': candidate_match_score_m})

    total_score = []        
    for i in range(0, len(candidate_data)):
        total_score+=[(candidate_data.loc[i, 'Candidate Match Score jp'] + candidate_data.loc[i, 'Candidate Match Score pe'] + candidate_data.loc[i, 'Candidate Match Score ed'])*2/3]
        i+=1
        
    candidate_data['Total Score']= pd.DataFrame({'Total Score': total_score})

        
    Result = pd.DataFrame({'First Name': candidate_data['First Name'], 'Last Name': candidate_data['Last Name'], 'Match Score': candidate_data['Total Score']})   

    csv = Result.to_csv(encoding='utf-8')

    return csv
