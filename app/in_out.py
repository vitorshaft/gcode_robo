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
    get_paths = re.compile('(?:\$\$(?:POLYLINE\/\d+,|HATCHES\/)\d\,\d+(?:\,\d+\.\d+,\d+\.\d+)*)')
    get_coords = re.compile('(?:\$\$(?:POLYLINE\/\d+\,|HATCHES\/)\d+\,\d+)?\,(\d+\.\d+\,\d+\.\d+)+')
    box = re.findall('\$\$DIMENSION\/(\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+)',code, re.M)[0]
    get_layers = re.finditer('\$\$LAYER\/(\d.+\d+)\n(?:\$\$((?:POLYLINE|HATCHES)\/(?:\d\,)?\d\,\d+(?:\,\d+.\d+,\d+.\d+)*)\n)*',code)
    z_inc = float(re.search('\$\$LAYER\/(\d+.\d+)', code).group(1))
    lim_coords = [float(coord) for coord in box]
    xc = (lim_coords[3] + lim_coords[0]) / 2
    yc = (lim_coords[4] + lim_coords[1]) / 2
    x_lims = (lim_coords[3]-xc, lim_coords[0]-xc)
    y_lims = (lim_coords[4]-yc, lim_coords[1]-yc)
    z_lims = (0, lim_coords[5]-lim_coords[2])
    lims = [x_lims, y_lims, z_lims]
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
    return Body(layers, lims)

DAT_HEADER = '''&ACCESS RVP
&REL 9
&PARAM EDITMASK = *
&PARAM TEMPLATE = C:\\KRC\\Roboter\\Template\\vorgabe
&PARAM DISKPATH = KRC:\\R1\\Program
DEFDAT  {}
DECL BASIS_SUGG_T LAST_BASIS={{POINT1[] "P315                    ",POINT2[] "P315                    ",CP_PARAMS[] "CPDAT8                  ",PTP_PARAMS[] "PDAT4                   ",CONT[] "C_DIS                   ",CP_VEL[] "0.05                    ",PTP_VEL[] "5                       ",SYNC_PARAMS[] "SYNCDAT                 ",SPL_NAME[] "S0                      ",A_PARAMS[] "ADAT0                   "}}
DECL E6POS XPREF={{X 1679.41125,Y -579.594604,Z 431.923492,A -87.1834106,B 60.0815239,C -88.5866776,S 22,T 18,E1 0.0,E2 0.0,E3 0.0,E4 0.0,E5 0.0,E6 0.0}}
DECL FDAT FP4={{TOOL_NO 1,BASE_NO 0,IPO_FRAME #BASE,POINT2[] " ",TQ_STATE FALSE}}
DECL PDAT PPDAT1={{VEL 50.0000,ACC 100.000,APO_DIST 100.000,GEAR_JERK 50.0000,EXAX_IGN 0}}
DECL LDAT LCPDAT1={{VEL 2.00000,ACC 100.000,APO_DIST 100.000,APO_FAC 50.0000,AXIS_VEL 100.000,AXIS_ACC 100.000,ORI_TYP #VAR,CIRC_TYP #BASE,JERK_FAC 50.0000,GEAR_JERK 50.0000,EXAX_IGN 0}}
DECL PDAT PPDAT3={{VEL 100.000,ACC 100.000,APO_DIST 100.000,GEAR_JERK 50.0000,EXAX_IGN 0}}\n'''

