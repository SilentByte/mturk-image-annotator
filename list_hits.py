#
# MTURK IMAGE ANNOTATION TOOL
#

# List available HITs.

import mturk

hits = mturk.client.list_hits()
for hit in hits['HITs']:
    print(hit['HITId'])
