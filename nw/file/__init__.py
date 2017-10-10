# -*- coding: utf-8 -*
"""novelWriter File Init

 novelWriter – File Init File
==============================
 initialisation of the file storage

 File History:
 Created: 2017-10-06 [0.4.0]

"""

import logging
import nw
import nw.const as NWC
import xml.etree.ElementTree as ET

from os           import path, mkdir
from xml.dom      import minidom
from time         import time
from hashlib      import sha256
from nw.file.item import BookItem

logger = logging.getLogger(__name__)

class Book():
    
    def __init__(self):
        
        self.bookLoaded  = False
        
        self.bookPath    = None
        self.docPath     = None
        self.theTree     = []
        self.theIndex    = {}
        
        self.bookHandle  = None
        self.charHandle  = None
        self.plotHandle  = None
        self.noteHandle  = None
        
        # Book Settings
        self.bookTitle   = ""
        self.bookAuthors = []
        
        return
    
    def openBook(self, bookPath):
        
        if not path.isfile(bookPath):
            logger.error("Path not found: %s" % bookPath)
            return
        
        self.bookPath = bookPath
        
        nwXML = ET.parse(bookPath)
        xRoot = nwXML.getroot()
        
        nwxRoot     = xRoot.tag
        appVersion  = xRoot.attrib["appVersion"]
        fileVersion = xRoot.attrib["fileVersion"]

        logger.verbose("XML: Root is %s" % nwxRoot)
        logger.verbose("XML: Version is %s" % fileVersion)
        
        if not nwxRoot == "novelWriterXML" or not fileVersion == "1.0":
            logger.error("BookOpen: Project file does not appear to be a novelWriterXML file version 1.0")
            return
        
        for xChild in xRoot:
            if xChild.tag == "book":
                logger.debug("BookOpen: Found book data")
                for xItem in xChild:
                    if xItem.tag == "title":
                        logger.verbose("BookOpen: Title is '%s'" % xItem.text)
                        self.bookTitle = xItem.text
                    elif xItem.tag == "author":
                        logger.verbose("BookOpen: Author: '%s'" % xItem.text)
                        self.bookAuthors.append(xItem.text)
            elif xChild.tag == "content":
                logger.debug("BookOpen: Found book content")
                for xItem in xChild:
                    itemAttrib = xItem.attrib
                    itemHandle = itemAttrib["handle"]
                    itemParent = itemAttrib["parent"]
                    bookItem   = BookItem()
                    for xValue in xItem:
                        bookItem.setFromTag(xValue.tag,xValue.text)
                    self.appendTree(itemHandle,itemParent,bookItem)
        
        self.bookLoaded = True
        
        return
    
    def saveBook(self):
        
        bookDir  = path.dirname(self.bookPath)
        bookFile = path.basename(self.bookPath)
        logger.vverbose("BookSave: Folder is %s" % bookDir)
        logger.vverbose("BookSave: File is %s" % bookFile)
        
        if bookFile[-4:] == ".nwx":
            self.docPath = path.join(bookDir,bookFile[:-4]+".nwd")
            if not path.isdir(self.docPath):
                logger.info("BookSave: Created folder %s" % self.docPath)
                mkdir(self.docPath)
        
        nwXML = ET.Element("novelWriterXML",attrib={
            "fileVersion" : "1.0",
            "appVersion"  : str(nw.__version__),
        })
        xBook = ET.SubElement(nwXML,"book")
        xBookTitle = ET.SubElement(xBook,"title")
        xBookTitle.text = self.bookTitle
        for bookAuthor in self.bookAuthors:
            xBookAuthor = ET.SubElement(xBook,"author")
            xBookAuthor.text = bookAuthor
        
        xContent = ET.SubElement(nwXML,"content",attrib={"count":str(len(self.theTree))})
        itemIdx  = 0
        for treeItem in self.theTree:
            
            itemHandle = str(treeItem["handle"])
            parHandle  = str(treeItem["parent"])
            
            xItem = ET.SubElement(xContent,"item",attrib={
                "idx"    : str(itemIdx),
                "handle" : str(itemHandle),
                "parent" : str(parHandle),
            })
            
            for entryTag in treeItem["entry"].validTags:
                entryValue = treeItem["entry"].getFromTag(entryTag)
                if not entryValue is None:
                    xValue = ET.SubElement(xItem,entryTag)
                    xValue.text = str(entryValue)
                        
            itemIdx += 1
        
        roughXML  = ET.tostring(nwXML,"utf-8")
        prettyXML = minidom.parseString(roughXML)
        with open(self.bookPath,"wt") as outFile:
            prettyXML.writexml(outFile,indent="",addindent="  ",newl="\n")
        
        return True
    
    def createBook(self):
        
        logger.debug("Creating empty book project")
        
        self.bookHandle = self.makeHandle()
        self.charHandle = self.makeHandle()
        self.plotHandle = self.makeHandle()
        self.noteHandle = self.makeHandle()
        
        newBookItem = BookItem()
        newBookItem.setClass("CONTAINER")
        newBookItem.setLevel("ROOT")
        newBookItem.setType("BOOK")
        newBookItem.setName("Book")
        
        newCharItem = BookItem()
        newCharItem.setClass("CONTAINER")
        newCharItem.setLevel("ROOT")
        newCharItem.setType("CHAR")
        newCharItem.setName("Characters")
        
        newPlotItem = BookItem()
        newPlotItem.setClass("CONTAINER")
        newPlotItem.setLevel("ROOT")
        newPlotItem.setType("PLOT")
        newPlotItem.setName("Plots")
        
        newNoteItem = BookItem()
        newNoteItem.setClass("CONTAINER")
        newNoteItem.setLevel("ROOT")
        newNoteItem.setType("NOTE")
        newNoteItem.setName("Notes")
        
        self.appendTree(self.bookHandle,None,newBookItem)
        self.appendTree(self.charHandle,None,newCharItem)
        self.appendTree(self.plotHandle,None,newPlotItem)
        self.appendTree(self.noteHandle,None,newNoteItem)
        
        return True
    
    def setBookPath(self, bookPath):
        self.bookPath = bookPath
        return
    
    def setTitle(self, bookTitle):
        logger.debug("Book title changed to '%s'" % bookTitle)
        self.bookTitle = bookTitle.strip()
        return
    
    def setAuthors(self, bookAuthors):
        self.bookAuthors = []
        authList = bookAuthors.split(",")
        for author in authList:
            logger.debug("Book author '%s' added" % author.strip())
            self.bookAuthors.append(author.strip())
        return
    
    def createDoc(self, docTitle, docType):
        return
    
    def addChapter(self):
        
        newItem = BookItem()
        newItem.setClass("CONTAINER")
        newItem.setLevel("ITEM")
        newItem.setType("BOOK")
        newItem.setSubType("CHAPTER")
        newItem.setName("New Chapter")
        newItem.setCompile(True)
        
        self.appendTree(None,self.bookHandle,newItem)
        
        return
    
    def addCharacter(self):
        
        newItem = BookItem()
        newItem.setClass("CONTAINER")
        newItem.setLevel("ITEM")
        newItem.setType("CHAR")
        newItem.setName("New Character")
        
        self.appendTree(None,self.charHandle,newItem)
        
        return
    
    def addPlot(self):
        
        newItem = BookItem()
        newItem.setClass("CONTAINER")
        newItem.setLevel("ITEM")
        newItem.setType("PLOT")
        newItem.setName("New Plot")
        
        self.appendTree(None,self.plotHandle,newItem)
        
        return
    
    def updateTreeEntry(self,tHandle,tTarget,tValue):
        self.theTree[self.theIndex[tHandle]]["entry"].setFromTag(tTarget,tValue.strip())
        return
    
    def getTreeEntry(self,itemHandle):
        return self.theTree[self.theIndex[itemHandle]]
    
    def appendTree(self,tHandle,pHandle,bookItem):
        """
        Appends an entry to the main project tree.
        """
        
        tHandle = self.checkString(tHandle,self.makeHandle(),False)
        pHandle = self.checkString(pHandle,None,True)
        
        logger.verbose("BookOpen: Adding item %s with parent %s" % (str(tHandle),str(pHandle)))
        
        self.theTree.append({
            "handle" : tHandle,
            "parent" : pHandle,
            "entry"  : bookItem,
        })
        lastIdx = len(self.theTree)-1
        self.theIndex[tHandle] = lastIdx
        
        return
    
    def makeHandle(self,seed=""):
        itemHandle = sha256((str(time())+seed).encode()).hexdigest()[0:13]
        if itemHandle in self.theIndex.keys():
            logger.warning("Duplicate handle encountered! Retrying ...")
            itemHandle = self.makeHandle(seed+"!")
        return itemHandle
    
    def checkBool(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        if isinstance(checkValue,bool):
            return checkValue
        if isinstance(checkValue,str):
            if checkValue.lower() == "false": return False
            if checkValue.lower() == "true":  return True
        return defaultValue
    
    def checkInt(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        try:
            return int(checkValue)
        except:
            return defaultValue
    
    def checkString(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        if isinstance(checkValue,str): return str(checkValue)
        return defaultValue
        
    
# End Class DataStore