DAT_FOOTER = '''DECL E6POS XPEND0={X 1717.05981,Y -625.878357,Z 314.948792,A -90.5500107,B 55.2100487,C -90.8301239,S 22,T 18,E1 0.0,E2 0.0,E3 0.0,E4 0.0,E5 0.0,E6 0.0}
DECL FDAT FPEND0={TOOL_NO 1,BASE_NO 0,IPO_FRAME #BASE,POINT2[] " ",TQ_STATE FALSE}
DECL LDAT LCPDAT2={VEL 2.00000,ACC 100.000,APO_DIST 100.000,APO_FAC 50.0000,AXIS_VEL 100.000,AXIS_ACC 100.000,ORI_TYP #VAR,CIRC_TYP #BASE,JERK_FAC 50.0000,GEAR_JERK 50.0000,EXAX_IGN 0}
DECL E6POS XPEND={X 1716.95618,Y -625.765625,Z 439.733551,A -90.5752258,B 55.2216797,C -90.8636856,S 22,T 18,E1 0.0,E2 0.0,E3 0.0,E4 0.0,E5 0.0,E6 0.0}
DECL FDAT FPEND={TOOL_NO 1,BASE_NO 0,IPO_FRAME #BASE,POINT2[] " ",TQ_STATE FALSE}
DECL PDAT PPDAT4={VEL 100.000,ACC 100.000,APO_DIST 100.000,APO_MODE #CDIS,GEAR_JERK 50.0000,EXAX_IGN 0}\n'''

DAT_LSR_HEADER = '''DECL LSR_SUGG_T LAST_LSR={DATA_SET[] "LS3                     ",MEDIA_SET[] "ME3                     ",PRESSURE_SET[] "PR0                     ",LSR_HANDLE[] "                        ",GEO_NAME[] "GP0                     ",CUT_NAME[] "CS0                     ",STEP_NAME[] "SP0                     ",PULSE_NAME[] "PULSE0                  "}
DECL LSR_GASDEF_T GDGasDef={ProcGas 1,RootGas 1,CutGas 1}
DECL LSR_LSRNET_T LNLSNDef={LASER 1,FIBER 1,ROBOT 1}
DECL LSR_USR_T LULU0={VAL1 0,VAL2 0,VAL3 0,VAL4 0,VAL5 0,VAL6 0,VAL7 0,VAL8 0,VAL9 0,VAL10 0,VAL11 0,VAL12 0}
DECL LSR_MEDIUM_T LMME1={LSR_GAS_PREFLOW_TIME 1.40000,LSR_GAS_POSTFLOW_TIME 1.50000,LSR_GAS_PRESSURE 2.00000,LSW_HEAT_START_DLY 0.0,LSW_HEAT_END_DLY 0.0,LSW_WFD 0.0,LSW_WFD_MIN 0.0,LSW_WFD_START_DLY 0.0,LSW_WFD_END_DLY 0.0,LSW_HOT_WIRE 0.0}
DECL LSR_PWR_T LPLS1={LSR_MAX_PWR 2500,LSR_MIN_PWR 60,LSR_PRG 1,LSR_RAISE_TIME 5,LSR_DROP_TIME 12,LSR_MAX_TEST_PWR 500,LSR_MAX_FOCUS_PWR 500}
DECL LSR_PWR_T LPLS2={LSR_MAX_PWR 1500,LSR_MIN_PWR 400,LSR_PRG 1,LSR_RAISE_TIME 12,LSR_DROP_TIME 12,LSR_MAX_TEST_PWR 500,LSR_MAX_FOCUS_PWR 500}
DECL LSR_MEDIUM_T LMME3={LSR_GAS_PREFLOW_TIME 1.40000,LSR_GAS_POSTFLOW_TIME 1.50000,LSR_GAS_PRESSURE 2.00000,LSW_HEAT_START_DLY 0.0,LSW_HEAT_END_DLY 0.0,LSW_WFD 0.0,LSW_WFD_MIN 0.0,LSW_WFD_START_DLY 0.0,LSW_WFD_END_DLY 0.0,LSW_HOT_WIRE 0.0}
DECL LSR_PWR_T LPLS3={LSR_MAX_PWR 500,LSR_MIN_PWR 500,LSR_PRG 1,LSR_RAISE_TIME 12,LSR_DROP_TIME 12,LSR_MAX_TEST_PWR 500,LSR_MAX_FOCUS_PWR 500}
'''

SRC_HEADER = '''&ACCESS RVP
&REL 9
&PARAM EDITMASK = *
&PARAM TEMPLATE = C:\\KRC\Roboter\\Template\\vorgabe
&PARAM DISKPATH = KRC:\\R1\\Program
DEF {} ( )
EXT BAS (BAS_COMMAND :IN,REAL :IN )
INT I
;FOLD INI;%{{PE}}
  ;FOLD BASISTECH INI
    GLOBAL INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM ( )
    INTERRUPT ON 3 
    BAS (#INITMOV,0 )
  ;ENDFOLD (BASISTECH INI)
  ;FOLD USER INI
    ;Make your modifications here
  ;ENDFOLD (USER INI)
;ENDFOLD (INI)
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
$ADVANCE = 5
PTP  XPREF
$VEL.CP=0.05  ;50mm/s\n'''

