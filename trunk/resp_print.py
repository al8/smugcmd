import sys

def resp_print(resp, f = sys.stdout):
#    if resp[u'stat'] == u'ok':
#        print "success"
#        for e, k in resp.iteritems():
#            print "    %s=%s" % (e, k)

    if resp[u'method'] == 'smugmug.albums.get':
        idx_category = None
        idx_id = None
        idx_key = None
        idx_title = None
        
        for i, a in enumerate(resp[u'Albums']):
            if i == 0:
                for cat_idx, e in enumerate(a.keys()):
                    if e.lower() == "category": idx_category = cat_idx
                    elif e.lower() == "id": idx_id = cat_idx
                    elif e.lower() == "key": idx_key = cat_idx
                    elif e.lower() == "title": idx_title = cat_idx
                        
                    f.write("%s " % e)
                f.write("\n")
            for idx, e in enumerate(a.values()):
                if idx == idx_category:
                    f.write("%s " % e[u'Name'])
                else:
                    f.write("%s " % e)
            f.write("\n")
    else:
        f.write("unknown method '%s'\n" % (resp[u'method']))
        for e, k in resp.iteritems():
            f.write("    %s=%s\n" % (e, k))
    

