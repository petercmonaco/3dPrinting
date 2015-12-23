
import sys

version = "E2"
oozRate = 0.05488
retract = 0.7
zHop = 0.1
tool = "T1"
firstZ = 0.2
deltaZ = 0.2

print "; GCode Test Pattern"
print "; version="+version
print "; oozRate={}".format(oozRate)
print "; retract={}".format(retract)
print "; zHop={}".format(zHop)
print "; tool="+tool
print "; firstZ={}".format(firstZ)
print "; deltaZ={}".format(deltaZ)


preamble = """
M190 S110.000000
M109 S230.000000

M103 (disable RPM)
M73 P0 (enable build progress)
G21 (set units to mm)
G90 (set positioning to absolute)
M109 S110 <TOOL> (set HBP temperature)
M104 S230 <TOOL> (set extruder temperature) (temp updated by printOMatic)
;(**** begin homing ****)
G162 X Y F2500 (home XY axes maximum)
G161 Z F1100 (home Z axis minimum)
G92 Z-5 (set Z to -5)
G1 Z0.0 (move Z to 0)
G161 Z F100 (home Z axis minimum)
M132 X Y Z A B (Recall stored home offsets for XYZAB axis)
;(**** end homing ****)
G1 X-110.5 Y-72 Z50 F3300.0 (move to waiting position)
G130 X20 Y20 A20 B20 (Lower stepper Vrefs while heating)
M6 <TOOL> (wait for toolhead, and HBP to reach temperature)
G130 X127 Y127 A127 B127 (Set Stepper motor Vref to defaults)
M108 <TOOL>
G0 X-110.5 Y-72 (Position Nozzle)
G0 Z0.6      (Position Height)
G92 E0 (Set E to 0)
G1 E4 F300 (Extrude 4mm of filament)
G92 E0 (Set E to 0 again)
;(**** end of start.gcode ****)
"""

ending = """
M109 S0 T0 ( Cool down the build platform )
M104 S0 T0 ( Cool down the Right Extruder )
M104 S0 T1 ( Cool down the Left Extruder )
M73 P100 ( End  build progress )
G0 Z150 ( Send Z axis to bottom of machine )
M18 ( Disable steppers )
G162 X Y F2500 ( Home XY endstops )
M18 ( Disable stepper motors )
M70 P5 ( We <3 Making Things!)
M72 P1  ( Play Ta-Da song )
"""

print preamble.replace("<TOOL>", tool)

extruded = 0.0
wasRetracted = False
currentZ = firstZ

for y in [-30, -20, -10, 0, 10, 20, 30]:
    print "; Line at {}".format(y)
    print "G1 F2400 X-50 Y{}   (move to point above start of line)".format(y)
    print "G1 F2400 Z{}       (drop to printing height)".format(currentZ)
    if (wasRetracted):
        print "G1 F2400 E{}    (un-retract)".format(extruded)
    extruded += (100.0*oozRate)
    print "G0 F900 X50 Y{} E{} (lay down the line)".format(y, extruded)
    print "G1 F2400 E{} (retract)".format(extruded - retract)
    wasRetracted = True
    print "G1 F2400 Z{} (hop)".format(currentZ + zHop)


print ending


