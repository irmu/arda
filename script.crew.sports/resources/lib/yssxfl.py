
import base64, codecs
thecrew = 'aW1wb3J0IHJlcXVlc3RzCmZyb20gYnM0IGltcG9ydCBCZWF1dGlmdWxTb3VwCmltcG9ydCByZQppbXBvcnQgYmFzZTY0CmZyb20gcmVzb3VyY2VzLmxpYiBpbXBvcnQgY2ZzY3JhcGUKZ2FtZSA9IFtdCgoKZGVmIGdldF9nYW1lcygpOgogICAgc2NyYXBlciA9IGNmc2NyYXBlLmNyZWF0ZV9zY3JhcGVyKCkKICAgIHVybCA9ICJodHRwOi8veW91cnNwb3J0cy5zdHJlYW0vIgogICAgYWdlbnQgPSAiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzc5LjAuMzk0NS4xMTcgU2FmYXJpLzUzNy4zNiIKICAgIGh0bWxDb250ZW50ID0gc2NyYXBlci5nZXQodXJsLGhlYWRlcnM9eyJ1c2VyLWFnZW50IjphZ2VudH0pLmNvbnRlbnQKICAgIHNvdXAgPSBCZWF1dGlmdWxTb3VwKGh0bWxDb250ZW50LCAnaHRtbC5wYXJzZXInKQogICAgeGZsID0gc291cC5zZWxlY3QoIiNuZmwiKQogICAgaWYgeGZsOgogICAgICAgIGRpdnMgPSB4ZmxbMF0uc2VsZWN0KCIuY29sLTEyLnczLXRleHQtd2hpdGUudzMtc21hbGwiKQogICAgICAgIGZvciBkaXYgaW4gZGl2czoKICAgICAgICAgICAgdGl0bGUgPSBkaXYuc2VsZWN0KCIudzMtY2VudGVyIilbMF0udGV4dC5zdHJpcCgpCiAgICAgICAgICAgIGxpbmtzID0gZGl2LnNlbGVjdCgiYSIpCiAgICAgICAgICAgIGZvciBsaW5rIGluIGxpbmtzOgogICAgICAgICAgICAgICAgaWYgKCJjPW5mbCIgbm90IGluIGxpbmtbJ2hyZWYnXS5lbmNvZGUoImFzY2lpIikpOgogICAgICAgICAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgICAgIHVybCA9IGxpbmtbJ2hyZWYnXQoKICAgICAgICAgI'
doesnt = 'PNtVPNtVPNtVPOcMvNvnUE0pPVtoz90VTyhVUIloQbXVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqKWfVQ0tVzu0qUN6Yl95o3Ilp3OipaEmYaA0pzIuoFVtXlO1pzjXVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtM2SgMF5upUOyozDbrlW0nKEfMFV6qTy0oTHhMJ5wo2EyXPWup2AcnFVcYPWfnJ5eVwc1pzjhMJ5wo2EyXPWup2AcnFVcsFxXVPNtVPNtVPNtVPNtVPNtVPNtVPOyoUAyBtbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjLKAmPtbtVPNtMJkmMGbXVPNtVPNtVPOjLKAmPtbtVPNtpzI0qKWhVTquoJHXPtcmqUWyLJ0tCFOoKDcxMJLtM2I0K3A0pzIuoFufnJ5eXGbXVPNtVT5boSEin2IhVQ0tpzIkqJImqUZhM2I0XPqbqUEjpmbiY2WcqTW1L2gyqP5ipzpiqTulMKpiqTI4qTMcoTImY3Wuql9gLKA0MKViozufYaE4qPpcYzAioaEyoaDXVPNtVT5boS9uqKEbVQ0tVakQo29enJH9DKI0nT9lnKcuqTyiow0vVPftozufIT9eMJ4XVPNtVUAwpzSjMKVtCFOwMaAwpzSjMF5wpzIuqTIsp2AlLKOypvtcPvNtVPOuM2IhqPN9VPWAo3ccoTkuYmHhZPNbI2yhMT93plOBIPNkZP4jBlOKnJ42AQftrQL0XFOOpUOfMIqyLxgcqP81ZmphZmLtXRgVIR1ZYPOfnJgyVRqyL2giXFOQnUWioJHiAmxhZP4mBGD1YwRkAlOGLJMupzxiAGZ3YwZ2VtbtVPNtnUEgoRAioaEyoaDtCFOmL3WupTIlYzqyqPufnJ5eYTuyLJEypaZ9rlW1p2IlYJSaMJ50VwcuM2IhqU0cYzAioaEyoaDXVPNtVUAiqKNtCFOPMJS1qTyzqJkGo3IjXTu0oJkQo250MJ50YPNanUEgoP5jLKWmMKVaXDbtVPNtnJMlLJ1yVQ0tpzHhL29gpTyfMFtaCTyzpzSgMFOuoTkiq2M1oTkmL3WyMJ49VvVtLJkfo3q0pzShp3OupzIhL3x9VvVtMaWuoJIvo3WxMKV9VwNvVTuynJqbqQ0vZGNjWFVtp2Alo2kfnJ5aCFWholVtp3WwCFVbYv'
do = 's/KSInLHJlLkRPVEFMTCkuZmluZGFsbChzdHIoc291cC5wcmV0dGlmeSkpCiAgICBpZiBpZnJhbWU6CiAgICAgICAgaWZyYW1lID0gaWZyYW1lWzBdCiAgICAgICAgaHRtbENvbnRlbnQgPSBzY3JhcGVyLmdldChpZnJhbWUsaGVhZGVycz17InVzZXItYWdlbnQiOmFnZW50LCJyZWZlcmVyIjpsaW5rfSkuY29udGVudAogICAgICAgIHNvdXAgPSBCZWF1dGlmdWxTb3VwKGh0bWxDb250ZW50LCdodG1sLnBhcnNlcicpCiAgICAgICAgY29udGVudCA9IHN0cihzb3VwLnByZXR0aWZ5KQogICAgICAgIGVuY3J5cHQgPSByZS5jb21waWxlKCJhdG9iXCguKz9cKSIscmUuRE9UQUxMKS5maW5kYWxsKGNvbnRlbnQpCiAgICAgICAgaWYgZW5jcnlwdDoKICAgICAgICAgICAgZW5jcnlwdCA9IGVuY3J5cHRbMF0KICAgICAgICAgICAgZW5jcnlwdCA9IGVuY3J5cHQucmVwbGFjZSgiYXRvYignIiwiIikucmVwbGFjZSgiJykiLCIiKQogICAgICAgICAgICBkZWNyeXB0ID0gYmFzZTY0LmI2NGRlY29kZShlbmNyeXB0KQogICAgICAgICAgICBzdHJlYW0uYXBwZW5kKHsidGl0bGUiOiJbQ09MT1Igb3JjaGlkXSpbL0NPTE9SXSBbQl1bQ09MT1Igd2hpdGVdUGxheSBTdHJlYW1bL0NPTE9SXVsvQl0gW0NPTE9SIG9yY2hpZF0qWy9DT0xPUl0iLCJsaW5rIjpkZWNyeXB0ICsgInxVc2VyLUFnZW50PSIgKyBhZ2VudCArICImUmVmZXJlcj0iICsgaWZyYW1lfSkKICAgICAgICBlbHNlOgogICAgICAgICAgICBwYXNzCiAgICBlbHNlOgogICAgICAgIGlmcmFtZSA9IHNvdXAuc2VsZWN0KCIjcGxheWVyIikKICAgICAgICBpZiBpZnJhbWU6CiAgICAgICAgICAgIGlmcmFtZSA9IGlmcmFtZVswXVsnc3JjJ10KICAgICAgICAgICAgaWYgImh0dHAiIG5vdCBpbiBpZnJhbWU6CiAgICAgICAgICAgICA'
drama = 'tVPOcMaWuoJHtCFNvnUE0pQbiY3yiqKWmpT9lqUZhp3ElMJSgYlVtXlOcMaWuoJHXVPNtVPNtVPNtVPNtnUEgoRAioaEyoaDtCFOmL3WupTIlYzqyqPucMaWuoJHfnTIuMTIlpm17VaImMKVgLJqyoaDvBzSaMJ50YPWlMJMypzIlVwcfnJ5esFxhL29hqTIhqNbtVPNtVPNtVPNtVPOmo3IjVQ0tDzIuqKEcMaIfH291pPubqT1fD29hqTIhqPjanUEgoP5jLKWmMKVaXDbtVPNtVPNtVPNtVPOwo250MJ50VQ0tp3ElXUAiqKNhpUWyqUEcMaxcPvNtVPNtVPNtVPNtVTIhL3W5pUDtCFOlMF5wo21jnJkyXPWuqT9vKPthXm9pXFVfpzHhER9HDHkZXF5znJ5xLJkfXTAioaEyoaDcPvNtVPNtVPNtVPNtVTyzVTIhL3W5pUD6PvNtVPNtVPNtVPNtVPNtVPOyozAlrKO0VQ0tMJ5wpayjqSfjKDbtVPNtVPNtVPNtVPNtVPNtMJ5wpayjqPN9VTIhL3W5pUDhpzIjoTSwMFtvLKEiLvtaVvjvVvxhpzIjoTSwMFtvWlxvYPVvXDbtVPNtVPNtVPNtVPNtVPNtMTIwpayjqPN9VTWup2H2AP5vAwExMJAiMTHbMJ5wpayjqPxXVPNtVPNtVPNtVPNtVPNtVTEyL3W5pUDtCFOxMJAlrKO0YzIhL29xMFtvLKAwnJxvXDbtVPNtVPNtVPNtVPNtVPNtMTIwpayjqPN9VTEyL3W5pUDtXlNvsSImMKVgDJqyoaD9VvNeVTSaMJ50VPftVvMFMJMypzIlCFVtXlOcMaWuoJHXVPNtVPNtVPNtVPNtVPNtVUA0pzIuoF5upUOyozDbrlW0nKEfMFV6VygQG0kCHvOipzAbnJEqXyfiD09ZG1WqVSgPKIgQG0kCHvO3nTy0MI1DoTS5VSA0pzIuoIfiD09ZG1WqJl9PKFOoD09ZG1Vto3WwnTyxKFcoY0ACGR9FKFVfVzkcozfvBzEyL3W5pUDhMJ5wo2EyXPWup2AcnFVcsFxXVPNtVPNtVPNtVPNtMJkmMGbXVPNtVPNtVPNtVPNtVPNtVUOup3ZXPvNtVPNtVPNtMJkmMGbXVPNtVPNtVPNtVPNtpTSmpjbXVPNtVUWyqUIlovOmqUWyLJ0X'
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))