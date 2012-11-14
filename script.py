# *-* encoding: utf-8 *-*

import os
from cronjob import reload

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


reload()