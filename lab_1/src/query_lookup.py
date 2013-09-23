from stemming.porter2 import stem
import pickle
import string
import re
import stop_words
import math
import time
import patricia

fob1 = open('index_file.txt','r')
index = pickle.load(fob1)
fob1.close()

fob2 = open('doc_max_freq.txt','r')
doc_max_freq = pickle.load(fob2)
fob2.close()

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



#for word in index:
    #fwrite.writelines(word+"\n")


def get_results(query_input):
    doc_score_map = {}
    prepro_query = pre_process(query_input)
    print query_input
    print prepro_query
    for word in prepro_query.split():
        if word in index:
            plist_of_word = index[word]
            if "<patricia._NonTerminal" in (str(plist_of_word)): 
                continue
            for ele in plist_of_word:        
                #score = ele[1]* T_weight + ele[2] * A_weight + ele[3]*W_weight
                doc_id = ele[0]
                f = float(ele[1])
                tf = 0.5 + (0.5*f)/float(doc_max_freq[doc_id])
                no_of_docs_having_term = len(plist_of_word)
                D = 3204
                idf = math.log10(float(D) / float(no_of_docs_having_term))
                score = float(tf)* idf
                doc = ele[0]
                if doc in doc_score_map:
                    doc_score_map[doc] += score
                else:
                    doc_score_map[doc]  = score

    #print doc_score_map
    doc_score_map_list = sorted(doc_score_map, key=doc_score_map.get, reverse = True)
    #for w in doc_score_map_list:
     #   print w , doc_score_map[w]
    return doc_score_map

# Testing goes here..

query_input = "What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers? Richard Alexander, Comp Serv, Langmuir Lab (TSS)"
#query_input = "I am interested in articles written either by Prieve or Udo Pooch Prieve, B. Pooch, U. Richard Alexander, Comp Serv, Langmuir Lab (author = Pooch or Prieve)"

#query_input = "Intermediate languages used in construction of multi-targeted compilers; TCOLL Donna Bergmark, Comp Serv, Uris Hall (intermed lang)"

#get_results(query_input)




