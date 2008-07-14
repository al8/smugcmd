import pysmug
import sys
import re
import pickle
import time

m = pysmug.login("smugrc.txt")



#u'stat' u'ok'
#u'method', u'smugmug.albums.get'
#'Statistics', ....
#


NickName = "alanw"
#target_cat = "Life 2001"
#re_match = "2000"
#re_match = "Nature 2008"
re_match = "(2000.*)|(2001.*)|(2002.*)|(2003.*)|(2004.*)|(2005.*)|(2006.*)|(2007.*)|(2008.*)"
re_notmatch = ""

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

keywords_dict = dict()


#    0: LargeURL=http://alanw.smugmug.com/photos/325499347_6kSJp-L.jpg
#    1: X3LargeURL=http://alanw.smugmug.com/photos/325499347_6kSJp-X3.jpg
#    2: OriginalURL=http://alanw.smugmug.com/photos/325499347_6kSJp-80d50f7e1d89449bbc2849f9b75cfcc7.jpg
#    3: X2LargeURL=http://alanw.smugmug.com/photos/325499347_6kSJp-X2.jpg
#    4: Width=3072
#    5: Hidden=False
#    6: Height=2048
#    7: SmallURL=http://alanw.smugmug.com/photos/325499347_6kSJp-S.jpg
#    8: id=325499347
#    9: Format=JPG
#   10: Key=6kSJp
#   11: Date=2008-07-04 16:16:24
#   12: ThumbURL=http://alanw.smugmug.com/photos/325499347_6kSJp-Th.jpg
#   13: XLargeURL=http://alanw.smugmug.com/photos/325499347_6kSJp-XL.jpg
#   14: MD5Sum=80d50f7e1d89449bbc2849f9b75cfcc7
#   15: Caption=
#   16: TinyURL=http://alanw.smugmug.com/photos/325499347_6kSJp-Ti.jpg
#   17: Position=16
#   18: LastUpdated=2008-07-04 16:17:13
#   19: FileName=20080704_1025-50_LR.jpg
#   20: MediumURL=http://alanw.smugmug.com/photos/325499347_6kSJp-M.jpg
#   21: Keywords="nature"
#   22: Serial=0
#   23: Size=25783013
#    0: LargeURL=http://alanw.smugmug.com/photos/325499297_8NWFF-L.jpg
#    1: X3LargeURL=http://alanw.smugmug.com/photos/325499297_8NWFF-X3.jpg
#    2: OriginalURL=http://alanw.smugmug.com/photos/325499297_8NWFF-79d64c5bc813121b4531a1871a88d315.jpg


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
        
        if reg is None: #note matched!
            print "**UnmatchedAlbum.Title:", e['Title']
        else:
        #if not (reg is None): #matched!
            cnt_match_albums += 1
            print "Album.Title:", e['Title'] #, "  ImageCount:", e["ImageCount"]
            #albuminforesp = m.albums_getInfo(albumId=album["id"], albumKey=album["Key"])
            

            
            #albumresp = m.albums_getInfo(AlbumID=e["id"], AlbumKey=e["Key"])
#
#            for i, (k, v) in enumerate(albumresp['Album'].iteritems()):
#                print "%3d: %s=%s" % (i, k, v)

            print "   getting images..."
            imgresp = m.images_get(AlbumID=e["id"], AlbumKey=e["Key"], Heavy=True)
            print "   finished"
            
            if imgresp["stat"] == "ok":
                for idx, (v) in enumerate(imgresp["Album"]["Images"]):
#                    print idx
                    #print "%3d: %s" % (i, v)
#                    for idx, (k,v) in enumerate(v.iteritems()):
#                        print "  %3d: %s=%s" % (idx, k, v)
#                    #next
                    #keywords_dict
                    keywords = v["Keywords"]

                    if len(keywords) > 0:
                        if keywords[0] == "\"": #detect if semicolon separated or quote separated
                            keywords = keywords.strip("\"")
                            keyword_list = filter(lambda x: len(x) > 0, map(lambda x: x.strip(), keywords.split("\" \"")))
                        else:
                            keyword_list = filter(lambda x: len(x) > 0, map(lambda x: x.strip(), keywords.split(";")))
                    else:
                        keyword_list = list()

                    if len(keyword_list) > 0:
                        for key in keyword_list:
                            occurrences = keywords_dict.get(key, list())
                            d = dict()
                            d['FileName'] = v["FileName"]
                            d['albumTitle'] = e['Title']
                            d['albumID'] = e["id"]
                            d['albumKey'] = e["Key"]
                            d['ImageID'] = v["id"]
                            d['ImageKey'] = v["Key"]
                            d['TinyURL'] = v["TinyURL"]
                            d['Keywords'] = v["Keywords"]
                            d['keyword_list'] = keyword_list
                            occurrences.append( d )
                            if len(occurrences) == 1: keywords_dict[key] = occurrences
                    
                #next
            #if stat = ok

            #sys.exit(-1)
        #else: print "skip"
    #next album

else:
    print "Error:", albumsresp[u'stat']

print "--------"
print "cnt_total_albums:", cnt_total_albums
print "cnt_match_albums:", cnt_match_albums
print "cnt_modified_albums", cnt_modified_albums

f = open("output_%s.txt" % (time.time()), "w")
pickle.dump(keywords_dict, f)
f.close()

#f = open("output.txt")
#newdict = pickle.load(f)
#f.close()

#for kw, occurrences in keywords_dict.iteritems():
#    print "----\n%s:%d" % (kw, len(occurrences))
#    for occurrence in occurrences:
#        o = occurrence
#        print "  %s | %s | %s" % (o["albumTitle"], o["FileName"], o["TinyURL"])








#import pysmug
#import sys
#import re
#import pickle
#
#
#f = open("output.txt")
#keywords_dict = pickle.load(f)
#f.close()
#
#for kw, occurrences in keywords_dict.iteritems():
#    print "----\n%s:%d" % (kw, len(occurrences))
#    for occurrence in occurrences:
#        o = occurrence
#        print "  %s | %s | %s" % (o["albumTitle"], o["FileName"], o["TinyURL"])
#




