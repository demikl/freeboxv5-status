#!/usr/bin/env python
# -*- coding: utf8 -*-

import statsd
import requests
import time

metrics_prefix = "freebox"


while True:
    timer = statsd.Timer(metrics_prefix)
    timer.start()
    try:
        r = requests.get("http://mafreebox.free.fr/pub/fbx_info.txt", timeout=1)
    except requests.exceptions.Timeout:
        continue
    if r.status_code != 200:
        continue    
    gauge = statsd.Gauge(metrics_prefix)
    data = r.text.splitlines()
    for line in data:
        items = line.split()
        if line.startswith(u"  Sonnerie"):
            c = statsd.Counter(metrics_prefix)
            c.increment("telephone.sonnerie", 0 if items[1] == "Inactive" else 1)
        if line.startswith(u"  Etat du combin"):
            c = statsd.Counter(metrics_prefix)
            c.increment("telephone.en_ligne", 1 if items[3] == u"Décroché" else 0)
        if line.startswith(u"  Débit ATM"):
            gauge.send("connection.debit.down", int(items[2]))
            gauge.send("connection.debit.up",   int(items[4]))
        if line.startswith("  WAN"):
            if items[3] == "ko/s":
                gauge.send("network.WAN.down", int(items[2]))
            gauge.send("network.WAN.up", int(items[4]))
        if line.startswith("  Ethernet"):
            if items[3] == "ko/s":
                gauge.send("network.ethernet.down", int(items[2]))
            gauge.send("network.ethernet.up", int(items[4]))
        if line.startswith("  Switch"):
            if items[3] == "ko/s":
                gauge.send("network.switch.down", int(items[2]))
            gauge.send("network.switch.up", int(items[4]))

    timer.stop("dataAcquisitionTime")
    time.sleep(1)
