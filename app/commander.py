from in_out import read_cli, get_krl, get_jbi
from mainwin import MainWin
from tkinter import filedialog
from model import Body, Layer

class Commander:
    def __init__(self, view: MainWin):
        self.view = view
        self.model = None
        view.robot.trace('w', self.show_rbt_opts)
        view.open_file_but['command'] = self.open_file
        view.exp_code_but['command'] = self.export_code
        view.altern_dir_chk['command'] = self.alternate_path_dirs
        view.exp_rect_but['command'] = self.export_surounding_rect
    
    def show_rbt_opts(self, *args):
        '''
        Mostra o frame para configurar parâmetros do robô
        '''
        robot = self.view.robot.get()
        if robot == 'KUKA':
            self.view.yask.hide()
            self.view.kuka.show()
        if robot == 'Yaskawa':
            self.view.kuka.hide()
            self.view.yask.show()
    
    def open_file(self):
        '''
        Abre arquivo CLI e instancia o model
        '''
        self.view.altern_dir_chk.select()
        dir = filedialog.askopenfilename(
            parent=self.view,
            title = 'Abrir arquivo de rotas',
            filetypes=[('Common Layer Interface', '*.cli')])
        if dir != '':
            with open(dir, 'r') as file:
                code = file.read()
            self.model = read_cli(code)
            self.update_plot()
    
    def update_plot(self):
        '''
        Atualiza a plotagem das trajetórias
        '''
        self.view.fig.clf()
        self.model.plot(self.view.fig)
        self.view.canvas.draw()
    
    def export_code(self):
        '''
        Exporta o código KRL/JBI
        '''
        ext = {"KUKA": ('KUKA Robot Language','*.src'),
            "Yaskawa": ('Yaskawa inteface', '*.JBI')}
        robot = self.view.robot.get()
        path = filedialog.asksaveasfilename(filetypes=[ext[robot]])
        if path != '':
            if robot == "KUKA":
                params = self.view.kuka.get_entries()
                get_krl(self.model, path, lsr=True, **params)
            if robot == "Yaskawa":
                params = self.view.yask.get_entries()
                if params['speed'] <= 0: params['speed'] = 50.0
                if params['dbcp'] <= 0: params['dbcp'] = 15.0
                if params['program'] <= 0:  params['program'] = 7
                if params['x']==0 and params['y']==0 and params['z']==0:
                    params['x'] = 765.63
                    params['y'] = 165.78
                    params['z'] = 434.10
                get_jbi(self.model, path, True, **params)
    
    def alternate_path_dirs(self):
        '''
        Deixa as trajetórias na mesma direção ou indo em direções alternadas
        '''
        self.model.unalternate_dirs()
        self.update_plot()
    
    def export_surounding_rect(self):
        '''
        Exporta o retângulo que delimita a região da peça
        '''
        ext = {"KUKA": ('KUKA Robot Language','*.src'),
            "Yaskawa": ('Yaskawa inteface', '*.JBI')}
        robot = self.view.robot.get()
        path = filedialog.asksaveasfilename(filetypes=[ext[robot]])
        model = Body([Layer(0,[self.model.surounding_rect])],lims=[])
        if path != '':
            if robot == "KUKA":
                get_krl(model, path, lsr=False)
            if robot == "Yaskawa":
                params = self.view.yask.get_entries()
                if params['speed'] <= 0: params['speed'] = 50.0
                if params['dbcp'] <= 0: params['dbcp'] = 15.0
                if params['program'] <= 0:  params['program'] = 7
                params['speed'] = params['mov_speed'] if params['mov_speed'] > 0 else 40
                if params['x']==0 and params['y']==0 and params['z']==0:
                    params['x'] = 765.63
                    params['y'] = 165.78
                    params['z'] = 434.10
                get_jbi(model, path, False, **params)