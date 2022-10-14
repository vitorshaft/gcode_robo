'''
      _              __  _   
     | |            / _|| |  
 ___ | |__    __ _ | |_ | |_ 
/ __|| '_ \  / _` ||  _|| __|
\__ \| | | || (_| || |  | |_ 
|___/|_| |_| \__,_||_|   \__|
                          
 *   DESENVOLVIDO POR VITOR SHAFT EM 09-AGO-2022
 * https://github.com/vitorshaft/gcode_robo.git
 * https://instagram.com/shaftrobotica
 * shaftrobotica@gmail.com

'''
#ARQUIVO DE ENTRADA DEVE TER O NOME "gcode.gcode"
gcode = open("gcode.gcode","r")
linhas = gcode.readlines()
gcode.close()
#OS ARQUIVOS DE SAIDA SERÃO "GCODE.src e GCODE.dat"
src = open("GCODE.src","a")
dat = open("GCODE.dat","a")

#[X,Y,Z,aplha,gamma,beta] DO PONTO INICIAL
atual = [1200.0,0.0,900.0,0.0,80.0,0.0,0.0]

nPontos = 0
#VERIFICAR UTILIDADE DO RCONF
l,m,n,o,p,q = 0,0,0,0,0,0
rconf = [l,m,n,o,p,q]
'''
l: virar/nao virar
m: subir/descer
n: frente/tras
o,p,q: <180/>=180
'''

dat_header= '''&ACCESS RVP
&REL 468
&PARAM EDITMASK = *
&PARAM TEMPLATE = C:\\KRC\\Roboter\\Template\\vorgabe
&PARAM DISKPATH = KRC:\\R1\\Program
DEFDAT  GCODE
DECL BASIS_SUGG_T LAST_BASIS={POINT1[] "P9                      ",POINT2[] "P9                      ",CP_PARAMS[] "CPDAT7                  ",PTP_PARAMS[] "PDAT3                   ",CONT[] "C_DIS C_DIS             ",CP_VEL[] "0.025                   ",PTP_VEL[] "5                       ",SYNC_PARAMS[] "SYNCDAT                 ",SPL_NAME[] "S0                      ",A_PARAMS[] "ADAT0                   "}
DECL FDAT FP1={TOOL_NO 1,BASE_NO 0,IPO_FRAME #BASE,POINT2[] " ",TQ_STATE FALSE}
DECL PDAT PPDAT1={VEL 50.000,ACC 100.000,APO_DIST 100.000,GEAR_JERK 50.0000,EXAX_IGN 0}\n'''

dat.write(dat_header)

#VARIAVEIS DE ITERACAO:
lista_pontos=[]	#VAI SER CONSULTADO NO PROXIMO LOOP
arco = 1	#INICIA O ARCO EM MODO ARCON
zGlobal = 430	#POSICAO Z MINIMA
for n,item in enumerate(linhas[:9900]):
	if item.find(';') == -1 and n%5 == 0:
		#arco = False
		atual = [100.0,-500.0,50.0,-23.743,-36.293,-206.374,0.0]
		nPontos = nPontos+1
		#se a linha tiver X...
		if item.find('X') != -1:
			xis = item.split('X')	#separa o que tem antes e depois do X
			try:
				xis = xis[1].split(' ')	#lista os valores separados por espaco
			except:
				pass
		#se a linha tiver Y...
		if item.find('Y') != -1:
			ips = item.split('Y')
			try:
				ips = ips[1].split(' ')
			except:
				pass
		#se a linha tiver Z...
		if item.find('Z') != -1:
			ze = item.split('Z')
			try:
				ze = ze[1].split(' ')
			except:
				pass

		try:
			tX = xis[0].split('.')	#pega o primeiro valor (X) e separa a parte inteira da flutuante
			tX = float(int(tX[0]))+(float(int(tX[1]))/1000.000)	#converte para float e soma as duas partes
			atual[0] = tX+100
		except Exception as a:
			print(a)
			pass
		try:
			tY = ips[0].split('.')
			tY = float(int(tY[0]))+(float(int(tY[1]))/1000.000)
			atual[1] = tY-600
		except Exception as b:
			print(b)
			pass
		try:
			tZ = ze[0].split('.')
			tZ = float(int(tZ[0]))+(float(int(tZ[1]))/1000.000)
			tZ = tZ+900	#offset do tampo da bancada
			#mudei o valor na subtracao abaixo, mas há divergência no comportamento do Z
			#creio que é algo devido a gcode, ou referência de versão
			atual[2] = tZ-874.1
			print("tZ: ",tZ,"zGlobal: ",zGlobal)
			if tZ > zGlobal:
				arco = 0	#Quando Z mudar, desligar o arco e esperar
				zGlobal = tZ
				atual[6] = arco
				arco = -1
			elif tZ == zGlobal:
				arco = 1
				atual[6] = arco
				#arco = -1
			'''
			elif tZ == zGlobal:
				arco = -1
				atual[6] = arco
			'''
			print(atual[6])
		except Exception as c:
			#arco = True	#O arco deve permanecer ligado enquanto nao houver mudanca em Z
			print(c)
			pass
		atual[3],atual[4],atual[5] = -23.743,-36.293,-206.374
		lista_pontos.append(atual)
