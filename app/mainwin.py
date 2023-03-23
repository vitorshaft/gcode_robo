from tkinter import Tk, Button, OptionMenu, StringVar, Checkbutton, DoubleVar, IntVar
from opt_frames import OptFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

kuka_opts = [
    {'text': 'Potência (W):','var_type': DoubleVar,'name': 'power'},
    {'text': 'Vel. de Soldagem (mm/s):','var_type': DoubleVar,'name': 'speed'},
    {'text': 'Espessura da chapa(mm):','var_type': DoubleVar,'name': 'thickness'},
    {'text': 'Over/Under Focus (mm):','var_type': DoubleVar,'name': 'focus'},
    {'text': 'Tempo entre camadas (s):', 'var_type': IntVar, 'name': 'hold_time'}
]

yask_opts = [
    {'text': 'Vel. de Soldagem (mm/s):','var_type': DoubleVar,'name': 'speed'},
    {'text': 'Vel. Aproximação (mm/s):','var_type': DoubleVar,'name': 'mov_speed'},
    {'text': 'DBPC (mm):','var_type': DoubleVar,'name': 'dbcp'},
    {'text': 'Programa da fonte','var_type': IntVar,'name': 'program'},
    {'text': 'X:', 'var_type': DoubleVar, 'name': 'x'},
    {'text': 'Y:', 'var_type': DoubleVar, 'name': 'y'},
    {'text': 'Z:', 'var_type': DoubleVar, 'name': 'z'}
]

class MainWin(Tk):
    def __init__(self):
        super().__init__()
        #botão de abrir aquivo
        self.open_file_but = Button(self)
        self.open_file_but.configure(text='Abrir arquivo')
        self.open_file_but.place(anchor="nw", relwidth=0.15, x=0, y=0)
        #painel do gráfico
        self.fig = Figure(figsize=(6,6))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().place(
            anchor="ne",
            relheight=0.80,
            relwidth=0.65,
            relx=1.0,
            rely=0.06,
            x=0,
            y=0)
        #seletor de robô
        self.robot = StringVar(self, value='Sel. robô')
        self.choose_robot_but = OptionMenu(self, self.robot, *['KUKA', 'Yaskawa'])
        self.choose_robot_but.place(
            anchor="ne",
            relwidth=0.15,
            relx=0.31,
            rely=0.0,
            x=0,
            y=0)
        #botão de exportar código
        self.exp_code_but = Button(self)
        self.exp_code_but.configure(text='Exportar código')
        self.exp_code_but.place(
            anchor="se",
            relwidth=0.16,
            relx=0.335,
            rely=1.0,
            x=0,
            y=0)
        #check de alternar direção
        self.altern_dir_chk = Checkbutton(self)
        self.altern_dir_chk.configure(text='Sentidos Alternados')
        self.altern_dir_chk.place(anchor="sw", rely=0.94, x=0, y=0)
        #botão de exportar o contorno externo da peça
        self.exp_rect_but = Button(self)
        self.exp_rect_but.configure(text='Exportar contorno')
        self.exp_rect_but.place(
            anchor="sw",
            relwidth=0.16,
            relx=0.0,
            rely=1.0,
            x=0,
            y=0)
        #tamanho da janela
        self.configure(height=480, width=640)
        #instanciamento dos frames de opções dos robôs
        self.kuka = OptFrame(self, kuka_opts)
        self.yask = OptFrame(self, yask_opts)
