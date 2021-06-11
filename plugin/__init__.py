# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MGP
                                 A QGIS plugin
 MGP
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-03-04
        copyright            : (C) 2021 by e
        email                : e
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MGP class from file MGP.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mgp_plugin import mgp_plugin
    return mgp_plugin(iface)
