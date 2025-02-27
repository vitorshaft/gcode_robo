import sys

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

# Verifica se o caminho do arquivo foi passado como argumento
if len(sys.argv) != 2:
    print("Uso correto: python gcode_to_jbi.py caminho/para/seu/arquivo.gcode")
    sys.exit(1)

gcode_path = sys.argv[1]

try:
    with open(gcode_path, "r") as gcode:
        linhas = gcode.readlines()
except FileNotFoundError:
    print(f"Erro: O arquivo '{gcode_path}' não foi encontrado.")
    sys.exit(1)

# O ARQUIVO DE SAÍDA SERÁ SEMPRE "GCODE.JBI"
jbi = open("GCODE.JBI", "a")

# [X, Y, Z, alpha, gamma, beta] DO PONTO INICIAL
atual = [700.0, 150.0, 434.0, 178.59, -37.97, 14.69, 0]

nPontos = 0
l, m, n, o, p, q = 0, 0, 0, 0, 0, 0
rconf = [l, m, n, o, p, q]

lista_pontos = []
arco = 1
zGlobal = 430

for item in linhas[:5000]:
    if item.find(';') == -1:
        atual = [700.0, 100.0, 431.0, 178.59, -37.97, 14.69, 0]
        nPontos += 1
        if 'X' in item:
            xis = item.split('X')
            try:
                xis = xis[1].split(' ')
            except:
                pass
        if 'Y' in item:
            ips = item.split('Y')
            try:
                ips = ips[1].split(' ')
            except:
                pass
        if 'Z' in item:
            ze = item.split('Z')
            try:
                ze = ze[1].split(' ')
            except:
                pass

        try:
            tX = float(xis[0])
            atual[0] = tX + 700
        except:
            pass
        try:
            tY = float(ips[0])
            atual[1] = tY + 100
        except:
            pass
        try:
            tZ = float(ze[0]) + 431
            atual[2] = tZ
            if tZ > zGlobal:
                arco = 0
                zGlobal = tZ
                atual[6] = arco
                arco = -1
            elif tZ == zGlobal:
                arco = 1
                atual[6] = arco
        except:
            pass
        
        atual[3], atual[4], atual[5] = 178.59, -37.97, 14.69
        lista_pontos.append(atual)

npos = f"///NPOS {nPontos},0,0,0,0,0\n"
cabecalho = [
    "/JOB\n", "//NAME GCODE\n", "//POS\n", npos,
    "///TOOL 0\n", "///POSTYPE BASE\n", "///RECTAN\n", "///RCONF 0,1,1,0,0,0,0,0\n"
]
cabecalho2 = [
    "//INST\n", "///DATE 2022/08/09 23:19\n",
    "///COMM Gerado com Python\n", "///ATTR SC,RW,RJ\n", "///GROUP1 RB1\n", "NOP\n"
]
jbi.writelines(cabecalho)

listaC = []
for item in range(nPontos):
    numeracao = str(item).zfill(5)
    coordenadas = ",".join(f"{coord:.3f}" for coord in lista_pontos[item][:6])
    listaC.append([numeracao, coordenadas])
    jbi.writelines([f"C{numeracao}={coordenadas}\n"])

jbi.writelines(cabecalho2)
jbi.writelines(["MOVJ C00000 V=150.0\n", "DOUT OT#(40) ON\n", "DOUT OG#(7) 2\n", "TIMER T=3.00\n", "\n"])

arcoGlobal = False
for i in range(nPontos):
    arco = lista_pontos[i][6]
    
    if arco == 0 and not arcoGlobal:
        jbi.writelines(["ARCOF\n", "TIMER T=60.0\n"])
        arcoGlobal = True
    elif arco == 1 and arcoGlobal:
        jbi.writelines(["ARCON\n"])
        arcoGlobal = False
    jbi.writelines([f"MOVJ C{listaC[i][0]} V=5.0\n"])

jbi.writelines(["ARCOF\n", "END"])
jbi.close()

print("Conversão concluída! O arquivo 'GCODE.JBI' foi gerado com sucesso.")
