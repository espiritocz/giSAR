# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Remotwatch
                                 A QGIS plugin
 This plugin is for visualize and manipulate points from Stamps and SAR PROZ Processing
                              -------------------
        begin                : 2015-06-11
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Milan Lazecky, Joaquim Sousa, Pedro Guimaraes, Antonio Sousa, Matus Bakon
        email                : vistamps@utad.pt
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py

import resources_rc
#import image_rc

# Import the code for the dialog
from remot_watch_dialog import RemotwatchDialog
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

#import frmremotwatch

# Numerical modules 
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

import csv
from qgis.gui import QgsMapToolEmitPoint

import start_rwt

class Remotwatch:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Estes atributos sao fornecidos no momento de criacao da estancia
        # Save reference to the QGIS interface
        self.iface = iface
        self.featFinder = None
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Remotwatch_{}.qm'.format(locale))
        #print "epdro",locale_path
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = RemotwatchDialog()

        # Declare instance attributes
        self.actions = []
        
        self.menu = self.tr(u'&RemotWatch')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Remotwatch')
        self.toolbar.setObjectName(u'Remotwatch')
      
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_output_file)
        #self.dlg.pushButtontsp.clicked.connect(self.open_graph)
     
        #############################################
        # Aqui chama a localizao das funcoes se algum checkbox for ativado 
        # Se o .checkBoxLOS for ativado vai executar o que estÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¡ na funcao 
        # self.changeActivelos
        # Event  handler
        #self.dlg.nomedowidget,o que vai deterar ,nome do metodo que vai chamar
        #################################################
        global loscheck
        global heighcheck
        global cohercheck
        
        cohercheck=0
        heighcheck =0
        loscheck=0
        
        QObject.connect(self.dlg.checkBoxLOS,SIGNAL("stateChanged(int)"),self.changeActivelos)
        QObject.connect(self.dlg.checkBox_HEI,SIGNAL("stateChanged(int)"),self.changeActivehei)
        QObject.connect(self.dlg.checkBox_COHE,SIGNAL("stateChanged(int)"),self.changeActivecohe)
        QObject.connect(self.dlg.checkBox_RHEIG,SIGNAL("stateChanged(int)"),self.changeActiverhei)
        QObject.connect(self.dlg.checkBoxTEMP,SIGNAL("stateChanged(int)"),self.changeActivetemp)
        ###mouse no ponto 

        #QObject.connect(self.dlg.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.selectFeature):
        
        ################################
        # Tudo o que diga respeito ao mapa 
        ################################
        # Store reference to the map canvas
  
        self.canvas = self.iface.mapCanvas()
        # Create the map tool using the canvas reference
        #self.pointTool = QgsMapToolEmitPoint(self.canvas)
