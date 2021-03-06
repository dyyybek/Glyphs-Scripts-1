#MenuTitle: Copy Layer to Layer
# -*- coding: utf-8 -*-
__doc__="""
Copies one master to another master in selected glyphs.
"""

import GlyphsApp
import vanilla
import math

def getComponentScaleX_scaleY_rotation( thisComponent ):
		a = thisComponent.transform[0]
		b = thisComponent.transform[1]
		c = thisComponent.transform[2]
		d = thisComponent.transform[3]

		scale_x = math.sqrt(math.pow(a,2)+math.pow(b,2))
		scale_y = math.sqrt(math.pow(c,2)+math.pow(d,2))
		if (b<0 and c<0):
			scale_y = scale_y * -1

		rotation = math.atan2(b, a) * (180/math.pi)
		
		return [scale_x, scale_y, rotation]
		
		
class CopyLayerToLayer( object ):

	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 280
		windowHeight = 155
		windowWidthResize  = 120 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Copy layer to layer", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.mekkablue.CopyLayerToLayer.mainwindow" # stores last window position and size
		)
		
		self.w.text_1 = vanilla.TextBox((15, 12+2, 120, 14), "Copy paths from", sizeStyle='small')
		self.w.masterSource = vanilla.PopUpButton((120, 12, -15, 17), self.GetMasterNames(), sizeStyle='small', callback=self.MasterChangeCallback)
		
		self.w.text_2 = vanilla.TextBox((15, 32+2, 120, 14), "into selection of", sizeStyle='small')
		self.w.masterTarget = vanilla.PopUpButton((120, 32, -15, 17), self.GetMasterNames(), sizeStyle='small', callback=self.MasterChangeCallback)

		self.w.includeComponents = vanilla.CheckBox((15, 52+2, -100, 20), "Include components", sizeStyle='small', callback=self.SavePreferences, value=True)
		self.w.includeAnchors = vanilla.CheckBox((15, 52+20, -100, 20), "Include anchors", sizeStyle='small', callback=self.SavePreferences, value=True)
		self.w.includeMetrics = vanilla.CheckBox((15, 52+38, -100, 20), "Include metrics", sizeStyle='small', callback=self.SavePreferences, value=True)
		self.w.keepWindowOpen = vanilla.CheckBox((15, 52+56, -100, 20), "Keep window open", sizeStyle='small', callback=self.SavePreferences, value=True)

		self.w.copybutton = vanilla.Button((-80, -30, -15, -10), "Copy", sizeStyle='small', callback=self.buttonCallback)
		self.w.setDefaultButton( self.w.copybutton )
		
		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Copy Layer to Layer' could not load preferences. Will resort to defaults."
		
		self.w.open()
		self.w.makeKey()
		self.w.masterTarget.set(1)
	
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.mekkablue.CopyLayerToLayer.includeComponents"] = self.w.includeComponents.get()
			Glyphs.defaults["com.mekkablue.CopyLayerToLayer.includeAnchors"] = self.w.includeAnchors.get()
			Glyphs.defaults["com.mekkablue.CopyLayerToLayer.includeMetrics"] = self.w.includeMetrics.get()
			Glyphs.defaults["com.mekkablue.CopyLayerToLayer.keepWindowOpen"] = self.w.keepWindowOpen.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			NSUserDefaults.standardUserDefaults().registerDefaults_(
				{
					"com.mekkablue.CopyLayerToLayer.includeComponents" : "1",
					"com.mekkablue.CopyLayerToLayer.includeAnchors" : "1",
					"com.mekkablue.CopyLayerToLayer.includeMetrics" : "1",
					"com.mekkablue.CopyLayerToLayer.keepWindowOpen" : "1"
				}
			)
			self.w.includeComponents.set( Glyphs.defaults["com.mekkablue.CopyLayerToLayer.includeComponents"] )
			self.w.includeAnchors.set( Glyphs.defaults["com.mekkablue.CopyLayerToLayer.includeAnchors"] )
			self.w.includeMetrics.set( Glyphs.defaults["com.mekkablue.CopyLayerToLayer.includeMetrics"] )
			self.w.keepWindowOpen.set( Glyphs.defaults["com.mekkablue.CopyLayerToLayer.keepWindowOpen"] )
		except:
			return False
			
		return True
	
	def GetMasterNames( self ):
		"""Collects names of masters to populate the menus in the GUI."""
		thisFont = Glyphs.font
		myMasterList = []
		for masterIndex in range( len( thisFont.masters ) ):
			thisMaster = thisFont.masters[masterIndex]
			myMasterList.append( '%i: %s' % (masterIndex, thisMaster.name) )
		return myMasterList
	
	def MasterChangeCallback( self, sender ):
		"""Disables the button if source and target are the same."""
		if self.w.masterSource.get() == self.w.masterTarget.get():
			self.w.copybutton.enable( False )
		else:
			self.w.copybutton.enable( True )
			
	def copyPathsFromLayerToLayer( self, sourceLayer, targetLayer ):
		"""Copies all paths from sourceLayer to targetLayer"""
		numberOfPathsInSource  = len( sourceLayer.paths )
		numberOfPathsInTarget  = len( targetLayer.paths )
		
		if numberOfPathsInTarget != 0:
			print "- Deleting %i paths in target layer" % numberOfPathsInTarget
			targetLayer.paths = []

		if numberOfPathsInSource > 0:
			print "- Copying paths"
			for thisPath in sourceLayer.paths:
				newPath = thisPath.copy()
				targetLayer.paths.append( newPath )
	
	def copyComponentsFromLayerToLayer( self, sourceLayer, targetLayer ):
		"""Copies all components from sourceLayer to targetLayer."""
		numberOfComponentsInSource = len( sourceLayer.components )
		numberOfComponentsInTarget = len( targetLayer.components )
		
		if numberOfComponentsInTarget != 0:
			print "- Deleting %i components in target layer" % numberOfComponentsInTarget
			targetLayer.components = []

		if numberOfComponentsInSource > 0:
			print "- Copying components:"
			for thisComp in sourceLayer.components:
				newComp = thisComp.copy()
				print "   Component: %s" % ( thisComp.componentName )
				targetLayer.components.append( newComp )

	def copyAnchorsFromLayerToLayer( self, sourceLayer, targetLayer ):
		"""Copies all anchors from sourceLayer to targetLayer."""
		numberOfAnchorsInSource = len( sourceLayer.anchors )
		numberOfAnchorsInTarget = len( targetLayer.anchors )
		
		if numberOfAnchorsInTarget != 0:
			print "- Deleting %i anchors in target layer" % numberOfAnchorsInTarget
			targetLayer.setAnchors_(None)
		
		if numberOfAnchorsInSource > 0:
			print "- Copying anchors from source layer:"
			for thisAnchor in sourceLayer.anchors:
				newAnchor = thisAnchor.copy()
				targetLayer.anchors.append( newAnchor )
				print "   %s (%i, %i)" % ( thisAnchor.name, thisAnchor.position.x, thisAnchor.position.y )
	
	def copyMetricsFromLayerToLayer( self, sourceLayer, targetLayer ):
		"""Copies width of sourceLayer to targetLayer."""
		sourceWidth = sourceLayer.width
		if targetLayer.width != sourceWidth:
			targetLayer.width = sourceWidth
			print "- Copying width (%.1f)" % sourceWidth
		else:
			print "- Width not changed (already was %.1f)" % sourceWidth

	def buttonCallback( self, sender ):
		Glyphs.clearLog()
		Glyphs.showMacroWindow()
		print "Copy Layer to Layer Protocol:"

		Font = Glyphs.font
		selectedGlyphs = [ x.parent for x in Font.selectedLayers ]
		indexOfSourceMaster = self.w.masterSource.get()
		indexOfTargetMaster = self.w.masterTarget.get()
		componentsYesOrNo  = self.w.includeComponents.get()
		anchorsYesOrNo  = self.w.includeAnchors.get()
		metricsYesOrNo  = self.w.includeMetrics.get()
				
		for thisGlyph in selectedGlyphs:
			try:
				
				print "\nProcessing %s..." % thisGlyph.name
				sourcelayer = thisGlyph.layers[ indexOfSourceMaster ]
				targetlayer = thisGlyph.layers[ indexOfTargetMaster ]
				
				Font.disableUpdateInterface()
				
				# Copy paths, components, anchors, and metrics:
				self.copyPathsFromLayerToLayer( sourcelayer, targetlayer )
				if componentsYesOrNo:
					self.copyComponentsFromLayerToLayer( sourcelayer, targetlayer )
				if anchorsYesOrNo:
					self.copyAnchorsFromLayerToLayer( sourcelayer, targetlayer )
				if metricsYesOrNo:
					self.copyMetricsFromLayerToLayer( sourcelayer, targetlayer )
					
				Font.enableUpdateInterface()
			except Exception, e:
				print e
		
		if not self.w.keepWindowOpen.get():
			self.w.close()

CopyLayerToLayer()
