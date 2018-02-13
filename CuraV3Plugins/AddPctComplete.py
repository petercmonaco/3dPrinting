from ..Script import Script
class AddPctComplete(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Add Percentage-Complete to GCode",
            "key": "AddPctComplete",
            "metadata":{},
            "version": 2,
            "settings": {}
        }"""

    def findLargestExtrusionValue(self, data):
        for layer in reversed(data):
            for line in reversed(layer.split("\n")):
                eVal = self.getValue(line, 'E')
                if (eVal != None):
                    return eVal
        return 1

    def execute(self, data):
        eMax = self.findLargestExtrusionValue(data)
        lastPct = 0
        for index in range(len(data)):
            lines = data[index].split("\n")
            newLayer = ""
            for line in lines:
                newLayer += line + "\n"
                eVal = self.getValue(line, 'E')
                if (eVal is None):
                    continue;
                pct = int(100.0 * eVal / eMax)
                if (pct > lastPct and pct < 100):
                    newLayer += "M73 P{}\n".format(pct)
                    lastPct = pct

            data[index] = newLayer

        return data
