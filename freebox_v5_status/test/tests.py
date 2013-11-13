import freebox_v5_status.freeboxstatus
import pprint, os

fbx_sample = open("../docs/fbx_info_1.5.20.log", "r")
fbx = freebox_v5_status.freeboxstatus.FreeboxStatus( externalDataFeed = fbx_sample )
pprint.pprint(fbx.status)
