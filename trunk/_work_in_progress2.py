import pysmug
import sys
import re
import pickle
import string

m = pysmug.login("smugrc.txt")


#f = open("keyword_dict.txt")
f = open(sys.argv[1])
keywords_dict = pickle.load(f)
f.close()


NickName = "alanw"
preview_mode = False

#use only lower case here
accepted_keywords = [
"hdr",
"panaramic",
"food",
"farmer's market",
"dog",
"lucy",
"nature",
"vegetable",
"lr",
]

#use only lower case here
rename_keywords = {
    "panaram" : "panaramic",
    "veggie" : "vegetable",
}

print "accepted keywords:", accepted_keywords
print "rename keywords:", rename_keywords
#isdigit

print "nickname:", NickName
print "preview_mode:", preview_mode


#for kw, occurrences in keywords_dict.iteritems():
#    print "----\n%s:%d" % (kw, len(occurrences))
#    for occurrence in occurrences:
#        o = occurrence
#        print "  %s | %s | %s" % (o["albumTitle"], o["FileName"], o["TinyURL"])


imglist = list()

change_dict = dict()


for kw, occurrences in keywords_dict.iteritems():
    #print "----\n%s:%d" % (kw, len(occurrences))
    #print kw
    add_this = None
    remove_this = None
    
    kw = kw.lower() #only compare lower case
    
#    imglist.append( (len(occurrences), kw) )
    if kw.isdigit():
        #print "skipping digits:", kw
        continue
    if kw in accepted_keywords:
        print "skipping accepted keyword:", kw
        continue
    elif kw in rename_keywords.iterkeys():
        print "rename %s to %s" % (kw, rename_keywords[kw])
        add_this = rename_keywords[kw]
        remove_this = kw
    else:
        print "not accepted kw:", kw
        remove_this = kw
        
    for occurrence in occurrences:
        o = occurrence
        #print o.keys()
        #print o["ImageID"], o["Keywords"]
        
        ch = change_dict.get(o["ImageID"], {"remove": list(), "add": list(), "old_keyword_list": None} )
        change_dict[o["ImageID"]] = ch
        
        ch['albumTitle'] = o['albumTitle']
        ch['TinyURL'] = o['TinyURL']
        ch['FileName'] = o['FileName']
        
        if ch["old_keyword_list"] is None:
            keyword_list = o.get("keyword_list", None)
            if keyword_list is None:
                keywords = o["Keywords"]
                if len(keywords) > 0:
                    if keywords[0] == "\"": #detect if semicolon separated or quote separated
                        keywords = keywords.strip("\"")
                        keyword_list = filter(lambda x: len(x) > 0, map(lambda x: x.strip(), keywords.split("\" \"")))
                    else:
                        keyword_list = filter(lambda x: len(x) > 0, map(lambda x: x.strip(), keywords.split(";")))
                else:
                    keyword_list = list()
            ch["old_keyword_list"] = keyword_list
        #end if ch["old_keyword_list"] is None
        if not remove_this is None: ch["remove"].append(remove_this)
        if not add_this is None: ch["add"].append(add_this)
        

        #print "  %s | %s | %s" % (o["albumTitle"], o["FileName"], o["TinyURL"])

ch_count = 0
print "changes:"
for k, v in change_dict.iteritems():
    keywords_list = filter(lambda e: not e in v["remove"], v["old_keyword_list"])
    for e in v["add"]:
        keywords_list.append(e)
        
    del v["old_keyword_list"]
    #v["keyword_list"] = keywords_list
    v["Keywords"] = string.join(keywords_list, "; ")
    #print k, v
    print "%s %s/%s %s" % (k, v['albumTitle'], v['FileName'], v['TinyURL'])
    print "  %s=%s" % ("Keywords", v["Keywords"])
    if len(v["remove"]) > 0: print "  %s=%s" % ("remove", v["remove"])
    if len(v["add"]) > 0: print "  %s=%s" % ("add", v["add"])
    
    ch_count += 1
    if not preview_mode:
        imgchresp = m.images_changeSettings(ImageID=k, Keywords=v["Keywords"])
        if imgchresp["stat"] == "ok":        
            #print imgchresp
            print "    success", ch_count
            pass
        else:
            print "    error on  ImageID=%s" % (k), imgchresp["stat"]
    #sys.exit(-1)
        
    
#    for k2, v2 in v.iteritems():
#        print "  %s=%s" % (k2, v2)
print "total images modified:", ch_count
sys.exit(-1)


imglist.sort()
imglist.reverse()

#images_changeSettings

matched = 0
for i, e in enumerate(imglist):
    #reg = re.match("[0-9]+", e[1])
    #if reg is None:
    if not e[1].isdigit():
        print e
        continue
    else:
        matched += 1
    
        #print e
        #if matched > 100: break

