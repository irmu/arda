
import base64, codecs
thecrew = 'aW1wb3J0IHJlcXVlc3RzCmZyb20gYnM0IGltcG9ydCBCZWF1dGlmdWxTb3VwCmltcG9ydCByZQppbXBvcnQgYmFzZTY0CmZyb20gcmVzb3VyY2VzLmxpYiBpbXBvcnQgY2ZzY3JhcGUKCmdhbWUgPSBbXQoKZGVmIGdldF9nYW1lcygpOgogICAgc2NyYXBlciA9IGNmc2NyYXBlLmNyZWF0ZV9zY3JhcGVyKCkKICAgIHVybCA9ICJodHRwOi8veW91cnNwb3J0cy5zdHJlYW0vIgogICAgYWdlbnQgPSAiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzc5LjAuMzk0NS4xMTcgU2FmYXJpLzUzNy4zNiIKICAgIGh0bWxDb250ZW50ID0gc2NyYXBlci5nZXQodXJsLGhlYWRlcnM9eyJ1c2VyLWFnZW50IjphZ2VudH0pLmNvbnRlbnQKICAgIHNvdXAgPSBCZWF1dGlmdWxTb3VwKGh0bWxDb250ZW50LCAnaHRtbC5wYXJzZXInKQogICAgbmJhID0gc291cC5zZWxlY3QoIiNuYmEiKQogICAgaWYgbmJhOgogICAgICAgIGRpdnMgPSBuYmFbMF0uc2VsZWN0KCIuY29sLTEyLnczLXRleHQtd2hpdGUudzMtc21hbGwiKQogICAgICAgIGZvciBkaXYgaW4gZGl2czoKICAgICAgICAgICAgdGl0bGUgPSBkaXYuc2VsZWN0KCIudzMtY2VudGVyIilbMF0udGV4dC5zdHJpcCgpCiAgICAgICAgICAgIGxpbmtzID0gZGl2LnNlbGVjdCgiYSIpCiAgICAgICAgICAgIGZvciBsaW5rIGluIGxpbmtzOgogICAgICAgICAgICAgICAgaWYgKCJ2PW5iYSIgbm90IGluIGxpbmtbJ2hyZWYnXS5lbmNvZGUoImFzY2lpIikpIGFuZCAoImxpdmUiIG5vdCBpbiBsaW5rWydocmVmJ10uZW5jb2RlKCJhc2NpaSIpKToKICAgICAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgICAgIC'
doesnt = 'O1pzjtCFOfnJ5eJlqbpzIzW10XPvNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtVzu0qUNvVT5iqPOcovO1pzj6PvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUIloPN9VPWbqUEjBv8irJ91paAjo3W0pl5mqUWyLJ0vVPftqKWfPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTquoJHhLKOjMJ5xXUfvqTy0oTHvBaEcqTkyYzIhL29xMFtvLKAwnJxvXFjvoTyhnlV6qKWfYzIhL29xMFtvLKAwnJxvXK0cPvNtVPNtVPNtVPNtVPNtVPNtVPNtMJkmMGbXVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpTSmpjbXVPNtVTIfp2H6PvNtVPNtVPNtpTSmpjbXVPNtVUWyqUIlovOaLJ1yPtbXPaA0pzIuoFN9VSgqPzEyMvOaMKEsp3ElMJSgXTkcozfcBtbtVPNtozufIT9eMJ4tCFOlMKS1MKA0pl5aMKDbW2u0qUOmBv8iLzy0LaIwn2I0Yz9lMl90nUWyql90MKu0MzyfMKZipzS3Y21up3Eypv9hnTjhqUu0WlxhL29hqTIhqNbtVPNtozufK2S1qTttCFNvsRAio2gcMG1OqKEbo3WcrzS0nJ9hCFVtXlOhnTkHo2gyotbtVPNtp2AlLKOypvN9VTAzp2AlLKOyYzAlMJS0MI9mL3WupTIlXPxXVPNtVTSaMJ50VQ0tVx1irzyfoTRiAF4jVPuKnJ5xo3qmVR5HVQRjYwN7VSqcowL0BlO4AwDcVRSjpTkyI2IvF2y0YmHmAl4mAvNbF0uHGHjfVTkcn2HtE2Iwn28cVRAbpz9gMF83BF4jYwZ5AQHhZGR3VSAuMzSlnF81ZmphZmLvPvNtVPObqT1fD29hqTIhqPN9VUAwpzSjMKVhM2I0XTkcozffnTIuMTIlpm17VaImMKVgLJqyoaDvBzSaMJ50sFxhL29hqTIhqNbtVPNtp291pPN9VRWyLKI0nJM1oSAiqKNbnUEgoRAioaEyoaDfVPqbqT1fYaOupaAypvpcPvNtVPOcMaWuoJHtCFOlMF5wo21jnJkyXPp8nJMlLJ1yVTSfoT93MaIfoUAwpzIyow0vVvOuoTkiq3ElLJ5mpTSlMJ5wrG0vVvOzpzSgMJWipzEypw0vZPVtnTIcM2u0CFVkZQNyVvOmL3WioTkcozp9'
do = 'Im5vIiBzcmM9IiguKz8pIicscmUuRE9UQUxMKS5maW5kYWxsKHN0cihzb3VwLnByZXR0aWZ5KSkKICAgIGlmIGlmcmFtZToKICAgICAgICBpZnJhbWUgPSBpZnJhbWVbMF0KICAgICAgICBodG1sQ29udGVudCA9IHNjcmFwZXIuZ2V0KGlmcmFtZSxoZWFkZXJzPXsidXNlci1hZ2VudCI6YWdlbnQsInJlZmVyZXIiOmxpbmt9KS5jb250ZW50CiAgICAgICAgc291cCA9IEJlYXV0aWZ1bFNvdXAoaHRtbENvbnRlbnQsJ2h0bWwucGFyc2VyJykKICAgICAgICBjb250ZW50ID0gc3RyKHNvdXAucHJldHRpZnkpCiAgICAgICAgZW5jcnlwdCA9IHJlLmNvbXBpbGUoImF0b2JcKC4rP1wpIixyZS5ET1RBTEwpLmZpbmRhbGwoY29udGVudCkKICAgICAgICBpZiBlbmNyeXB0OgogICAgICAgICAgICBlbmNyeXB0ID0gZW5jcnlwdFswXQogICAgICAgICAgICBlbmNyeXB0ID0gZW5jcnlwdC5yZXBsYWNlKCJhdG9iKCciLCIiKS5yZXBsYWNlKCInKSIsIiIpCiAgICAgICAgICAgIGRlY3J5cHQgPSBiYXNlNjQuYjY0ZGVjb2RlKGVuY3J5cHQpCiAgICAgICAgICAgIHN0cmVhbS5hcHBlbmQoeyJ0aXRsZSI6IltDT0xPUiBvcmNoaWRdKlsvQ09MT1JdIFtCXVtDT0xPUiB3aGl0ZV1QbGF5IFN0cmVhbVsvQ09MT1JdWy9CXSBbQ09MT1Igb3JjaGlkXSpbL0NPTE9SXSIsImxpbmsiOmRlY3J5cHQgKyAifFVzZXItQWdlbnQ9IiArIGFnZW50ICsgIiZSZWZlcmVyPSIgKyBpZnJhbWV9KQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIHBhc3MKICAgIGVsc2U6CiAgICAgICAgaWZyYW1lID0gc291cC5zZWxlY3QoIiNwbGF5ZXIiKQogICAgICAgIGlmIGlmcmFtZToKICAgICAgICAgICAgaWZyYW1lID0gaWZyYW1lWzBdWydzcmMnXQogICAgICAgICAgICBpZiAiaHR0cCIgbm90IGluIGlmcmFtZToKICAgICAgICAgICAgICAgIGlmcm'
drama = 'SgMFN9VPWbqUEjBv8irJ91paAjo3W0pl5mqUWyLJ0iVvNeVTyzpzSgMDbtVPNtVPNtVPNtVPObqT1fD29hqTIhqPN9VUAwpzSjMKVhM2I0XTyzpzSgMFkbMJSxMKWmCKfvqKAypv1uM2IhqPV6LJqyoaDfVaWyMzIlMKVvBzkcozg9XF5wo250MJ50PvNtVPNtVPNtVPNtVUAiqKNtCFOPMJS1qTyzqJkGo3IjXTu0oJkQo250MJ50YPqbqT1fYaOupaAypvpcPvNtVPNtVPNtVPNtVTAioaEyoaDtCFOmqUVbp291pP5jpzI0qTyzrFxXVPNtVPNtVPNtVPNtMJ5wpayjqPN9VUWyYzAioKOcoTHbVzS0o2WpXP4eC1jcVvklMF5RG1EOGRjcYzMcozEuoTjbL29hqTIhqPxXVPNtVPNtVPNtVPNtnJLtMJ5wpayjqQbXVPNtVPNtVPNtVPNtVPNtVTIhL3W5pUDtCFOyozAlrKO0JmOqPvNtVPNtVPNtVPNtVPNtVPOyozAlrKO0VQ0tMJ5wpayjqP5lMKOfLJAyXPWuqT9vXPpvYPVvXF5lMKOfLJAyXPVaXFVfVvVcPvNtVPNtVPNtVPNtVPNtVPOxMJAlrKO0VQ0tLzSmMGL0YzV2ATEyL29xMFuyozAlrKO0XDbtVPNtVPNtVPNtVPNtVPNtMTIwpayjqPN9VTEyL3W5pUDhMJ5wo2EyXPWup2AcnFVcPvNtVPNtVPNtVPNtVPNtVPOxMJAlrKO0VQ0tMTIwpayjqPNeVPW8IKAypv1OM2IhqQ0vVPftLJqyoaDtXlNvWyWyMzIlMKV9VvNeVTyzpzSgMDbtVPNtVPNtVPNtVPNtVPNtp3ElMJSgYzSjpTIhMPu7VaEcqTkyVwbvJ0ACGR9FVT9lL2ucMS0dJl9QG0kCHy0tJ0WqJ0ACGR9FVUqbnKEyKIOfLKxtH3ElMJSgJl9QG0kCHy1oY0WqVSgQG0kCHvOipzAbnJEqXyfiD09ZG1WqVvjvoTyhnlV6MTIwpayjqP5yozAiMTHbVzSmL2ycVvy9XDbtVPNtVPNtVPNtVPOyoUAyBtbtVPNtVPNtVPNtVPNtVPNtpTSmpjbtVPNtVPNtVPNtVPNtVPNtPvNtVPNtVPNtMJkmMGbXVPNtVPNtVPNtVPNtpTSmpjbtVPNtVPNtVNbXVPNtVUWyqUIlovOmqUWyLJ0X'
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))