
import base64, codecs
thecrew = 'aW1wb3J0IHJlcXVlc3RzDQpmcm9tIGJzNCBpbXBvcnQgQmVhdXRpZnVsU291cA0KaW1wb3J0IHJlDQppbXBvcnQgYmFzZTY0DQojOTc4NjYNCmdhbWVzID0gW10NCg0KZGVmIGdldF9nYW1lcygpOg0KICAgIHVybCA9ICJodHRwOi8vd3d3LjcyMHBzdHJlYW0ubWUvbmNhYW0tc3RyZWFtIg0KICAgIGFnZW50ID0gIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS83OS4wLjM5NDUuMTE3IFNhZmFyaS81MzcuMzYiDQogICAgaHRtbENvbnRlbnQgPSByZXF1ZXN0cy5nZXQodXJsLGhlYWRlcnM9eyJ1c2VyLWFnZW50IjphZ2VudH0pLmNvbnRlbnQNCiAgICBzb3VwID0gQmVhdXRpZnVsU291cChodG1sQ29udGVudCwiaHRtbC5wYXJzZXIiKQ0KICAgIGdhbWVMaXN0ID0gc291cC5zZWxlY3QoIi5jYXJkLmNhcmQtYm9keS5ib3JkZXItc2Vjb25kYXJ5Lm1iLTMiKQ0KICAgIGlmIGdhbWVMaXN0Og0KICAgICAgICBmb3IgZ2FtZSBpbiBnYW1lTGlzdDoNCiAgICAgICAgICAgIHRpdGxlID0gZ2FtZS5hWyd0aXRsZSddLmVuY29kZSgiYXNjaWkiKQ0KICAgICAgICAgICAgbGluayA9ICJodHRwOi8vd3d3LjcyMHBzdHJlYW0ubWUiICsgZ2FtZS5hWydocmVmJ10NCiAgICAgICAgICAgIGdhbWVzLmFwcGVuZCh7InRpdGxlIjp0aXRsZSwibGluayI6bGluay5lbmNvZGUoImFzY2lpIil9KQ0KICAgIGVsc2U6DQogICAgICAgIHBhc3MNCg0KICAgIHJldHVybiBnYW1lcw0KDQoNCg0Kc3RyZWFtID0gW10NCmRlZiBnZXRfc3RyZWFtKGxpbmspOg0KICAgIHRhcmdldCA9IE5vbmUNCiAgICBhZ'
doesnt = '2IhqPN9VPWAo3ccoTkuYmHhZPNbI2yhMT93plOBIPNkZP4jBlOKnJ42AQftrQL0BlOlqwb3Zv4jXFOUMJAeol8lZQRjZQRjZFOTnKWyMz94YmplYwNvQDbtVPNtnUEgoRAioaEyoaDtCFOlMKS1MKA0pl5aMKDboTyhnlkbMJSxMKWmCKfvqKAypv1uM2IhqPV6LJqyoaE9XF5wo250MJ50QDbtVPNtp291pPN9VRWyLKI0nJM1oSAiqKNbnUEgoRAioaEyoaDfW2u0oJjhpTSlp2IlWlxAPvNtVPOcMaWuoJHtCFOmo3IjYaAyoTIwqPtaYzIgLzIxYKWyp3OioaAcqzHgnKEyoFpcQDbtVPNtnJLtnJMlLJ1yBt0XVPNtVPNtVPOcMaWuoJHtCFOcMaWuoJIoZS1oW3AlLlqqQDbtVPNtVPNtVT9lnJqcovN9VTyzpzSgMF5mpTkcqPtvYlVcJl0kKD0XVPNtVPNtVPOipzyanJ4tCFOcMaWuoJHhpzIjoTSwMFuipzyanJ4fVvVcQDbtVPNtVPNtVN0XVPNtVPNtVPObqT1fD29hqTIhqPN9VUWypKIyp3EmYzqyqPucMaWuoJHfnTIuMTIlpm17VaWyMzIlMKVvBzkcozffVaImMKVgLJqyoaDvBzSaMJ50sFxhL29hqTIhqN0XVPNtVPNtVPOmo3IjVQ0tDzIuqKEcMaIfH291pPubqT1fD29hqTIhqPjanUEgoP5jLKWmMKVaXD0XVPNtVPNtVPNwpUWcoaDbp291pP5jpzI0qTyzrFxAPvNtVPNtVPNtpTEyqUE4qPN9VUWyYzAioKOcoTHbWmkmL3WcpUD+pTEyqUE4qPN9VPVbYvf/XFVaYUWyYxECIRSZGPxhMzyhMTSfoPumqUVbp291pP5jpzI0qTyzrFxcQDbtVPNtVPNtVUcgnJDtCFOlMF5wo21jnJkyXPp8p2AlnKO0CacgnJDtCFNvXP4eClxvWlklMF5RG1EOGRjcYzMcozEuoTjbp3ElXUAiqKNhpUWyqUEcMaxcXD0XVPNtVPNtVPOjnJDtCFOlMF5wo21jnJkyXPqjnJDtCFNbYvf/XGfaYUWyYxECIRSZGPxhMzyhMT'
do = 'FsbChzdHIoc291cC5wcmV0dGlmeSkpDQogICAgICAgIGVkbSA9IHJlLmNvbXBpbGUoJ2VkbSA9ICIoLis/KSInLHJlLkRPVEFMTCkuZmluZGFsbChzdHIoc291cC5wcmV0dGlmeSkpDQogICAgICAgIHNjcmlwdHMgPSBzb3VwLmZpbmRfYWxsKCJzY3JpcHQiLGF0dHJzPXsiYXN5bmMiOiIifSkNCiAgICAgICAgcmVmZXJlciA9ICJodHRwczovLyIgKyBlZG1bMF0gKyAiLyIgDQogICAgICAgIHVybCA9ICJodHRwczovLyIgKyBlZG1bMF0gKyAiL3NkZW1iZWQ/dj0iICsgem1pZFswXQ0KICAgICAgICAjcHJpbnQodXJsKQ0KICAgICAgICAjcHJpbnQob3JpZ2luKQ0KICAgICAgICBodG1sQ29udGVudCA9IHJlcXVlc3RzLnBvc3QodXJsLCBkYXRhPXsicGlkIjpwaWRbMF0sInB0eHQiOnBkZXR0eHR9LGhlYWRlcnM9eyJvcmlnaW4iOm9yaWdpbiwicmVmZXJlciI6aWZyYW1lLCJ1c2VyLWFnZW50IjphZ2VudH0pLmNvbnRlbnQNCiAgICAgICAgc291cCA9IEJlYXV0aWZ1bFNvdXAoaHRtbENvbnRlbnQsJ2h0bWwucGFyc2VyJykNCiAgICAgICAgI3ByaW50KHNvdXAucHJldHRpZnkpDQogICAgICAgIGVuY3J5cHQgPSByZS5jb21waWxlKCJjb25zdCBzb3VyZVVybCA9IFwnKC4rPyknIixyZS5ET1RBTEwpLmZpbmRhbGwoc3RyKHNvdXAucHJldHRpZnkpKQ0KICAgICAgICBpZiBlbmNyeXB0Og0KICAgICAgICAgICAgZGVjcnlwdCA9IGJhc2U2NC5iNjRkZWNvZGUoZW5jcnlwdFswXSkNCiAgICAgICAgICAgIGRlY3J5cHQgPSBkZWNyeXB0KyJ8cmVmZXJlcj0iK3JlZmVyZXINCiAgICAgICAgICAgIGRlY3J5cHQgPSBkZWNyeXB0LnJlcGxhY2UoInBsYXlsaXN0IiwiY2h1bmtsaXN0IikNCiA'
drama = 'tVPNtVPNtVPNtVUA0pzIuoF5upUOyozDbrlW0nKEfMFV6VaA0pzIuoFVfVzkcozfvBzEyL3W5pUE9XD0XVPNtVPNtVPNtVPNtpUWcoaDbMTIwpayjqPxAPvNtVPNtVPNtVPNtVPAjpzyhqPtvJJSbo29iVFOTo3IhMPOcqPVcQDbtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPOjLKAmQDbAPvNtVPNtVPNtWlpaQDbtVPNtVPNtVTyzVUAwpzyjqUZ6QDbtVPNtVPNtVPNtVPOzo3Vtp2AlnKO0VTyhVUAwpzyjqUZ6QDbtVPNtVPNtVPNtVPNtVPNtqUW5Bt0XVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvNvMJ1vMJDvVTyhVUAwpzyjqSfap3WwW106QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO0LKWaMKDtCFOmL3WcpUEoW3AlLlqqQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjpzyhqPu0LKWaMKDcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOwo250nJ51MD0XVPNtVPNtVPNtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtL29hqTyhqJHAPvNtVPNtVPNtMJkmMGbAPvNtVPNtVPNtVPNtVUOup3ZAPt0XVPNtVPNtVPOcMvO0LKWaMKD6QDbtVPNtVPNtVPNtVPObqT1fD29hqTIhqPN9VUWypKIyp3EmYzqyqPu0LKWaMKDcYzAioaEyoaDAPvNtVPNtVPNtVPNtVN0XVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtpTSmpj0XVPNtVPNtVPNaWlptVPNtVPNtVN0XVPNtVTIfp2H6QDbtVPNtVPNtVUOup3ZAPt0XVPNtVUWyqUIlovOmqUWyLJ0APvNtVPNtVPNtQDbAPvAjpzyhqPuaMKEsp3ElMJSgXPWbqUEjBv8iq3q3YwplZUOmqUWyLJ0hoJHiozMfYJ5yqUqipzfgoTy2MF1mqUWyLJ0iVvxcQDbwpUWcoaDbM2I0K2quoJImXPxcQDb='
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))