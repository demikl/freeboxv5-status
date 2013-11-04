freeboxv5-status
================

Récupération du statut de la Freebox V5 en Python

pour parser l'uptime :

regex = "(?P<days>\d+ jours?)? (?P<hours>\d+ heures?)? (?P<min>\d+ minutes?)"
r = re.compile(regex)
up = "5 jours 1 heure 26 minutes"
res.groupdict()
  {'days': '5 jours', 'hours': '1 heure', 'min': '26 minutes'}
dur = datetime.timedelta(hours=h, minutes=m, seconds=s)
