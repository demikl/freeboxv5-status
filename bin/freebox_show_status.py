#!/usr/bin/env python
# -*- coding: utf-8 -*-

import freebox_v5_status.freeboxstatus
import pprint

fbx = freebox_v5_status.freeboxstatus.FreeboxStatus()
pprint.pprint( fbx.status )
