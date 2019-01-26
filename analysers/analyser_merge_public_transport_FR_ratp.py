#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class _Analyser_Merge_Public_Transport_FR_Ratp(Analyser_Merge):
    def __init__(self, config, logger, clas, select, osmTags, defaultTag):
        place = "RATP"
        self.missing_official = {"item":"8040", "class": 1+10*clas, "level": 3, "tag": ["merge", "railway", "public transport"], "desc": T_(u"%s stop not integrated", place) }
        self.possible_merge   = {"item":"8041", "class": 3+10*clas, "level": 3, "tag": ["merge", "railway", "public transport"], "desc": T_(u"%s stop, integration suggestion", place) }
        Analyser_Merge.__init__(self, config, logger,
            u"http://data.ratp.fr/fr/les-donnees/fiche-de-jeu-de-donnees/dataset/positions-geographiques-des-stations-du-reseau-ratp.html",
            u"Positions géographiques des stations du réseau RATP",
            CSV(Source(attribution = u"RATP", millesime = "07/2012",
                    file = "ratp_arret_graphique.csv.bz2"),
                separator = u"#"),
            Load("lon", "lat",
                create = """
                    id VARCHAR(254),
                    lon VARCHAR(254),
                    lat VARCHAR(254),
                    nom_station VARCHAR(254),
                    ville_cp VARCHAR(254),
                    reseau VARCHAR(254)""",
                select = {"reseau": select}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = osmTags),
                osmRef = "ref:FR:RATP",
                conflationDistance = 100,
                generate = Generate(
                    static1 = defaultTag,
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:RATP": "id"},
                    mapping2 = {"name": "nom_station"},
                    text = lambda tags, fields: T_(u"%s stop of %s", place, tags["name"]) )))


#class Analyser_Merge_Ratp_Bus(_Analyser_Merge_Public_Transport_FR_Ratp):
#    def __init__(self, config, logger = None):
#        _Analyser_Merge_Public_Transport_FR_Ratp.__init__(self, config, logger, 3, "bus", {"highway": "bus_stop"}, {"highway": "bus_stop", "public_transport": "stop_position", "bus": "yes"})

class Analyser_Merge_Ratp_Metro(_Analyser_Merge_Public_Transport_FR_Ratp):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Public_Transport_FR_Ratp.__init__(self, config, logger, 0, "metro", {"railway": "station"}, {"railway": "station"})

class Analyser_Merge_Ratp_RER(_Analyser_Merge_Public_Transport_FR_Ratp):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Public_Transport_FR_Ratp.__init__(self, config, logger, 1, "rer", {"railway": "station"}, {"railway": "station"})

class Analyser_Merge_Ratp_Tram(_Analyser_Merge_Public_Transport_FR_Ratp):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Public_Transport_FR_Ratp.__init__(self, config, logger, 2, "tram", {"railway": "tram_stop"}, {"railway": "tram_stop", "public_transport": "stop_position", "tram": "yes"})
