#Name: Nozzle Chooser
#Info: Choose between left nozzle (T1) and right nozzle (T0)
#Depend: GCode
#Type: postprocess
#Param: nozzle(list:Left,Right) Choose Nozzle

## Written by Peter Monaco, 12/24/2015
import re

if nozzle == 0:
    # Left was chosen
    currentNozzle="T1"
    otherNozzle="T0"
else:
    # Right was chosen
    currentNozzle="T0"
    otherNozzle="T1"

with open(filename, "r") as f:
	lines = f.readlines()

with open(filename, "w") as f:
    for line in lines:
        line = line.replace("T0", currentNozzle)  # When 'T0' appears in the generated code, they mean the current nozzle
        # Prev line needs to be first, because following lines may write "T0" to the string
        line = line.replace("<CURRENT_NOZZLE>", currentNozzle)
        line = line.replace("<OTHER_NOZZLE>", otherNozzle)
        line = line.replace("<RIGHT_NOZZLE>", "T0")
        line = line.replace("<LEFT_NOZZLE>", "T1")
        f.write(line)
