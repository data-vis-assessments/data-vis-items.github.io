print('ready!')
##Import packages
import numpy as np
print('imported numpy!')
import pandas as pd
print('imported pandas!')
import os
print('imported os!')
from PyPDF2 import PdfReader
print('imported PdfReader!')
import re
print('imported regex!')
print('packages imported!')


#extract raw text from pdf
text = ''
reader = PdfReader('/Users/averyyue/Downloads/data_vis_assessments_downloads/ARTIST.pdf') #replace with own directory
for i, page in enumerate(reader.pages): #loop through pages in pdf
    raw_text = page.extract_text()
    if not raw_text:
        continue
    text += raw_text
    
items_caps = text.split("ITEM") #split by item
blocks = []
for item in items_caps:
    if "Item" in item:
        new = item.split("Item")
        for item in new:
            blocks.append(item)
    else:
        blocks.append(item)
print('text extracted!')

#Make easier to separate blocks
ARTIST_items = []
for item in blocks:
    if re.match('^ \d{1}', item):
        ARTIST_items.append(item)



## Finding question stems and creating item ids

i = 0
item_ids = []
qs = []
for item in ARTIST_items:

    ##Create item id
    i += 1
    item_id = f'ARTIST_{i}'
    item_ids.append(item_id)
    
    #identifying and fixing some mistakes
    if "very easy" in item: #part of question mistakenly removes
        item = "  Match each description to the appropriate histogram below" + item
        
    if "PlayerProportion" in item: #remove junk text
        start_r = item.find("PlayerProportion")
        end_r = item.find("MH0.108") + len("MH0.108")
        item = item[:start_r] + item[end_r:]
        
    end = len(item)
    #identify end of question
    if "?" in item:
        end = item.find("?") + 1
    elif "Response" in item:
        end = item.find("Response")
    else:
        print('NOPE!')

    #identify start of question
    s = 0
    while s < len(item) and not item[s].isalpha():
        s += 1

    #form question and clean
    q = item[s:end].strip()
    qs.append(q)
print('questions found!')


##Now we can create the dataframe!
ARTIST_testdf = pd.DataFrame(item_ids)
ARTIST_testdf = ARTIST_testdf.rename(columns={0 : 'item_ids'})
ARTIST_testdf['question_stems'] = qs

i = 0
answers = []

print('starting the for loop!')
for item in ARTIST_items:
    i += 1
    print(i)
    ans = []
    if "very easy" in item: #add back part of question mistakenly removed
        item = "  Match each description to the appropriate histogram below" + item
#these questions involve selecting a visualization to match certain data
    if "Match " in item: #items 8, 9, 10
        url = 'https://data-visualization-benchmark.s3.us-west-2.amazonaws.com/ARTIST/images/'
        answer_options = ['I', 'II', 'III', 'IV']
        for op in answer_options:
            ans.append(url + 'histogram_' + op + '.png')

    elif "the following boxplots" in item: #item 11
        answer_options = ['A', 'B', 'C']
        for op in answer_options:
            ans.append(url + 'box_plot_11' + op + '.png')

    elif "Which box plot seems" in item: #item 12
        answer_options = ['A', 'B', 'C']
        for op in answer_options:
            ans.append(url + 'box_plot_12' + op + '.png')
            
    elif "Which of the above graphs" in item: #item 13
        answer_options = ['histogram_Graph_A', 'bar_Graph_B', 'box_plot_Graph_C']
        for op in answer_options:
            ans.append(url + op + '.png')

    elif "Which of the following graphs" in item: #item 14
        answer_options = ['A', 'B', 'C', 'D']
        for op in answer_options:
            ans.append(url + 'histogram_' + op + '.png')
    
    elif "Response" in item:
        print('running through answer choices!')
        if 'a.' in item:
            s = item.find('a.')
            e_a = s
            while item[e_a:e_a+2] != 'b.':
                e_a += 1
            ans.append(item[s:e_a]) #a.
            
            if 'c.' in item[e_a:]:
                e_b = e_a
                while item[e_b:e_b+2] != 'c.':
                    e_b += 1
                ans.append(item[e_a:e_b]) #b.
                
                if 'd.' in item[e_b:]:
                    e_c = e_b
                    while item[e_c:e_c+2] != 'd.':
                        e_c += 1
                    ans.append(item[e_b:e_c])

                    if 'e.' in item[e_c:]:
                        e_d = e_c
                        while item[e_d:e_d+2] != 'e.':
                            e_d += 1
                        ans.append(item[e_c:e_d])
                        ans.append(item[e_d:])
                    else:
                        ans.append(item[e_c:])
                else:
                    ans.append(item[e_b:])
                        
    answers.append(ans)
print('answers found!')

##Cleaning answers of junk text
answers = [[re.sub(r'[\d.]+$', '', ans).strip() for ans in answer] for answer in answers]

##fixing errors—numbers. These items have numeric answers. This makes it difficult to separate
    #them from participant data by heuristic. 
answers[0] = ['a. 1', 'b. 2', 'c. 3', 'd. 4']
answers[1] = ['a. 5', 'b. 10', 'c. 20', 'd. 30']
answers[3] = ['a. 6', 'b. 7', 'c. 12', 'd. 13', 'e. Can’t be determined']
ARTIST_testdf['answer_choices'] = answers

##Adding graph types as identified by hand, other columns
graph_types_ctl = ['Histogram', 'Histogram', 'Histogram', 'Histogram', 'Histogram', 'Histogram', 
                   'Histogram', None, None, None, 'Histogram', 'Histogram', None, 'Table']
ARTIST_testdf['graph_types_ctl'] = graph_types_ctl
task_types_ctl = ['literacy', 'literacy', 'literacy', 'literacy', 'reasoning', 
                  'literacy', 'literacy', 'reasoning', 'reasoning', 'reasoning',
                  'reasoning', 'reasoning', 'reasoning', 'reasoning']
ARTIST_testdf['task_types_ctl'] = task_types_ctl
ARTIST_testdf['graph_types'] = None
ARTIST_testdf['task_types'] = None
ARTIST_testdf['test_name'] = 'ARTIST'


##Adding urls to graph images
directory = 'https://data-visualization-benchmark.s3.us-west-2.amazonaws.com/ARTIST/images/'
def graph_url(row):
    image_name = ''
    item_id = row['item_ids']
    graph_type = row['graph_types_ctl']
    if graph_type != None:
        for char in graph_type:
            if char != ' ':
                image_name += char.lower()
            else:
                image_name += '_'
        row['graph_url'] = directory + image_name + '_' + item_id + '.png'
    else:
        row['graph_url'] = None
    return row
ARTIST_testdf = ARTIST_testdf.apply(graph_url, axis = 1)


#Save csv
ARTIST_testdf.to_csv("/Users/averyyue/Downloads/data-vis-dashboard/public/ARTIST.csv", index = False)
print('done!')