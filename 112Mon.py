#################################################
# 112Mon
# Version 3.1
#
# Your name: John Cost
# Your andrew id: jcost
#################################################

import cs112_f22_week8_linter
from cmu_112_graphics import *

import decimal
import copy
#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Classes and functions for you to write
#################################################

def loadElementData(filename):
    dataDict = {}
    with open(filename, "r", encoding="utf-8") as f:
        fileString = f.read()

    firstLine = True
    for linePreSplit in fileString.splitlines():
        line = linePreSplit.split(",")
        if firstLine:
            firstLine = False
        else:
            dataDict[line[0]] = line[1]
    return dataDict

def loadReactionData(filename):
    dataDict = {}
    with open(filename, "r", encoding="utf-8") as f:
        fileString = f.read()

    firstLine = True
    for linePreSplit in fileString.splitlines():
        line = linePreSplit.split(",")
        if firstLine:
            firstLine = False
        else:
            dataDict[(line[0], line[1])] = line[2]
    return dataDict

def tryReaction(elem1, elem2, reactionsDict):

    if (elem1, elem2) in reactionsDict.keys():
        return reactionsDict[(elem1, elem2)]

    if (elem2, elem1) in reactionsDict.keys():
        return reactionsDict[(elem2, elem1)]

    return None

def isTerminalElement(elem, reactionsDict):
    for pairs in reactionsDict.keys():
        if pairs[0] == elem or pairs[1] == elem:
            return False
    return True

def allNextElements(elementSet, reactionsDict):
    prodSet = []
    for el1 in elementSet:
        for el2 in elementSet:
            k1 = (el1, el2)
            k2 = (el2, el1)
            if k1 in reactionsDict.keys():
                if not(
                    reactionsDict[k1] in prodSet or 
                    reactionsDict[k1] in elementSet
                    ):
                    prodSet.append(reactionsDict[k1])
            elif k2 in reactionsDict.keys():
                if not(
                    reactionsDict[k2] in prodSet or 
                    reactionsDict[k2] in elementSet
                    ):
                    prodSet.append(reactionsDict[k2])
    return set(prodSet)

def bestNextElement(elementSet, reactionsDict):
    sAllNextEl = allNextElements(elementSet, reactionsDict)
    if len(sAllNextEl) == 0:
        return None
    tiebreaker = ["z", 0]
    for pEl in sAllNextEl:
        lList = list(elementSet) + [pEl]
        nES = allNextElements(lList, reactionsDict)
        if len(nES) > tiebreaker[1]:
            tiebreaker = [pEl, len(nES)]
        elif len(nES) == tiebreaker[1]:
            if len(pEl) >= len(tiebreaker[0]):
                maxI = len(tiebreaker[0])
            else:
                maxI = len(pEl)
            for char in range(maxI):
                if ord(pEl[char]) < ord(tiebreaker[0][char]):
                    tiebreaker = [pEl, len(nES)]
                    break
                elif ord(pEl[char]) > ord(tiebreaker[0][char]):
                    tiebreaker = [tiebreaker[0], len(nES)]
                    break
    return tiebreaker[0]

#################################################
# Little Alchemy app
# Based on https://littlealchemy.com/
#################################################

def appStarted(app):
    app.bgColor = 'snow1'
    app.bgDark = 'indigo'
    app.darkMode = False

    app.elemSize = 40
    app.toolboxWidth = app.elemSize*4.5
    app.toolboxMargin = app.elemSize//4
    app.toolboxCellHeight = app.elemSize + app.toolboxMargin*2
    app.toolboxFont = f'Arial {int(app.elemSize/3)}'
    app.toolboxFontTerminal = f'Arial {int(app.elemSize/3)} underline'
    app.toolboxFontColor = 'gray'
    app.toolboxScroll = 0
    app.scrollbarWidth = app.elemSize//2
    app.toolboxExtent = 0
    
    app.workspaceElements = []
    app.toolboxElements = []
    
    app.mousePressedLoc = None
    app.pressedElem = None
    app.pressedScroll = None
    app.selectedIndex = None

    app.showAllNext = False
    app.showBestNext = False

    app.elementIconFilenameDict = loadElementData('./lilAl_elements.csv')
    #app.elementIconFilenameDict = loadElementData('./lilAl_elements_small.csv')

    # We load icons on demand, so start with this empty
    app.elementIconDict = {} 

    app.reactionsDict = loadReactionData('./lilAl_reactions.csv')
    #app.reactionsDict = loadReactionData('./lilAl_reactions_small.csv')

    initElementSet(app)

