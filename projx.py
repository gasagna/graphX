import sys

import numpy as np
from PyQt4 import QtCore,QtGui

"""WISHES:
* mettere icona vicino ad ogni punto con il colore del punto
* dockbar con tipi di simboli e colori
* regression tool
* cursore con zoom
"""

"""TODO:
* double click on an rectpoint ask true positions
* logarithmic mapping
* quando fai il wheelEvent fai si che zoomi nella posizione voluta.
* reorder and complete help list
"""

"""BUGS:
* sistema il drag and drop dei vari elementi
* quadrato dello zoom o selezione
* se il file di immagine non is buono scrivi un messaggio
"""

zoomFactor = 1.05

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.imageView = ImageView(parent=self)
        self.setCentralWidget( self.imageView )
        self.resize(900, 700)
        
        # make widgets
        self.makePropertiesDockWidget()
        self.makePointsDockWidget()
        self.makeToolBar()
        self.makeStatusBar()
        
    def makeToolBar( self ):
        # make toolbar
        loadImageAction = QtGui.QAction(QtGui.QIcon.fromTheme("insert-image"), 'Load Image', self)
        loadImageAction.setShortcut('l')
        loadImageAction.setToolTip( QtCore.QString("Load an image into the application") )
        loadImageAction.triggered.connect( self.imageView.on_load_image_clicked )
        loadImageAction.setCheckable(False)
        
        drawAxisAction = QtGui.QAction(QtGui.QIcon.fromTheme("select-rectangular"), 'Draw Axis', self)
        drawAxisAction.setShortcut('d')
        drawAxisAction.setEnabled(False)
        drawAxisAction.setCheckable(True)
        drawAxisAction.setToolTip( QtCore.QString("Set known points value on the figure") )
        drawAxisAction.triggered.connect( self.imageView.setDrawAxisMode )

        addPointAction = QtGui.QAction(QtGui.QIcon.fromTheme("edit-node"), 'Add Point', self)
        addPointAction.setShortcut('a')
        addPointAction.setEnabled(False)
        addPointAction.setCheckable(True)
        addPointAction.setToolTip( QtCore.QString("Add points to the figure, to compute the true value") )
        addPointAction.triggered.connect( self.imageView.setAddPointMode )

        selectPointsAction = QtGui.QAction(QtGui.QIcon.fromTheme("edit-select"), 'Select Points', self)
        selectPointsAction.setShortcut('s')
        selectPointsAction.setCheckable(True)
        selectPointsAction.setEnabled(False)
        selectPointsAction.setToolTip( QtCore.QString("Select points") )
        selectPointsAction.triggered.connect( self.imageView.setSelectPointMode )
        
        panAction = QtGui.QAction(QtGui.QIcon.fromTheme("transform-move"), 'Pan view', self)
        panAction.setShortcut('p')
        panAction.setCheckable(True)
        panAction.setEnabled(False)
        panAction.setToolTip( QtCore.QString("Move the image into the view") )
        panAction.triggered.connect( self.imageView.setPanMode )

        zoomAction = QtGui.QAction(QtGui.QIcon.fromTheme("zoom-select"), 'Zoom tool', self)
        zoomAction.setShortcut('z')
        zoomAction.setCheckable(True)
        zoomAction.setEnabled(False)
        zoomAction.setToolTip( QtCore.QString("Zoom tool") )
        zoomAction.triggered.connect( self.imageView.setZoomMode)

        fitAction = QtGui.QAction(QtGui.QIcon.fromTheme("zoom-fit-best"), 'Fit View', self)
        fitAction.setShortcut('f')
        fitAction.setCheckable(False)
        fitAction.setEnabled(False)
        fitAction.setToolTip( QtCore.QString("Fit the view to the image") )
        fitAction.triggered.connect( self.imageView.fit )
        
        
        fitObjectsAction = QtGui.QAction(QtGui.QIcon.fromTheme("zoom-draw"), 'Fit Objects', self)
        fitObjectsAction.setShortcut('o')
        fitObjectsAction.setCheckable(False)
        fitObjectsAction.setEnabled(False)
        fitObjectsAction.setToolTip( QtCore.QString("Fit the view to the selected objects") )
        fitObjectsAction.triggered.connect( self.imageView.fitObjects )

    
        self.toolbar = QtGui.QToolBar()
        self.toolbar.actions = { 'loadImageAction'     : loadImageAction,
                                 'drawAxisAction'      : drawAxisAction,
                                 'addPointAction'      : addPointAction,
                                 'selectPointsAction'  : selectPointsAction,
                                 'panAction'           : panAction,
                                 'zoomAction'          : zoomAction,
                                 'fitAction'           : fitAction,
                                 'fitObjectsAction'     : fitObjectsAction,                                   }
                            
        self.toolbar.setToolButtonStyle( QtCore.Qt.ToolButtonTextUnderIcon )
        self.toolbar.addAction(loadImageAction)
        self.toolbar.addAction(drawAxisAction)
        self.toolbar.addAction(addPointAction)
        self.toolbar.addAction(selectPointsAction)
        self.toolbar.addAction(panAction)
        self.toolbar.addAction(zoomAction)
        self.toolbar.addAction(fitAction)
        self.toolbar.addAction(fitObjectsAction)
        
        self.addToolBar( self.toolbar )
        
    def makeStatusBar( self ):
        # statusbar
        sb = QtGui.QStatusBar( self )
        sb.setFixedHeight(20)
        self.setStatusBar(sb)
        
        # labels for the status bar
        label = QtGui.QLabel(QtCore.QString('Ready'))
        self.statusBar().addPermanentWidget( label )
        self.statusBar().statusLabel = label
        
        label = QtGui.QLabel(QtCore.QString(''))
        self.statusBar().insertWidget( 0, label )
        self.statusBar().positionLabel = label

    def save_text_file( self ):
        pass

    def makePointsDockWidget( self ):
        self.pointDock = QtGui.QDockWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.pointDock.setSizePolicy(sizePolicy)
        self.pointDock.setWindowTitle("Points")

        # build table for points
        self.pointsTable = QtGui.QTreeWidget( self )
        item = QtGui.QTreeWidgetItem()
        item.setText(0, 'x')
        item.setText(1, 'y')
        self.pointsTable.setHeaderItem(item)
        self.pointsTable.setColumnCount(2)
        
        # build button box
        hbox = QtGui.QHBoxLayout()
        button = QtGui.QPushButton( 'Save these points' )
        hbox.addStretch()
        hbox.addWidget(button)
        
        # build dockwidget widget
        widget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.pointsTable)
        vbox.addLayout(hbox)
        widget.setLayout(vbox)
        
        self.pointDock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.pointDock)
        self.pointDock.hide()
        
    def makeRectDockWidget( self ):
        self.rectDock = QtGui.QDockWidget()
        self.rectDock.setWindowTitle("Rectangle Points")

        # build table for points
        self.rectTable = RectTable(self)
        
        # build dockwidget widget
        widget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        widget.setSizePolicy(sizePolicy)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.rectTable)
        widget.setLayout(vbox)
        
        self.rectDock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.rectDock)
        self.rectDock.hide()
        
    def makePropertiesDockWidget( self ):
        self.propDock = QtGui.QDockWidget()
        self.propDock.setWindowTitle("Axis Properties")

        # build dockwidget widget
        widget = QtGui.QWidget(self)
        gridLayout = QtGui.QGridLayout(widget)
        xlabel = QtGui.QLabel('X-axis')
        gridLayout.addWidget(xlabel, 0, 0, 1, 1)
        self.xComboBox = QtGui.QComboBox(widget)
        self.xComboBox.addItems( ['linear', 'logarithmic'] )
        gridLayout.addWidget(self.xComboBox, 0, 1, 1, 1)
        ylabel = QtGui.QLabel('Y-label')
        gridLayout.addWidget(ylabel, 1, 0, 1, 1)
        self.yComboBox = QtGui.QComboBox(widget)
        self.yComboBox.addItems( ['linear', 'logarithmic'] )
        gridLayout.addWidget(self.yComboBox, 1, 1, 1, 1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        widget.setSizePolicy(sizePolicy)
        #widget.setLayout(gridlayout)
        
        self.propDock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.propDock)
        self.propDock.hide()


