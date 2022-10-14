import re

def parse_layers(gcode: str) -> list[dict]:
    '''
    Lê as coordenadas do GCode e as estrutura numa lista de dicts
    contendo a altura z de cada camada e uma lista de coordenadas xy
    
    Parâmetro
        gcode (str): código g sendo analisado
    
    Retorno
        layers_coords (list): lista de dicts das camadas
    '''
    layers = re.split(';LAYER:\d+', gcode)[2:]
    layers_coords = []
    for layer in layers:
        layer_xy = []
        start = re.findall('G0 F\d+ X(\d+.\d+) Y(\d+.\d+) Z(\d+.\d+)', layer)[0]
        coords = re.findall('(?:G0|G1) (?:F60 |F9000 )?X(\d+.\d+) Y(\d+.\d+)(?: E\d+.\d+)?\n', layer)
        layer_xy.append((float(start[0]), float(start[1])))
        for coord in coords:
            layer_xy.append((float(coord[0]), float(coord[1])))
        layers_coords.append({'z': float(start[2]),
                              'xy': layer_xy})
    return layers_coords
    