#        self.pointEmitter = QgsMapToolEmitPoint(self.iface.mapCanvas()) # barriginha
#        QObject.connect( self.pointEmitter, SIGNAL("canvasClicked(const QgsPoint, Qt::MouseButton)"), self.selectNow)
#        self.iface.mapCanvas().setMapTool( self.pointEmitter )   
        
		#result = QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.selectFeature)
		# connect signal that the canvas was clicked
        #self.pointTool.canvasClicked.connect(self.display_point)
		
        #self.dlg.Slidercoherence = QSlider()
        #self.dlg.Slidercoherence.setOrientation(Qt.Horizontal)
        #self.label = QLabel('Slider at position 0')
        #self.dlg.addWidget(self.label)
        #self.dlg.addWidget(self.slider)
        
        # Valor por defeito da coerencia
        self.dlg.labelcoherence.setText('0.0')
        
        # O que acontece se mover o slidder da coerencia 
        self.dlg.Slidercoherence.valueChanged.connect(self.slider_moved)
        
        #print "passei por aqui"
        #self.dlg.setupUi(self.dlg)
        #self.dlg.checkBoxLOS.toggled.connect(self.dlg.checkBoxLOS) ###ckheck
        #self.dlg.connect(self.dlg.checkBoxLOS, SIGNAL("stateChanged(int)"),self.dlg.CheckBox_stateChanged)
        
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Remotwatch', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        
        # Localizacao dos icones do RWT
        print icon_path
        
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # Create action that will start plugin configuration
       
        icon_path = ':/plugins/Remotwatch/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'StaMPs and SAR-PROZ'),
            callback=self.run,
            parent=self.iface.mainWindow())
            
    def selectNow(self, point, button):
        layer = self.iface.activeLayer()
        if not layer or layer.type() != QgsMapLayer.VectorLayer:
            QMessageBox.warning(None, "No!", "Select a vector layer")
            return
        print "cheguei aqui"
        width = self.iface.mapCanvas().mapUnitsPerPixel() * 2
        type(width)
        print width
        print point.x()
        print point.y()
        rect = QgsRectangle(point.x() - width, point.y() - width, point.x() + width, point.y() + width)
        print type(rect)
        print dir(rect)
        rect = self.iface.mapCanvas().mapRenderer().mapToLayerCoordinates(layer, rect)
        print dir(rect)
        print "cheguei aqui2"

        #layer.select(rect, True)
        #features = layer.getFeatures()
        #f = features.next()
        #print f.attributes()
        
        #print dir(layer)
        
        print "cheguei aqui2"
        
        #request = QgsFeatureRequest().setFilterRect(rect)
        
        #for feature in layer.getFeatures(request):
            # do something with the feature
        #    print feature.id()
        
        #print layer.fieldNameIndex("LAT")
        
       ######################################################### 
        #print layer.selectedFeaturesIds()
        
        #selectedList = layer.selectedFeaturesIds()
        #for f in selectedList:
            #print f.attributes()
         #   print f.attributeMap()
        
        #print layer.selectedFeaturesIterator()
        
####################################################
        
        #f1= layer.selectedFeaturesIds()
        #print f1.attributes()
        #features = layer.getFeatures(f1)
        
        #print features.attributes()
        #for feature in layer.getFeatures(iddd):
            # do something with the feature
         #   print feature.id()
            
        #print layer.select()
        #print layer.selectedFeatures()
        #print layer.selectedFeaturesIterator()
        #print layer.selectedFeatureCount()
        #feature = layer.getFeatures().next()
        # Add this features to the selected list
        #print layer.setSelectedFeatures([feature.id()])
        #print layer.setSelectedFeatures()
        
        #print feature[0]
        #print feature[1]
        #print feature[2]
