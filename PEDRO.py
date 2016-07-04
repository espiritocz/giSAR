#!/usr/bin/python
 # -*- coding: latin-1 -*-
import os.path
import sys

from qgis.core import *
from qgis.utils import iface
from PyQt4.QtGui import QColor
from PyQt4.QtGui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py



import os.path
import sys
 
#layer = QgsVectorLayer('C:\Users\Pedro\Desktop\NYC_MUSEUMS_GEO\NYC_MUSEUMS_GEO.shp', "New York City Museums", "ogr")
#
#if not layer.isValid():
#    print "Layer %s did not load" % layer.name()
##
#QgsMapLayerRegistry.instance().addMapLayers([layer])

#features = layer.getFeatures()
#f = features.next()
#g = f.geometry()
#print g.asPoint()
#print f.attributes()
#print [c.name() for c in f.fields().toList()]

#lyrPts = QgsVectorLayer('C:\Users\Pedro\Desktop\NYC_MUSEUMS_GEO\NYC_MUSEUMS_GEO.shp', "New York City Museums", "ogr")
#QgsMapLayerRegistry.instance().addMapLayers([lyrPts])
#selection =lyrPts.getFeatures(QgsFeatureRequest().setFilterExpression(u'"ZIP" =10002'))
#lyrPts.setSelectedFeatures([s.id() for s in selection])
#iface.mapCanvas().zoomToSelected()

#######
# Alterar valores de atributos  Changing a vector layer feature’s attribute
########

#vectorLyr = QgsVectorLayer('C:\Users\Pedro\Desktop\NYC_MUSEUMS_GEO\NYC_MUSEUMS_GEO.shp', "New York City Museums", "ogr")
#vectorLyr.isValid()
#fid1 = 22
#fid2 = 23
#tel = vectorLyr.fieldNameIndex("TEL")
#city = vectorLyr.fieldNameIndex("CITY")
#attr1 = {tel:"(555) 555-1111", city:"NYC"}
#attr2 = {tel:"(555) 555-2222", city:"NYC"}
#vectorLyr.dataProvider().changeAttributeValues({fid1:attr1,fid2:attr2})

#######
# Elimina linhas  22 e 95 Deleting a vector layer feature
########
#vectorLyr = QgsVectorLayer('C:\Users\Pedro\Desktop\NYC_MUSEUMS_GEO\NYC_MUSEUMS_GEO.shp', "New York City Museums", "ogr")
#vectorLyr.isValid()
#vectorLyr.dataProvider().deleteFeatures([ 22, 95 ])


#vectorLyr = QgsVectorLayer('C:\Users\Pedro\Desktop\NYC_MUSEUMS_GEO\NYC_MUSEUMS_GEO.shp', "New York City Museums", "ogr")
#vectorLyr.isValid()
#vectorLyr.dataProvider().deleteAttributes([1])
#vectorLyr.updateFields()

################################################3
# Get the active layer (must be a vector layer)
layer = iface.activeLayer()
# Get the first feature from the layer
feature = layer.getFeatures().next()
# Add this features to the selected list
layer.setSelectedFeatures([feature.id()])


featuretotal=[feature [0], feature [1]]
print featuretotal
selection = layer.selectedFeatures()

print len(selection)
for feature in selection:
    print feature
    
import processing
features = processing.features(layer)
for feature in features:
    print feature
    
for feature in layer.getFeatures():
    #print feature.id()
    name = [feature[3], feature[4], feature[5], feature[6]]
    print name

#QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.selectFeature)

from qgis.gui import QgsMapToolEmitPoint

# Store reference to the map canvas
self.canvas = self.iface.mapCanvas()
# Create the map tool using the canvas reference
self.pointTool = QgsMapToolEmitPoint(self.canvas)