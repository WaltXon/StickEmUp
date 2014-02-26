##StickEmUp Functions
##Walt Nixon
##20140226
import math
import arcpy

#Calcuate the area of a polygon
def AreaOfPolygon(polygon):
    # print("AreaOfPolygon()")
    area = 0.0
    n = len(polygon)
    for i in range(n):
        j = (i+1)%n
        area += polygon[i][0]*polygon[j][1] - polygon[j][0]*polygon[i][1]
    area *= 0.5
    return abs(area)

#Calcuate the Centroid of a polygon
def Centroid(polygon):
    # print("Centroid()")
    area = AreaOfPolygon(polygon)
    n = len(polygon)
    sumCx = 0.0
    sumCy = 0.0
    for i in range(n):
        j = (i+1)%n
        sumCx += (polygon[i][0] + polygon[j][0])*(polygon[i][0]*polygon[j][1] - polygon[j][0]*polygon[i][1])
        # print 'sumCx += ({0} + {1})*({0}*{2} - {1}*{3})'.format(polygon[i][0],  polygon[j][0],polygon[j][1],polygon[i][1])
        # print 'sumCx = {0}'.format(sumCx)
        sumCy += (polygon[i][1] + polygon[j][1])*(polygon[i][0]*polygon[j][1] - polygon[j][0]*polygon[i][1])
        # print 'sumCy += ({0} + {1})*({2}*{1} - {3}*{0})'.format(polygon[i][1],  polygon[j][1],polygon[i][0],polygon[j][0])
        # print 'sumCy = {0}'.format(sumCy)
    cX = (1.0/(6.0*area))* sumCx
    cY = (1.0/(6.0*area))* sumCy
    # print "sumCx = {0}, sumCy = {1}, cX = {2}, cY = {3}, area = {4}".format(sumCx, sumCy, cX, cY, area)
    return (cX,cY)

#Get Distance between two points function
def Distance(a, b):
    """get the distance between two points where a = (x,y) and b = (x,y)"""
    # print("Distance()")
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

#Find two longest edges
def LongEdgeLen(pointList):
    """Input a list of points, calulates the distance between the points 
    and returns the two top longest lengths"""
    # print("LongEdgeLen()")
    distances = []
    # print "pointList = {0}".format(pointList)
    n = len(pointList)
    i = 0
    for i in range(n):
        j = (i+1)%n
        # print("i,j = {0},{1}".format(i,j))
        distance = Distance(pointList[i], pointList[j])
        # print "({0},{1}) distance = {2}".format(pointList[i], pointList[j],distance)
        distances.append(distance)
    
    distances.sort()
    distances.reverse()
    # print distances
    return (distances[0], distances[1])

#Get angle of a line function
def Angle(a,b):
    """get the angle of a line in degrees between two points where a = (x,y) and b = (x,y)"""
    # print("Angle()")
    deltaX = b[0] - a[0]
    deltaY = b[1] - a[1]
    angle_degrees = math.atan2(deltaY, deltaX) * 180 / math.pi
    # print "deltaX = {0} deltaY = {1} angle = {2}".format(deltaX, deltaY, angle_degrees)
    return angle_degrees


#Find angle of the longest edge
def LongEdgeAngle(pointList):
    """Input a list of points, calulates the distance between the points 
    and returns the angle of the longest edge"""
    # print("LongEdgeAngle()")
    a = 0
    b = 0
    longest = 0.0
    n = len(pointList)
    i = 0
    for i in range(n):
        j = (i+1)%n
        # print("i,j = {0},{1}".format(i,j))
        distance = Distance(pointList[i], pointList[j])
        if distance > longest:
            longest = distance
            a = pointList[i]
            b = pointList[j]   
            # print "({0},{1}) distance = {2}".format(a,b,distance)
    # print "longestEdge = {0}, a = {1}, b = {2}".format(longest, a, b)
    angle = Angle(a,b)
    # print "longeEdge Angle = {0}".format(angle)
    return angle

#Draw Lines Function
def DrawLinesFromPointList(pointList, outputFile, projection):
    print("DrawLinesFromPointList()")
    # A list of features and coordinate pairs
    feature_info = [[[1, 2], [2, 4], [3, 7]],
                    [[6, 8], [5, 7], [7, 2], [9, 5]]]

    # A list that will hold each of the Polyline objects
    features = []

    for feature in pointList:
        # Create a Polyline object based on the array of points
        # Append to the list of Polyline objects
        features.append(
            arcpy.Polyline(
                arcpy.Array([arcpy.Point(*coords) for coords in feature])))

    # Persist a copy of the Polyline objects using CopyFeatures
    arcpy.CopyFeatures_management(features, outputFile)
    arcpy.DefineProjection_management (outputFile, projection)
    return outputFile

def GetUnitGeom(unit_fc):
    # print("GetUnitGeom()")
    units = []
    with arcpy.da.SearchCursor(unit_fc, ["SHAPE@", "SHAPE@XY"]) as cursor:
        centroids = []
        for row in cursor: 
            # print("row = {0}".format(row))
            centroids.append(row[1])
            unit = []
            for part in row[0]:
                # print("part = {0}".format(part))
                for pnt in part:
                    # print('pnt = {0}'.format(pnt))
                    if pnt:
                        unit.append((pnt.X,pnt.Y))
                    else:
                        # print("Pnt = None")
                        break
            units.append(unit)
        # print "UNIT = {0}".format(unit)
        # print "UNITS = {0}".format(units)
        print "NUMBER OF UNITS = {0}".format(len(units))
        # print "CENTROIDS = {0}".format(centroids)
    return (units, centroids)

def GetPointFromAngleAndDistance(point, angle, distance):
    # print("GetPointFromAngleAndDistance()")
    angle = math.radians(angle)
    cosDistance = math.cos(angle) * distance
    # print ("cos = {0} cosDistance = {1}".format(math.cos(angle), cosDistance))
    sineDistance = math.sin(angle) * distance
    # print ("sine = {0} sineDistance = {1}".format(math.sin(angle), sineDistance))
    x = point[0] + cosDistance
    y = point[1] + sineDistance
    return (x,y)
