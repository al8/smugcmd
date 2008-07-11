import pysmug
import sys
import re
import pickle

f = open("keyword_dict.txt")
keywords_dict = pickle.load(f)
f.close()

#for kw, occurrences in keywords_dict.iteritems():
#    print "----\n%s:%d" % (kw, len(occurrences))
#    for occurrence in occurrences:
#        o = occurrence
#        print "  %s | %s | %s" % (o["albumTitle"], o["FileName"], o["TinyURL"])


imglist = list()

for kw, occurrences in keywords_dict.iteritems():
    #print "----\n%s:%d" % (kw, len(occurrences))
    imglist.append( (len(occurrences), kw) )
#    for occurrence in occurrences:
#        o = occurrence
#        print "  %s | %s | %s" % (o["albumTitle"], o["FileName"], o["TinyURL"])

imglist.sort()
imglist.reverse()


matched = 0
for i, e in enumerate(imglist):
    reg = re.match("[0-9]+", e[1])

    if reg is None:
        print e
        continue
    else:
        matched += 1
    
        #print e
        #if matched > 100: break

