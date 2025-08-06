### Now working with NAAL
##The places this pdf splits is by paragraph—that doesn't work well for the way this test is formatted
##Would be better to split by item

##import packages
import numpy as np
import pandas as pd
import os
from PyPDF2 import PdfReader
from langdetect import detect
from langdetect import DetectorFactory
print('packages imported!')

#extract raw text from pdf
text = ''
reader = PdfReader("/Users/averyyue/Downloads/data_vis_assessments_downloads/NAAL.pdf") #replace with own directory
for i, page in enumerate(reader.pages): #loop through pages in pdf
    raw_text = page.extract_text()
    if not raw_text:
        continue
    text += raw_text
    
items = text.split("Item ") #split by item
items[1] #checking work
NAAL_items = [] #clearing blank items
for item in items:
    if len(item) > 0:
        NAAL_items.append(item)
print('text extracted!')

## PARSING

#item_id and question stem
NAAL_qs = []
NAAL_item_ids = []
i = 0
for item in NAAL_items:
    #create item id
    i += 1
    ids = f'NAAL_{i}'
    NAAL_item_ids.append(ids)

    #find question start
    start = item.find('Question:') + len('Question:')
    question_start = item[start:]

    #find question end—from looking at data, a few options
    if 'A. ' in question_start:
        end = question_start.find('A. ')
    elif '- Sample' in question_start:
        end = question_start.find('- Sample')
    elif '?' in question_start:
        end = question_start.find('?') + 1
    elif 'Notes:' in question_start:
        end = question_start.find('Notes:')
        
    q = question_start[:end].strip() #clean & append
    NAAL_qs.append(q)
print('questions found!')

#Now can create dataframe
NAAL_testdf = pd.DataFrame(NAAL_item_ids)
NAAL_testdf = NAAL_testdf.rename(columns={0:'item_ids'})
NAAL_testdf['question_stems'] = NAAL_qs


## Identifying answer choices
NAAL_ans = []
for item in NAAL_items:
    #find question start
    start = item.find('Question:') + len('Question:')
    question_start = item[start:]

    #identify if multiple choice question
    if 'A. ' in question_start:
        a_start = question_start.find('A. ')
        a_start = question_start[a_start:]

        #identify end to answers
        if '- Sample' in a_start:
            end = a_start.find('- Sample')
        elif 'Notes:' in a_start:
            end = a_start.find('Notes:')

        ## clean and reformat
        answers_str = a_start[:end].strip()
        answers_lst = answers_str.split('. ')
        
        #fix first answer format
        A = answers_lst[0]
        answers_lst[1] = A + '. ' + answers_lst[1][:len(answers_lst[1])]
        answers_lst = answers_lst[1:]
        
        #rearrange letters for readability
        letters = []
        for i in range(0, len(answers_lst) - 1):
            letter = answers_lst[i][len(answers_lst[i])-1]
            letters.append(letter)
            answers_lst[i] = answers_lst[i][:len(answers_lst[i])-1]
        for i in range(1, len(answers_lst)):
            answers_lst[i] = letters[i-1] + '. ' + answers_lst[i]

        #finally, assign to answer choices
        answers = answers_lst
        
    else:
        answers = 'open-answer'

    NAAL_ans.append(answers)
NAAL_testdf['answer_choices'] = NAAL_ans
print('answers found!')

## Find task type—since the assessment is so short, I scanned for task types by hand
scale_types = ['Document Literacy', 'DocumentLiteracy', 'Quantitative Literacy']
task_types = []

for item in NAAL_items:
    for scale in scale_types:
        if scale in item:
            start = item.find(scale) + len(scale)
    if "Graph" in item:
        end = item.find("Graph")
    tasks = item[start:end]
    #cleaning
    if "ProseLiteracy" in tasks:
        start = tasks.find('ProseLiteracy') + len('ProseLiteracy')
        tasks = tasks[start:]
    task_types.append(tasks)
NAAL_testdf['task_types'] = task_types


##graph types are not encoded in the text itself. Since the dataframe is so short, I will add them by hand
graph_types = ['Stacked bar chart', 'Stacked bar chart', 'Stacked bar chart',
               'Line chart', 'Line chart', 'Line chart', 'Line chart', 'Grouped bar chart', 
               'Grouped bar chart', 'Grouped bar chart'
              ]

#create columns for future merging
NAAL_testdf['graph_types'] = None
NAAL_testdf['graph_types_ctl'] = graph_types
NAAL_testdf['task_types_ctl'] = NAAL_testdf['task_types']
NAAL_testdf['test_name'] = 'NAAL'


##Creating url to image in amazonaws
amazon_url = 'https://data-visualization-benchmark.s3.us-west-2.amazonaws.com/NAAL/images/'
def create_link(row):
    graph_name = row['graph_types_ctl']
    item_id = row['item_ids']
    image_name = ''
    for char in graph_name:
        if char != ' ':
            image_name += char.lower()
        else:
            image_name += '_'
    link = amazon_url + image_name + "_" + item_id + '.png'
    row['graph_url'] = link
    return row
NAAL_testdf = NAAL_testdf.apply(create_link, axis=1)


NAAL_testdf.to_csv("/Users/averyyue/Downloads/data-vis-dashboard/public/NAAL.csv", index = False)
print('done!')