#        feat = QgsFeature()
#        
#        ids = []
#        while layer.nextFeature(feat):
#            ids.append( feat.id() )
#        layer.setSelectedFeatures( ids )
#        
        #for feature in layer:
        #    geom = feature.geometry()
        #    attrs = feature.attributeMap()
            # the result is a dictionary
        #    for atr in attrs.values():
         #       print '{0} de {1}: {2}'.format(feature.id(), layer.featureCount(), atr.toString())
        onlyTheClosestOne=True
        onlyIds=False
        ret = None
        if onlyTheClosestOne:
            request=QgsFeatureRequest()
            request.setFilterRect(rect)
            minDist = -1
            featureId = None
            rect = QgsGeometry.fromRect(rect)
            count = 0
            
            for f in layer.getFeatures(request):
                if onlyTheClosestOne:
                    geom = f.geometry()
                    distance = geom.distance(rect)
                    if minDist < 0 or distance < minDist:
                        minDist = distance
                        featureId = f.id()
                        
            if onlyIds:
                ret = featureId
            elif featureId != None:
                f = QgsFeature()
                feats = layer.getFeature( QgsFeatureRequest(featureId) )
                feats.nextFeature(f)
                ret = f
                
        else:
            IDs = []
            for f in layer.getFeatures():
                IDs.append( f.id() )
            
            if onlyIds:
                ret = IDs
            else:
                ret = []
                request = QgsFeatureRequest()
                QgsFeatureRequest.setFilterFids(IDs)
                for f in layer.getFeatures( request ):
                    ret.append( f )
        QApplication.restoreOverrideCursor()
	
	print ret
        
            
    # Callback do LOS VELOCITY 
    def changeActivelos(self,state):
        global loscheck
        if (state==Qt.Checked):
            loscheck =1
        else:
            loscheck=0
    
    # Callback do Height
    def changeActivehei(self,state):
        global heighcheck
        if (state==Qt.Checked):
            heighcheck =1
        else :
            heighcheck =0
     
    # Callback da Coerencia    
    def changeActivecohe(self,state):
        global cohercheck
        if (state==Qt.Checked):
            cohercheck =1
        else :
            cohercheck =0
    
    # Callback da Residual Height    
    def changeActiverhei(self,state):
        global rheicheck
        rheicheck=0
        if (state==Qt.Checked):
            rheicheck =1
        else :
            rheicheck =0
    
    # Callback da Temperatura
    def changeActivetemp(self,state):
        global tempcheck
        tempcheck=0
        if (state==Qt.Checked):
            tempcheck =1
            QMessageBox.about( None, 'Atention',
            'The file you select doesnt this attribute')
        else :
            tempcheck =0
    
    # Callback do slider da coerencia 
    def slider_moved(self, position): ##### slider
        #self.label.setText('Slider at position %d' % position)
        position=float(position)/100
        #ose= "%s" % position/10
        self.dlg.labelcoherence.setText('%f'%position)
    
    def keyPressEvent(self, event):
        print "vim ate aqui"
        if event.key()==Qt.Key_Right:
            self.Slidercoherence.setValue(self.Slidercoherence.value() + 1)
        elif event.key()==Qt.Key_Left:
            self.Slidercoherence.setValue(self.Slidercoherence.value() - 1)
        else:
             self.dlg.keyPressEvent(self, event)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&RemotWatch'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolba
        del self.toolbar

 
    def open_graph(self):
        print "Carreguei no Time Series"
        self.pointEmitter = QgsMapToolEmitPoint(self.iface.mapCanvas()) # barriginha
        QObject.connect( self.pointEmitter, SIGNAL("canvasClicked(const QgsPoint, Qt::MouseButton)"), self.selectNow)
        self.iface.mapCanvas().setMapTool( self.pointEmitter ) 
       # if not self.featFinder:  
        #    from MapTools import FeatureFinder
         #   print "entrei no maptools"
         #   self.featFinder = FeatureFinder(self.iface.mapCanvas())
         #   self.featFinder.setAction(self.action)
         #   QObject.connect(self.featFinder, SIGNAL("pointEmitted"), self.onPointClicked)
        
        #t = arange(0.0, 2.0, 0.01)
        #s = sin(2*pi*t)
        #plot(t, s)
        #xlabel('time (s)')
        #ylabel('voltage (mV)')
        #title('About as simple as it gets, folks')
        #grid(True)
        #show()
        
    def onPointClicked(self, point):
        print "estou no onpointcliocked"
        layer = self.iface.activeLayer()
        if not layer or layer.type() != QgsMapLayer.VectorLayer or layer.geometryType() != QGis.Point:
            QMessageBox.information(self.iface.mainWindow(), "PS Time Series Viewer", u"Select a vector layer and try again.")
            return
            
            # set the waiting cursor
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                dlg = self._onPointClicked( layer, point )
            finally:
                # restore the cursor
                QApplication.restoreOverrideCursor()
                
            #if dlg:
            #    dlg.exec_()
                
            #self.run()   
            
    def _onPointClicked(self, ps_layer, point):
        # get the id of the point feature under the mouse click
        from .MapTools import *
        fid = FeatureFinder.findAtPoint(ps_layer, point, canvas=self.iface.mapCanvas(), onlyTheClosestOne=True, onlyIds=True)
        if fid is None:
            return
            
        # get the attribute map of the selected feature
        feat = QgsFeature()
        feats = ps_layer.getFeatures( QgsFeatureRequest(fid) )
        feats.nextFeature(feat)
        attrs = feat.attributes()
        
        print attrs
        
     
    def handleLayerChange(self, layer):
        self.cLayer = self.canvas.currentLayer()
        if self.cLayer:
            self.provider = self.cLayer.dataProvider()

    def select_output_file(self):
        global nameloadfile
        filename     = QFileDialog.getOpenFileName(self.dlg, "Select output file ","", '*.*')
        nameloadfile = start_rwt.format_rwt_file(filename,self)
        layer        = iface.activeLayer()   # Cria uma layer 
        start_rwt.update_rwt_form(layer,self,filename)
        
