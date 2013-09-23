from stemming.porter2 import stem

import string
import re
import stop_words
import time
import patricia

string = "This is my text , this's is a nice ways to inputting text!! , ;. There are, infact!several other ways of giving an inputs to the texts!! nicer ways of should"
print re.split(r'[ |,|.|;|!]+', string)

def pre_process(line):
    line = line.lower()
    word_list = re.split(r'[ |,|. |;|!|?|(|)|-|{|}|"|\'|\n]+', line)
    prepro_line = ""
    for x in word_list:
        y = stem(x)
        if stop_words.match_word_with_regex(y)==None: 
            prepro_line = prepro_line + y + " "
            
    prepro_line = prepro_line.strip()
    #print prepro_line
    return prepro_line

pre_process(string)


index = patricia.trie()  # This is the Index Data Structure 

def doc_present_in_posting_list(posting_list,doc_id):
    counter = 0
    for ele_tuple in posting_list:
        if ele_tuple[0] ==  doc_id:
            return (True,counter)
        else:
            counter += 1
    return (False, -1)

def add_word_to_index(word, doc_id, label,index):
    if word in index:
        doc_in_posting_list_status = doc_present_in_posting_list(index[word],doc_id )
        if doc_in_posting_list_status[0]:
            get_count = doc_in_posting_list_status[1] 
            index[word][get_count][1]+= 1
        else:
            index[word].append([doc_id, 1])
            
    else:
        index[word] =[[doc_id, 1]]


def add_to_index(line,doc_id,label,index):
    for word in line.split():
        add_word_to_index(word, doc_id, label, index )

doc_id = 0
fp = open('cacm_all.txt','r')
label = ''
process_line = 0


temp_doc_string = ""
doc_max_freq = {}
def max_freq_in_doc(temp_string ):
    temp_hash = {}
    for word in temp_string.split():
        if word in temp_hash:
            temp_hash[word] += 1
        else:
            temp_hash[word] = 1
    freq_list_sorted = sorted(temp_hash.values())
    max_freq_value = freq_list_sorted[0]
    return max_freq_value

first = time.time()
doc_id = 0
for line in fp.readlines():
    if line[0] == '.':
        if line[1] == 'I':   
            label = 'I'
            doc_id = int(line.split()[1])
            print doc_id
            if doc_id != 1:
                max_freq = max_freq_in_doc(temp_doc_string)
                doc_max_freq[doc_id-1] = max_freq
                temp_doc_string = ""
            #write.writelines("Doc:"+str(doc_id)+"\n")
        elif line[1] == 'T':
            label = 'T'
            process_line  = 1
        elif line[1] == 'A':
            label = 'A'
            process_line  = 1
        elif line[1] == 'W' :
            label = 'W'
            process_line  = 1
        elif line[1] == 'K' :
            label = 'K'
            process_line = 1
        elif line[1] == 'N' :
            label = 'N'
            process_line  = 0
        elif line[1] == 'X' :
            label = 'X'
            process_line  = 0
        elif line[1] == 'B' :
            label = 'B'
            process_line  = 0
    else :
        if process_line == 1 :
            #fwrite.writelines(line  + "  " + label+"\n")
            prepro_line = pre_process(line)
            add_to_index(prepro_line,doc_id,label, index )
            temp_doc_string += " "+ prepro_line

max_freq = max_freq_in_doc(temp_doc_string)
doc_max_freq[doc_id] = max_freq

temp_doc_string = ""

import pickle

fob1 = open('index_file.txt','w')
pickle.dump(index,fob1)
fob1.close()

fob2 = open('doc_max_freq.txt','w')
pickle.dump(doc_max_freq, fob2)
fob2.close()

second = time.time()

print second-first
''' Testing goes here..  '''
