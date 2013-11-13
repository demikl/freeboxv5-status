import FreeboxStatus
import pprint, os

fbx_sample = open("fbx_info_1.5.20.log", "r")
fbx = FreeboxStatus.FreeboxStatus( externalDataFeed = fbx_sample )
pprint.pprint(fbx.status)
