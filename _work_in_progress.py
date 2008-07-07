import pysmug
import sys
import re


m = pysmug.login("smugrc.txt")



#u'stat' u'ok'
#u'method', u'smugmug.albums.get'
#'Statistics', ....
#


NickName = "alanw"
#target_cat = "Life 2001"
re_match = "2000"


if False:
    if len(sys.argv) < 4:
        print "%s username dst:target_category src:re_match [preview]" % sys.argv[0]
        sys.exit(-1)
    
    NickName = sys.argv[1]
    target_cat = sys.argv[2]
    re_match = sys.argv[3]
    
    if len(sys.argv) >= 4:
        preview_mode = sys.argv[4] == "preview"
        if not preview_mode:
            print "expected: preview"
            sys.exit(-1)
    else: preview_mode = False
    
    print "nickname:", NickName
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
            albumresp = m.albums_getInfo(AlbumID=e["id"], AlbumKey=e["Key"])
#            print "found. before changing:", albumresp['Album']['Title'],
#
#            #for i, (k, v) in enumerate(albumresp['Album'].iteritems()):
#            #    print "%3d: %s=%s" % (i, k, v)
#            
#            print ": %s %s %s %s %s" % (
#                'Larges' if albumresp['Album']['Larges'] else '',
#                'XLarges' if albumresp['Album']['XLarges'] else '',
#                'X2Larges' if albumresp['Album']['X2Larges'] else '',
#                'X3Larges' if albumresp['Album']['X3Larges'] else '',
#                'Originals' if albumresp['Album']['Originals'] else '',
#            )
            imgresp = m.images_get(AlbumID=e["id"], AlbumKey=e["Key"], Heavy=True)
            
            if imgresp["stat"] == "ok":
                for i, (v) in enumerate(imgresp["Album"]["Images"]):
                    print i
                    #print "%3d: %s" % (i, v)
                    for i, (k,v) in enumerate(v.iteritems()):
                        print "  %3d: %s=%s" % (i, k, v)

            sys.exit(-1)

#            if len(albumresp['Album']['Password']) != 0:
#                print "************ skipping", albumresp['Album']['Title']
#                continue
            
            if (not albumresp['Album']['Larges'] or not albumresp['Album']['XLarges'] or not albumresp['Album']['X2Larges'] or not albumresp['Album']['X3Larges'] or not albumresp['Album']['Originals']):
                print "found. before changing:", albumresp['Album']['Title'],
                
#                for i, (k, v) in enumerate(albumresp['Album'].iteritems()):
#                    print "%3d: %s=%s" % (i, k, v)
                
                print ": %s %s %s %s %s" % (
                    'Larges' if albumresp['Album']['Larges'] else '',
                    'XLarges' if albumresp['Album']['XLarges'] else '',
                    'X2Larges' if albumresp['Album']['X2Larges'] else '',
                    'X3Larges' if albumresp['Album']['X3Larges'] else '',
                    'Originals' if albumresp['Album']['Originals'] else '',
                )

                cnt_modified_albums += 1
                if False:
                    print "  preview mode... changes would be made here"
                elif True:
                    #print resp
                    #for i, (k, v) in enumerate(resp['Album'].iteritems()):
                    #    if k == "Category": print "%3d: %s=%s" % (i, k, v)
                    changedict = {
                        'Larges' : True,
                        'XLarges' : True,
                        'X2Larges' : True,
                        'X3Larges' : True,
                        'Originals' : True,
                    }
                    print "  changing now:",
                    resp = m.albums_changeSettings(albumID=e["id"], **changedict)
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
                        print ": %s %s %s %s %s" % (
                            'Larges' if resp['Album']['Larges'] else '',
                            'XLarges' if resp['Album']['XLarges'] else '',
                            'X2Larges' if resp['Album']['X2Larges'] else '',
                            'X3Larges' if resp['Album']['X3Larges'] else '',
                            'Originals' if resp['Album']['Originals'] else '',
                        )
                        #for i, (k, v) in enumerate(resp['Album'].iteritems()):
                        #    print "%3d: %s=%s" % (i, k, v)
                    #sys.exit(0) #debug
            else:
                print "no changes required:",  albumresp['Album']['Title']
#            continue #debug

    
             
        #else: print "skip"

else:
    print "Error:", albumsresp[u'stat']

print "--------"
print "cnt_total_albums:", cnt_total_albums
print "cnt_match_albums:", cnt_match_albums
print "cnt_modified_albums", cnt_modified_albums