class RectTable( QtGui.QTableWidget):
    def __init__( self, parent ):
        QtGui.QTableWidget.__init__( self, parent )
        self.horizontalHeader().setStretchLastSection(True)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels( ['x', 'y'] )
        self.setRowCount(4)
        self.counter = 0
        
    def displayPoint( self, rectPoint ):
        xitem = QtGui.QTableWidgetItem( "%.2e" % rectPoint.truePos().x() )
        yitem = QtGui.QTableWidgetItem( "%.2e" % rectPoint.truePos().y() )
        self.setItem(self.counter, 0, xitem)
        self.setItem(self.counter, 1, yitem)
        self.counter += 1


class ImageView( QtGui.QGraphicsView ):
    def __init__(self, parent=None):
        """A custom graphics view"""
        # init
        QtGui.QGraphicsView.__init__(self, parent)
        # set background Color
        self.setBackgroundBrush( QtGui.QBrush(QtGui.QColor(126,126,126,255)))
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        # show init message
        self.init_message()

        # connect to slots
        self.connect( self, QtCore.SIGNAL('clicked()'), self.on_load_image_clicked )

        # do we already have an image to display?
        self.imagePixmap = None

        # in which mode are we?
        self.mode = None

        # which element should we drag
        self.dragging = None

        # list of selected items
        self.selected = None

        # initial point of zoom rectangle
        self.initialZoomPoint = None
        self.zoomRect = QtGui.QGraphicsRectItem()
        
        # initial point of the selection rectangle
        self.initialSelectionPoint = None
        self.selectionRect = QtGui.QGraphicsRectItem()

        # get position of the cursor
        self.setMouseTracking(True)
        self.setAcceptDrops(True) 

        # a group of 4 points used to draw the axes polygon
        self.axis_points = []

        # the data points of which we want to extract the coordinates
        self.points = []

        # the pAth defining the axes rectangle
        self.path = QtGui.QGraphicsPathItem()

        # do we have defined a rectangle
        self.has_rect = False

        # mapper to go from scene position to true position
        self.mapper = Mapper()

        # is the help screen shown?
        self.help_is_shown = False
        
        self.lastPos = False

    def init_message(self):
        """Show greating message."""

        # create font
        font = QtGui.QFont('Sans', 20)

        # create
        scene = QtGui.QGraphicsScene()
        main_text = scene.addText( "Click here to load an image", font )

        # create font
        font = QtGui.QFont('Sans', 11)
        hint_text = scene.addText( "press ? for help at anytime", font )
        hint_text.setDefaultTextColor( QtGui.QColor("#323232") )
        hint_text.setPos( 90, 35 )

        self.setScene(scene)

    def fit ( self ):
        self.fitInView( self.scene().sceneRect(), QtCore.Qt.KeepAspectRatio)

    def fitObjects ( self ):
        group = QtGui.QGraphicsItemGroup()
        self.scene().addItem(group)
        for item in self.scene().selectedItems():
            group.addToGroup( item )
        self.fitInView( group, QtCore.Qt.KeepAspectRatio)
        self.scene().destroyItemGroup(group)

    def on_load_image_clicked( self ):
        """Get an image and show it."""
        # get filename
        filename = QtGui.QFileDialog.getOpenFileName()

        # we have a pixmap
        image = QtGui.QPixmap(filename)

        # build scene
        self.scene().clear()
        self.scene().setSceneRect( 0, 0, image.width(), image.height() )
        self.imagePixmap = self.scene().addPixmap( image )
        
        # show docks
        self.parent().pointDock.show()
        #self.parent().propDock.show()
        
        # fit view
        self.fitInView( self.scene().sceneRect(), QtCore.Qt.KeepAspectRatio)
        
        # enable some actions
        self.parent().toolbar.actions['drawAxisAction'].setEnabled(True)
        self.parent().toolbar.actions['selectPointsAction'].setEnabled(True)
        self.parent().toolbar.actions['zoomAction'].setEnabled(True)
        self.parent().toolbar.actions['panAction'].setEnabled(True)
        self.parent().toolbar.actions['fitAction'].setEnabled(True)
        self.parent().toolbar.actions['fitObjectsAction'].setEnabled(True)
        
    def sendSBMode(self):
        self.parent().statusBar().statusLabel.setText( self.mode )

    def sendSBPosition( self, point ):
        self.parent().statusBar().positionLabel.setText( QtCore.QString("Cursor at %.3e, %.3e" % (point.x(), point.y())))

    def setDrawAxisMode(self):
        """"""
        self.mode = 'drawAxisMode'
        self.sendSBMode()
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        
        for action in self.parent().toolbar.actions.values():
            action.associatedWidgets()[1].setChecked(False)
        
        self.parent().toolbar.actions['drawAxisAction'].associatedWidgets()[1].setChecked(True)

    def setAddPointMode(self):
        """"""
        self.mode = 'addPointMode'
        self.sendSBMode()
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        
        for action in self.parent().toolbar.actions.values():
            action.associatedWidgets()[1].setChecked(False)
        self.parent().toolbar.actions['addPointAction'].associatedWidgets()[1].setChecked(True)

    def setSelectPointMode(self):
        """"""
        self.mode = 'selectMode'
        self.sendSBMode()
        QtGui.QApplication.restoreOverrideCursor()
        
        for action in self.parent().toolbar.actions.values():
            action.associatedWidgets()[1].setChecked(False)
        self.parent().toolbar.actions['selectPointsAction'].associatedWidgets()[1].setChecked(True)

    def setZoomMode(self):
        """"""
        self.mode = 'zoomMode'
        self.sendSBMode()
        QtGui.QApplication.restoreOverrideCursor()
        for action in self.parent().toolbar.actions.values():
            action.associatedWidgets()[1].setChecked(False)
        self.parent().toolbar.actions['zoomAction'].associatedWidgets()[1].setChecked(True)
        
    def setPanMode(self):
        """"""
        self.mode = 'panMode'
        self.sendSBMode()
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.parent().toolbar.actions['panAction'].associatedWidgets()[1].setChecked(True)

    def saveToFile( self ):
        pass

    def wheelEvent( self, event ):
        if self.imagePixmap:
            if event.delta() > 0:
                # zoom towards the cursor
                cursor = QtGui.QCursor()
                #print cursor.pos()
                #print self.mapFromGlobal(cursor.pos())
                #print self.mapToScene(self.mapFromGlobal(cursor.pos()))
                #pos = cursor.pos()
                self.scale(zoomFactor, zoomFactor)
                #self.centerOn( self.mapToScene(self.mapFromGlobal(pos)) )
            else:
                self.scale( 1/zoomFactor, 1/zoomFactor)

    def keyPressEvent( self, event ):
        """Handle key press events"""

        if event.key() == QtCore.Qt.Key_F:
            self.fitInView( self.scene().sceneRect(), QtCore.Qt.KeepAspectRatio)

        if event.key() == QtCore.Qt.Key_X:
            cursor = QtGui.QCursor()
            self.centerOn( QtCore.QPointF( self.mapToScene(self.mapFromGlobal(cursor.pos()))) )

        if event.key() == QtCore.Qt.Key_Question:
            if not self.help_is_shown:
                self.help_is_shown = True
                self.overlay = HelpOverlay(self)
                self.overlay.show()

        if event.key() == QtCore.Qt.Key_Escape:
            if self.help_is_shown:
                self.overlay.hide()
                self.help_is_shown = False

        # if something is selected move it with the arrow
        if self.scene().selectedItems():
            if event.key() == QtCore.Qt.Key_Up:
                deltax, deltay = 0, -0.05
            elif event.key() == QtCore.Qt.Key_Down:
                deltax, deltay = 0, 0.05
            elif event.key() == QtCore.Qt.Key_Left:
                deltax, deltay = -0.05, 0
            elif event.key() == QtCore.Qt.Key_Right:
                deltax, deltay = 0.05, 0
            else:
                deltax, deltay = 0, 0

            if event.modifiers() == QtCore.Qt.ControlModifier:
                deltax *= 20
                deltay *= 20
            if event.modifiers() == QtCore.Qt.ShiftModifier:
                deltax *= 200
                deltay *= 200

            # move each point
            for item in self.scene().selectedItems():
                item.move(deltax, deltay)
    
            # then redraw axis rectangle
            self.draw_axis_rect()

    def mousePressEvent( self, event ):
        # LOAD IMAGE INTO VIEW
        if event.button() == 1 and not self.imagePixmap:
            self.on_load_image_clicked()
            
        # DRAW AXIS POINTS
        elif event.button() == 1 and self.mode == 'drawAxisMode':
            # if we dont already have a rect
            if not self.has_rect:
                # if we click on the image
                if self.itemAt( event.pos() ):
    
                    rpoint = RectPoint( self.mapToScene(event.pos()),
                            min( self.imagePixmap.pixmap().width(), self.imagePixmap.pixmap().height()),
                            counter=len(self.axis_points) )
                            
                    ok = rpoint.askTruePos( )
                    
                    if ok:
                        self.scene().addItem( rpoint )
                        self.axis_points.append( rpoint )
    
                    if len(self.axis_points) == 4:
                        self.has_rect = True
                        self.draw_axis_rect()
                        self.mode = "Ready"
                        self.sendSBMode()
                        QtGui.QApplication.restoreOverrideCursor()
                        # set draw axis action enabled
                        self.parent().toolbar.actions['addPointAction'].setEnabled(True)
                    
        # ADD POINTS, these are the data point of which we want to obtain the position
        elif event.button() == 1 and self.mode == 'addPointMode':
            # if we click on the image
            if self.itemAt( event.pos() ):

                # create ellipse item
                ell = Point( self.mapToScene(event.pos()), min( self.imagePixmap.pixmap().width(), self.imagePixmap.pixmap().height() ), parent=self.scene() )

                # add it to the scene and get pointer
                pointer = self.scene().addItem( ell )

                # remember added points
                self.points.append( pointer )
                
                # build item and create
                truepoint = self.mapper.map(ell.scenePos())
                item = QtGui.QTreeWidgetItem()
                item.setText( 0, "%.2e" % truepoint.x() )
                item.setText( 1, "%.2e" % truepoint.y() )
                self.parent().pointsTable.addTopLevelItem(item)
                
        # SELECT POINTS
        elif event.button() == 1 and self.mode == 'selectMode':
            
            #if isinstance( self.itemAt( event.pos() ), RectPoint):
            #    self.itemAt( event.pos()).mouseDoubleClickEvent( event )
            
            self.hasMoved = False
            
            # point of the rectangle of selection
            self.initialSelectionPoint = event.pos()
            
            # get clicked item
            item = self.itemAt( event.pos() )
            
            # if it is a point highlight it, otherwise clear selection
            if isinstance( item, Point ) or isinstance( item, RectPoint ) :
                if item.isSelected():
                    item.setSelected(False)
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    item.setSelected(True)
                else:
                    self.scene().clearSelection()
                    item.setSelected(True)
            else:
                self.scene().clearSelection()
            
        # ZOOM MODE
        elif event.button() == 1 and self.mode == 'zoomMode':
            self.initialZoomPoint = event.pos()
            
        # PAN MODE
        elif event.button() == 1 and self.mode == 'panMode':
            self.lastPos = QtCore.QPoint(QtGui.QCursor.pos())
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
            self.startScroll = (self.horizontalScrollBar().value(),
                                    self.verticalScrollBar().value())

    def mouseMoveEvent(self, event):
        # if we have drawn a rectangle
        if self.has_rect:
    
            # get true position
            truepos = self.mapper.map( QtCore.QPointF( self.mapToScene( event.pos() ) ) )
            
            # send message to statusbar
            self.sendSBPosition( truepos )
        
        if self.mode == 'selectMode':
            self.hasMoved = True
            if self.initialSelectionPoint is None:
                return
                
            # this is the zoom rectangle
            selectionRect = QtCore.QRectF( QtCore.QPointF(self.mapToScene(self.initialSelectionPoint)), QtCore.QPointF( self.mapToScene(event.pos() )))
            # remove old rectangle
            self.scene().removeItem(self.selectionRect)
            # add new rectangle
            self.selectionRect = self.scene().addRect(selectionRect, QtGui.QPen(QtCore.Qt.SolidLine), QtGui.QBrush(QtGui.QColor(187,48,51,10)))
            
            # if there is nothing to be dragged
            #if not self.scene().selectedItems():
            #    return

            # this is the location of the click and drag event
            #point = self.mapToScene(event.pos())

            # compute distance and move items
            #dx = self.clickDragPosition.x()-point.x()
            #dy = self.clickDragPosition.y()-point.y()
            #for item in self.scene().selectedItems():
            #    item.move(dx, dy)
            
            # draw axis rectangle
            #if self.has_rect:
            #    self.draw_axis_rect()

        elif self.mode == 'zoomMode':
            # if we are is zoom mode
            if self.initialZoomPoint is None:
                return

            # this is the zoom rectangle
            zoomRect = QtCore.QRectF( QtCore.QPointF(self.mapToScene(self.initialZoomPoint)), QtCore.QPointF( self.mapToScene(event.pos() )))
            # remove old rectangle
            self.scene().removeItem(self.zoomRect)
            # add new rectangle
            self.zoomRect = self.scene().addRect(zoomRect, QtGui.QPen(QtCore.Qt.DashLine), QtGui.QBrush(QtGui.QColor(20,20,250,10)))
            
        elif self.mode == 'panMode':
            if self.lastPos:
                globalPos = QtGui.QCursor.pos()
                self.horizontalScrollBar().setValue(self.startScroll[0] -
                                                        globalPos.x() +
                                                        self.lastPos.x())
                self.verticalScrollBar().setValue(self.startScroll[1] -
                                                        globalPos.y() +
                                                        self.lastPos.y())
                                                    
    def mouseReleaseEvent(self, event):
        # delete zoom rectangle and fit view
        if self.initialZoomPoint:
            self.fitInView( self.zoomRect, QtCore.Qt.KeepAspectRatio )
            try:
                self.scene().removeItem(self.zoomRect)
            except:
                pass
            
        # delete selection rectangle and select points
        if self.initialSelectionPoint and self.hasMoved:
            path = QtGui.QPainterPath()
            path.addRect( self.selectionRect.rect() )
            self.scene().setSelectionArea( path )
            try:
                self.scene().removeItem(self.selectionRect)
            except:
                pass

        # reset things
        self.dragging = None
        self.initialZoomPoint = None
        self.initialSelectionPoint = None
        self.hasMoved=False
        self.lastPos = False

    def draw_axis_rect( self ):
        if self.has_rect:
            # get new points
            points = []
            for item in self.axis_points:
                points.append(  QtCore.QPointF( item.scenePos().x(), item.scenePos().y() ) )
    
            # redefine polygon defining axis
            axis_rect = QtGui.QPainterPath( points[0] )
            for i in range(1,4):
                axis_rect.lineTo( points[i] )
            axis_rect.closeSubpath()
    
            # color of the polygon line
            color = QtGui.QColor("#700094")
    
            # remove old path
            self.scene().removeItem(self.path)
    
            # draw new path
            self.path = self.scene().addPath( axis_rect, QtGui.QPen(color), QtGui.QBrush(QtGui.QColor(50,50,250,5)) )
            
            # compute mapping from scene to true coordinates
            self.mapper.fit( scene_pos = [ (el.scenePos().x(), el.scenePos().y()) for el in self.axis_points],
                              true_pos = [ (el.truePos.x(), el.truePos.y()) for el in self.axis_points ] )

    def contextMenuEvent(self, event):
        #change value of point
        #changeValueAction = QtGui.QAction(QtGui.QIcon(''), 'Change true value', self)
        #changeValueAction.triggered.connect( self.ask_coordinate )

        #menu = QtGui.QMenu( self )
        #menu.addAction(changeValueAction)

        ## if we are clicking on one of the axes rect ellispes
        #if self.itemAt( event.pos() ) in self.axis_points:
        #    menu.exec_(self.mapToGlobal(event.pos()))
        pass


