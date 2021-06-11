# -*- coding: UTF-8 -*-

import os.path
import en


scraper_source = os.path.dirname(__file__)
__all__ = [x[1] for x in os.walk(os.path.dirname(__file__))][0]


##--en--##
hoster_source = en.sourcePath
hoster_providers = en.__all__


##--All Providers--##
total_providers = {'en': hoster_providers}
all_providers = []
for key, value in total_providers.iteritems():
    all_providers += value