# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Remotwatch
                                 A QGIS plugin
 This plugin is for visualize and manipulate points from Stamps and SAR PROZ Processing
                             -------------------
        begin                : 2015-06-11
        copyright            : (C) 2015 by Milan Lazecky, Joaquim Sousa, Pedro Guimaraes, Antonio Sousa, Matus Bakon
        email                : vistamps@utad.pt
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
    """Load Remotwatch class from file Remotwatch.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .remot_watch import Remotwatch
    return Remotwatch(iface)
