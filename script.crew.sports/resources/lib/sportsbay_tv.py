
import base64, codecs
thecrew = 'aW1wb3J0IHJlcXVlc3RzDQppbXBvcnQgcmUNCmZyb20gYnM0IGltcG9ydCBCZWF1dGlmdWxTb3VwDQpmcm9tIHJlc291cmNlcy5saWIubW9kdWxlcyBpbXBvcnQgY2xpZW50DQppbXBvcnQgeGJtY2d1aQ0KDQphZ2VudCA9ICdNb3ppbGxhLzUuMCAoV2luZG93cyBOVCA2LjE7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS83Ni4wLjM4MDkuMTMyIFNhZmFyaS81MzcuMzYnDQp1X2xpbmsgPSAnaHR0cHM6Ly9zcG9ydHNiYXkub3JnL3Nwb3J0cy90di1jaGFubmVscycNCmdhbWVfbGlzdCA9IFtdDQoNCg0KZGVmIGdldF9nYW1lcygpOg0KICAgIGh0bWwgPSByZXF1ZXN0cy5nZXQodV9saW5rLCBoZWFkZXJzPXsndXNlci1hZ2VudCc6IGFnZW50fSkuY29udGVudA0KICAg'
doesnt = 'VUAiqKNtCFOPMJS1qTyzqJkGo3IjXTu0oJjfVPqbqT1fYaOupaAypvpcQDbtVPNtMKMyoaDtCFOmo3IjYzMcozEsLJkfXPquWlkuqUElpm17W2AfLKAmWmbvqKWfVUA1oJ1upaxvsFxAPvNtVPOzo3VtM2SgMFOcovOyqzIhqQbAPvNtVPNtVPNtqTy0oTHtCFOaLJ1yYaEyrUDhMJ5wo2EyXPqup2AcnFpfW2yaoz9lMFpcQDbtVPNtVPNtVPA4Lz1wM3IcYxEcLJkiMltcYaEyrUE2nJI3MKVbW0Ilpz9lWljtp3ElXUEcqTkyXFxAPvNtVPNtVPNtoTyhnlN9VTquoJIoW2ulMJLaKD0XVPNtVPNtVPOcMvNvnUE0pPVtoz90VTyhVTkcozf6QDbtVPNtVPNtVPNtVPOfnJ5eVQ0tVzu0qUOmBv8ip3OipaEmLzS5Yz9lMlVtXlOfnJ5eQDbtVPNtVPNtVTquoJIsoTymqP5upUOyozDbrlq0nKEfMFp6qTy0oTHfW2kcozfaBzkcozg9XD0XVPNt'
do = 'IHJldHVybiBnYW1lX2xpc3QNCg0KDQoNCnN0cmVhbSA9IFtdDQoNCg0KZGVmIGdldF9zdHJlYW0obGluayk6DQogICAgaHRtbCA9IHJlcXVlc3RzLmdldChsaW5rLCBoZWFkZXJzPXsndXNlci1hZ2VudCc6IGFnZW50fSkuY29udGVudA0KICAgIHNvdXAgPSBCZWF1dGlmdWxTb3VwKGh0bWwsICdodG1sLnBhcnNlcicpDQogICAgZnJhbWUgPSBzb3VwLmZpbmQoJ2lmcmFtZScpDQogICAgaWYgZnJhbWU6DQogICAgICAgIGZyYW1lID0gZnJhbWVbJ3NyYyddDQogICAgICAgIG1hc3RlciA9IHJlcXVlc3RzLmdldChmcmFtZSwgaGVhZGVycz17J3JlZmVyZXInOiBsaW5rfSkuY29udGVudA0KICAgICAgICBzb3VwID0gQmVhdXRpZnVsU291cChtYXN0ZXIsICdodG1sLnBhcnNlcicpDQogICAgICAgIGNsYXBwZXIgPSByZS5jb21w'
drama = 'nJkyXPqQoTSjpUVhHTkurJIlWljtpzHhER9HDHkZXF5znJ5xLJkfXN0XVPNtVPNtVPNtVPNtp3ElXUAiqKNhpUWyqUEcMaxcXD0XVPNtVPNtVPOzo3VtoGA1BPOcovOwoTSjpTIlBt0XVPNtVPNtVPNtVPNtoGA1BPN9VUWyYzAioKOcoTHbVaAiqKWwMGbtWlthXm8cWlVfpzHhER9HDHkZXF5znJ5xLJkfXUA0pvumo3IjYaOlMKE0nJM5XFxAPvNtVPNtVPNtVPNtVT0mqGttCFOgZ3H4JmOqQDbtVPNtVPNtVPNtVPOgZ3H4VQ0toGA1BPNeVPq8IKAypv1OM2IhqQbaVPftLJqyoaDtXlNaWyWyMzIlMKV9WlNeVTMlLJ1yQDbtVPNtVPNtVUA0pzIuoF5upUOyozDbrlq0nKEfMFp6VPqHFRyGWljtW2kcozfaBvOgZ3H4sFxAPvNtVPNtVPNtpTSmpj0XVPNtVTIfp2H6QDbtVPNtVPNtVUOup3ZAPt0XVPNtVUWyqUIlovOmqUWyLJ0APt=='
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))