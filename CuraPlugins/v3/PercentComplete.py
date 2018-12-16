# -*- coding: utf-8 -*-

import json
import re

from ..Script import Script


class PercentComplete(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        # Create settings as an object
        settings = {
            'name': 'Percentage Complete',
            'key': 'PercentComplete',
            'metadata': {},
            'version': 2,
            'settings': {
            }
        }

        # Dump to json string
        json_settings = json.dumps(settings)
        return json_settings

    def execute(self, data):
        output = []
        pct = 0
        started = False
        lastPct = 0
        maxExtrusion = 0
        eValue = 0
        tests = 0

        for layer in reversed(data):
            if tests > 10:
                break
            for line in layer.split('\n'):
                if tests > 10:
                    break
                if line.startswith(';'):
                    continue
                tokens = line.split()
                for token in tokens:
                    if (token.startswith("E")):
                        tests = tests + 1
                        floatVal = token[1:(len(token))]
                        try:
                            v = float(floatVal);
                            if (v > maxExtrusion):
                                maxExtrusion = v
                        except ValueError:
                            continue

        for layer in data:
            output_line = ''
            for line in layer.split('\n'):
                # If we see LAYER:0, this means we are in the main layer code
                if 'LAYER:0' in line:
                    started = True

                if line.startswith(';') or not started or maxExtrusion <= 0:
                    output_line += '%s\n' % line
                    continue

                tokens = line.split()
                for token in tokens:
                    if (token.startswith("E")):
                        floatVal = token[1:(len(token))]
                        try:
                            eValue = float(floatVal);
                        except ValueError:
                            continue

                pct = int(100.0 * eValue / maxExtrusion)
                if (pct > lastPct and pct < 100):
                    lastPct = pct
                    output_line += ';TYPE:CUSTOM\n'
                    output_line += 'M73 P%d\n' % pct

                output_line += '%s\n' % line

            output.append(output_line)

        return output
