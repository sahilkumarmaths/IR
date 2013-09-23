import query_lookup
import time

while 1:
    query = raw_input("Enter query:\n")
    time1 = time.time()
    doc_score_map = query_lookup.get_results(query)
    time2 = time.time()
    doc_score_map_list = sorted(doc_score_map, key=doc_score_map.get, reverse=True)
    for w in doc_score_map_list:
        print w, doc_score_map[w]
    print "Latency : " + str(time2-time1)