class HelpOverlay(QtGui.QWidget):
    """A Gmail-like help screen"""
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.resize( self.parent().size())

    def paintEvent(self, event):
        # get new size of the parent (qgraphicsview)
        self.resize( self.parent().size().width(), self.parent().size().height() )

        # begin painting
        painter = QtGui.QPainter()
        painter.begin(self)

        # set some properties
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen( QtGui.QPen(QtGui.QColor(2, 2, 2, 200)) )
        painter.setBrush( QtGui.QBrush(QtGui.QColor(100, 100, 100, 250)) )

        # draw bounding  rect
        delta = 50
        rect = QtCore.QRectF( delta, delta, self.parent().size().width()-2*delta, self.parent().size().height()-2*delta, )
        painter.drawRoundedRect(rect, 10, 10)

        #draw title
        painter.setFont( QtGui.QFont("Monospace", 22) )
        title_rect = QtCore.QRectF( self.parent().size().width()/2 - 90, 140, 350, 100 )
        painter.drawText( title_rect, QtCore.QString('Shortcuts') )

        # draw shortcuts
        cfont = QtGui.QFont("Monospace", 11)
        cfont.setBold(True)
        painter.setFont(cfont)

        # all the shortcuts
        keys = { 'd': "Draw axes",
                 'a': "Add point",
                 's': "Select tool",
                 'z': "Zoom tool",
                 'x': "Pan view to cursor position",
                 'f': "Fit image to window",
                 '?': "Show this help screen",
                 'mouse wheel': "Zoom",
                 'right click': "select a point",
                 'Esc': "Hide this help screen",
                 'arrows': "Move selected point",
                 'Ctrl + arrows': "Move selected point a little bit more",
                 'Shift + arrows': "Move selected point a much more",
                 'Esc': "Hide this help screen",
                 }

        # spacing between keys
        spacing = 20

        # write
        for i, (key, value) in enumerate( keys.iteritems() ):
            key_rect = QtCore.QRectF( self.parent().width()/2-220, 250+i*spacing, 500, 100 )
            painter.drawText( key_rect, QtCore.QString('%s : %s' % (key.rjust( max( map(len, keys.keys()) )), value)) )


        # end
        painter.end()


