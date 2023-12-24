# -*- coding: utf-8 -*-
'''
	The Crew Add-on

	@package plugin.video.thecrew

	@copyright (c) 2023, The Crew
	@license GNU General Public License, version 3 (GPL-3.0)

'''

from sys import argv

from resources.lib.modules import crew
from urllib.parse import parse_qsl

try:
	params = dict(parse_qsl(argv[2].replace('?', '')))
except:
	params = {}

crew.router(params)