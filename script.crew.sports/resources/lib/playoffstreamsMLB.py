
import base64, codecs
thecrew = 'ZnJvbSBiczQgaW1wb3J0IEJlYXV0aWZ1bFNvdXANCmltcG9ydCByZXF1ZXN0cw0KaW1wb3J0IHJlDQppbXBvcnQgb3MNCicnJw0KaW1wb3J0IHhibWMNCmltcG9ydCBzeXMNCg0KY2hrViA9ICh4Ym1jLmdldEluZm9MYWJlbCgnU3lzdGVtLkJ1aWxkVmVyc2lvbicpKSANCg0KaWYgY2hrVi5zdGFydHN3aXRoKCcxNycpOg0KICAgIG15UGF0aCA9IHN5cy5wYXRoWzBdICsgJy9yZXNvdXJjZXMveG1sJyANCmVsc2U6DQogICAgbXlQYXRoID0gb3MucGF0aC5kaXJuYW1lKF9fZmlsZV9fKS5yZXBsYWNlKCdsaWInLCd4bWwnKQ0KDQonJycNCiNUaGlzIG1ldGhvZCB3aWxsIHNjcmFwZSB0aGUgR2FtZXNMaXN0DQpwbGF5T2ZmU3RyZWFtTUxCUGxheUxpc3QgPSBbXQ0KZ2FtZUxpc3QgPVtdDQpkZWYgZ2V0TUxCTGlzdCgpOg0KICAgIHVybCA9IHIiaHR0cDovL3BsYXlvZmZzc3RyZWFtLmxpdmUvcmVkZGl0LW1sYi1zdHJlYW1zIg0KICAgIGh0dHBfcmVxdWVzdCA9IHJlcXVlc3RzLmdldCh1cmwpDQogICAgaHR0cF9yZXNwb25zZSA9IGh0dHBfcmVxdWVzdC5jb250ZW50DQogICAgc291cCA9IEJlYXV0aWZ1bFNvdXAoaHR0cF9yZXNwb25zZSwgJ2h0bWwucGFyc2VyJykNCiAgICBtbGJfbGlzdCA9IHNvdXAuZmluZF9hbGwoJ2EnLGF0dHJzPXsnY2xhc3MnOididG4gYnRuLWluZm8gYnRuLWJsb2NrJ30pDQogICAgZm9yIGdhbWUgaW4gbWxiX2xpc3Q6DQogICAgICAgICNwcmludChnYW1lWyd0aXRsZSddKQ0KICAgICAgICB0cnk6DQogICAgICAgICAgICB0aXRsZSA9IGdhbWVbJ3RpdGxlJ10NCiAgICAgICAgICAgIHRpbWUgPSBnYW1lLmZpbmRDaGlsZCgpLnRleHQNCiAgICAgICAgICAgICNwcmludChnYW1lLmZpbmRDaGlsZCgpLnRleHQpDQogICAgICAgIGV4Y2VwdDoNCiAgICAgICAgICAgIHRpbWUgPSAnJw0KICAgICAgICAgICAgcHJpbnQoJycpDQogICAgICAgIGdhbWVMaXN0LmFwcGVuZCh7J3RpdGxlJzogdGl0bGUuZW5jb2RlKCdhc2NpaScsJ2lnbm9yZScpLCAndGltZSc6dGltZX0pDQogICA'
doesnt = 'tpzI0qKWhVTquoJIZnKA0VPNtVN0XVPNtVPNtVPNAPvAHnTymVT1yqTuiMPOiozk5VTAbMJAeVTMipvO0nTHtp3ElMJSgVTyzVUImMKVtL2kcL2fto24tqTuuqPOmpTIwnJMcLlOhLJ1yQDcxMJLtM2I0H3ElMJSgXT5uoJHcBt0XVPNtVUIloPN9VUVvnUE0pQbiY3OfLKyiMzMmp3ElMJSgYzkcqzHipzIxMTy0YJ1fLv1mqUWyLJ1mVt0XVPNtVTu0qUOspzIkqJImqPN9VUWypKIyp3EmYzqyqPu1pzjcQDbtVPNtnUE0pS9lMKAjo25mMFN9VTu0qUOspzIkqJImqP5wo250MJ50QDbtVPNtp291pPN9VRWyLKI0nJM1oSAiqKNbnUE0pS9lMKAjo25mMFjtW2u0oJjhpTSlp2IlWlxAPvNtVPOgoTWsoTymqPN9VUAiqKNhMzyhMS9uoTjbW2RaYTS0qUWmCKfaL2kup3ZaBvqvqT4tLaEhYJyhMz8tLaEhYJWfo2AeW30cQDbtVPNtMz9lVTquoJHtnJ4toJkvK2kcp3D6QDbtVPNtVPNtVPAjpzyhqPuaLJ1yJlq0nKEfMFqqXD0XVPNtVPNtVPO0nKEfMFN9VTquoJIoW3EcqTkyW10APvNtVPNtVPNtqTy0oTHtCFO0nKEfMF5yozAiMTHbW2SmL2ycWljanJqho3WyWlxAPvNtVPNtVPNtnJLtozSgMFOcovOmqUVbqTy0oTHcBt0XVPNtVPNtVPNtVPNtV3OlnJ50XPqcoaAcMTHtnJLaXD0XVPNtVPNtVPNtVPNtoTyhnlN9VPWbqUEjBv8iq3q3YaOfLKyiMzMmqUWyLJ0hL29gVvNeVTquoJIoW2ulMJLaKD0XVPNtVPNtVPNtVPNtqT9eMJ4tCFOlMKS1MKA0pl5aMKDbVzu0qUN6Yl8kAmVhZGN1YwV2YwVjZF9goTWmYaE4qPVcYzAioaEyoaDAPvNtVPNtVPNtVPNtVTS1qTttCFNvsRAio2gcMG1OqKEbo3WcrzS0nJ9hCFVtXlO0o2gyot0XVPNtVPNtVPNtVPNtp3ElMJSgHzIkqJImqPN9VUWypKIyp3EmYzqyqPufnJ5eXF5wo250MJ50QDbtVPNtVPNtVPNtVPNwpUWcoaDbp3ElMJSgHzIkqJImqPxAPvNtVPNtVPNtVPNtVUAiqKNtCFOPMJS1qTyzqJkGo3IjXUA0pzIuoIWypKIyp3DfVPqbqT1fYaOupaAypvpcQDbtVPNtVPNtVPNtVPOgZ3H4K1IFFFN9VUWyYzAioKOcoTHbW1kmCIkmVvthXm8cVwfaYPOlMF5RG1EOGRjcYzMcoz'
do = 'RhbGwoc3RyKHNvdXAucHJldHRpZnkpKQ0KICAgICAgICAgICAgI3ByaW50KG0zdThfVVJJKQ0KICAgICAgICAgICAgDQogICAgICAgICAgICBpZiBsZW4obTN1OF9VUkkpID4gMToNCiAgICAgICAgICAgICAgICBtM3U4X25hbWUgPSBzdHIobTN1OF9VUklbMV0pLnNwbGl0KCcvJylbLTFdDQogICAgICAgICAgICAgICAgI3ByaW50KG0zdThfbmFtZSkNCiAgICAgICAgICAgICAgICBiaXRSYXRlTGluayA9IHN0cihtM3U4X1VSSVsxXSkucmVwbGFjZShtM3U4X25hbWUsJycpLnN0cmlwKCkNCiAgICAgICAgICAgICAgICAjcHJpbnQoYml0UmF0ZUxpbmspDQogICAgICAgICAgICAgICAgVVJJX3Jlc3BvbnNlID0gcmVxdWVzdHMuZ2V0KG0zdThfVVJJWzFdKQ0KICAgICAgICAgICAgICAgIGJpdHJhdGVzID0gcmUuY29tcGlsZSgiXFxuW14jXS4qP1wubTN1OFxcbiIpLmZpbmRhbGwoVVJJX3Jlc3BvbnNlLnRleHQpDQogICAgICAgICAgICAgICAgI3ByaW50KGJpdHJhdGVzKQ0KICAgICAgICAgICAgICAgICNyZXR1cm4NCiAgICAgICAgICAgICAgICBmb3IgYml0cmF0ZSBpbiBiaXRyYXRlczoNCiAgICAgICAgICAgICAgICAgICAgYml0UmF0ZSA9IGludChiaXRyYXRlLnNwbGl0KCcvJylbLTJdLnJlcGxhY2UoJ0snLCcnKS5yZXBsYWNlKCdrJywnJykpDQogICAgICAgICAgICAgICAgICAgICNwcmludChiaXRSYXRlKQ0KICAgICAgICAgICAgICAgICAgICBpZiBiaXRSYXRlID49IDE4MDA6DQogICAgICAgICAgICAgICAgICAgICAgICBiaXRyYXRlID0gYml0cmF0ZS5yZXBsYWNlKCdjb21wbGV0ZScsJ3NsaWRlJykNCiAgICAgICAgICAgICAgICAgICAgICAgIHBsYXlPZmZTdHJlYW1NTEJQbGF5TGlzdC5hcHBlbmQoeyd0aXRsZSc6dGl0bGUsICdzdHJlYW0nOmJpdFJhdGVMaW5rICsgYml0cmF0ZS5zdHJpcCgiXG4iKSArIGF1dGgsICdxdWFsaXR5JzpiaXRSYXRlfSkNCg0KICAgICAgICAgICAgZWxpZiBsZW4obTN1OF9VUkkpID09IDE6DQogICAgICAgICAgICAgICAgbTN1OF9uYW1lID0gc3RyK'
drama = 'T0mqGusIIWWJmOqXF5mpTkcqPtaYlpcJl0kKD0XVPNtVPNtVPNtVPNtVPNtVPAjpzyhqPugZ3H4K25uoJHcQDbtVPNtVPNtVPNtVPNtVPNtLzy0HzS0MHkcozftCFOmqUVboGA1BS9IHxyoZS0cYaWypTkuL2HboGA1BS9hLJ1yYPpaXF5mqUWcpPtcQDbtVPNtVPNtVPNtVPNtVPNtV3OlnJ50XTWcqSWuqTIZnJ5eXD0XVPNtVPNtVPNtVPNtVPNtVSIFFI9lMKAjo25mMFN9VUWypKIyp3EmYzqyqPugZ3H4K1IFFIfjKFxAPvNtVPNtVPNtVPNtVPNtVPOvnKElLKEyplN9VUWyYzAioKOcoTHbVykpoygrV10hXw9pYz0mqGupKT4vXF5znJ5xLJkfXSIFFI9lMKAjo25mMF50MKu0XD0XVPNtVPNtVPNtVPNtVPNtVPAjpzyhqPuvnKElLKEyplxAPvNtVPNtVPNtVPNtVPNtVPNwpzI0qKWhQDbtVPNtVPNtVPNtVPNtVPNtMz9lVTWcqUWuqTHtnJ4tLzy0pzS0MKZ6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVTWcqSWuqTHtCFOcoaDbLzy0pzS0MF5mpTkcqPtaYlpcJl0lKF5lMKOfLJAyXPqYWljaWlxhpzIjoTSwMFtanlpfWlpcXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNwpUWcoaDbLzy0HzS0MFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtLzy0HzS0MFN+CFNkBQNjBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtLzy0pzS0MFN9VTWcqUWuqTHhpzIjoTSwMFtaL29gpTkyqTHaYPqmoTyxMFpcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjoTS5G2MzH3ElMJSgGHkPHTkurHkcp3DhLKOjMJ5xXUfaqTy0oTHaBaEcqTkyYPNap3ElMJSgWmcvnKEFLKEyGTyhnlNeVTWcqUWuqTHhp3ElnKNbVykhVvxtXlOuqKEbYPNapKIuoTy0rFp6Lzy0HzS0MK0cQDbAPvNtVPNtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPAjpzyhqPuvnKElLKEyXD0XVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtL29hqTyhqJHAPvNtVPNtVPNtpzI0qKWhVUOfLKyCMzMGqUWyLJ1AGRWDoTS5GTymqN0XV3OlnJ50XTqyqR1ZDxkcp3DbXFxAPvAjpzyhqPuaMKEGqUWyLJ0bVx1ZDvOBMKE3o3WeVRkcqzHtH3ElMJSgVvxcQDb='
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))