SRC_LSR_HEADER = ''';FOLD GasInit    Gas: GasDef;%{{PE}}%R 6.1.22,%MKUKATPLASER,%CLSR_GAS_INIT,%VLSR_GAS_INIT,%P 3:#TECH, 5:GasDef 
Trigger When PATH = 0 DELAY=Lsr_InitGasDly DO LSR_InitGas(#TECH , GDGasDef.ProcGas , GDGasDef.RootGas , 0 ) PRIO=-1
;ENDFOLD
;FOLD LIN P4 CONT Vel={speed} m/s CPDAT1 Tool[1]:teste_D70 Base[0];%{{PE}}%R 8.3.42,%MKUKATPBASIS,%CMOVE,%VLIN,%P 1:LIN, 2:P4, 3:C_DIS C_DIS, 5:{speed}, 7:CPDAT1
$BWDSTART=FALSE
LDAT_ACT=LCPDAT1
FDAT_ACT=FP4
BAS(#CP_PARAMS,0.2)
LIN XP4 C_DIS C_DIS
;ENDFOLD

;FOLD LSR   INIT Allocation=False Gas: GasDef LSN: LSNDef;%{{PE}}%R 6.1.22,%MKUKATPLASER,%CLSR_INIT,%VLASER_INIT_ADV,%P 2:#TECH, 5:FALSE, 7:GasDef, 9:LSNDef, 10:False, 12:LU0 
LSR_ErrorType = #NONE
LSR_INIT_LASER (#TECH, LNLSNDef, GDGasDef, False, FALSE)
;ENDFOLD

;FOLD GasSwi Proc_Gas ON Nicht Haltend;%{{PE}}%R 6.1.22,%MKUKATPLASER,%CLSR_GAS_SWI,%VLSR_GAS_SWI,%P 3:#Proc, 5:TRUE, 7:1, 10:FALSE 
Trigger When PATH = 0 DELAY=Lsr_GasDlySwi DO LSR_Gas_Swi(#Proc , TRUE , -1 , FALSE ) PRIO=-1
;ENDFOLD
;FOLD GasSwi Root_Gas ON ;%{{PE}}%R 6.1.22,%MKUKATPLASER,%CLSR_GAS_SWI,%VLSR_GAS_SWI,%P 3:#Root, 5:TRUE, 7:1, 10:TRUE 
Trigger When PATH = 0 DELAY=Lsr_GasDlySwi DO LSR_Gas_Swi(#Root , TRUE , -1 , TRUE ) PRIO=-1
;ENDFOLD

;FOLD OUT 1 'DEPOSITOR_DE_PO_Start/Stop' State=TRUE CONT;%{{PE}}%R 8.3.42,%MKUKATPBASIS,%COUT,%VOUTX,%P 2:1, 3:DEPOSITOR_DE_PO_Start/Stop, 5:TRUE, 6:CONTINUE
CONTINUE
$OUT[1]=TRUE
;ENDFOLD
;FOLD WAIT FOR ( IN 1 'LMD_NO-ERROR' );%{{PE}}%R 8.3.42,%MKUKATPBASIS,%CEXT_WAIT_FOR,%VEXT_WAIT_FOR,%P 2:, 4:, 5:$IN, 6:1, 7:LMD_NO-ERROR, 9:
WAIT FOR  ( $IN[1] ) 
;ENDFOLD
;FOLD WAIT FOR ( IN 2 'PROCESS_STABLE' );%{{PE}}%R 8.3.42,%MKUKATPBASIS,%CEXT_WAIT_FOR,%VEXT_WAIT_FOR,%P 2:, 4:, 5:$IN, 6:2, 7:PROCESS_STABLE, 9:
WAIT FOR  ( $IN[2] ) 
;ENDFOLD
\n'''