def initElementSet(app):
    app.elementSet = set()

    startingElements = ['water','fire','earth','air']
    for elementName in startingElements:
        app.elementSet.add(elementName)
        loadIcon(app, elementName)

    updateToolbox(app)
    
def loadIcon(app, elementName):
    if elementName not in app.elementIconFilenameDict:
        print(f'Element "{elementName} not in icon filename dictionary')
        return

    if elementName not in app.elementIconDict:
        # Load the icon
        iconFilename = app.elementIconFilenameDict[elementName]
        print(f'Loading icon {iconFilename}')
        im = app.loadImage(iconFilename)

        # Resize image
        imWidthOrig, imHeightOrig = im.size
        imSizeOrig = max(imWidthOrig, imHeightOrig)
        im = app.scaleImage(im, app.elemSize/imSizeOrig)

        im = ImageTk.PhotoImage(im)

        app.elementIconDict[elementName] = im

def pointInElement(app, elemX, elemY, mouseX, mouseY):
    if mouseX < elemX:
        return False
    elif mouseX >= elemX + app.elemSize:
        return False
    elif mouseY < elemY:
        return False
    elif mouseY >= elemY + app.elemSize:
        return False
    else:
        return True

def pointInToolbox(app, x, y):
    if x < app.width-app.toolboxWidth or x >= app.width:
        return False
    if y < 0 or y >= app.height:
        return False

    return True       

def pointInWorkspace(app, x, y):
    workspaceWidth = app.width-app.toolboxWidth

    if x < 0 or x >= workspaceWidth:
        return False
    if y < 0 or y >= app.height:
        return False

    return True       

def viewToElementIndex(app, x, y, skipIndex=None):
    for i in reversed(range(len(app.workspaceElements))):
        if i == skipIndex:
            continue

        element = app.workspaceElements[i]
        if pointInElement(app, element[0], element[1], x, y):
            return i

    return None
    
def viewToToolboxIndex(app, x, y):
    for i in range(len(app.toolboxElements)):
        elem = app.toolboxElements[i]
        if pointInElement(app, elem[0], elem[1] + app.toolboxScroll, x, y):
            return i

    return None

def selectElement(app, x, y):
    app.selectedIndex = None
    app.pressedElem = None
    elem = None

    elemIndex = viewToElementIndex(app, x, y)
    if elemIndex is not None:
        # Move app to end of list so that it will be displayed on top
        elem = app.workspaceElements.pop(elemIndex)
    else:
        elemIndex = viewToToolboxIndex(app, x,y)
        if elemIndex is not None:
            elemX, elemY, elemColor = app.toolboxElements[elemIndex]
            elemY += app.toolboxScroll
            elem = (elemX, elemY, elemColor)
        
    if elem is not None:
        app.workspaceElements.append(elem)

        app.selectedIndex = len(app.workspaceElements)-1
        app.pressedElem = app.workspaceElements[app.selectedIndex]

def updateToolbox(app):
    workspaceWidth = app.width - app.toolboxWidth
    elemX = workspaceWidth + app.toolboxMargin
    
    app.toolboxElements = []
    i = 0
    for elem in sorted(app.elementSet):
        elemY = i*app.toolboxCellHeight + app.toolboxMargin
        
        app.toolboxElements.append((elemX, elemY, elem))
        
        i += 1
    
    app.toolboxExtent = len(app.elementSet)*app.toolboxCellHeight + \
        app.toolboxMargin*2

