import math

def ellipse_area(major, minor):
    majorRadius = major
    minorRadius = minor
    ellipseArea = majorRadius * minorRadius * math.pi
    return ellipseArea


def rectangle_area(base, height):
    recBase = base
    recHeight = height
    recArea = recBase * recHeight
    return recArea

def trapezoid_area(top, bottom, height):
    trapTop = top
    trapBottom = bottom
    trapHeight = height
    trapArea = (1/2) * trapHeight * (trapTop + trapBottom)
    return trapArea