SRC_LSR_FOOTER = ''';ENDFOLD
;FOLD LIN P314 CONT Vel=0.05 m/s CPDAT8 Tool[1]:teste_D70 Base[0];%{{PE}}%R 8.3.42,%MKUKATPBASIS,%CMOVE,%VLIN,%P 1:LIN, 2:P314, 3:C_DIS C_DIS, 5:0.05, 7:CPDAT8
$BWDSTART=FALSE
LDAT_ACT=LCPDAT2
FDAT_ACT=FPEND0
BAS(#CP_PARAMS,0.05)
LIN XPEND0 C_DIS C_DIS
;ENDFOLD
;FOLD OUT 1 'DEPOSITOR_DE_PO_Start/Stop' State=FALSE ;%{{PE}}%R 8.3.42,%MKUKATPBASIS,%COUT,%VOUTX,%P 2:1, 3:DEPOSITOR_DE_PO_Start/Stop, 5:FALSE, 6:
$OUT[1]=FALSE
;ENDFOLD
;FOLD PTP PEND CONT Vel=50 % PDAT4 Tool[1]:teste_D70 Base[0];%{{PE}}%R 8.3.42,%MKUKATPBASIS,%CMOVE,%VPTP,%P 1:PTP, 2:P315, 3:C_DIS, 5:50, 7:PDAT4
$BWDSTART=FALSE
PDAT_ACT=PPDAT4
FDAT_ACT=FPEND
BAS(#PTP_PARAMS,50)
PTP XPEND C_DIS\n'''

trigger_laser = ''';FOLD LSR   On Path=10 mm MSet=ME1 LSet=LS1;%{{PE}}%R 6.1.22,%MKUKATPLASER,%CLSR_ON,%VLSR_ON_TECH,%P 2:#TECH, 5:10, 8:1, 10:1400, 13:500, 16:ME1, 18:LS1, 20:LU0 
TRIGGER WHEN PATH=10 DELAY= LsrDelay(LSR_ShutterOn, PreDelay, GasPreFlowValue, LMME1) DO LSR_PRE_ON(#TECH, #OFF_SPL, LPLS1) PRIO=-1
TRIGGER WHEN PATH=10 DELAY=LSR_ShutterDelay DO LSR_ON(#TECH, #OFF_SPL, LMME1, LPLS1) PRIO=-1
TRIGGER WHEN PATH=10 DELAY=GasDelay(GasPreFlowValue, LMME1) DO LSR_GAS_ON(LMME1) PRIO=-1
;ENDFOLD\n'''

lsr_on_str = ''';FOLD LSR   On Path=10 mm MSet=ME1 LSet=LS1;%{{PE}}%R 6.1.22,%MKUKATPLASER,%CLSR_ON,%VLSR_ON_TECH,%P 2:#TECH, 5:10, 8:1, 10:{power}, 13:500, 16:ME1, 18:LS1, 20:LU0 
TRIGGER WHEN PATH=10 DELAY= LsrDelay(LSR_ShutterOn, PreDelay, GasPreFlowValue, LMME1) DO LSR_PRE_ON(#TECH, #OFF_SPL, LPLS1) PRIO=-1
TRIGGER WHEN PATH=10 DELAY=LSR_ShutterDelay DO LSR_ON(#TECH, #OFF_SPL, LMME1, LPLS1) PRIO=-1
TRIGGER WHEN PATH=10 DELAY=GasDelay(GasPreFlowValue, LMME1) DO LSR_GAS_ON(LMME1) PRIO=-1
;ENDFOLD\n'''
lsr_off_str = ''';FOLD LSR   Switch Path=0 mm LSet=LS4;%{{PE}}%R 6.1.22,%MKUKATPLASER,%CLSR_SWI,%VLSR_SWI_TECH,%P 2:#TECH, 5:0, 8:1500, 11:60, 14:ME4, 16:LS2, 18:LU0 
TRIGGER WHEN PATH=0 DELAY=LsrDelay(0, PreDelay, GasPreFlowValue, LMDEFAULT) DO LSR_PRE_SWI(#TECH, #OFF_SPL, LPLS2) PRIO=-1
TRIGGER WHEN PATH=0 DELAY=LSR_ShutterDelay DO LSR_SWI(#TECH, #OFF_SPL, LMDEFAULT, LPLS2) PRIO=-1
;ENDFOLD
;FOLD LSR   End Path=0 mm MSet=ME4 LSet=LS3 ;%{{PE}}%R 6.1.22,%MKUKATPLASER,%CLSR_END,%VLSR_END_TECH,%P 2:#TECH, 5:0, 8:500, 11:500, 14:12, 17:ME4, 19:LS3, 21:LU0, 22:False 
TRIGGER WHEN PATH=0 DELAY=LsrOffDelay(LSR_ShutterOff, LPLS3, GasPreFlowValue, LMME1) DO LSR_PRE_OFF(#TECH, #OFF_SPL, LPLS3) PRIO=-1
TRIGGER WHEN PATH=0 DELAY=LsrDelayOff DO LSRO_LsrSync1 = FALSE
TRIGGER WHEN PATH=0 DELAY=LSR_ShutterDelay DO LSR_OFF(#TECH, #OFF_SPL, LMME1, LPLS3,  False) PRIO=-1
;ENDFOLD\n'''