def combineWorkspaceElements(app, elemIndex1, elemIndex2):
    elem1 = app.workspaceElements[elemIndex1][2]
    elem2 = app.workspaceElements[elemIndex2][2]
    newElem = tryReaction(elem1, elem2, app.reactionsDict)

    if newElem is None:
        return

    app.elementSet.add(newElem)
    loadIcon(app, newElem)

    updateToolbox(app)

    newX, newY = app.workspaceElements[app.selectedIndex][:2]

    app.workspaceElements.append((newX, newY, newElem))

    # Remove the bigger index first
    # (Shouldn't be needed because elemIndex1 should be the selectedIndex,
    # which should be the last index)
    if elemIndex1 > elemIndex2:
        app.workspaceElements.pop(elemIndex1)
        app.workspaceElements.pop(elemIndex2)
    else:
        app.workspaceElements.pop(elemIndex2)
        app.workspaceElements.pop(elemIndex1)

def keyPressed(app, event):
    if event.key == 'Escape':
        app.showAllNext = False
        app.showBestNext = False
    elif event.key == 'a':
        app.showAllNext = not app.showAllNext
    elif event.key == 'b':
        app.showBestNext = not app.showBestNext
    elif event.key == 'c':
        app.workspaceElements = []
    elif event.key == 'd':
        app.darkMode = not app.darkMode

def mousePressed(app, event):
    if app.showAllNext or app.showBestNext:
        return

    app.mousePressedLoc = (event.x, event.y)

    selectElement(app, event.x, event.y)

    if app.selectedIndex is None:
        # Check for toolbox background selection
        if pointInToolbox(app, event.x, event.y):
            app.pressedScroll = app.toolboxScroll
    
def mouseDragged(app, event):
    if app.showAllNext or app.showBestNext:
        return

    dx = event.x - app.mousePressedLoc[0]
    dy = event.y - app.mousePressedLoc[1]

    if app.selectedIndex is not None:
        startElemX, startElemY, elem = app.pressedElem

        app.workspaceElements[app.selectedIndex] = \
            (startElemX+dx, startElemY+dy, elem)

    elif app.pressedScroll is not None:
        app.toolboxScroll = min(0, app.pressedScroll + dy)

def mouseReleased(app, event):
    if app.showAllNext or app.showBestNext:
        return

    if app.selectedIndex is not None:
        if pointInWorkspace(app, event.x, event.y):
            # React as needed
            secondElemIndex = viewToElementIndex(app, event.x, event.y, 
            skipIndex=app.selectedIndex)
            if secondElemIndex is not None:
                combineWorkspaceElements(app, 
                    app.selectedIndex, secondElemIndex)

        else:
            app.workspaceElements.pop(app.selectedIndex)

        app.selectedIndex = None

    app.mousePressedLoc = None
    app.pressedElem = None
    app.pressedScroll = None

###
### View
###

def drawAllNext(app, canvas):
    if app.showAllNext:
        workspaceWidth = app.width - app.toolboxWidth
        canvas.create_rectangle(app.elemSize, app.elemSize,
            workspaceWidth - app.elemSize, app.height-app.elemSize,
            fill='dark magenta', outline='black', width=5)

        nextElementsSet = allNextElements(app.elementSet, app.reactionsDict)
        if len(nextElementsSet) > 0:
            nextElementsString = '\n'.join(sorted(nextElementsSet))
        else:
            nextElementsString = "No more elements to find!"

        canvas.create_text(app.elemSize*2, app.elemSize*2,
            text="Try creating one of the following:\n\n"+nextElementsString, 
            fill='white', anchor='nw', font=app.toolboxFont)

def drawBestNext(app, canvas):
    if app.showBestNext:
        bestNext = bestNextElement(app.elementSet, app.reactionsDict)
        if bestNext is None:
            bestNext = "No more elements to find!"

        workspaceWidth = app.width - app.toolboxWidth
        canvas.create_rectangle(app.elemSize, app.elemSize,
            workspaceWidth - app.elemSize, app.height-app.elemSize,
            fill='dark magenta', outline='black', width=5)

        canvas.create_text(app.elemSize*2, app.elemSize*2,
            text="Try creating :\n\n"+bestNext, 
            fill='white', anchor='nw', font=app.toolboxFont)

