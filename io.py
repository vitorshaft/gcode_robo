import re
from model import PolyLine, Hatch, Layer, Body

def read_cli(code: str):
    '''
    Importa as camadas de um arquivo .cli exportado pelo Fusion

    Parâmetros:
        code (str): código CLI
    Retorno
        body (Body): Objeto representando o corpo a ser imprimido
    '''
    #code = ''
    get_paths = re.compile('(?:\$\$(?:POLYLINE|HATCHES)\/(?:\d\,)?\d\,\d+(?:\,\d+.\d+,\d+.\d+)*)')
    get_coords = re.compile('(?:\$\$(?:POLYLINE\/0|HATCHES\/)\,2\,\d+)?\,(\d+\.\d+\,\d+\.\d+)+')
    box = re.findall('\$\$DIMENSION\/(\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+)',code, re.M)[0]
    layer_num = int(re.search('\$\$LAYERS\/(\d+)',code).group(1))
    get_layers = re.finditer('\$\$LAYER\/(\d.+\d+)\n(?:\$\$((?:POLYLINE|HATCHES)\/(?:\d\,)?\d\,\d+(?:\,\d+.\d+,\d+.\d+)*)\n)*',code)
    z_inc = float(re.search('\$\$LAYER\/(\d+.\d+)', code).group(1))
    lim_coords = [float(coord) for coord in box]
    xc = (lim_coords[3] + lim_coords[0]) / 2
    yc = (lim_coords[4] + lim_coords[1]) / 2
    zc = (lim_coords[5] + lim_coords[2]) / 2
    center_pt = (xc, yc, zc)
    layers = []
    for layer in get_layers:
        layer_paths =[]
        z = float(layer.group(1)) - z_inc
        lines = get_paths.finditer(layer.group(0))
        for line in lines:
            point_list = []
            for point in get_coords.findall(line.group()):
                x, y  = point.split(',')
                point_list.append((float(x)-xc, float(y)-yc, z))
            if 'POLYLINE' in line.group():
                layer_paths.append(PolyLine(point_list))
            if 'HATCHES' in line.group():
                layer_paths.append(Hatch(point_list))
        layers.append(Layer(z, layer_paths))
    return Body(layers, center_pt)

DAT_HEADER = '''&ACCESS RVP
&REL 468
&PARAM EDITMASK = *
&PARAM TEMPLATE = C:\\KRC\\Roboter\\Template\\vorgabe
&PARAM DISKPATH = KRC:\\R1\\Program
DEFDAT  TESTE_FUSION1
DECL BASIS_SUGG_T LAST_BASIS={POINT1[] "P9                      ",POINT2[] "P9                      ",CP_PARAMS[] "CPDAT7                  ",PTP_PARAMS[] "PDAT3                   ",CONT[] "C_DIS C_DIS             ",CP_VEL[] "0.025                   ",PTP_VEL[] "5                       ",SYNC_PARAMS[] "SYNCDAT                 ",SPL_NAME[] "S0                      ",A_PARAMS[] "ADAT0                   "}
DECL FDAT FP1={TOOL_NO 1,BASE_NO 0,IPO_FRAME #BASE,POINT2[] " ",TQ_STATE FALSE}
DECL PDAT PPDAT1={VEL 50.000,ACC 100.000,APO_DIST 100.000,GEAR_JERK 50.0000,EXAX_IGN 0}\n'''
SRC_HEADER = '''&ACCESS RVP
&REL 1
&PARAM TEMPLATE = C:\\KRC\Roboter\\Template\\vorgabe
&PARAM EDITMASK = *
DEF TESTE_FUSION1 ( )
EXT BAS (BAS_COMMAND :IN,REAL :IN )
INT I
BAS (#INITMOV,0)
FOR I=1 TO 6
$VEL_AXIS[I]=25
$ACC_AXIS[I]=50
ENDFOR
$VEL.CP=0.05
$VEL.ORI1=200
$VEL.ORI2=200
$ACC.ORI1=100
$ACC.ORI2=100
$APO.CDIS = 0.5000
$ORI_TYPE = #VAR
$BASE = {X 1462.4854,Y 0.0000,Z 664.8991,A 0.0000,B 0.0000,C 0.0000}
$TOOL={X 326.6638,Y 0.0000,Z 454.2762,A 180.0000,B -60.0005,C 0.0000}
$ADVANCE = 5
PTP  {A1 0.0000,A2 -90.0000,A3 90.0000,A4 0.0000,A5 0.0000,A6 0.0000}
PTP  {X 75.0000,Y 150.0000,Z 100.0000,A -23.4034,B 0.0000,C 180.0000,S 2,T 35}
$VEL.CP=0.05  ;50mm/s'''

def get_krl(body: Body, filename:str):
    '''
    A partir de um 

    TODO Ajustar referência do robô
    '''
    src = open(filename+".src","a")
    dat = open(filename+".dat","a")
    src.write(SRC_HEADER)
    dat.write(DAT_HEADER)
    
    dat_str = 'DECL E6POS XP{:}={{X {:.3f},Y {:.3f},Z {:.3f},A {:.3f},B {:.3f},C {:.3f}}}\n'
    src_str = 'LIN XP{} C_DIS C_DIS\n'
    ang = [-23.743, -36.293, -206.374]
    var_n = 0
    for layer in body:
        for path in layer:
            if type(path) == PolyLine:
                for n, point in enumerate(path):
                    pt= (100.000+point[0],-500.000+point[1], 50.000+point[2])
                    N = var_n + n
                    dat.write(dat_str.format(N, *pt, *ang))
                    src.write(src_str.format(N))
                var_n =+ len(path)
    src.writelines(["END"])
    src.close()
    dat.write('ENDDAT')
    dat.close()

