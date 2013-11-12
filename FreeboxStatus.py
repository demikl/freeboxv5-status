#!/usr/bin/env python
# -*- coding: utf8 -*-

import urllib2, re, datetime

class FreeboxStatus():
    def __init__( self, loadData=True, externalDataFeed=None ):    
        self._registerCategoryParsers()
        self._registerSubCategoryParsers()
        self._razInfos()
        if loadData:
            self.update( externalDataFeed )


    def _registerCategoryParsers( self ):
        self._category_parsers = {
            "general":      self._parseCategory_general,
            "telephone":    self._parseCategory_telephone,
            "adsl":         self._parseCategory_adsl,
            "wifi":         self._parseCategory_wifi,
            "network":      lambda status: self._notImplemented, #self._parseCategory_network
        }


    def _registerSubCategoryParsers( self ):
        self._subcategory_parsers = {
            "history":                  lambda status: self._notImplemented, #self._parseSubCategory_general_history,
            "dhcp":                     lambda status: self._notImplemented, #self._parseSubCategory_network_dhcp,
            "port_forwarding":          lambda status: self._notImplemented, #self._parseSubCategory_network_portForwarding,
            "port_range_forwarding":    lambda status: self._notImplemented, #self._parseSubCategory_network_portRangeForwarding,
            "interfaces":               lambda status: self._notImplemented, #self._parseSubCategory_network_interfaces
        }


    def _razInfos( self ):
        self.status = {
            "general": {},
            "telephone": {},
            "adsl": { "history":{} },
            "wifi": {},
            "network": {
                "dhcp":{},
                "port_forwarding":{},
                "port_range_forwarding":{},
                "interfaces":{}
            }
        }


    def update( self, externalDataFeed=None ):
        self._razInfos()
        if not externalDataFeed:
            try:
                r = urllib2.urlopen("http://mafreebox.free.fr/pub/fbx_info.txt", timeout=2)
            except:
                return
            if r.getcode() != 200:
                return
            charset = r.headers["Content-Type"].split('charset=')[-1]
            feed = unicode( r.read(), charset )
        else:
            feed = unicode( externalDataFeed.read(), 'ISO-8859-1' )
        self._parseStatus( feed.splitlines() )

    
    def _parseStatus( self, status ):
        cat, subcat = None, None
        pos = 0
        for line in status:
            pos += 1
            # Changement de catégorie
            if line.startswith( "====" ):
                cat = self._parseCategoryName( status[pos-2] )
                subcat = None
                continue
            if line.startswith( " -----" ):
                subcat = self._parseSubCategoryName( status[pos-2] )
                continue
            try:
                if subcat:
                    self._subcategory_parsers[subcat]( line )
                elif cat:  
                    self._category_parsers[cat]( line )
            except AttributeError, e:
                print e


    def _parseCategoryName( self, category_fullname ):
        return {
            u"Informations générales :": "general",
            u"Téléphone :": "telephone",
            u"Adsl :": "adsl",
            u"Wifi :": "wifi",
            u"Réseau :": "network"
        }.get( category_fullname.strip() )


    def _parseSubCategoryName( self, subcategory_fullname ):
        return {
            u"Iournal de connexion adsl :": "history",
            u"Attributions dhcp :": "dhcp",
            u"Redirections de ports :": "port_forwarding",
            u"Redirections de plage de ports :": "port_range_forwarding",
            u"Interfaces réseau :": "interfaces"
        }.get( subcategory_fullname.strip() )


    def _parseCategory_general( self, line ):
        key_mapper = {
            u"Modèle":               "fbx_model",
            u"Version du firmware":  "fw_version",
            u"Mode de connection":   "connection_mode",
            u"Temps depuis la mise en route": "uptime"
        }
        value_parsers = {
            u"fbx_model":        lambda s:s,
            u"fw_version":       lambda s: [ int(v) for v in s.split(".") ],
            u"connection_mode":  lambda s:s,
            u"uptime":           self._parseUptime
        }
        self._parseLine( line, key_mapper, value_parsers, self.status["general"] )


    def _parseUptime( self, uptime_str ):
        regex = "(?P<days>\d+ jours?,)? (?P<hours>\d+ heures?,)? (?P<min>\d+ minutes?)"
        res = re.match( regex, uptime_str )
        if not res:
            return None
        groups = res.groupdict()
        #{'days': '5 jours', 'hours': '1 heure', 'min': '26 minutes'}
        return datetime.timedelta(
            days    = int(groups["days"].partition(" ")[0]),
            hours   = int(groups["hours"].partition(" ")[0]),
            minutes = int(groups["min"].partition(" ")[0])
        )
    

    def _parseCategory_telephone( self, line ):
        key_mapper = {
            u"Etat":             "configured",
            u"Etat du combiné":  "online",
            u"Sonnerie":         "ringing"
        }
        value_parsers = {
            u"configured":   lambda s: True if s == u"Ok" else False,
            u"online":       lambda s: False if s == u"Raccroché" else False,
            u"ringing":      lambda s: False if s == u"Inactive" else True
        }
        self._parseLine( line, key_mapper, value_parsers, self.status["telephone"] )


    def _parseLine( self, line, key_mapper, value_parsers, cfg_node ):
        groups = line.strip().partition("  ")

        # Si la ligne ne contient pas de clé/valeur
        if not groups[1]:
            return

        key, value = groups[0].strip(), groups[2].strip()

        key_mapped = key_mapper.get( key )
        if not key_mapped:
            return

        value_parser = value_parsers.get( key_mapped )
        if not value_parser:
            return

        cfg_node[key_mapped] = value_parser( value )


    def _parseCategory_adsl( self, line ):
        key_mapper = {
            u"Etat":         "ready",
            u"Protocole":    "protocol",
            u"Mode":         "synchro_mode",
            u"Débit ATM":    "synchro_speed",
            u"Atténuation":  "attenuation",
            u"FEC":          "FEC",
            u"CRC":          "CRC",
            u"HEC":          "HEC"
        }
        value_parsers = {
            u"ready":        lambda s: True if s == "Showtime" else False,
            u"protocol":     lambda s:s,
            u"synchro_mode": lambda s:s,
            u"synchro_speed":lambda v: self._parseTwoValues( v, unit="kb/s", keys=['down','up'], cast=int),
            u"attenuation":  lambda v: self._parseTwoValues( v, unit="dB",   keys=['down','up'], cast = float),
            u"FEC":          lambda v: self._parseTwoValues( v, unit=None,   keys=['down','up'], cast = int),
            u"CRC":          lambda v: self._parseTwoValues( v, unit=None,   keys=['down','up'], cast = int),
            u"HEC":          lambda v: self._parseTwoValues( v, unit=None,   keys=['down','up'], cast = int),
        }
        self._parseLine( line, key_mapper, value_parsers, self.status["adsl"] )


    def _parseTwoValues( self, values, unit, keys, cast=lambda s:s ):
        value1, _, value2 = [ v.strip() for v in values.partition("  ") ]
        if unit:
            value1, value2 = [ v.partition(" ")[0] for v in [ value1, value2 ] ]
        return { keys[0]:cast(value1), keys[1]:cast(value2) }


    def _parseCategory_wifi( self, line ):
        key_mapper = {
            u"Etat":            "state",
            u"Modèle":          "model",
            u"Canal":           "channel",
            u"État du réseau":  "isActive",
            u"Ssid":            "ssid",
            u"Type de clé":     "key_algorithm",
            u"FreeWifi":        "isFreeWifiActive",
            u"FreeWifi Secure": "isFreeWifiSecureActive"
        }
        value_parsers = {
            "state":                    lambda s:s,
            "model":                    lambda s:s,
            "channel":                  lambda s: int(s),
            "isActive":                 lambda s: (s == u"Activé" ),
            "ssid":                     lambda s:s,
            "key_algorithm":            lambda s:s,
            "isFreeWifiActive":         lambda s: (s == "Actif"),
            "isFreeWifiSecureActive":   lambda s: (s == "Actif")
        }
        self._parseLine( line, key_mapper, value_parsers, self.status["wifi"] )





    def _notImplemented( self ):
        raise NotImplemented()