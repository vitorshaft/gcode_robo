from tkinter import Frame, Label, Entry, DoubleVar, IntVar

kuka_opts = [
    {'text': 'Potência (W):','var_type': DoubleVar,'name': 'power'},
    {'text': 'Vel. de Soldagem (mm/s):','var_type': DoubleVar,'name': 'speed'},
    {'text': 'Espessura da chapa(mm):','var_type': DoubleVar,'name': 'thickness'},
    {'text': 'Over/Under Focus (mm):','var_type': DoubleVar,'name': 'focus'}
]

class OptFrame(Frame):
    def __init__(self, master, opts:list[dict]):
        super().__init__(master)
        self.active = False
        self.opts = []
        for n,opt in enumerate(opts):
            label = Label(self,text=opt['text'])
            label.place(anchor='nw', rely=n*0.06, x=0, y=0)
            var = opt['var_type'](self)
            ent = Entry(self, textvariable=var)
            ent.place(anchor='ne', relwidth=0.3, relx=1.0, rely=n*0.06, x=0, y=0)
            self.opts.append({'name': opt['name'],'label': label, 'var': var, 'entry': ent})
    
    def get_entries(self):
        return {opt['name']:opt['var'].get() for opt in self.opts}
    
    def show(self):
        if self.active == False:
            self.place(anchor="nw", relheight=0.785, rely=0.115, x=0, y=0, relwidth=0.32)
            self.active = True

    def hide(self):
        if self.active == True:
            self.place_forget()
            self.active = False
            