def drawHints(app, canvas):
    hintStr = "Press 'A' for all next elements\n" + \
        "Press 'B' for best next element\n" + \
        "Press 'C' to clear workspace\n" + \
        "Press 'D' to toggle dark mode\n" + \
        "\nhttps://littlealchemy.com/" 
    canvas.create_text(app.elemSize/2, app.height-app.elemSize/2,
        text=hintStr, anchor='sw', font=app.toolboxFont,
        fill=app.toolboxFontColor)

    drawAllNext(app, canvas)
    drawBestNext(app, canvas)


def drawElement(app, canvas, x, y, elem, isSelected=False, drawName=False):
    if isSelected:
        outline = 'black'
    else:
        outline = ''

    width=2
    # width=5

    if elem in app.elementIconDict:
        im = app.elementIconDict[elem]
        canvas.create_image(x, y, image=im, anchor='nw')
    else:
        label = elem[0].upper() + elem[1]
        font = f'Arial {int(app.elemSize/2)}'
        canvas.create_text(x+app.elemSize//2, y+app.elemSize//2, text=label,
            font=font)

    if drawName:
        if isTerminalElement(elem, app.reactionsDict):
            font = app.toolboxFontTerminal
        else:
            font = app.toolboxFont

        textX = x + app.elemSize + app.toolboxMargin
        textY = y + app.elemSize//2
        canvas.create_text(textX, textY, text=elem, font=font,
            anchor='w', fill=app.toolboxFontColor)

    if isSelected:
        canvas.create_rectangle(x, y, x+app.elemSize, y+app.elemSize,
            fill='', outline=outline, width=width)

def drawSelectedElement(app, canvas):
    if app.selectedIndex is not None:
        x, y, elem = app.workspaceElements[app.selectedIndex]
    
        isSelected = True
        drawElement(app, canvas, x, y, elem, isSelected)

def drawWorkspaceElements(app, canvas):
    for i in range(len(app.workspaceElements)):
        x, y, elem = app.workspaceElements[i]
        isSelected = (i == app.selectedIndex)
        if isSelected:
            continue

        drawElement(app, canvas, x, y, elem, isSelected)

def drawScrollbar(app, canvas):
    if app.toolboxExtent <= app.height:
        return
    
    scrollbarHeight = app.height*(app.height / app.toolboxExtent)

    maxScroll = app.toolboxExtent - app.height
    maxScrollbarMove = app.height - scrollbarHeight
    scrollBarY = maxScrollbarMove*(-app.toolboxScroll/maxScroll)

    scrollBarY0 = min(scrollBarY, maxScrollbarMove)

    canvas.create_rectangle(
        app.width-app.scrollbarWidth, scrollBarY0,
        app.width, scrollBarY0+scrollbarHeight,
        fill='light gray', outline='')

def drawToolbox(app, canvas):
    if app.darkMode:
        bgColor = app.bgDark
    else:
        bgColor = app.bgColor

    canvas.create_rectangle(app.width-app.toolboxWidth, 0, 
        app.width, app.height,
        fill=bgColor, outline='')

    for x, y, elem in app.toolboxElements:
        isSelected = False
        drawName = True
        drawElement(app, canvas, x, y + app.toolboxScroll, elem, 
            isSelected, drawName)        
        
def drawWorkspace(app, canvas):
    if app.darkMode:
        bgColor = app.bgDark
    else:
        bgColor = app.bgColor

    workspaceWidth = app.width-app.toolboxWidth

    canvas.create_rectangle(0, 0, workspaceWidth, app.height,
        fill=bgColor, outline='')

    lineWidth = 5
    canvas.create_line(workspaceWidth, 0, workspaceWidth, app.height,
        fill='gray', width=lineWidth)

def redrawAll(app, canvas):
    drawWorkspace(app, canvas)
    drawWorkspaceElements(app, canvas)
    drawToolbox(app, canvas)
    drawScrollbar(app, canvas)
    drawSelectedElement(app, canvas)
    drawHints(app, canvas)

def playLittleAlchemy():
    runApp(width=600, height=800)

#################################################
# main
#################################################

def main():
    cs112_f22_week8_linter.lint()
    playLittleAlchemy()

if __name__ == '__main__':
    main()
