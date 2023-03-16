import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class CoordIndex:  
    def __init__(self, value):
        self.value = value
    
    @classmethod
    def start(cls):
        return CoordIndex(0)
    
    def restart(self):
        self.value = 0
    
    def next(self):
        self.value += 1
    
    def get(self):
        return self.value


INDEX = CoordIndex.start()


class PolyLine(list):
    '''
    Objeto que representa linhas de adição de material
    
    Parâmetros:
        points (list[tuple]): lista de pontos que compõem a linha
    '''
    def __init__(self, points: list[tuple]):
        super().__init__(points)
        self.was_clockwise = self.dir == -1
    
    @property
    def is_polygon(self):
        '''
        booleano representado se a linha forma circuito fechado
        '''
        return True if self[0] == self[-1] else False
    
    @property
    def dir(self):
        '''
        Retorna o sentido da linha, 1 para anti-horário, -1 para horário
        Se linha aberta 1 para x crescente ou y crescente se x não mudar
        '''
        if self.is_polygon:
            return 1 if sum((p2[0]-p1[0])*(p2[1]+p2[1]) for p1,p2 in zip(self[::2], self[1::2])) > 0 else -1
        else:
            vec = (self[1][0] - self[0][0], self[1][1] - self[0][1])
            if vec[0] > 0:
                return 1
            elif vec[0] < 0:
                return -1
            else:
                if vec[1] > 0: return 1
                else: return -1
    
    @property
    def x(self) -> list:
        return [item[0] for item in self]
    
    @property
    def y(self) -> list:
        return [item[1] for item in self]
    
    @property
    def z(self):
        return self[0][2]
    
    def plot(self, ax=False):
        if self.dir == 1:
            color = 'blue'
        else:
            color = 'red'
        if ax:
            ax.plot(self.x, self.y, zs = self.z, color=color)
        else:
            plt.plot(self.x, self.y, color=color)


class Hatch(list):
    '''
    Hatch com linhas para preenchimento da peça

    Parâmetros:
        point_list (list[tuple]): lista de pontos que definem as linhas do hatch
    '''
    def __init__(self, point_list: list[tuple]):
        lines = [PolyLine([i,f]) for i,f in zip(point_list[::2], point_list[1::2])]
        super().__init__(lines)
    
    def plot(self, ax=None):
        for item in self:
            item.plot(ax)


class Layer(list[Hatch|PolyLine]):
    def __init__(self, z: float, paths: list):
        self.z = z
        super().__init__(paths)
    
    def plot(self, ax = None):
        for path in self:
            path.plot(ax)
    
    def unpack_paths_for_velocity(self, adjust_function, params):
        lines = []
        for path in self:
            if type(path) == Hatch:
                path = [*path]
            for coord in path:
                adj_coord = adjust_function(coord, self.z, params)
                lines.append({"i":f"{INDEX.get():0>5}",
                                "x": f"{adj_coord[0]:.3f}",
                                "y": f"{adj_coord[1]:.3f}",
                                "z": f"{adj_coord[2]:.3f}"})
                INDEX.next()
        return {"lines": lines}


class Body(list[Layer]):
    '''
    Objeto representando peça a ser produzida por MA

    Parâmetros
        layers (list[Layer]): lista de camadas que produzem a peça
        center (tuple[float]): tupla com as coordenadas do centro da peça
    '''
    def __init__(self, layers: list[Layer], lims:list[tuple[float]]):
        self.lims = lims
        super().__init__(layers)
    
    def plot(self, fig:Figure = None):
        ax = fig.add_subplot(projection='3d')
        ax.set_zlim(self[0].z, self[-1].z)
        rect = PolyLine(self.surounding_rect[1:-1])
        ax.plot(rect.x,rect.y,zs=rect.z, color='black')
        for layer in self:
            layer.plot(ax)
        plt.show()
    
    def coord_num(self) -> int:
        coords = []
        for layer in self:
            for path in layer:
                if type(path) == PolyLine:
                    for point in path:
                        coords.append(point)
                if type(path) == Hatch:
                    for line in path:
                        coords.append(line[0])
                        coords.append(line[1])
        return len(coords)

    def unalternate_dirs(self):
        for layer in self:
            for path in layer:
                if type(path) == PolyLine:
                    if path.was_clockwise:
                        path.reverse()
                if type(path) == Hatch:
                    for line in path:
                        if line.was_clockwise:
                            line.reverse()
    
    @property
    def surounding_rect(self) -> PolyLine:
        '''
        Obtém os pontos que delimitam o retângulo no qual o trajeto está contido
        '''
        x0, x1 = self.lims[0]
        y0, y1 = self.lims[1]
        z0 = self.lims[2][0]
        center = ((x1+x0)/2, (y1+y0)/2, z0)
        pts = [center, (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0), (x0,y0,z0),center]
        return PolyLine(pts)

    def gen_velocity_dict(self, adjust_func, func_params) -> dict:
        '''
        Gera um dicionário com as entradas para geração de um dicionário para
        escrita no template velocity
        '''
        INDEX.restart()
        return {'layers': [layer.unpack_paths_for_velocity(adjust_func, func_params) for layer in self]}
    