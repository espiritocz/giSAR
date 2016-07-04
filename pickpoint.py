#from qgis.gui import *
#from PyQt4.QtGui import QAction, QMainWindow
#
#
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
#
#from qgis.core import *
#from qgis.gui import *
#
#class MyWnd(QMainWindow):
#  def __init__(self, layer):
#    QMainWindow.__init__(self)
#
#    self.canvas = QgsMapCanvas()
#    self.canvas.setCanvasColor(Qt.white)
#
#    self.canvas.setExtent(layer.extent())
#    self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
#
#    self.setCentralWidget(self.canvas)
#
##    actionZoomIn = QAction(QString("Zoom in"), self)
##    actionZoomOut = QAction(QString("Zoom out"), self)
##    actionPan = QAction(QString("Pan"), self)
##
##    actionZoomIn.setCheckable(True)
##    actionZoomOut.setCheckable(True)
##    actionPan.setCheckable(True)
##
##    self.connect(actionZoomIn, SIGNAL("triggered()"), self.zoomIn)
##    self.connect(actionZoomOut, SIGNAL("triggered()"), self.zoomOut)
##    self.connect(actionPan, SIGNAL("triggered()"), self.pan)
##
##    self.toolbar = self.addToolBar("Canvas actions")
##    self.toolbar.addAction(actionZoomIn)
##    self.toolbar.addAction(actionZoomOut)
##    self.toolbar.addAction(actionPan)
#
#    # create the map tools
#    self.toolPan = QgsMapToolPan(self.canvas)
#    self.toolPan.setAction(actionPan)
#    self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
#    self.toolZoomIn.setAction(actionZoomIn)
#    self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
#    self.toolZoomOut.setAction(actionZoomOut)
#
#    self.pan()
#
#  def zoomIn(self):
#    self.canvas.setMapTool(self.toolZoomIn)
#
#  def zoomOut(self):
#    self.canvas.setMapTool(self.toolZoomOut)
#
#  def pan(self):
#    self.canvas.setMapTool(self.toolPan)

def run(self):
    self.pointEmitter = QgsMapToolEmitPoint(self.iface.mapCanvas())
    QObject.connect( self.pointEmitter, SIGNAL("canvasClicked(const QgsPoint, Qt::MouseButton)"), self.selectNow)
    self.iface.mapCanvas().setMapTool( self.pointEmitter )

def selectNow(self, point, button):
  #QMessageBox.information(None, "Clicked coords", " x: " + str(point.x()) + " Y: " + str(point.y()) )

  layer = self.iface.activeLayer()
  if not layer or layer.type() != QgsMapLayer.VectorLayer:
     QMessageBox.warning(None, "No!", "Select a vector layer")
     return

  width = self.iface.mapCanvas().mapUnitsPerPixel() * 2
  rect = QgsRectangle(point.x() - width,
                      point.y() - width,
                      point.x() + width,
                      point.y() + width)

  rect = self.iface.mapCanvas().mapRenderer().mapToLayerCoordinates(layer, rect)

  layer.select([], rect)
  feat = QgsFeature()

  ids = []
  while layer.nextFeature(feat):
    ids.append( feat.id() )

  layer.setSelectedFeatures( ids )