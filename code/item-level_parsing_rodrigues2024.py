##import packages
import numpy as np
import pandas as pd
import os
from PyPDF2 import PdfReader
print('done!')


#Function:
#Extracts text from pdfs to later be split into question stem and answer choices

def extract_assessment_text(pdf_path, min_chars=20):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    reader = PdfReader(pdf_path) #open pdf where assessment is stored
    text = [] #initialize list to store text

    for i, page in enumerate(reader.pages): #loop through pages in pdf
        raw_text = page.extract_text()
        if not raw_text:
            continue
            
        #strip/split text
        raw_text = raw_text.strip() 
        chunks = raw_text.split('\n')

        #in case of junk text
        good_chars = [',', '.', ':', '\'', '(', ')', ' ', '?', '!'] 
        for chunk in chunks:
            cleaned_text = ''
            for i in range(len(chunk)):
                if chunk[i].isalpha() or chunk[i].isdigit() or chunk[i] in good_chars:
                    cleaned_text += chunk[i]
            chunk_clean = cleaned_text.strip()

            text.append(chunk_clean) #finally, save cleaned chunk to text list

    return text

#extract text for rodrigues2024 and save
rodrigues2024_test = extract_assessment_text("/Users/averyyue/Downloads/data_vis_assessments_downloads/rodrigues2024.pdf")
print('text extracted!')

##PARSING


##parse [rodrigues2024] for question stem, answer choices, and any additional information in pdf
#identify question stem
tasks = ['Conceptual', 'Suitable', 'Unsuitable'] #task type indicating start of question

item_ids = []
questions = []
task_types = []

i = 0
for value in rodrigues2024_test:
    for task in tasks:
        if task in value:
            
            task_types.append(task) #add task type
            task_end = len(task)
            
            q = value[task_end:] #add question stem
            questions.append(q.strip())
            
            i += 1 #create and add item id
            item = 'rodrigues2024_' + str(i)
            item_ids.append(item)

#can now create dataframe for rodrigues2024
rodrigues2024_testdf = pd.DataFrame(item_ids)
rodrigues2024_testdf['task_types'] = task_types
rodrigues2024_testdf['question_stems'] = questions
            
rodrigues2024_testdf = rodrigues2024_testdf.rename(columns={0:'item_ids'}) #renaming columns for later merging
print('tasks found!')

#identify and add graph type, create amazon url based on graph name
graph_types = []
amazon_url = 'https://data-visualization-benchmark.s3.us-west-2.amazonaws.com/rodrigues2024/images/'
image_urls = []
for value in rodrigues2024_test:
    if "Fig. " in value: #identify start to label
        fig = value.find("Fig. ")
        num = value.find(". ", fig + 4) #so as not to get image number id
        
        graph_type = value[num + 2:]
        #three items per graph
        graph_types.append(graph_type)
        graph_types.append(graph_type)
        graph_types.append(graph_type)

        image_name = '' #create image name for url
        for char in graph_type:
            if char != ' ':
                image_name += char.lower()
            else:
                image_name += '_'
        link = amazon_url + 'rodrigues2024_' + image_name + '.png'
        image_urls.append(link)
        image_urls.append(link)
        image_urls.append(link)
        
rodrigues2024_testdf['graph_types'] = graph_types
rodrigues2024_testdf['graph_url'] = image_urls
print('graphs found!')

#identify and add answer choices (rodrigues2024)
r_qna = {} #initialize dictionary
i = 0

#goal is to loop through each value and identify the questions.
#Then, for each question, loop through the answer choices (A-F) for that question and add to a list
#this list will be the value for that row in the answer choices column
while i < len(rodrigues2024_test): #loop
    
    value = rodrigues2024_test[i]
    if any(task in value for task in tasks): #check if question
        for task in tasks:
            if task in value:
                task_end = len(task)
                q = value[task_end + 1:]
                r_qna[q] = [] #add question as key in dictionary
                
        s = i + 1
        while s < len(rodrigues2024_test) and not any(task in rodrigues2024_test[s] for task in tasks): #check for next question
            if "( )" in rodrigues2024_test[s]: #between each question, check if answer choice
                letter = rodrigues2024_test[s][0] #reformat
                start = rodrigues2024_test[s].find(")") + 1
                choice = letter + '.' + rodrigues2024_test[s][start:] #add answer choice to list in dictionary
                r_qna[q].append(choice)
            s += 1
    i += 1             


## Now that we have a dictionary of question stems and answer choices, match each answer choice list to
# the dataframe of questions
def match_questions_r(row):
    for key in r_qna.keys():
        if key == row['question_stems']:
            row['answer_choices'] = r_qna[key]
    return row
rodrigues2024_testdf = rodrigues2024_testdf.apply(match_questions_r, axis=1)
print('questions matched!')

##Fill in columns in preparation for future merging
rodrigues2024_testdf['test_name'] = 'rodrigues2024'
rodrigues2024_testdf['task_types_ctl'] = rodrigues2024_testdf['task_types']
def standard_format(value):
    if value == 'Clustered bar chart':
        print('cluster')
        return 'Grouped bar chart'
    if 'Simple' in value:
        print('simple')
        return 'Bar chart'
    if 'Stacked' in value:
        print('stack')
        return 'Stacked bar chart'
    if value == 'Boxplot':
        return 'Box plot'
    if "Bubble" in value:
        return "Bubble chart"
    if "Line" in value:
        return 'Line graph'
    if "Scatterplot" in value:
        return "Scatter plot"
    else:
        print('none')
        return value
rodrigues2024_testdf['graph_types_ctl'] = rodrigues2024_testdf['graph_types'].apply(standard_format)
print('graph types found!"')

##Save as csv
rodrigues2024_testdf.to_csv("/Users/averyyue/Downloads/data-vis-dashboard/public/rodrigues2024.csv", index = False)
print('done!')
