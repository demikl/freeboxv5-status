#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests

class FreeboxStatus():
    def __init__( self, loadData=True ):
        self._registerCategoryParsers()
        self._registerSubCategoryParsers()
        self._razInfos()
        if loadData:
            self.update()


    def _registerCategoryParsers( self ):
        self._category_parsers = {
            "general":      self._parseCategory_general,
            "telephone":    self._parseCategory_telephone,
            "adsl":         self._parseCategory_adsl,
            "wifi":         self._parseCategory_wifi,
            "network":      self._parseCategory_network
        }


    def _registerSubCategoryParsers( self ):
        self._subcategory_parsers = {
            "history":                  self._parseSubCategory_general_history,
            "dhcp":                     self._parseSubCategory_network_dhcp,
            "port_forwarding":          self._parseSubCategory_network_portForwarding,
            "port_range_forwarding":    self._parseSubCategory_network_portRangeForwarding,
            "interfaces":               self._parseSubCategory_network_interfaces
        }


    def _razInfos( self ):
        status = {
            "general" = {}
            "telephone" = {}
            "adsl" = { "history":{} }
            "wifi" = {}
            "network" = {
                "dhcp":{},
                "port_forwarding":{},
                "port_range_forwarding":{},
                "interfaces":{}
            }
        }


    def update( self ):
        self._razInfos()
        try:
            r = requests.get("http://mafreebox.free.fr/pub/fbx_info.txt", timeout=1)
        except requests.exceptions.Timeout:
            return
        if r.status_code != 200:
            return
        self._parseStatus( r.text.splitlines() )

    
    def _parseStatus( self, status ):
        cat, subcat = None, None
        pos = 0
        for line in status:
            pos += 1
            # Changement de catégorie
            if line.startswith( "====" ):
                cat = self._parseCategoryName( status[pos-1] )
                subcat = None
                continue
            if line.startswith( " -----" ):
                subcat = self._parseSubCategoryName( status[pos-1] )
                continue
            if subcat:
                self._subcategory_parsers[subcat]( line )
            else:  
                self._category_parsers[cat]( line )


    def _parseCategoryName( self, category_fullname ):
        return {
            "Informations générales :": "general",
            "Téléphone :": "telephone",
            "Adsl :": "adsl",
            "Wifi :": "wifi",
            "Réseau :": "network"
        }.get( category_fullname.strip() )


    def _parseSubCategoryName( self, subcategory_fullname ):
        return {
            "Iournal de connexion adsl :": "history",
            "Attributions dhcp :": "dhcp",
            "Redirections de ports :": "port_forwarding",
            "Redirections de plage de ports :": "port_range_forwarding",
            "Interfaces réseau :": "interfaces"
        }.get( subcategory_fullname.strip() )


    def _parseCategory_general( self, line ):
        groups = line.partition("  ")

        # Si la ligne ne contient pas de clé/valeur
        if not groups[1]:
            return

        key, value = groups[0].strip(), groups[2].strip()

        key_mapped = {
            "Modèle":               "fbx_model",
            "Version du firmware":  "fw_version",
            "Mode de connection":   "connection_mode",
            "Temps depuis la mise en route": "uptime"
        }.get( key )
        if not key_mapped:
            return

        value_parser = {
            "fbx_model":        lambda s:s,
            "fw_version":       lambda s: s.split(".")
            "connection_mode":  lambda s:s,
            "uptime":           self._parseUptime
        }.get( key_mapped )
        if not value_parser:
            return
        self.status["general"][key_mapped] = value_parser( value )


    def _parseUptime( self, uptime_str ):
        regex = "(?P<days>\d+ jours?)? (?P<hours>\d+ heures?)? (?P<min>\d+ minutes?)"
        res = re.match( regex, uptime_str )
        if not res:
            return None
        groups = res.groupdict()
          {'days': '5 jours', 'hours': '1 heure', 'min': '26 minutes'}
        return datetime.timedelta()
            hours   = groups["days"].partition()[0]
            minutes = groups["hours"].partition()[0]
            seconds = groups["min"].partition()[0]
        )