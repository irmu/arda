# -*- coding: utf-8 -*-

import base64
from six import ensure_text



tmdb_key = ensure_text(base64.b64decode(b'MDA0OTc5NWVkYjU3NTY4Yjk1MjQwYmM5ZTYxYTlkZmM='))
fanart_key = ensure_text(base64.b64decode(b'MzliOTBhMDE3ZTM5MWFmZDMzNzUwZjk3ODI3ZjhkOTY='))
trakt_client_id = ensure_text(base64.b64decode(b'NWFjOTI4YjAzYTI5ZDBlYzkzMjI1MDZmMTAwZjE5MmI2Mzc5YmQ3YTI2YTFhNzJjNTczY2EyMDI4Mjk4YTQyZg=='))
trakt_secret = ensure_text(base64.b64decode(b'MTBmYzU5OTEzZjA5ZjMyNWZjZjdiN2NjZDhiY2FhYjkwYzgwODEyYTIwMzg4MzA4YmQ0YzFlNGQyMDRlYjZhNg=='))
