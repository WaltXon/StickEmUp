import StickEmUpFunctions as sf

print """========================================================
StickEmUpFunctions Test Page
========================================================
"""

pointList = [((-2,-3),(-4,4)),((5,2),(3,-9)),((2,0),(6,-4)),((-5,7),(-3,4))]
polygon = [[0,0],[2,0],[2,2],[0,2]]

a = (-2,-3)
b = (-4,4)

print 'Distance() with (-2,-3) and (-4,4) should return 7.28'
print sf.Distance(a,b)
print ""
print 'LongEdgeLen() with pointList should return (11.180339887498949, 7.280109889280518)'
print sf.LongEdgeLen(pointList)
print ""
print "Angle() with (-2,-3) and (-4,4) should return 105.945395901 "
print sf.Angle(a,b)
print ""
print 'LongEdgeAngle() with pointList should return ??'
print sf.LongEdgeAngle(pointList)
print ""
print "AreaOfPolygon() with polygon = [[0,0],[2,0],[2,2],[0,2]]"
print sf.AreaOfPolygon(polygon)
print ""
print "Centroid() with polygon = [[0,0],[2,0],[2,2],[0,2]]"
print sf.Centroid(polygon)
print ""
print """GetPointFromAngleAndDistance() with 
Angle: 37 degrees Distance: 27 feet Starting point: x0 = 3; y0 = 5 returns 24.563, 21.249"""
print sf.GetPointFromAngleAndDistance((0,5), 37.0, 27.0)