MOV_CMD = ''';FOLD LIN P{index} CONT Vel={speed} m/s CPDAT1 Tool[1]:teste_D70 Base[0];%{{PE}}%R 8.3.42,%MKUKATPBASIS,%CMOVE,%VLIN,%P 1:LIN, 2:P{index}, 3:C_DIS C_DIS, 5:{speed}, 7:CPDAT1
LIN XP{index} C_DIS C_DIS
;ENDFOLD\n'''

WAIT_CMD = ''';FOLD WAIT Time={hold_time} sec; %{{PE}}%R 8.3.42,%MKUKATPBASIS,%CWAIT,%VWAIT,%P 3:{hold_time}\n'''

#{A1 0.0000,A2 -90.0000,A3 90.0000,A4 0.0000,A5 0.0000,A6 0.0000}

def get_krl(body: Body, filename:str, lsr:bool, power:float=None, speed: float=None,
    thickness:float=None, focus:float=None, hold_time:float=None):
    '''
    A partir de um objeto body gera o código KRL para manufatura do objeto

    Parâmetros:
        body (Body): objeto representando a peça a ser produzida
        filename (str): nome do arquivo de texto utilizado 
        lsr (bool): bool informando se os códigos de laser devem ser escritos

    TODO
    adicionar parametros de laser:
        Potência
        Velocidade
        Espessura da chapa
        Over/Under focus
    '''
    #z_adj = thickness + focus
    src = open(filename+".src","w")
    dat = open(filename+".dat","w")
    src.write(SRC_HEADER.format(filename))
    dat.write(DAT_HEADER.format(filename))
    if lsr:
        dat.write(DAT_LSR_HEADER)
        src.write(SRC_LSR_HEADER.format(speed=speed))
    
    dat_str = 'DECL E6POS XP{:}={{X {:.3f},Y {:.3f},Z {:.3f},A {:.3f},B {:.3f},C {:.3f}}}\n'
    src_str = 'LIN XP{} C_DIS C_DIS\n'
    #src_str = 'LIN XP{} CONT Vel=0.1 m/s LCPDAT1 Tool[1] Base[0]\n'
    ang = [-90.55, 55.21, -90.83]
    var_n = 0
    z_inc = 314.95 + thickness - focus
    for layer in body:
        for path_num, path in enumerate(layer):
            if type(path) == PolyLine:
                if lsr:
                    src.write(lsr_on_str.format(power=power))
                for n, point in enumerate(path):
                    pt= (1717.55+point[0],-595.8+point[1], z_inc+point[2])
                    N = var_n + n
                    dat.write(dat_str.format(N, *pt, *ang))
                    #src.write(src_str.format(N))
                    src.write(MOV_CMD.format(index=N, speed=speed))
                if lsr:
                    src.write(lsr_off_str)
                var_n = var_n + len(path) + path_num
            if type(path) == Hatch:
                for line in path:
                    if lsr:
                        src.write(lsr_on_str.format(power=power))
                    for n, point in enumerate(line):
                        pt= (1717.55+point[0],-595.8+point[1], z_inc+point[2])
                        N = var_n + n + 1
                        dat.write(dat_str.format(N, *pt, *ang))
                        #src.write(src_str.format(N))
                        src.write(MOV_CMD.format(index=N, speed=speed))
                    if lsr:
                        src.write(lsr_off_str)
                    var_n = var_n + 2
        src.write(WAIT_CMD.format(hold_time=hold_time))
    src.write(SRC_LSR_FOOTER)
    src.write("END")
    src.close()
    dat.write(DAT_FOOTER)
    dat.write('ENDDAT')
    dat.close()

