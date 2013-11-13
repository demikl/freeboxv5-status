freeboxv5-status
================

Récupération du statut de la Freebox V5 en Python

Python wrapper for Freebox V5 status

L'état de la Freebox est accessible via un dictionnaire Python.

Exemple d'usage :

```python
import FreeboxStatus
import pprint

fbx = FreeboxStatus.FreeboxStatus( )
pprint.pprint(fbx.status)
```

Exemple de résultat :

```python
{'adsl': {'CRC': {'down': 4, 'up': 0},
          'FEC': {'down': 6583, 'up': 82},
          'HEC': {'down': 1, 'up': 108},
          'attenuation': {'down': 17.0, 'up': 8.9},
          'history': {},
          'protocol': u'ADSL2+',
          'ready': True,
          'synchro_mode': u'Interleaved',
          'synchro_speed': {'down': 18941, 'up': 1025}},
 'general': {'connection_mode': u'D\xe9group\xe9',
             'fbx_model': u'Freebox ADSL',
             'fw_version': [1, 5, 20],
             'uptime': datetime.timedelta(7, 79260)},
 'network': {'dhcp': {},
             'interfaces': {'USB': {'down': None,
                                    'status': u'Non connect\xe9',
                                    'up': None},
                            'WAN': {'down': 2, 'status': u'Ok', 'up': 107},
                            'ethernet': {'down': 0,
                                         'status': u'100baseTX-FD',
                                         'up': 0},
                            'switch': {'down': 108,
                                       'status': u'100baseTX-FD',
                                       'up': 4}},
             'port_forwarding': {},
             'port_range_forwarding': {}},
 'telephone': {'configured': True, 'online': False, 'ringing': False},
 'wifi': {'DMZ_ip': u'192.168.0.0',
          'channel': 11,
          'dynamic_ip_range': (u'192.168.0.10', u'192.168.0.50'),
          'freeplayer_ip': u'192.168.0.104',
          'hasDHCPServer': True,
          'hasIPv6': True,
          'hasWakeOnLanProxy': False,
          'isActive': True,
          'isRespondingToPing': True,
          'key_algorithm': u'WPA (TKIP+AES)',
          'model': u'Ralink RT2880',
          'private_ip': u'192.168.0.254',
          'public_ip': u'127.0.0.1',
          'routerMode': True,
          'ssid': u'MySSID',
          'state': u'Ok'}}
```