from stemming.porter2 import stem
import re
fp = open('common_words.txt','r')

def form_regex_for_common_words():
    expr = ""
    count = 0
    common_words = fp.read().split()
    for word in common_words:
        count+= 1
        if count == len(common_words):
            expr += "^"+stem(word)+"$"
        else:
            expr += "^"+stem(word)+"$|"
    return expr


reg_expression = form_regex_for_common_words()  # So, the resultant regular expression is calculated here.. 

#print reg_expression
p = re.compile(reg_expression)
    
# function which matches a given word to the regular expression computed above.. and returns the result of the match.. 
def match_word_with_regex(word):
    exists =  p.match(word) 
    return exists
