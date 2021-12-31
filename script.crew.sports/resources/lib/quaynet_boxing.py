
import base64, codecs
thecrew = 'DQppbXBvcnQgYmFzZTY0LCBjb2RlY3MNCnRoZWNyZXcgPSAnRFFwcGJYQnZjblFnWW1GelpUWTBMQ0JqYjJSbFkzTU5DblJvWldOeVpYY2dQU0FuWVZjeGQySXpTakJKU0Vwc1kxaFdiR016VW5wRVVYQndZbGhDZG1OdVVXZGpiVlZPUTIxYWVXSXlNR2RaYmswd1NVZHNkR05IT1hsa1EwSkRXbGRHTVdSSGJHMWtWM2hVWWpOV2QwUlJjSEJpV0VKMlkyNVJaMWx0Um5wYVZGa3dSRkZ2VGtOdFJtNWFWelV3U1VRd1owb3dNWFpsYld4ellrZEZkazVUTkhkSlEyaFlZVmMxYTJJelpIcEpSVFZWU1VSWmRVMVVjMmRXTW14MVRtcFJOMGxJWnpKT1EydG5VVmhDZDJKSFZsaGFWMHBNWVZoUmRrNVVUVE5NYWsweVNVTm9URk5HVWs1VVEzZG5Za2RzY2xwVFFraGFWMDV5WW5scloxRXlhSGxpTWpGc1RIcGpNa3hxUVhWTmVtZDNUMU0wZUUxNlNXZFZNa1p0V1ZoS2NFeDZWWHBPZVRSNlRtbGpUa051Vm1aaVIyeDFZWGxCT1VsRFpHOWtTRkozVDJrNGRtTllWbWhsVnpWc1pFTTFNV041T1dwWldGSnNXakk1ZVdWVE9XbGlNMmh3WW0xamRHTXpVbmxhVjBaMFkzazRia1JSY0c1WlZ6RnNXREo0Y0dNelVXZFFVMEppV0ZFd1MwUlJiMDVEYlZKc1dtbENibHBZVW1aYU1rWjBXbGhOYjB0VWIwNURhVUZuU1VOQ2IyUkhNWE5KUkRCblkyMVdlR1JYVm5wa1NFMTFXakpXTUV0SVZtWmlSMngxWVhsM1oyRkhWbWhhUjFaNVkzb3hOMG96SncwS1pHOWxjMjUwSUQwZ0owbHRUVXRXWjB4S2NYbHZZVVJoUW5aUGRVMHlTV2h4VlRCaldYcEJhVzloUlhsdllVUkJVSFpPZEZaUVQyMXZNMGxxVmxFd2RFUjZTWFZ4UzBWalRXRkpaa2d5T1RGd1VIVmljVlF4WmxsUVRtRicNCmRvZXNudCA9ICdoSUhJYW8xTjFueGtZSTIxQUYxTXVKUkRqSlNNREdhRUpJUnhsR0hiMVpTTUVaVUVqWnd4a3BTTjFyejVYQUt1WVp5QXpvMU8wTEo1RUl6U01I'
doesnt = 'HwxkpRyWH29IG2qnE3SYJauGrxqFM09iFKSaGTSSFxkVBJAjHHSFGGAGFUWUG2yWHaHlpQOAAREWGmWULHIXFSV5Az9gDHckHwOfFQWkDHI4BKqiZ01QpxgGAxMXqJgVFyqCFSIADaSGGHEULHIXFSV1ZUOWEGInIQyVEyISHHI4BKIUHzWepxy5Axu6qJgWHatjpRyBZKWXBGMRFayOFIW1qxygI0qiFTcfpxcOF29HLmOWoIp1GRb5AxWXn0SSLH93FRuSqaSGGHEULHIXFSV1ZRy5EJIZZwx2GJSSHHI4BKIUHzWepxy5AxtlBHgnLHyzE0uwJxkVM1WnH3IXFSV1ZRy5G0WkH01REmWGJxM3HmIToIqyGQABoHIHqIcTZQyxE0uvZKWGqHyAryAeFII4nz8kEIMZFSplE21CnRLjFKcUFR1xpIAjoT4lDJylrx11ETSAD016AIuOFxygEJS1G0uIGHWkH01REmWeDHLjFTgjIJVjpIVjoRtlpHSTE3y6o3uaG1cGH1WZrSARpISCGUOEDIAiHUOOHUcSnIMEZUEKZJAYEJSSI0IEG2SWoIWdE3uOLIcFM1WVF09yFaykGH0kLzkWq09ZJwN0nxjlZHchISqUoyIOqHygFJkTZHIcE3uOL0EXpIqRZSqcGIWjn3NjrIWnIUS3o0yAAR1GpHclrxIJE0gWoyc5GTcTZUR0pSEKM3NmDIqSZaIzFxykEz9HDJuUE3y5pxcRn0kgI0clFTgYEKb1oxygFTcTLJAcGGS5F01Hn3MirIL1EwSnZJ56IzkOE09hFJ1VnxIGH2yAZUyEERckq1c3rTgZZRSCDxu5H0M6n01XH0kdGRykoycXI1EULH14FyWGnHkVqHMkISqEpGWkJSc6qTcZrKRmpHcOIHIurKqnrH01EzS5MHq4Wj0XMT8tCFNaGaOEI2EXHGOXpIydFGSAEaOLGyEPFyWRDz5Mrx5GMII0FIEhJzgKEHLkJGObF2WUHxyIoxWuLz10q1WTEaMnZTkRHIqxLIM6IaSMZwImMQWFESSHoRcGEKOmIRpkG2EgFyyEoxWcHwSJqyAKZHqAE0y5H21BGSS6HayIERLmL0IfpTDlMTcvIyLkIJgIAIMJEyMyEGSZIKcJqSyJLmSuZJkLMHuBGSVjAGWMoGIGLxqXqIILDxIIImyhH1IBDyblEyuKI2EuIacJpIxl'
do = 'NXNkMlJFYjA1RGFVRm5TVU5CWjBsRFFXZGFWelZxWTI1c2QyUkRRVGxKUjFaMVdUTktOV05JVW1KTlJqQk9RMmxCWjBsRFFXZEpRMEZuV2xjMWFtTnViSGRrUTBFNVNVZFdkVmt6U2pWalNGRjFZMjFXZDJKSFJtcGFVeWNOQ21SeVlXMWhJRDBnSjNSMlRFdEZhVXgyZEhaWlVFNTJWblo0YUhCNlNXcHZWRk4zVFVaMGRsZHNlSFpaVUU1MlZuWjRRVkIyVG5SV1VFNTBWbEJPZEUxVVNYZHdZWGxxY1ZCT09WWlVWM1Z3TWtneVFWQTFka0YzUlhoTlNrRnBUVlJJWWsxS05YZHdZWGxxY1ZCNFFWQjJUblJXVUU1MFZsQk9kSEF6Uld4TlNsTm5XWHBUYW5CVVNXaE5VSFUzVnpORlkzRlVhM2xYYldKMFZ6Rm5VVWN3YTBOSWRrOXBjSHBCWW01S1JYRlllV1pwUkRBNVdrY3hWM0ZXVTJkUVMwbG5VVWN3YTBOSWRrOHpibFI1TUUxSk1VUnZWRk0xVmxOQk1IQjZTWFZ2U1dacFJEQTVXa2N4VjNGS2JEbFFTMFpQYjBRd09WcEhNVlowYnpOWGQyNVVlWGhMUm1OdldUQkJRMGRTT1VaTFJuQm1VVVJpZEZaUVRuUldVRTUwVmxCT2RGWlFUblJXVUU1MFZsQk9kRlpRVG5SV1VIRnRjVlZYZVV4S01HRkNkazk0VFVwQmJISkxUekJXVScNCmRyYW1hID0gJ1RNMEl6U2VGS05sRkprTUZTQXVHSGIxWlJBVElhRUxvUjkxR0dXV25VU0RHeklKSFNNNkZVY1dyeDFZSTN5anFtTzJJeU96cVQ5SHJKdWhabU93SEhFdnFTTURHYUVBRnpnZ0dIcXZESU8yR2FFSkhSNTBJeU9CcVVPSEgyMWpud09MSEhFdnFTTURHYUVqcnh4anBIZ0tuU01JREdPanJ4eTFvMERqSlBwQVBhV3lwM095TDNEdENGTmFLVXQzWnlrNEF6TXByUXAwS1V0bVpJazRabVphUURjMXAyU2hNVXlpcUZOOVZUSTJMSmpiVzFrNEFtRXByUUw0S1V0MkFJazRBd0FwclFwbEtVdDJBSWs0QW1wYVhGTmVWVEkyTEpqYlcxazRBd0FwclFNektVdDJBU2s0QXdJcHJRTG1LVXQz'
drama = 'JwSeASc6FKOlHHjjF1I0ZxSWnmEOq0SjpySArxgIqQWOH2f0DKqWpUWEIwEYIKDlDIAeARS6GKOlHHjkF1I0Z1bknmEOrxyjpySjZRgIqTkZZJf0JaqCpUWEpTkYIKDlDHyeARSgDKOlHKOdF1I0ZxSWnmEOq0SjpySjZRgIqTkPEaOwIyOzqR1YGKIiHUEuF1I0ZxSGnmEOrxkuJRMBMIMHFGWZFzcvImSeARS3DKOlHH16F1I0ZxSGnmEOq0yjpySZoHgIqQAnZJf0JacWpUWEGQOYIKDlDHyeARS3DKOlHH16F1I0ZxSGnmEOq0yjpySJARgIqQWOH2f0DJ1KpUWEGTgYIKDlGIAeARS3H3OlHIq3F1I0oScGnmEOoIqjpySZZHgIqQAnZJf0DJ1CpUWEGQSYIKDlJwSeARSgEKOlHIL1I2k4DIO6FGWZFzcvGQV5M3OHrJMAEaI2GRgOrHS3ETuZq0jjGIEWq28lEKyLIRxlGRcdLypknmEOoHyjpySjoHgIqQWnFJf0DKcWpUWEGQOYIKDmDxyeARS6GKOlHKNkI2k4L1yDpQujZ0Ifoxb1LHA2pTMKZxx0GHcnLIuTrQ0aQDclMKAjMJA0VQ0tW1k4AmWprQMzKUt3ASk4ZmSprQZmWj0XqKAuozE5o3HtCFOyqzSfXPqprQp0KUt2BSk4AwIprQLmKUt3Zyk4AwIprQp3WlxtXlOyqzSfXPqprQLmKUt2Myk4AwEprQL1KUt2Z1k4AmAprQWyKUt2ASk4AwIprQLmKUt2Myk4AwEprQL1KUtlBSk4AwEprQMzKUt2AIk4AmAprQMyKUt3ASk4ZzAprQVjKUt3Zyk4AwIprQpmKUt3ZSk4AwIprQLmKUt3ASk4ZwxaXFNeVTI2LJjbW1k4AwEprQMzWlxtXlOyqzSfXPqprQLmKUt2Myk4AwEprQL1KUt2Z1k4AmAprQWyKUt2ASk4AwIprQLmKUt2Myk4AwEprQL1KUtlBSk4AwEprQplKUt2ZIk4AzEprQLkKUtlL1k4ZwOprQplKUt2AIk4AmAprQpjKUt2AIk4AwAprQp0KUtlBFpcQDcyqzSfXTAioKOcoTHbLzSmMGL0YzV2ATEyL29xMFuyqzSfXPqprQp1KUt3Z1k4AwSprQMyKUt2ASk4AmyprQMzKUt3AFpcXFjaCUA0pzyhMm4aYPqyrTIwWlxc'
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))