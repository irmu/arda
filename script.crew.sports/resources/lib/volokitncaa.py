
import base64, codecs
thecrew = 'aW1wb3J0IHJlcXVlc3RzDQpmcm9tIGJzNCBpbXBvcnQgQmVhdXRpZnVsU291cA0KaW1wb3J0IHJlDQpmcm9tIHJlc291cmNlcy5saWIgaW1wb3J0IGNmc2NyYXBlDQoNCmdhbWVfbGlzdCA9IFtdDQoNCmRlZiBnZXRfZ2FtZXMoKToNCiAgICBhZ2VudCA9ICdNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzYuMC4zODA5LjEzMiBTYWZhcmkvNTM3LjM2Jw0KICAgIHNjcmFwZXIgPSBjZnNjcmFwZS5jcmVhdGVfc2NyYXBlcigpDQogICAgaHRtbCA9IHNjcmFwZXIuZ2V0KHIiaHR0cDovL3d3dy52b2xva2l0LmNvbS9hbGwtZ2FtZXMvc2NoZWR1bGUvbmNhYS5waHAiLGhlYWRlcnM9eyd1c2VyLWFnZW50JzphZ2VudH0p'
doesnt = 'YzAioaEyoaDAPvNtVPOmo3IjVQ0tDzIuqKEcMaIfH291pPubqT1fYPqbqT1fYaOupaAypvpcQDbtVPNtLJ5wnT9lVQ0tp291pP5znJ5xK2SfoPtaLFpfLKE0paZ9rlqwoTSmplp6VaIloPObnJExMJ4grUZgMT93ovOmqJ1gLKW5Va0cQDbtVPNtMz9lVTRtnJ4tLJ5wnT9lBt0XVPNtVPNtVPOfnJ5eVQ0tLIfanUWyMvqqQDbtVPNtVPNtVUEcqTkyVQ0toTyhnl5mpTkcqPtaYlpcJl0lKD0XVPNtVPNtVPO0nKEfMFN9VUEcqTkyYaIjpTIlXPxAPvNtVPNtVPNtM2SgMI9fnKA0YzSjpTIhMPu7W3EcqTkyWmc0nKEfMF5yozAiMTHbW2SmL2ycWljanJqho3WyWlxfW2kcozfaBzkcozfhMJ5wo2EyXPqup2AcnFpfW2yaoz9lMFpcsFxAPvNtVPNtVPNtQDbtVPNtpzI0qKWhVTquoJIsoTymqN0XQDcmqUWyLJ0tCFOoKD0XMTIzVTqyqS9m'
do = 'dHJlYW0obGluayk6DQogICAgYWdlbnQgPSAnTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzc2LjAuMzgwOS4xMzIgU2FmYXJpLzUzNy4zNicNCiAgICBzY3JhcGVyID0gY2ZzY3JhcGUuY3JlYXRlX3NjcmFwZXIoKQ0KICAgIGh0bWwgPSBzY3JhcGVyLmdldChsaW5rLGhlYWRlcnM9eyd1c2VyLWFnZW50JzphZ2VudH0pLmNvbnRlbnQNCiAgICBzb3VwID0gQmVhdXRpZnVsU291cChodG1sLCdodG1sLnBhcnNlcicpDQogICAgZnJhbWUgPSBzb3VwLmZpbmQoJ2lmcmFtZScseydpZCc6J3ZvbG9raXQtZmVlZCd9KQ0KICAgIGZyYW1lID0gZnJhbWVbJ3NyYyddDQogICAgZnJhbWUgPSAnaHR0cDovL3d3dy52b2xva2l0'
drama = 'YzAioFptXlOzpzSgMD0XVPNtVT1up3EypvN9VUAwpzSjMKVhM2I0XTMlLJ1yYTuyLJEypaZ9rlq1p2IlYJSaMJ50WmcuM2IhqU0cYzAioaEyoaDAPvNtVPOmo3IjVQ0tDzIuqKEcMaIfH291pPugLKA0MKVfW2u0oJjhpTSlp2IlWlxAPvNtVPOgZ3H4VQ0tpzHhL29gpTyfMFtaqzSlVTEuqTRtCFO7p291pzAyBvVbYvf/XFVaYUWyYxECIRSZGPxhMzyhMTSfoPumqUVbp291pP5jpzI0qTyzrFxcQDbtVPNtoGA1BPN9VT0mqGuoZS0APvNtVPOmqUWyLJ0hLKOjMJ5xXUfvp3ElMJSgVwcgZ3H4sFxAPvNtVPOlMKE1pz4tp3ElMJSgQDbAPt0XQDbAPvAjpzyhqPuaMKEsp3ElMJSgXPWbqUEjBv8iq3q3YaMioT9enKDhL29gY3MioT9mqUWyLJ0iozMfYJquoJImY2AbnJIzpl1dLJq1LKWmYlVcXD0XV3OlnJ50XTqyqS9aLJ1ypltcXD0X'
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))