class Mapper( object ):
    def __init__ ( self ):
        pass

    def fit(self, scene_pos, true_pos ):
        """Solve linear system for mapping"""

        # arrays of scene position
        xs = np.array( scene_pos )[:,0].reshape(-1,1)
        ys = np.array( scene_pos )[:,1].reshape(-1,1)

        # arrays of true position
        xt = np.array( true_pos )[:,0].reshape(-1,1)
        yt = np.array( true_pos )[:,1].reshape(-1,1)

        # matrix for coefficients
        V = np.hstack( (xs, ys, xs*ys, np.ones_like(xs)) ).astype(np.float32)

        # solution of the linear transform
        self._coeffsX = np.linalg.solve( V, xt )
        self._coeffsY = np.linalg.solve( V, yt )

    def map( self, point ):
        """Map from scene to true value"""
        xt = self._coeffsX[0]*point.x() + self._coeffsX[1]*point.y() + self._coeffsX[2]*point.y()*point.x() + self._coeffsX[3]
        yt = self._coeffsY[0]*point.x() + self._coeffsY[1]*point.y() + self._coeffsY[2]*point.y()*point.x() + self._coeffsY[3]
        return QtCore.QPointF( xt, yt )


class Point( QtGui.QGraphicsItem ):
    
    # class properties
    size = 0.015 
    edgeColor = QtGui.QColor(0, 0, 0, 200)
    selectedEdgeColor = QtGui.QColor('red')
    faceColor = QtGui.QColor(164, 84, 188, 200)
    
    def __init__ ( self, pointCenter, imageSize):
        # size of the circle
        self.circleSize = imageSize*self.size
        
        # rect of the circle
        self.rect = QtCore.QRectF( pointCenter.x()-self.circleSize/2, pointCenter.y()-self.circleSize/2, self.circleSize, self.circleSize)
        
        # create  ellipse
        QtGui.QGraphicsItem.__init__(self)
        self.setAcceptHoverEvents( True )
        self.setAcceptDrops(True)
        self.setFlags( QtGui.QGraphicsItem.ItemIsSelectable )
        
        # are we on the ellipse?
        self.hovering = False
        
    def scenePos( self ):
        return QtCore.QPointF( self.rect.x()+self.circleSize/2, self.rect.y()+self.circleSize/2)
        
    def boundingRect(self):
        return QtCore.QRectF( self.rect.x()-self.circleSize,
                              self.rect.y()-self.circleSize,
                              self.circleSize*3, 
                              self.circleSize*3)

    def paint(self, painter, option, widget):
       
        if self.isSelected():
            ec = self.selectedEdgeColor
        else:
            ec = self.edgeColor

        # draw ellipse
        path = QtGui.QPainterPath()
        path.addEllipse( self.rect )

        # draw path
        painter.fillPath(path, QtGui.QBrush(self.faceColor))
        painter.setPen(QtGui.QPen(ec, 1) )
        painter.drawEllipse( self.rect )
    
    def move( self, dx, dy):
        self.prepareGeometryChange()
        self.rect = QtCore.QRectF(self.rect.x()+dx, self.rect.y()+dy, self.circleSize, self.circleSize )


