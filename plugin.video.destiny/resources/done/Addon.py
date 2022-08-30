
def getSetting(data):

   try:
    import xbmcaddon
    Addon = xbmcaddon.Addon()
    return Addon.getSetting(data)
   except:
   
       if data=="Email":
           return 'meni4321@gmail.com'
       if data=='Password':
          return 'meni1234'
       if data=='username_hebits':
          return ''
       if data=='Password_sdr_hebits':
          return ''
       if data=='username':
          return ''
       if data=='Password_sdr':
          return ''
       if data=='filter_fp':
          return 'false'
       if data=='ftp_size':
          return '5'
       if data=='rdsource':
          return 'true'
       if data=='size_limit':
          return '400'
       if data=='domain_sp5':
          return 'sparo.club'
       if data=='regex_mode':
          return '0'
       if data=='ghaddr':
          return 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL21vc2hlcDE1L2JhY2svbWFzdGVyLzUudHh0'