#!/usr/bin/env python
# -*- coding: utf8 -*-

import freebox_v5_status.freeboxstatus
import statsd

metrics_prefix = "freebox"
fbx = freeboxstatus.FreeboxStatus()
while True:
    timer = statsd.Timer(metrics_prefix)
    timer.start()
    fbx.update()
    timer.stop("dataAcquisitionTime")

    gauge = statsd.Gauge(metrics_prefix)
    gauge.send("connection.debit.down",     fbx.status["adsl"]["synchro_speed"]["down"])
    gauge.send("connection.debit.up",       fbx.status["adsl"]["synchro_speed"]["up"])
    gauge.send("network.WAN.down",          fbx.status["network"]["interfaces"]["WAN"]["down"])
    gauge.send("network.WAN.up",            fbx.status["network"]["interfaces"]["WAN"]["up"])
    gauge.send("network.ethernet.down",     fbx.status["network"]["interfaces"]["ethernet"]["down"])
    gauge.send("network.ethernet.up",       fbx.status["network"]["interfaces"]["ethernet"]["up"])
    gauge.send("network.switch.down",       fbx.status["network"]["interfaces"]["switch"]["down"])
    gauge.send("network.switch.up",         fbx.status["network"]["interfaces"]["switch"]["up"])
    c.increment("telephone.sonnerie", 1 if fbx.status["telephone"]["ringing"] else 0)
    c.increment("telephone.en_ligne", 1 if fbx.status["telephone"]["online"] else 0)

    time.sleep(1)
