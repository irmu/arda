#!/usr/bin/python
# -*- coding: utf-8 -*-

# Addon Watchstates Handler
# Copyright (C) 2016 kit500


import xbmc, xbmcaddon #,xbmcgui, xbmcplugin,
import os, sqlite3, re, sys,logging

Addon = xbmcaddon.Addon()
addon_path    = Addon.getAddonInfo('path')
addon_id      = Addon.getAddonInfo('id')
addon_icon    = Addon.getAddonInfo('icon')
addon_fanart  = Addon.getAddonInfo('fanart')
addon_version = Addon.getAddonInfo('version')
addon_name    = Addon.getAddonInfo('name')
addon_profile = Addon.getAddonInfo('profile')
addon_icon    = xbmc.translatePath(addon_icon)
addon_fanart  = xbmc.translatePath(addon_fanart)
addon_profile = xbmc.translatePath(addon_profile)
dbpath        = os.path.join(addon_profile, 'storage.db')
#debug_mode    = Addon.getSetting("debug_mode") == 'true'


def GetKodiDB():
    try:
        dbpath = xbmc.translatePath('special://database')
        dblist = os.listdir(dbpath)
        dbvs = []
        for file in dblist:
            if re.findall('MyVideos(\d+)\.db', file): dbvs.append(int(re.findall('MyVideos(\d+)\.db', file)[0]))
        dbv = str(max(dbvs))
        ##print 'DB version: ' + dbv
        dbpath = xbmc.translatePath(os.path.join('special://database', 'MyVideos' + dbv + '.db'))
        ##print "DB path: " + dbpath
        return dbpath
    except:
       return ''

def ConnectDB(path = dbpath):  # exec conn.commit() и conn.close() after call
	if not os.path.isdir(addon_profile):
		#print 'ConnectDB: path: ' + path
		#print 'ConnectDB: dir: ' + addon_profile
		#print 'isdir: ' + str(os.path.isdir(addon_profile))
		os.makedirs(addon_profile)
	##print 'isfile: ' + str(os.path.isfile(path))
	#if not os.path.isfile(path):
	conn = sqlite3.connect(path)
	c = conn.cursor()
	return conn, c

def InitDB():
	conn, c = ConnectDB()
	c.execute('SELECT * FROM sqlite_master WHERE type = "table" AND name = "WatchStatus"')
	tablesexist = c.fetchone()
	##print 'InitDB: tablesexist: ' + str(tablesexist)
	if not tablesexist:
		#print 'InitDB: Creating DB...'
		c.executescript("""
			CREATE TABLE WatchStatus (Title TEXT NOT NULL, Season INTEGER, Epidode INTEGER, EpisodeDescr TEXT, PlayCount INTEGER NOT NULL, TimeStamp TEXT, Duration TEXT, Watched INTEGER, ID INTEGER PRIMARY KEY, UNIQUE (Title, Season, Epidode), UNIQUE (Title, Season, EpisodeDescr));
			CREATE TABLE Location (Location TEXT UNIQUE NOT NULL, ID INTEGER NOT NULL, Queue INTEGER);
			CREATE TABLE Info (Var TEXT UNIQUE, Value TEXT);
			CREATE TABLE TitleAliases (TitleAlias TEXT UNIQUE, Title);
			INSERT INTO Info (Var, Value) VALUES ("DBVersion", "1.0");
			""")
	# todo add UNIQUE (Title, Season, EpisodeDescr) -> done
	conn.commit()
	conn.close()

def UpdateDB():
    # Update queued files in internal DB from Kodi DB
    conn, c = ConnectDB()
    kpath = GetKodiDB()
    if kpath=='':
        #xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'KODI DB EMPTY'.decode('utf8'))).encode('utf-8'))
        return ''
    kconn, kc = ConnectDB(kpath)
    c.execute('SELECT Location, ID FROM Location WHERE Queue = 1')
    ##print list(c)
    # using cusrsor as iterator

    
    for row in list(c):
        
        fpath, id = row
    
        '''response = xbmc.executeJSONRPC('{ \
            "jsonrpc": "2.0", \
            "id": 1, \
            "method": "Files.GetFileDetails", \
            "params": {"file": "%s", "media": "video", "properties": ["playcount"]} \
            }' % (fpath, ))
        #print response'''
        kc.execute('SELECT idFile, playCount FROM files WHERE strFilename = ?', (fpath, ))
        fres = kc.fetchone()
      
        if fres:
            idfile, pc = fres
            #print 'UpdateDB: found idfile in Kodi DB: ' + str(idfile)
            kc.execute('SELECT timeInSeconds, totalTimeInSeconds FROM bookmark WHERE idFile = ?', (idfile, ))
            bres = kc.fetchone()
    
            if bres: 
                TimeStamp = bres[0]
                duration = bres[1]
                #print 'UpdateDB: found bookmark in Kodi DB: %s %d %d' % (TimeStamp, id, idfile)
                c.execute('UPDATE WatchStatus SET TimeStamp = ?, Duration = ?, Watched = NULL WHERE ID = ?', (TimeStamp, duration, id))
       
                if c.rowcount == 0:
                    #print 'UpdateDB: internal DB exception: file id not found...'
                    continue
            elif pc:
                c.execute('UPDATE WatchStatus SET TimeStamp = NULL, Watched = 1 WHERE ID = ?', (id, ))
            #else:
                #print "UpdateDB: Kodi DB integrity exception: no playcount with no bookmark..."
        #else:
            #print "UpdateDB: file not found in Kodi DB..."
        #c.execute('DELETE FROM Location WHERE Location = ?', (fpath, ))
        c.execute('UPDATE Location SET Queue = NULL WHERE Location = ?', (fpath, ))
        
    conn.commit()
    kconn.close()
    conn.close()

