##StickEmUp
##Walt Nixon
##20140226

import StickEmUpFunctions as sf
import arcpy
import numpy

print("Setting Configuration")
###Configuration (Distances in Feet)
SPACING = 1000.0

WORKSPACE = r'K:\SCRIPTS\StickEmUp\StickEmUp.gdb'
arcpy.env.workspace = WORKSPACE
UNITS = "MKR_AllUnits_20131114" #'ChiefPudAUnits'
LATERALS_OUT = "Laterals2" 
INTERSECT_OUT= "Laterals3"
EXPLODE_OUT = "LateralsFinal"
UNIT_BUFFER = "UnitsBuffered"
proj = arcpy.Describe(UNITS).spatialReference

arcpy.env.overwriteOutput = True
print("Configuration Complete")
#Loop through units and Read Unit Geometery

units, centriods = sf.GetUnitGeom(UNITS)

print("Begin Unit Loop")
i = 0
lines = []
for unit in units:
    #Find Two longest edges 
    longEdges = sf.LongEdgeLen(unit)
    ##Average edges and divide by 2 to get  avg lateral length substract unit buffer to get effective latlen
    #latLen = (numpy.mean(longEdges) / 2.0) - UNIT_BUFFER
    latLen = 6000.0
    #Find unit azimuth 
    azimuth = sf.LongEdgeAngle(unit)
    perpendicularAzi = azimuth + 90.0
    #Find unit centroid 
    centroid = centriods[i]
    # print("Centroid = {0}".format(centroid))
    i += 1

    #From Centroid Calculate beginning and end points for laterals 
    A0 = centroid
    B0 = sf.GetPointFromAngleAndDistance(centroid, azimuth, latLen)
    
    A1 = sf.GetPointFromAngleAndDistance(centroid, perpendicularAzi, SPACING)
    B1 = sf.GetPointFromAngleAndDistance(A1, azimuth, latLen)

    A2 = sf.GetPointFromAngleAndDistance(centroid, 180+perpendicularAzi, SPACING)
    B2 = sf.GetPointFromAngleAndDistance(A2, azimuth, latLen)

    C0 = sf.GetPointFromAngleAndDistance(centroid, 180+azimuth, latLen)
    C1 = sf.GetPointFromAngleAndDistance(A1, 180+ azimuth, latLen)
    C2 = sf.GetPointFromAngleAndDistance(A2, 180+azimuth, latLen)

    #Store Line point pairs in a list of tuples
    lines.extend([(A0,B0),(A0,C0),(A1,B1),(A1,C1),(A2,B2),(A2,C2)])
# print lines
print("End Unit Loop")
#Draw lines
print("Draw Lines")
polylines = sf.DrawLinesFromPointList(lines, LATERALS_OUT, proj)


#Clean up lines ##Run intersect 
print("Buffer Units")
arcpy.Buffer_analysis(UNITS, UNIT_BUFFER, "-50 feet")
print("Run Intersect")
arcpy.Intersect_analysis([polylines,UNIT_BUFFER], INTERSECT_OUT, "ALL")

##Consider Re-calcuating Geometry After Inersect
arcpy.MultipartToSinglepart_management (INTERSECT_OUT, EXPLODE_OUT)
print("Remove Short Laterals")
with arcpy.da.UpdateCursor(EXPLODE_OUT,"SHAPE@LENGTH") as cursor:
    for row in cursor:
        if row[0] < 1500.0:
            print("deleted lateral = {0} ...too short".format(row[0]))
            cursor.deleteRow()


