##import packages
import numpy as np
import pandas as pd
from PyPDF2 import PdfReader
from langdetect import detect
from langdetect import DetectorFactory
import re ##important——this pdf has particularly odd formatting due to translation

print('imported packages')

## Extract text from pdf

merk2020_pdf = '/Users/averyyue/Downloads/data_vis_assessments_downloads/merk2020.pdf'

reader = PdfReader(merk2020_pdf) #open pdf where assessment is stored
text = '' #initialize list to store text

for i, page in enumerate(reader.pages): #loop through pages in pdf
    raw_text = page.extract_text()
    if not raw_text:
        continue
            
        #strip/split text
    raw_text = raw_text.strip() 
    chunks = raw_text.split('\n')

    good_chars = [',', '.', ':', '\'', '(', ')', ' ', '?', '!'] 
    for chunk in chunks:
        cleaned_text = ''
        for i in range(len(chunk)):
            if chunk[i].isalpha() or chunk[i].isdigit() or chunk[i] in good_chars:
                cleaned_text += chunk[i]
            chunk_clean = cleaned_text.strip()
    
                #if multilingual assessment, only save English text
        if len(chunk_clean) > 1:
            lang = detect(chunk_clean)
            if lang != 'en': # Skip text if not English
                continue
        text+=chunk_clean

print('extracted text')

#it looks like 1.# shows the page number. 
merk2020_text = text.split('1.')

##Split items by question for easier parsing
merk2020_text_split = []
dk = "Don't know"
for item in merk2020_text:
    if dk.lower() in item.lower():
        
        start = item.lower().find(dk.lower()) +len("Don't know")
        
        pt1 = item[:start]
        merk2020_text_split.append(pt1)
        
        pt2 = item[start:]
        if dk.lower() in pt2.lower():
            start = pt2.lower().find(dk.lower()) +len("Don't know")
            
            pt3 = pt2[:start]
            merk2020_text_split.append(pt3)
            
            pt4 = pt2[start:]
            if dk.lower() in pt4.lower():
                start = pt4.lower().find(dk.lower()) +len("Don't know")
            
                pt5 = pt4[:start]
                merk2020_text_split.append(pt5)
                
                pt6 = pt4[start:]
                merk2020_text_split.append(pt6)
            else:
                merk2020_text_split.append(pt4)
            
        else:
            merk2020_text_split.append(pt2)
        
    else:
        merk2020_text_split.append(item)

print('split chunks')
## Parsing question stem and creating item id
# This will be done in two halves to better identify the beginning and end
#of each question. Pt 1 is to identify the end of each question
    #(and split questions in the same chunk into different chunks)
#pt 2 is to identify the beginning of each question
    #and exclude junk text


# parse question stem pt 1—identify end of questions
q_firsthalf = []

for item in merk2020_text_split:
    end = 0
    if len(item) > 57: #filter for non-questions caught in item
        #find where each question ends, generally   

        #This is to pre-empt a chunk that has two questions in it,
        if "two histograms" in item:
            mid = item.find('.', 1)

            qs1 = item[1:mid + 1]
            q_firsthalf.append(qs1)
    
            end1 = item.find('?')
            qs2 = item[mid:end1+1]
            q_firsthalf.append(qs2)
        
        #Identify the end of each question
        elif "?" in item:
            end = item.find("?")
        elif "!" in item:
            end = item.find("!")
        elif ":" in item:
            end = item.find(":")
        elif ("...") in item:
            end = item.find("...") + 2
        elif "a girl" in item:
            end = item.find("a girl") - 1
        qs = item[:end + 1]

        #For questions where the end is signified by capital letters
        if end == 0:
            start = 0
            while item[start].isdigit() or item[start].islower() or item[start] in ' ,':
                start+=1
            next_s = start + 1
            while item[next_s].islower() or item[next_s] in ' ,':
                next_s += 1
            qs = item[start:next_s]
        
        q_firsthalf.append(qs)
print('first half of questions')

#parsing question stem pt 2—identify beginning of questions
questions = []
item_ids = []
i = 0
for q in q_firsthalf:
    
    #identify question beginnings
    if "The graph above " in q:
        start = q.find("The graph above")
    elif "In the table above" in q:
        start = q.find("In the table above")
    elif "If " in q:
        start = q.find("If ")
    elif "Which " in q:
        start = q.find("Which ")
    elif "Wich " in q:
        start = q.find("Wich ")
    elif "The diff" in q:
        start = q.find("The diff")
    elif "In the table" in q:
        start = q.find("In the table")
    else:
        start = 0
    question = q[start:].strip() 
    if len(question) >1:
        #create item ids
        i += 1
        ids = f'merk2020_{i}'
        item_ids.append(ids)
        questions.append(q[start:].strip())
print('second half of questions')

#Now can start our dataframe
merk2020_testdf = pd.DataFrame(item_ids)
merk2020_testdf = merk2020_testdf.rename(columns={0 : 'item_ids'})
merk2020_testdf['question_stems'] = questions
print('df created')        

##Identifying answer choices
#Create chunks of each question
## Parsing answer choices
## creating question blocks with answers in them
blocks = []
for item in merk2020_text_split:
    if len(item) > 57:
        if "two histograms" in item:
            mid = item.find('.', 1)
            qs1 = item[1:mid + 1]
            
            blocks.append(qs1)
            
            qs2 = item[mid:]
            blocks.append(qs2)
            
        else:
            blocks.append(item)


##Find the end to each question / where the answer choices begin
#some questions have no answer choices (ie are open-answer)
    #(This was done seperately from identifying questions for easier bug catching)
