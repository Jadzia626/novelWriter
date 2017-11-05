# -*- coding: utf-8 -*
"""novelWriter GUI TimeLine

 novelWriter – GUI TimeLine
============================
 Class holding the book time line view

 File History:
 Created: 2017-11-02 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from nw.file.book  import BookItem

logger = logging.getLogger(__name__)

class GuiTimeLine(Gtk.Grid):
    
    def __init__(self, theBook):
        
        Gtk.Grid.__init__(self)
        
        self.theBook = theBook
        self.tblRows = []
        self.tblCols = []
        
        self.set_name("gridTimeLine")
        self.set_row_spacing(4)
        self.set_column_spacing(12)
        
        return
    
    def loadContent(self):
        
        self.tblRows = []
        self.tblCols = []
        
        tmpChars = []
        tmpPlots = []
        
        for treeHandle in self.theBook.theTree.treeOrder:
            
            treeItem   = self.theBook.getItem(treeHandle)
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            itemLevel  = treeItem["entry"].itemLevel
            itemClass  = treeItem["entry"].itemClass
            itemType   = treeItem["entry"].itemType
            
            if itemLevel == BookItem.LEV_ITEM:
                if itemType == BookItem.TYP_CHAR:
                    tmpChars.append({
                        "handle" : itemHandle,
                        "name"   : treeItem["entry"].itemName,
                    })
                elif itemType == BookItem.TYP_PLOT:
                    tmpPlots.append({
                        "handle" : itemHandle,
                        "name"   : treeItem["entry"].itemName,
                    })
            elif itemLevel == BookItem.LEV_FILE:
                if itemType == BookItem.TYP_BOOK:
                    treeParent  = self.theBook.getItem(itemParent)
                    itemSubType = treeParent["entry"].itemSubType
                    if itemSubType in (BookItem.SUB_PRO,BookItem.SUB_CHAP,BookItem.SUB_EPI):
                        self.tblCols.append({
                            "handle"    : itemHandle,
                            "name"      : treeItem["entry"].itemName,
                            "parhandle" : itemParent,
                            "partype"   : treeParent["entry"].itemSubType,
                            "parnum"    : treeParent["entry"].itemNumber,
                        })
        
        self.tblRows = tmpChars+tmpPlots
        self.buildGrid()
        self.show_all()
        
        return
    
    def buildGrid(self):
        
        self.attach(Gtk.Label(""),0,0,1,1)
        self.attach(Gtk.Label(""),0,1,1,1)
        
        rowNum = 2
        for rowItem in self.tblRows:
            tmpLabel = Gtk.Label(rowItem["name"])
            self.attach(tmpLabel,0,rowNum,1,1)
            rowNum += 1
        
        chapOrder = []
        chapName  = {}
        chapCount = {}
        currChap  = None
        scnCount  = 0
        colNum    = 0
        for colItem in self.tblCols:
            
            scnCount += 1
            colNum   += 1
            parHandle = colItem["parhandle"]
            
            if parHandle not in chapOrder: chapOrder.append(parHandle)
            if colItem["partype"] == BookItem.SUB_CHAP:
                chapName[parHandle] = "%s %d" % (colItem["partype"],colItem["parnum"])
            else:
                chapName[parHandle] = "%s" % colItem["partype"]
            chapCount[parHandle] = scnCount
            
            if not colItem["parhandle"] == currChap:
                currChap = colItem["parhandle"]
                scnCount = 0
            
            tmpLabel = Gtk.Label("SCN %d" % scnCount)
            self.attach(tmpLabel,colNum,1,1,1)
        
        print(chapOrder)
        print(chapName)
        print(chapCount)
        
        return
    
# End Class GuiTimeLine
