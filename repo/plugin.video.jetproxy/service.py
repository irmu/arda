import xbmc, requests

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    
    while not monitor.abortRequested():
        if monitor.waitForAbort(5):
            if is_port_in_use(49777):
                requests.get("http://127.0.0.1:49777/stop")
            break