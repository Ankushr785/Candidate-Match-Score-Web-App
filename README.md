# Candidate-Match-Score-Web-App
An NLP based Web-App that asks the user to input some Job Posting along with a candidate list (in a defined format) to give scores to the candidates based on their proficiency in the job profile required.

The algorithm creates a 10-point score metric to assess how proficient a certain candidate is for a defined job posting based on the LinkedIn profile of the candidate.
The score has been assigned on the basis of the candidate's job title, past experience and skill endorsements.

1. Job Title - CountVectorizer from scikit learn's feature extraction library has been used to create a dictionary of the keywords involved in the job posting, using the '.fit_transform()' function. After that, the job title of every candidate is compared with the created dictionary using the '.transform' function.
The '.toarray()' funtion creates an array of comparison. This array lets you know how many times every word from the dictionary has been found in the sentence that is being compared.

         e.g If the dictionary contains the following words -> ['Machine Learning, Research Engineer']
         Then the comparison array of the string ['Assistant Engineer'] would be -> [0 0 0 1]
         
The motive behind this process is to assess how closely every candidate's job title resembles the required candidature in the job posting. The more words match, the more likely is the candidate appropriate for the job.
Based on the number of words matched, the candidates are divided into three scoring categories:
         
         a. 2 or more than 2 words match - 5 points 
         
         b. 1 word match - 3 points
         
         c. No word matches - 1 point, since there's always a possibility of an outlier.

2. Past Experience - Based on the past experience of the candidates, they have been divided into 5 categories around the preferable past experience of the job posting:

         a. For past experience less than 1 year - 1 point, again, to acknowledge the outliers

         b. For past experience between 1 year and (preferable past experience - 1) years - 2 points

         c. For past experience between (preferable past experience - 1) years and (preferable past experience + 1) years - 3 points
         
         d. For preferable past experience between (preferable past experience + 1) years and (preferable past experience + 3) years - 4 points
         
         e. For preferable past experience more than (preferable past experience + 3) years - 5 points
         
3. Skill endorsements - Based on the number of endorsements received by the candidates on relevant skills, they've been classified into 3 scoring categories:
 
         a. For endorsements < (endorsement sample mean - 2) -  1 point
         
         b. For (endorsement sample mean - 2) <= endorsements < (endorsement sample mean + 2) - 3 points
         
         c. For endorsements> (endorsement sample mean + 2) - 5 points
         
         Note: Owing to the unavailability of endorsement data, it has been obtained by simulating a normal distribution along the complete sample by a defined mean and standard deviation.
         
The total score has been obtained by giving equal weightage to all the individual score categories. Since a 10 point score metric is desired, a complete candidate score is the 2/3rd of the sum of the total score across all the three categories, i.e.
 
         Total Score = (Job Profile Score + Past Experience Score + Skill Endorsements Score) x (2/3)
         
Apart from all these, some other criteria might also prove beneficial, like:
 
         a. Present organization (Tier 1, Tier 2, Tier 3...) - Score categories could be formulated on the basis of the tier in which   the organization lies
         
         b. Graduation College - (Tier 1, Tier 2, Tier 3...)
         
         c. Projects as well as Independent Courseworks - Scores on the basis of number of relevant and verified projects and courseworks

The output is a csv file containing the candidate names along with their respective scores.