def CheckWS(info):
    # Update status from internal DB
    ##print info
    #UpdateDB()
    conn, c = ConnectDB()
    

    title = info['title']

    if title==' ':
       return False    
    if info['season']==' ' or info['season']=='%20':
       season=0
       episode=0
    elif info['episode']==' ' or info['episode']=='%20':
       season = int(info['season']) if 'season' in info else None
       episode=0
    else:
        season = int(info['season']) if 'season' in info else None
        episode = int(info['episode']) if 'episode' in info else None
    edescr = info['episode_info'] if 'episode_info' in info and not episode else None
    req = 'SELECT Watched, TimeStamp, Duration, PlayCount FROM WatchStatus WHERE Title = :t AND (Season = :s OR (:s IS NULL AND Season IS NULL)) AND (Epidode = :e OR (:e IS NULL AND Epidode IS NULL)) AND (EpisodeDescr = :ed OR (:ed IS NULL AND EpisodeDescr IS NULL))'
    c.execute(req, {'t': title, 's': season, 'e': episode, 'ed': edescr})
    res = c.fetchone()

    
    result = None
    if res:
        result = {'wflag': False, 'resumetime': None, 'totaltime': None}
        wflag, timestamp, duration, playcount = res
        if wflag: 
            #print 'found w flag'
            # для редких случаев, если в Kodi DB playCount = null, отметка не ставится (имеет значение только для синхронизации разных плагинов, если, допустим, в одном просмотренно, а в другом просмотренно частично, можно ли что-то сделать с этим пока неизвестно) Т.е у kodi db есть приоритет.
            result['wflag'] = True
        elif timestamp:
            #print 'found TimeStamp: ' + timestamp
            result['resumetime'] = timestamp
            result['totaltime'] = duration
            # todo: проверить, перезаписываются ли значения из Kodi DB -> нет
    return result

def QueueWS(info,f_tit=''):
    # Queue file to update after playback
   try:
    UpdateDB()
    conn, c = ConnectDB()
    title = info['title']
    if title==' ':
       return False    
    if info['season']==' ' or info['season']=='%20':
       season=0
       episode=0
    elif info['episode']==' ' or info['episode']=='%20':
       season = int(info['season']) if 'season' in info else None
       episode=0
    else:
        season = int(info['season']) if 'season' in info else None
        episode = int(info['episode']) if 'episode' in info else None
    
    edescr = info['episode_info'] if 'episode_info' in info and not episode else None
    if episode != None and season == None: season = 1
    # Get ID if exist
    req = 'SELECT ID FROM WatchStatus WHERE Title = :t AND (Season = :s OR (:s IS NULL AND Season IS NULL)) AND (Epidode = :e OR (:e IS NULL AND Epidode IS NULL)) AND (EpisodeDescr = :ed OR (:ed IS NULL AND EpisodeDescr IS NULL))'
    c.execute(req, {'t': title, 's': season, 'e': episode, 'ed': edescr})
    res = c.fetchone()
    #print 'result: ' + str(res)
    if not res:
        #print 'inserting new row...'
        c.execute('INSERT INTO WatchStatus (Title, Season, Epidode, EpisodeDescr, PlayCount) VALUES (?, ?, ?, ?, ?)', (title, season, episode, edescr, 1))
        id = c.lastrowid
        #print 'c.lastrowid: ' + str(id)
    else:
        id = res[0]
        c.execute('UPDATE WatchStatus SET PlayCount = ifnull(PlayCount, 0) + 1 WHERE ID = ?', (id, ))
    if f_tit!='':
        c.execute('INSERT OR REPLACE INTO Location (Location, ID, Queue) VALUES (?, ?, ?)', (f_tit, id, 1))
    else:
        c.execute('INSERT OR REPLACE INTO Location (Location, ID, Queue) VALUES (?, ?, ?)', (sys.argv[0] + sys.argv[2].decode('utf8'), id, 1))

    conn.commit()
    conn.close()
   except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)

            logging.warning('ERROR IN AWS:'+str(lineno))
            logging.warning('inline:'+line)
            logging.warning('Error:'+str(e))
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'inLine:'+str(lineno))).encode('utf-8'))
            done_nextup=1
            marked_trk=1


