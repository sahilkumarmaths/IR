
import query_lookup
import time
fp = open('query_input.txt','r')


fout = open('query_results.txt', 'w')

frels = open('qrels.txt','r')

process_line = 0
query = ""


qrels_line = frels.readline()

precision_list = []
latency_list = []

for line in fp.readlines():
    if line[0] == '.':
        if line[1] == 'I':
            query_id = int(line.split()[1])
            if query_id != 1:
                print query_id-1
                fout.write(str(query_id-1) + "\n")
                time1 = time.time()
                doc_score_map = query_lookup.get_results(query)
                time2 = time.time()
                doc_score_map_list = sorted(doc_score_map, key=doc_score_map.get, reverse=True)
                qrels_line_split = qrels_line.split()
                temp_hash = {}
                actual_rel_count = 0
                while int(qrels_line_split[0]) == (query_id-1):
                    actual_rel_count += 1
                    doc = int(qrels_line_split[1])
                    if doc in doc_score_map_list:   # The given doc is not present in the resultant list of docs.. 
                        doc_position_in_pl = doc_score_map_list.index(doc) + 1
                        #print doc , doc_position_in_pl
                        temp_hash[doc] = doc_position_in_pl 
                    else:
                        #print doc, "Not found"
                        print ""
                    qrels_line = frels.readline()
                    qrels_line_split = qrels_line.split()
                temp_hash_sorted = sorted(temp_hash, key = temp_hash.get,reverse = False)
                precision = 0
                counter = 1
                for w in temp_hash_sorted:
                    print w , temp_hash[w]
                    fout.write(str(w) + "  " + str(temp_hash[w]) + "\n" )
                    precision += float( counter ) / float (temp_hash[w])
                    last_retreived_doc_pos = temp_hash[w]
                    counter += 1
                if actual_rel_count != 0 :
                    precision = precision / float(actual_rel_count)
                else:
                    precision = 0
                print "Precision :" + str(precision)
                fout.write("Precision :" + str(precision) + "\n")
                precision_list.append(precision)
                print "Latency :" + str(time2-time1)
                fout.write("Latency :" + str(time2-time1)+ "\n")
                latency_list.append(time2-time1)
                query = ""
                   
        elif line[1] == 'W':
            process_line = 1

        elif line[1] == 'T':
            process_line = 1

        elif line[1] == 'A':
            process_line = 1

        elif line[1] == 'N':
            process_line = 1

        elif line[1] == 'K':
            process_line = 1

        else:
            process_line = 0
    else:
        if process_line  == 1 :
            query += " " + line

def find_map(precision_list):
    sum_val = 0
    for ele in precision_list:
        sum_val += ele
    sum_val = float(sum_val)/float(len(precision_list))
    return sum_val

def find_avg_latency(latency_list):
    sum_val = 0
    for ele in latency_list:
        sum_val += ele
    sum_val = float(sum_val)/float(len(latency_list))
    return sum_val

print find_map(precision_list)
                       
fout.write("MAP :" + str(find_map(precision_list)) + "\n" )
print find_avg_latency(latency_list)           
fout.write("Avg. latency :" + str(find_avg_latency(latency_list)) + "\n")
           
fout.close()
