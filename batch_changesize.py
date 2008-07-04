import pysmug
import sys
import re


m = pysmug.login("smugrc.txt")



#u'stat' u'ok'
#u'method', u'smugmug.albums.get'
#'Statistics', ....
#


NickName = ""
target = ""
re_match = "."
preview_mode = False

if True:
    if len(sys.argv) < 4:
        print "%s username [m,l,xl,xxl,xxxl,o] src:re_match [preview]" % sys.argv[0]
        sys.exit(-1)
    
    NickName = sys.argv[1]
    target = sys.argv[2]
    re_match = sys.argv[3]
    
    if len(sys.argv) >= 4:
        preview_mode = sys.argv[4] == "preview"
        if not preview_mode:
            print "expected: preview"
            sys.exit(-1)
    else: preview_mode = False
    
    print "nickname:", NickName
    print "target:", target
    print "re_match:", re_match
    print "preview_mode:", preview_mode
    #sys.exit(0)
    
    print "--------------"
    
    changedict = {
        'Larges' : True,
        'XLarges' : True,
        'X2Larges' : True,
        'X3Larges' : True,
        'Originals' : True,
    }
    
    helper = {
        'm': 'Larges',
        'l': 'XLarges',
        'xl': 'X2Larges',
        'xxl': 'X3Larges',
        'xxxl': 'Originals',
        'o': '[skip]',
    }.get(target.lower(), None)
    if helper == None:
        print "invalid target"
        sys.exit(-1)
    if helper != '[skip]': changedict[helper] = False
    print "found target:", changedict
    #sys.exit(0) #debug


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

        
        reg = re.match(re_match, e['Title'])
        
        if not (reg is None): #matched!
            cnt_match_albums += 1
            albumresp = m.albums_getInfo(AlbumID=e["id"], AlbumKey=e["Key"])

            is_require_cfg = (
                albumresp['Album']['Larges'] != changedict['Larges'] or
                albumresp['Album']['XLarges'] != changedict['XLarges'] or
                albumresp['Album']['X2Larges'] != changedict['X2Larges'] or
                albumresp['Album']['X3Larges'] != changedict['X3Larges'] or
                albumresp['Album']['Originals'] != changedict['Originals']
            )

            if not (is_require_cfg):
                print "no changes required:",  albumresp['Album']['Title']
            else:
                print "found. before changing:", albumresp['Album']['Title'],
                
                print ": %s %s %s %s %s" % (
                    'Larges' if albumresp['Album']['Larges'] else '',
                    'XLarges' if albumresp['Album']['XLarges'] else '',
                    'X2Larges' if albumresp['Album']['X2Larges'] else '',
                    'X3Larges' if albumresp['Album']['X3Larges'] else '',
                    'Originals' if albumresp['Album']['Originals'] else '',
                )

                cnt_modified_albums += 1
                if preview_mode:
                    print "  preview mode... changes would be made here"
                elif True:
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
            #end if is_require_cfg
        #if matched album name
    #for in albums
else:
    print "Error:", albumsresp[u'stat']

print "--------"
print "cnt_total_albums:", cnt_total_albums
print "cnt_match_albums:", cnt_match_albums
print "cnt_modified_albums", cnt_modified_albums