JBI_HEADER = '''/JOB
//NAME {}
//POS
///NPOS {},0,0,0,0,0
///TOOL 0
///POSTYPE ROBOT
///RECTAN
///RCONF 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
C00000=700.000,100.000,431.000,178.590,-37.970,14.690\n'''

JBI_HEADER1 = '''//INST
///DATE 2022/08/09 23:19
///ATTR SC,RW,RJ
////FRAME ROBOT
///GROUP1 RB1
NOP
MOVL C00000 V=50.0
DOUT OT#(40) ON\n'''

def get_jbi(body: Body, filename:str, arc:bool = False, **params):
    '''
    A partir de um objeto body gera o código JBI para manufatura do objeto

    Parâmetros:
        body (Body): objeto representando a peça a ser produzida
        filename (str): nome do arquivo de texto utilizado 
        arc (bool): bool informando se os códigos do arco devem ser escritos
        params (dict): dict com os parâmetros de usuário (speed, mov_speed, program, x,y,z e dbcp)
    '''
    if arc == False:
        params['speed'] = 40
        params['program'] = 1
    jbi = open(filename+".JBI","w")
    jbi.write(JBI_HEADER.format(filename.split('/')[-1], body.coord_num()+1)) #ADICIONAR NUMERO DE POSICOES
    decl_fmt = 'C{:0>5}={:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\n'
    movj_fmt = 'MOVL C{:0>5} V={}\n'
    ang = [-179.3958, -7.3004, 0.7371]
    O = [params['x'], params['y'], params['z']+params['dbcp']]
    var_n = 0
    decls = ''
    comms = ''
    for layer in body:
        for path_num, path in enumerate(layer):
            if type(path) == PolyLine:
                pt= (O[0]+path[0][0],O[1]+path[0][1],O[2]+path[0][2])
                N = var_n + 1
                decls = decls + decl_fmt.format(N, *pt, *ang)
                comms = comms + movj_fmt.format(N,params['mov_speed'])
                if arc:
                    comms = comms + 'DOUT OG#(7) {}\nARCON\n'.format(params['program'])
                for n, point in enumerate(path[1:]):
                    pt= (O[0]+point[0],O[1]+point[1],O[2]+point[2])
                    N = var_n + n + 2
                    decls = decls + decl_fmt.format(N, *pt, *ang)
                    comms = comms + movj_fmt.format(N,params['speed'])
                if arc:
                    comms = comms + 'ARCOF\n'
                var_n = var_n + len(path) #+ path_num
            if type(path) == Hatch:
                for line in path:
                    pt= (O[0]+line[0][0],O[1]+line[0][1],O[2]+line[0][2])
                    N = var_n + 1
                    decls = decls + decl_fmt.format(N, *pt, *ang)
                    comms = comms + movj_fmt.format(N, params['mov_speed'])
                    if arc:
                        comms = comms + 'DOUT OG#(7) {}\nARCON\n'.format(params['program'])
                    pt= (O[0]+line[1][0],O[1]+line[1][1],O[2]+line[1][2])
                    N = var_n + 2
                    decls = decls + decl_fmt.format(N, *pt, *ang)
                    comms = comms + movj_fmt.format(N, params['speed'])
                    if arc:
                        comms = comms + 'ARCOF\n'
                    var_n = var_n + 2
    jbi.write(decls + JBI_HEADER1 + comms)
    jbi.write("END\n")
    jbi.close()
