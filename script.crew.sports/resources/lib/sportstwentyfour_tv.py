
import base64, codecs
thecrew = 'aW1wb3J0IHJlcXVlc3RzDQppbXBvcnQgcmUNCmZyb20gYnM0IGltcG9ydCBCZWF1dGlmdWxTb3VwDQppbXBvcnQgYmFzZTY0DQppbXBvcnQgeGJtY2d1aQ0KDQphZ2VudCA9ICdNb3ppbGxhLzUuMCAoV2luZG93cyBOVCA2LjE7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS83Ni4wLjM4MDkuMTMyIFNhZmFyaS81MzcuMzYnDQp1X2xpbmsgPSAnaHR0cDovL3Nwb3J0czI0LmNsdWIvdHYvJw0KZ2FtZV9saXN0ID0gW10NCg0KZGVmIGdldF9nYW1lcygpOg0KICAgIGh0bWwgPSByZXF1ZXN0cy5nZXQodV9saW5rLCBoZWFkZXJzPXsndXNlci1hZ2VudCc6IGFnZW50fSkuY29udGVudA0KICAgIHNvdXAgPSBCZWF1dGlmdWxTb3VwKGh0bWwsICdodG1sLnBhcnNlcicpDQogICAgZXZl'
doesnt = 'oaDtCFOmo3IjYzMcozEsLJkfXPquWlkuqUElpm17W2AfLKAmWmbvLaEhVTW0ov1iqKEfnJ5yYKOlnJ1upaxtMauvqT4vsFxAPvNtVPOzo3VtM2SgMFOcovOyqzIhqQbAPvNtVPNtVPNtqTy0oTHtCFOaLJ1yYaEyrUDhMJ5wo2EyXPqup2AcnFpfW2yaoz9lMFpcQDbtVPNtVPNtVPA4Lz1wM3IcYxEcLJkiMltcYaEyrUE2nJI3MKVbW0Ilpz9lWljtp3ElXUEcqTkyXFxAPvNtVPNtVPNtoTyhnlN9VTquoJIoW2ulMJLaKD0XVPNtVPNtVPOcMvNvnUE0pPVtoz90VTyhVTkcozf6QDbtVPNtVPNtVPNtVPOfnJ5eVQ0tVzu0qUN6Yl9mpT9lqUZlAP5woUIvY3E2YlVtXlOfnJ5eQDbtVPNtVPNtVTquoJIsoTymqP5upUOyozDbrlq0nKEfMFp6qTy0oTHfW2kcozfaBzkcozg9XD0XVPNtVUWyqUIlovOaLJ1yK2kcp3DAPt0XQDcmqUWyLJ0tCFOoKD0X'
do = 'DQpkZWYgZ2V0X3N0cmVhbShsaW5rKToNCiAgICBodG1sID0gcmVxdWVzdHMuZ2V0KGxpbmssaGVhZGVycz17J3VzZXItYWdlbnQnOmFnZW50fSkuY29udGVudA0KICAgIHNvdXAgPSBCZWF1dGlmdWxTb3VwKGh0bWwsJ2h0bWwucGFyc2VyJykNCiAgICBjb250ZW50ID0gc3RyKHNvdXAucHJldHRpZnkpDQogICAgZW5jcnlwdCA9IHJlLmNvbXBpbGUoImF0b2JcKC4rP1wpIixyZS5ET1RBTEwpLmZpbmRhbGwoY29udGVudCkNCiAgICBpZiBlbmNyeXB0Og0KICAgICAgICBlbmNyeXB0ID0gZW5jcnlwdFswXQ0KICAgICAgICBlbmNyeXB0ID0gZW5jcnlwdC5yZXBsYWNlKCJhdG9iKCIsIiIpLnJlcGxhY2UoIicpIiwiIikNCiAgICAgICAgZGVjcnlwdCA9IGJhc2U2NC5iNjRkZWNvZGUoZW5jcnlwdCkNCiAgICAgICAgI3hibWNndWkuRGlh'
drama = 'oT9aXPxhqTI4qUMcMKqypvtaEKWlo3VaYPOmqUVbMTIwpayjqPxcQDbtVPNtVPNtVTyzVPWbqUEjVvOho3DtnJ4tMTIwpayjqQbAPvNtVPNtVPNtVPNtVTEyL3W5pUDtCFNvnUE0pQbvVPftMTIwpayjqN0XVPNtVPNtVPNtVPNtV3uvoJAaqJxhETyuoT9aXPxhqTI4qUMcMKqypvtaEKWlo3VaYPOmqUVbMTIwpayjqPxcQDbtVPNtVPNtVUA0pzIuoF5upUOyozDbrlq0nKEfMFp6VPqoD09ZG1Vto3WwnTyxKFcoY0ACGR9FKFOoDy1oD09ZG1Vtq2ucqTIqHTkurFOGqUWyLJ1oY0ACGR9FKIfiDy0tJ0ACGR9FVT9lL2ucMS0dJl9QG0kCHy0aYPqmqUWyLJ0aBvOxMJAlrKO0VPftVakIp2IlYHSaMJ50CFVtXlOuM2IhqPNeVPVzHzIzMKWypw0vVPftoTyhn30cQDbtVPNtMJkmMGbAPvNtVPNtVPNtpTSmpj0XQDbtVPNtpzI0qKWhVUA0pzIuoD=='
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))