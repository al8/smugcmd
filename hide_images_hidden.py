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


NickName = ""
#target_cat = "Life 2001"
#re_match = "2000"
#re_match = "Nature 2008"
#re_match = "(2000.*)|(2001.*)|(2002.*)|(2003.*)|(2004.*)|(2005.*)|(2006.*)|(2007.*)|(2008.*)"
re_match = ".*"
#re_match = "20080620 sigma.*"

show_unhide = False

hidden_keywords = [ "hidden", "hide" ]

if True:
    if len(sys.argv) < 3:
        print "%s username re_match_album [show_unhide]" % sys.argv[0]
        print "  hide images that have the keyword \"hidden\" or \"hide\""
        print "  show_unhide will unhide images without these keywords"
        sys.exit(-1)
    
    NickName = sys.argv[1]
    re_match = sys.argv[2]
    
    if len(sys.argv) >= 4:
        show_unhide = sys.argv[3] == "show_unhide"
        if not show_unhide:
            print "expected: show_unhide"
            sys.exit(-1)
    else: show_unhide = False
    
    print "nickname:", NickName
    print "re_match:", re_match
    print "show_unhide:", show_unhide
    #sys.exit(0)
    
    print "--------------"
    
albumsresp = m.albums_get(NickName=NickName)


cnt_total_albums = 0
cnt_match_albums = 0
cnt_modified_albums = 0

cnt_modified_images = 0

modified_list = list()

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
                    #print idx
                    #print "%3d: %s" % (i, v)
#                    for idx, (k,v) in enumerate(v.iteritems()):
#                        print "  %3d: %s=%s" % (idx, k, v)
                    #next
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
                        set_hidden = False
                        for key in keyword_list:
                            if key in hidden_keywords:
                                set_hidden = True
                                break
                                
                        if (set_hidden):
                            if (v["Hidden"]):
                                print "photo already hidden", v["SmallURL"]
                            else:
                                cnt_modified_images += 1
                                print "hide photo", v["SmallURL"]
                                imgchresp = m.images_changeSettings(ImageID=v["id"], Hidden=True)
                                if imgchresp["stat"] == "ok":        
                                    print "    success"
                                    modified_list.append( ("hide image", v) )
                                else:
                                    print "    error on  ImageID=%s" % (v["id"]), imgchresp["stat"]
                        elif (show_unhide):
                            if (not v["Hidden"]):
                                print "photo already unhidden", v["SmallURL"]
                            else:
                                cnt_modified_images += 1
                                print "unhide photo", v["SmallURL"]
                                imgchresp = m.images_changeSettings(ImageID=v["id"], Hidden=False)
                                if imgchresp["stat"] == "ok":        
                                    print "    success"
                                    modified_list.append( ("unhide image", v) )
                                else:
                                    print "    error on  ImageID=%s" % (v["id"]), imgchresp["stat"]
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
#print "cnt_modified_albums", cnt_modified_albums
print "cnt_modified_images", cnt_modified_images

