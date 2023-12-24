from http.server import HTTPServer
from player import ProxyPlayer
import routing, xbmc, xbmcgui
from threading import Thread
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory

from server import MyServer

plugin = routing.Plugin()

def startProxy():
    def serve_forever(httpd):
        with httpd:
            httpd.serve_forever()
    
    webServer = HTTPServer(("127.0.0.1", 49777), MyServer)
    
    xbmc.log("JetProxy: starting server at http://127.0.0.1:49777"), xbmc.LOGINFO
    webServer.server_activate()
    thread = Thread(target=serve_forever, args=(webServer,))
    thread.setDaemon(True)
    thread.start()
    xbmc.log("JetProxy: server started!", xbmc.LOGINFO)

    return webServer

@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(play, "http://oscartv.mine.nu:25461/live/jmr1234/jmr1234/6139.m3u8"), ListItem("Example link"), False)
    addDirectoryItem(plugin.handle, plugin.url_for(test), ListItem("Test link"), False)
    endOfDirectory(plugin.handle)

@plugin.route("/test")
def test():
    link = xbmcgui.Dialog().input("Enter link")
    if not link:
        return
    play(link)

@plugin.route('/play/<path:url>')
def play(url):
    try:
        proxy = startProxy()
    except:
        proxy = None
        pass
    player = ProxyPlayer(server=proxy)
    player.play("http://127.0.0.1:49777?url=" + url)

if __name__ == '__main__':
    plugin.run()