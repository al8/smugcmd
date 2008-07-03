import pysmug
import sys
import re


m = pysmug.login("smugrc.txt")

NickName = "alanw"


#u'stat' u'ok'
#u'method', u'smugmug.albums.get'
#'Statistics', ....
#


target_cat = "Life 2001"
re_match = "2001."



if len(sys.argv) < 3:
    print "%s dst:target_category src:re_match [preview]" % sys.argv[0]
    sys.exit(-1)


target_cat = sys.argv[1]
re_match = sys.argv[2]

if len(sys.argv) >= 3:
    preview_mode = sys.argv[3] == "preview"
    if not preview_mode:
        print "expected: preview"
        sys.exit(-1)
else: preview_mode = False

print "target_category:", target_cat
print "re_match:", re_match
print "preview_mode:", preview_mode
#sys.exit(0)

print "--------------"


catinfo = None
r = m.categories_get(NickName=NickName)
for e in r['Categories']:
    #print type(e), e
    if e['Name'] == target_cat: catinfo = e

if catinfo is None:
    print "cannot find category info"
    sys.exit(-1)
else:
    print "found category:", catinfo


albumsresp = m.albums_get(NickName=NickName)


cnt_total_albums = 0
cnt_match_albums = 0
cnt_modified_albums = 0


if albumsresp[u'stat'] == u'ok':
    print "total album count:", len(albumsresp[u'Albums'])
    for i, e in enumerate(albumsresp[u'Albums']):
        cnt_total_albums += 1
        if False:
            print "%4d : %5s %8s %60s %10s %10s" % (
                i,
                e.get(u'id', '*NONE'),
                e.get(u'Key', '*NONE'),
    
                e.get(u'Title', '*NONE'),
                e.get(u'Category', dict()).get(u'Name', "*None"),
                e.get(u'SubCategory', dict()).get(u'Name', "*None"),
            )
        #b = m.batch()
        #for album in m.albums_get()["Albums"]:
        #  b.albums_getInfo(albumId=album["id"], albumKey=album["Key"])
        #return (info["Album"] for params, info in b() if info["Album"]["ImageCount"] == 0)
        
        
        reg = re.match(re_match, e['Title'])
        
        if not (reg is None): #matched!
            cnt_match_albums += 1
            resp = m.albums_getInfo(albumID=e["id"], albumKey=e["Key"])
            print "found. before changing:", resp['Album']['Title'],
            print ": %s" % resp['Album']['Category']['Name'],

            if resp['Album']['Category']['id'] == catinfo['id']:
                print ": no changes required"
            else:
                print
                cnt_modified_albums += 1
                if preview_mode:
                    print "  preview mode... changes would be made here"
                else:
                    #print resp
                    #for i, (k, v) in enumerate(resp['Album'].iteritems()):
                    #    if k == "Category": print "%3d: %s=%s" % (i, k, v)
                    print "  changing now:",
                    resp = m.albums_changeSettings(albumID=e["id"], CategoryID=catinfo['id'])
                    #print resp
                    print "status:%s" % resp["stat"]
                    if False:
                        for k,v in resp.iteritems():
                            if type(v) is dict:
                                print k
                                for e2 in v.iteritems():
                                    print " ", e2
                            else:
                                print k, v
                    if resp["stat"] == "ok":
                        print "  after changing:",
                        resp = m.albums_getInfo(albumID=e["id"], albumKey=e["Key"])
                        print "new_cat:%s" % resp['Album']['Category']['Name']
                        #for i, (k, v) in enumerate(resp['Album'].iteritems()):
                        #    print "%3d: %s=%s" % (i, k, v)
    
                #sys.exit(0)
        #else: print "skip"

else:
    print "Error:", albumsresp[u'stat']

print "--------"
print "cnt_total_albums:", cnt_total_albums
print "cnt_match_albums:", cnt_match_albums
print "cnt_modified_albums", cnt_modified_albums