class RectPoint( Point ):
    
    # class properties
    size = 0.025
    edgeColor = QtGui.QColor(0, 0, 0, 200)
    selectedEdgeColor = QtGui.QColor('red')
    faceColor = QtGui.QColor(80, 164, 67, 200)

    def __init__( self, pointCenter, imageSize, counter ):
        super(RectPoint, self).__init__( pointCenter, imageSize )
        self._truePos = QtCore.QPointF(0,0)
        self.counter = counter
        
        # the small tet label we show for each rectangle point
        self.textItem = QtGui.QGraphicsTextItem( '(%.2e, %.2e)' % (self._truePos.x(), self._truePos.y()) )
        self.textItem.setPos( self.scenePos().x()-55, self.scenePos().y()-25 )
        self.textItem.setFont(QtGui.QFont('Monospace', 7))
        self.textItem.setParentItem(self)
        
    def setTruePos(self, truePos):
        self._truePos = truePos
        self.setToolTip( "Point %d is at: %.5e, %.5e)" % (self.counter+1, self._truePos.x(), self._truePos.y()) )
        self.textItem.setPlainText( '(%.2e, %.2e)' % (self._truePos.x(), self._truePos.y() ))
    
    def truePos(self):
        return self._truePos
        
    def move( self, dx, dy ):
        self.prepareGeometryChange()
        self.rect = QtCore.QRectF(self.rect.x()+dx, self.rect.y()+dy, self.circleSize, self.circleSize )
        self.textItem.setPos( self.scenePos().x()-55, self.scenePos().y()-25 )
        
    def paint(self, painter, option, widget):
       
        if self.isSelected():
            ec = self.selectedEdgeColor
        else:
            ec = self.edgeColor

        # draw ellipse
        path = QtGui.QPainterPath()
        path.addEllipse( self.rect )

        # fill ellipse
        painter.setPen(QtGui.QPen(ec, 0.05*self.circleSize) )
        painter.fillPath(path, QtGui.QBrush(self.faceColor))
        painter.drawEllipse( self.rect )
        
        # draw the cross
        path = QtGui.QPainterPath()
        path.moveTo( self.scenePos().x() - self.circleSize*0.46, self.scenePos().y() )
        path.lineTo( self.scenePos().x() + self.circleSize*0.46, self.scenePos().y() )
        painter.setPen(QtGui.QPen(QtGui.QColor('white'), 0.02*self.circleSize) )
        painter.drawPath(path)
        path.moveTo( self.scenePos().x(), self.scenePos().y()+self.circleSize*0.46 )
        path.lineTo( self.scenePos().x(), self.scenePos().y()-self.circleSize*0.46 )
        painter.drawPath(path)
        
    def mouseDoubleClickEvent(self, event):
        self.askCoordinates()
        
    def askTruePos( self ):
        
        # display error message function
        def showError():
            QtGui.QMessageBox.warning(self,
                "Error",
                "The inserted point is not valid")
        
        # open dialog
        dialog = QtGui.QInputDialog()
        dialog.setTextValue( "%f %f" % (self._truePos.x(), self._truePos.y()) )
        point, ok = dialog.getText(self, 'Input dialog', 'Enter true coordinates of the point, (separated by space):')
        
        if ok:
            try:
                pos = [float(element) for element in str(point).split()]
            except ValueError:
                showError()
                return 
        
        if len(pos) != 2:
            showError()
            return 
            
        self.setTruePos( pos )
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    sys.exit(app.exec_())

