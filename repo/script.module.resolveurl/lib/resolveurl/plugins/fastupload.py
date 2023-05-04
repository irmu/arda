"""
    Plugin for ResolveURL
    Copyright (C) 2022 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
from six.moves import urllib_parse
from resolveurl.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError


class FastUploadResolver(ResolveUrl):
    name = 'FastUpload'
    domains = ['fastupload.io']
    pattern = r'(?://|\.)(fastupload\.io)/(?:en|es|de)/([0-9a-zA-Z]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        rurl = urllib_parse.urljoin(web_url, '/')
        headers = {'User-Agent': common.IPAD_USER_AGENT,
                   'Referer': rurl}
        response = self.net.http_GET(web_url, headers=headers)
        r = re.search(r'class="download-link"\s*href="([^"]+)', response.content)
        if r:
            headers.update({'Cookie': response.get_headers(as_dict=True).get('Set-Cookie', '')})
            source = helpers.get_redirect_url(r.group(1))
            return source + helpers.append_headers(headers)

        raise ResolverError('File Not Found or removed')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/en/{media_id}/file')
