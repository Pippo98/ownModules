#!/usr/bin/env python3

class reference():
    BOTTOM = 0
    TOP = 1
    LEFT = 2
    RIGHT = 3


class alignment():
    BOTTOM_BOTTOM = 0.1
    BOTTOM_TOP = 0.2
    TOP_TOP = 1.1
    TOP_BOTTOM = 1.2

    LEFT_LEFT = 2.1
    LEFT_RIGHT = 2.2
    RIGHT_RIGHT = 3.1
    RIGHT_LEFT = 3.2

    CENTER = 4
    FULLWIDTH = 5


class CoordinateManager():

    Reference = None
    Alignment = None

    minX = 0
    minY = 0
    maxX = None
    maxY = None

    def __init__(self):
        self.rectangles = {}

        self.Reference = reference()
        self.Alignment = alignment()

        super().__init__()

    def addRect(self, id, upLeft, bottomRight):
        upLeft, bottomRight = self.checkConstraint(upLeft, bottomRight)

        self.rectangles[id] = {"ul": upLeft, "br": bottomRight}

    def checkConstraint(self, upLeft, bottomRight):
        if not self.minX == None:
            if upLeft[0] < self.minX:
                upLeft = (self.minX, upLeft[1])
            if bottomRight[0] < self.minX:
                bottomRight = (self.minX, bottomRight[1])

        if not self.maxX == None:
            if upLeft[0] > self.maxX:
                upLeft = (self.maxX, upLeft[1])
            if bottomRight[0] > self.maxX:
                bottomRight = (self.maxX, bottomRight[1])

        if not self.minY == None:
            if upLeft[1] < self.minY:
                upLeft = (upLeft[0], self.minY)
            if bottomRight[1] < self.minY:
                bottomRight = (bottomRight[0], self.minY)

        if not self.maxY == None:
            if upLeft[1] > self.maxY:
                upLeft = (upLeft[0], self.maxY)
            if bottomRight[1] > self.maxY:
                bottomRight = (bottomRight[0], self.maxY)
        return upLeft, bottomRight

    def getRectangles(self):
        return self.rectangles

    def alignHoriziontal(self, alignment, width, upLeft, bottomRight):
        if alignment == self.Alignment.LEFT_RIGHT:
            bottomRight = (bottomRight[0] + width, bottomRight[1])
        if alignment == self.Alignment.LEFT_LEFT:
            bottomRight = (upLeft[0], bottomRight[1])
            upLeft = (upLeft[0] - width, upLeft[1])
        if alignment == self.Alignment.RIGHT_RIGHT:
            upLeft = (bottomRight[0], upLeft[1])
            bottomRight = (bottomRight[0] + width, bottomRight[1])
        if alignment == self.Alignment.RIGHT_LEFT:
            upLeft = (upLeft[0] - width, upLeft[1])

        return upLeft, bottomRight

    def alignVertical(self, alignment, height, upLeft, bottomRight):
        if alignment == self.Alignment.BOTTOM_TOP:
            upLeft = (upLeft[0], upLeft[1] - height)
        if alignment == self.Alignment.TOP_TOP:
            bottomRight = (bottomRight[0], upLeft[1])
            upLeft = (upLeft[0], upLeft[1] - height)
        if alignment == self.Alignment.TOP_BOTTOM:
            bottomRight = (bottomRight[0], bottomRight[1] + height)
        if alignment == self.Alignment.BOTTOM_BOTTOM:
            upLeft = (upLeft[0], bottomRight[1])
            bottomRight = (bottomRight[0], bottomRight[1] + height)

        return upLeft, bottomRight

    def addRelativeTo(self, id, newID, referenceType, alignmentType, width=None, height=None, padding=1):

        referenceRectangle = None
        if(id in self.rectangles.keys()):
            referenceRectangle = self.rectangles[id]
        else:
            return None

        if referenceRectangle == None:
            return None

        upLeft = (0, 0)
        bottomRight = (0, 0)

        upLeft = referenceRectangle["ul"]
        bottomRight = referenceRectangle["br"]
        _width = abs(upLeft[0] - bottomRight[0]) + padding
        _height = abs(upLeft[1] - bottomRight[1]) + padding

        ###### BOTTOM ######
        if(referenceType == self.Reference.BOTTOM):
            upLeft = (upLeft[0], upLeft[1] + _height)
            bottomRight = (bottomRight[0], bottomRight[1] + _height)

            if not height == None:
                bottomRight = (bottomRight[0], bottomRight[1] + height)

            if not width == None:
                upLeft, bottomRight = self.alignHoriziontal(
                    alignmentType, width, upLeft, bottomRight)

        ###### TOP ######
        if(referenceType == self.Reference.TOP):

            upLeft = (upLeft[0], upLeft[1] - _height)
            bottomRight = (bottomRight[0], bottomRight[1] - _height)

            if not height == None:
                upLeft = (upLeft[0], upLeft[1] - height)

            if not width == None:
                upLeft, bottomRight = self.alignHoriziontal(
                    alignmentType, width, upLeft, bottomRight)

        ###### RIGHT ######
        if(referenceType == self.Reference.RIGHT):

            upLeft = (upLeft[0] + _width, upLeft[1])
            bottomRight = (bottomRight[0] + _width, bottomRight[1])

            if not width == None:
                bottomRight = (bottomRight[0] + width, bottomRight[1])

            if not height == None:
                upLeft, bottomRight = self.alignVertical(
                    alignmentType, height, upLeft, bottomRight)

        ###### LEFT ######
        if(referenceType == self.Reference.LEFT):

            upLeft = (upLeft[0] - _width, upLeft[1])
            bottomRight = (bottomRight[0] - _width, bottomRight[1])

            if not width == None:
                upLeft = (upLeft[0] - width, upLeft[1])

            if not height == None:
                upLeft, bottomRight = self.alignVertical(
                    alignmentType, height, upLeft, bottomRight)

        upLeft, bottomRight = self.checkConstraint(upLeft, bottomRight)

        self.rectangles[newID] = {"ul": upLeft, "br": bottomRight}
