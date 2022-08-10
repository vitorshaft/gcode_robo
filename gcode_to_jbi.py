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
#O ARQUIVO DE SAIDA SERA SEMPRE "GCODE.JBI"
jbi = open("GCODE.JBI","a")
#print(linhas[:25])

#[X,Y,Z,aplha,gamma,beta] DO PONTO INICIAL
atual = [700.0,150.0,434.0,178.59,-37.97,14.69,0]

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
#VARIAVEIS DE ITERACAO:
lista_pontos=[]	#VAI SER CONSULTADO NO PROXIMO LOOP
arco = 1	#INICIA O ARCO EM MODO ARCON
zGlobal = 430	#POSICAO Z MINIMA
for item in linhas:#[20:3000]:
	if item.find(';') == -1:
		#arco = False
		atual = [700.0,100.0,431.0,178.59,-37.97,14.69,0]
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
			atual[0] = tX+700
		except Exception as a:
			print(a)
			pass
		try:
			tY = ips[0].split('.')
			tY = float(int(tY[0]))+(float(int(tY[1]))/1000.000)
			atual[1] = tY+100
		except Exception as b:
			print(b)
			pass
		try:
			tZ = ze[0].split('.')
			tZ = float(int(tZ[0]))+(float(int(tZ[1]))/1000.000)
			tZ = tZ+431	#offset do tampo da bancada
			atual[2] = tZ
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
		atual[3],atual[4],atual[5] = 178.59,-37.97,14.69
		lista_pontos.append(atual)
print(lista_pontos[1])
print(lista_pontos[-1])
npos = "///NPOS 5"+str(nPontos)+",0,0,0,0,0\n"
cabecalho = ["/JOB\n","//NAME GCODE\n","//POS\n",npos,\
    "///TOOL 0\n","///POSTYPE BASE\n","///RECTAN\n","///RCONF 0,1,1,0,0,0,0,0\n"]
cabecalho2 = ["//INST\n","///DATE 2022/08/09 23:19\n",\
    "///COMM Gerado com Python\n","///ATTR SC,RW,RJ\n","///GROUP1 RB1\n","NOP\n"]
jbi.writelines(cabecalho)
listaC = []
for item in range(nPontos):
	numeracao = str(item)
	diferenca = 5-len(numeracao)
	for c in range(diferenca):
		numeracao = "0"+numeracao
	coordenadas = "{:.3f}".format(lista_pontos[item][0])+" "+\
		"{:.3f}".format(lista_pontos[item][1])+" "+\
		"{:.3f}".format(lista_pontos[item][2])+" "+\
		"{:.3f}".format(lista_pontos[item][3])+" "+\
		"{:.3f}".format(lista_pontos[item][4])+" "+\
		"{:.3f}".format(lista_pontos[item][5])
	listaC.append([numeracao,coordenadas])
	jbi.writelines(["C"+numeracao+"="+coordenadas,"\n"])
jbi.writelines(cabecalho2)
jbi.writelines(["MOVL "+"C00000"+" V=150.0","\n"])
jbi.writelines(["DOUT OT#(40) ON\n","DOUT OG#(7) 2\n","TIMER T=3.00\n","\n"])

arcoGlobal = False
for i in range(nPontos):
	arco = lista_pontos[i][6]
	
	if arco == 0 and arcoGlobal == False:
		jbi.writelines(["ARCOF\n","TIMER T=60.0","\n"])#,"ARCON\n"])
		arcoGlobal = True
	elif arco == 1 and arcoGlobal == True:
		jbi.writelines(["ARCON","\n"])
		arcoGlobal = False
	jbi.writelines(["MOVL "+"C"+listaC[i][0]+" V=5.0","\n"])

jbi.writelines(["ARCOF\n"])
jbi.writelines(["END"])
jbi.close()