#        if nameloadfile=='StAMPs':
#            start_rwt.update_stp_rwt_form(layer,self,filename)
#        
        print"estou no selectfile:",nameloadfile
        
    def run(self):
        """Run method that performs all the real work"""
        global loscheck
        global nameloadfile
        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        print result 
        print "resultado"
        if result:
            filename      = self.dlg.lineEdit.text()
            form_values = start_rwt.read_filter_form(self)
            #start_rwt.creat_rwt_files(layer,filename,last,lyr)
            print filename
            
            # Teste if los has select 
            if loscheck ==1:
                start_rwt.creat_rwt_los_csvfiles(nameloadfile,filename,form_values)
                start_rwt.creat_vel_layer(nameloadfile,filename)
                
            # Teste if HEIGH has select     		
            if heighcheck ==1:
                start_rwt.creat_rwt_heigh_csvfiles(nameloadfile,filename,form_values)
                start_rwt.creat_heigh_layer(nameloadfile,filename)
                
            if cohercheck ==1:
                #start_rwt.creat_rwt_heigh_csvfiles(nameloadfile,filename,form_values)
                #start_rwt.creat_heigh_layer(nameloadfile,filename)
                
                
                name=filename.split('/')
                CoheFlnm='COHERENCE'
                last=name[-1]
                cohefile = filename.replace(last,"QGCOHER.csv")
                CoheFile="file:///"+cohefile
                uricohe = CoheFile+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % (",","LON","LAT")
                CoheLayer = QgsVectorLayer(uricohe, CoheFlnm, "delimitedtext")
                CoheLayer.isValid()
                QgsMapLayerRegistry.instance().addMapLayer(CoheLayer)
                # Colormap
                targetField = 'COHER'
                classes = 8
                mode = QgsGraduatedSymbolRendererV2.EqualInterval
                symbol = QgsSymbolV2.defaultSymbol(VelLayer.geometryType())
                colorRamp = QgsVectorGradientColorRampV2.create({'color1' : '255,0,0,255', 'color2' : '0,0,255,255', 'stops':'0.25;255,180,0,255:0.50;0,255,0,255:0.75;0,212,212,255'})
                renderer = QgsGraduatedSymbolRendererV2.createRenderer(CoheLayer, targetField, classes, mode, symbol, colorRamp)
                CoheLayer.setRendererV2(renderer)
                
                
#            #--- 3 Set file name here
#            pedro=filename
#            InFlnm='visSTAMPS'
#            #--- 4  Set pathname here
#            #InDrPth='C:/Users/Pedro/Desktop/'
#            InDrPth=filename
#            #--- 5 Build file name an path for uri
#            InFlPth="file:///"+InDrPth
#            #---  6 Set import Sting here note only need to set x and y other come for free
#            uri1 = InFlPth+"?delimiter=%s&xField=%s&yField=%s" % (",","LON","LAT")
#            #--- 7 Load point layer
#            bh = QgsVectorLayer(uri1, InFlnm, "delimitedtext")
#			#--- 8 Confirm something is loaded and valid
#            bh.isValid()
#			#--- 9 Set CRS
#            #bh.setCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId))
#			#--- 10 Display the layer into QGIS (but it asks for CRS before displaying_
#            QgsMapLayerRegistry.instance().addMapLayer(bh)
#            renderer = bh.rendererV2()
#            symbol = renderer.symbol()
#            symbol.dump()
#            symbol.setColor(QColor('#800000'))
#            #features = bh.getFeatures()
#            #pedro=features['LAT']
#            #print pedro
#            #f = features.next()
#            #f.attributes()
#            #print f.attributes()
#            #for f in bh.getFeatures():
#            #    minlat=f['LAT']
#            #    minlong= f['LON']
#            #    print minlat