##finding end to question
anss = [] 
for block in blocks:
    #find question endings
    if "?" in block:
        start = block.find("?")
    elif "!" in block:
        start = block.find("!")
    elif ":" in block:
        start = block.find(":")
    elif ("...") in block:
        start = block.find("...") + 2
    elif "a girl" in block:
        start = block.find("a girl") - 1
    ans = block[start + 1:]
    
    #identify questions that are not multiple choice (ie are open-answer)
    if dk.lower() not in ans.lower():
        answer = "open-answer"
        ans = "open-answer"

    #identify answers that are initiated by capital letters
    if start == 0:
        end = 0
        while item[end].isdigit() or item[end].islower() or item[end] in ' ,':
            end+=1
        next_e = end + 1
        while item[next_e].islower() or item[next_e] in ' ,':
            next_e += 1
        ans = item[next_e:]
    
    #identify other common endings
    else:
        if "." in ans:
            answer = ans.split(".")
        elif "...." in ans:
            answer = ans.split("....")
        elif " " in ans:
            answer = ans.split(" ")
    anss.append(ans)
print('answers identified')

## Identify where answer choices split into separate answers, to be added
#into a list
def split_answer_choices(text):
    if not text or text.strip() == "":
        return []
    
    # Replace abbreviations (to later restore) so as not to be caught when splitting
    text = text.replace("e.g.", "__eg__")
    
    text = re.sub(r'\.{3,}', '|', text)  # Replace ellipses with | for later splitting
    
    # Separate lowercase to uppercase boundary, but NOT within parentheses
    text = re.sub(r'(?<=[a-z])(?=[A-Z])(?![^()]*\))', '|', text)
    text = re.sub(r'(?<=\))(?=[A-Z])', '|', text)  # separate ) to uppercase boundary
    
    # Handle number sequences like "1 Child3 Children"
    text = re.sub(r'(\d+\s*[A-Za-z]+)', r'|\1', text)

    # Identify anchor ("Don't know") and add delimeter
    text = text.replace("Don't know", "|Don't know")
    text = re.sub(r'read\d+', r'|\g<0>', text)
    
    # Split on "|" or ". "
    chunks = re.split(r'\s*\|\s*|\.\s*', text)
    
    # Filter out empty strings
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    
    # Restore abbreviations
    chunks = [chunk.replace("__eg__", "e.g.") for chunk in chunks]
    
    return chunks
        
            
#Split answer choices into lists using function
splits = []
for ans in anss:
    split = split_answer_choices(ans)
    splits.append(split)
print(splits)
print(len(splits))
#Identify and fix mistakes from splitting
cleaned_splits = []
for split in splits:
    new_split = []

    if "4 to" in split: #identify the error item: "'4 to', '69 to 2'" -> '4 to 6', '9 to 2'
        for i in range(1, len(split)-1): #fix by moving number at beginning of next item
            split[i-1] = split[i-1] + ' ' + split[i][0]
            split[i] = split[i][1:]
        new_split = [item for item in split if len(item) > 0] #remove empty values
        cleaned_splits.append(new_split)
    
    elif '3read' in split: #identify error: "'Don't knowread', '3read', '4read'" -> "'Don't know'"
        for i in range(len(split)): #fix by removing the 'read' values (this was from text formatting)
            split[i] = split[i].replace('read', '')
            if len(split[i]) == 1:
                split[i] = ''
        new_split = [item for item in split if len(item) > 0] #remove empty values
        cleaned_splits.append(new_split)
    
    elif 'M(S1)' in split: #identify error: M(S1) and M(kA) mistakenly split from answers
        includes = ['M(kA)', 'M(S1)']
        for i in range(len(split)): #replace at end of original answers
            if split[i] in includes:
                split[i-1] = split[i-1] + '.' + split[i]
                split[i] = ''
        new_split = [item for item in split if len(item) > 0] #remove empty values
        cleaned_splits.append(new_split)

    else:
        cleaned_splits.append(split)
print(cleaned_splits)
print(len(cleaned_splits))
print('answer choices split')

#Add to dataframe
merk2020_testdf['answer_choices'] = cleaned_splits


##Add graph types. These were identified by hand
graph_types_ctl = ['Histogram', 'Histogram', None, 'Scatter plot', 'Scatter plot', 
                   'Dot graph', 'Dot graph', 'Dot graph', 'Dot graph', 'Box plot', 'Box plot', 
                   'Table', 'Line graph', 'Ranking table', 'Box plot', 'Scatter plot',
                   None, 'Line graph', 'Table', 'Table']
merk2020_testdf['graph_types_ctl'] = graph_types_ctl
merk2020_testdf['graph_types'] = None

##Add task types. No information in assessment pdf on task types.
merk2020_testdf['task_types'] = None
task_types_ctl = ['Understand statistics & psychometrics', 'Understand how to interpret data', 
                  'Understand how to interpret data', 'Understand & use data displays & representations', 
                  'Understand & use data displays & representations', 'Summarize & explain data', 
                  'Summarize & explain data', 'Summarize & explain data', 'Understand & use data displays & representations',
                  'Aggregate data', 'Aggregate data', 'Understand data properties', 'Understand data properties',
                  'Understand data properties', 'Aggregate data', 'Use statistics', 'Use statistics', 
                  'Manipulate data', 'Manipulate data', 'Manipulate data']
merk2020_testdf['task_types_ctl'] = task_types_ctl
merk2020_testdf['test_name'] = 'merk2020'

##Add url to graph image
directory = 'https://data-visualization-benchmark.s3.us-west-2.amazonaws.com/merk2020/images/'
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
merk2020_testdf = merk2020_testdf.apply(graph_url, axis = 1)
print('graph url, graph type, task type added')

merk2020_testdf.to_csv("/Users/averyyue/Downloads/data-vis-dashboard/public/merk2020.csv", index = False)
print('done!')