print(lista_pontos[1])
print(lista_pontos[-1])
npos = "///NPOS "+str(nPontos)+",0,0,0,0,0\n"
cabecalho = ["&ACCESS RVP\n","&REL 1\n","&PARAM TEMPLATE = C:\KRC\Roboter\Template","\\vorgabe\n","&PARAM EDITMASK = *\n",
    "DEF GCODE ( )\n","EXT BAS (BAS_COMMAND :IN,REAL :IN )\n","INT I\n","BAS (#INITMOV,0)\n","FOR I=1 TO 6\n   $VEL_AXIS[I]=25\n   $ACC_AXIS[I]=50\nENDFOR\n","$VEL.CP=0.05\n$VEL.ORI1=200\n$VEL.ORI2=200\n$ACC.ORI1=100\n$ACC.ORI2=100\n","  $APO.CDIS = 0.5000\n  $ORI_TYPE = #VAR\n"]
cabecalho2 = ["$BASE = {X 1462.4854,Y 0.0000,Z 664.8991,A 0.0000,B 0.0000,C 0.0000}\n","$TOOL={X 326.6638,Y 0.0000,Z 454.2762,A 180.0000,B -60.0005,C 0.0000}\n","$ADVANCE = 5\n","PTP  {A1 0.0000,A2 -90.0000,A3 90.0000,A4 0.0000,A5 0.0000,A6 0.0000}\n","PTP  {X 75.0000,Y 150.0000,Z 100.0000,A -23.4034,B 0.0000,C 180.0000,S 2,T 35}\n$VEL.CP=0.05  ;50mm/s\n"]
src.writelines(cabecalho)
src.writelines(cabecalho2)
listaC = []
dat_str = 'DECL E6POS XP{:}={{X {:.3f},Y {:.3f},Z {:.3f},A {:.3f},B {:.3f},C {:.3f}}}\n'
src_str = 'LIN XP{} C_DIS C_DIS\n'
primeiro_ponto = dat_str.format(0,100.0,-500.0,50.0,-23.743,-36.293,-206.374)
dat.write(primeiro_ponto)
for n, ponto in enumerate(lista_pontos[1:]):
	coordenada = dat_str.format(n+1, *ponto[:-1])
	dat.write(coordenada)
	src.write(src_str.format(n))

arcoGlobal = False
for i in range(nPontos):
	arco = lista_pontos[i][6]
	
	if arco == 0 and arcoGlobal == False:
		#src.writelines(["ARCOF\n","TIMER T=60.0","\n"])#,"ARCON\n"])
		arcoGlobal = True
	elif arco == 1 and arcoGlobal == True:
		#src.writelines(["ARCON","\n"])
		arcoGlobal = False
src.writelines(["END"])
src.close()
dat.write('ENDDAT')
dat.close()