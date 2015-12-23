
import sys

def modifyZString(zstr):
    if (len(zstr) == 1):
        return zstr
    floatPart = zstr[1:(len(zstr))];
    f = float(floatPart);
    f2 = f - 0.10;
    if (f2 < 0):
        f2 = 0
    newToken = "Z{}".format(f2)
    #print "Sliced "+zstr+" to "+newToken
    return newToken

def rewriteLine(line):
    if not ((line.startswith("G0 ") or line.startswith("G1 ")) and ' Z' in line):
        return line;

    tokens = line.split()
    newTokens = []
    for token in tokens:
        if token.startswith("Z"):
            token = modifyZString(token)
        newTokens.append(token);
    newLine = " ".join(newTokens);
    print "Rewrote line to: "+newLine
    return newLine+"\n"
    

if len(sys.argv) != 2:
    print "Usage:  "+ sys.argv[0]+" filename"
    sys.exit()

infileName = sys.argv[1];
outfileName = infileName.replace(".gcode","") + "-d14.gcode"

lineNum = 1;
with open(infileName, 'r') as infile, open(outfileName, 'w') as outfile:
    for line in infile:
        print "Processing line {}".format(lineNum)
        lineNum += 1
        newLine = rewriteLine(line)
        outfile.write(newLine)





