#
# MTURK IMAGE ANNOTATION TOOL
#

# Creates a HIT for the specified images.


import sys
from uuid import UUID

import mturk

print('CURRENT BALANCE:', mturk.account_balance())

uuids = list(map(UUID, sys.argv[1:]))

mturk.dev_template_reload(f'https://s3.amazonaws.com/gttc2/mturk/images/{uuids[0]}.jpg')

hit = mturk.create_hit(f'https://s3.amazonaws.com/gttc2/mturk/images/{uuids[0]}.jpg')

print(hit)
