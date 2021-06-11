import logging
logging.warning('a')
import xbmcaddon,xbmc,os,sys,xbmcvfs,xbmcplugin
import  requests

import AWSHandler
AWSHandler.InitDB()
Addon = xbmcaddon.Addon()
Domain_sparo=Addon.getSetting("domain_sp2")

addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
done_dir = os.path.join(addonPath, 'resources', 'done')
sys.path.append( done_dir)
import cache
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database


user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
logo_path=os.path.join(user_dataDir, 'logo')
if not os.path.exists(logo_path):
     os.makedirs(logo_path)
m3_path=os.path.join(user_dataDir, 'm3u8')
if not os.path.exists(m3_path):
     os.makedirs(m3_path)
cacheFile_trk = os.path.join(user_dataDir, 'cache_play_trk.db')

cacheFile = os.path.join(user_dataDir, 'cache_play.db')
xbmcvfs.mkdir(user_dataDir)
addonInfo = xbmcaddon.Addon().getAddonInfo
dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
save_file=os.path.join(user_dataDir,"fav.txt")

try:
  time_to_save=int(Addon.getSetting("save_time"))
except:
  time_to_save=3
if xbmc.getCondVisibility('system.platform.windows'):
   win_system=True
else:
   win_system=False


level_images=['http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Cherry.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Strawberry.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Orange.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Apple.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Pear.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Banana.ico','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTaOe61sWWiQLqgknayKHvVfPtb59o_acSgPLMLhnxZEqHwuymWYQ','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Mango.ico','https://cdn.iconscout.com/public/images/icon/premium/png-512/pretzel-breakfast-appetizer-pastry-37ebe79fde250ac4-512x512.png','https://i.ytimg.com/vi/vPa45_0ozqE/maxresdefault.jpg']
level_fanart=['https://i0.wp.com/cidadegamer.com.br/wp-content/uploads/2012/02/Pac-man-the-adventure-begins-estreia-no-disney-XD-em-2013.jpg?fit=298%2C298','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-sj9LxuMDN64yD2GqxiUXpbJwstVmq4rZbOJJlNtX9q5twNqR','https://vignette.wikia.nocookie.net/fantendo/images/2/25/Mario_Artwork_-_Super_Mario_3D_World.png/revision/20131025223057','https://cdn.thisiswhyimbroke.com/images/iron-man-lamp.jpg','https://www.avforums.com/image.php?imageparameters=editorial/products/a197b-thor-2-the-dark-world-photos-2.jpg|909','https://i.pinimg.com/originals/99/27/aa/9927aab09a32ff610086758078fe792e.jpg','https://news.marvel.com/wp-content/uploads/2016/09/57852a5335bb6.jpg','http://cdn-static.denofgeek.com/sites/denofgeek/files/styles/main_wide/public/0/04//batman-v-superman-dawn-of-justice.jpg?itok=SwDBZWJJ','https://www.sideshowtoy.com/wp-content/uploads/2014/01/902174-product-feature1.jpg','https://vignette.wikia.nocookie.net/emporea/images/d/d9/Black_dragon_preloader.jpg/revision/latest?cb=20160216171424']
level_movies=['https://www.youtube.com/watch?v=nRCTMwgBGxM','https://www.youtube.com/watch?v=M0Es2B7aUHo','https://www.youtube.com/watch?v=mSolF3QBVBY','https://www.youtube.com/watch?v=QgRyng9w38g','https://www.youtube.com/watch?v=NlfoaCVHP0s','https://www.youtube.com/watch?v=KMR-6-YizZQ','https://www.youtube.com/watch?v=pBbsvavno8I','https://www.youtube.com/watch?v=lUIDCuYszqI','https://www.youtube.com/watch?v=opji5DgE_nQ']


dbcon = database.connect(cacheFile)
dbcur = dbcon.cursor()
dbcon_trk = database.connect(cacheFile_trk)
dbcur_trk  = dbcon_trk.cursor()





def update_once():
    logging.warning('updating DB')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'AllData')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""speed TEXT);" % 'servers')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""o_name TEXT,""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""saved_name TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""prev_name TEXT,""id TEXT);"% 'lastlinktv')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""o_name TEXT,""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""saved_name TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""prev_name TEXT,""id TEXT);"% 'lastlinkmovie')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""id TEXT);"% 'nextup')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""id TEXT);"% 'sources')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""plot TEXT,""option TEXT,""option1 TEXT,""option2 TEXT,""option3 TEXT);" % 'acestream')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""inc TEXT, ""discription TEXT);" % 'mychan')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""id TEXT, ""season TEXT, ""episode TEXT);" % 'subs')

    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""link TEXT NOT NULL UNIQUE,""status TEXT,""option TEXT);" % 'historylinks')
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""link TEXT);" % 'torrents')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""link TEXT);" % 'rest')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""link TEXT);" % 'rest2')
    try:
        dbcur.execute("VACUUM 'AllData';")
        dbcur.execute("PRAGMA auto_vacuum;")
        dbcur.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
        dbcur.execute("PRAGMA temp_store=MEMORY ;")
    except:
     pass
    dbcon.commit()


    dbcur_trk.execute("CREATE TABLE IF NOT EXISTS %s ( ""data_ep TEXT, ""dates TEXT, ""fanart TEXT,""color TEXT,""id TEXT,""season TEXT,""episode TEXT, ""next TEXT);" % 'AllData3')
    dbcon_trk.commit()

    dbcur.execute("SELECT * FROM lastlinktv WHERE o_name='f_name'")

    match = dbcur.fetchone()

    if match==None:
      dbcur.execute("INSERT INTO lastlinktv Values ('f_name','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s');" %  (' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '))
      dbcon.commit()

    dbcur.execute("SELECT * FROM lastlinkmovie WHERE o_name='f_name'")

    match = dbcur.fetchone()
    if match==None:
      dbcur.execute("INSERT INTO lastlinkmovie Values ('f_name','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s');" %  (' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '))
      dbcon.commit()
    return 'ok'
all_img=cache.get(update_once,24, table='posters')
