import matplotlib.pyplot as plt

class PolyLine(list):
    '''
    Objeto que representa linhas de adição de material
    
    Parâmetros:
        points (list[tuple]): lista de pontos que compõem a linha
    '''
    def __init__(self, points: list[tuple]):
        super().__init__(points)
    
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


class Layer(list):
    def __init__(self, z: float, paths: list):
        self.z = z
        super().__init__(paths)
    
    def plot(self, ax = None):
        for path in self:
            path.plot(ax)


class Body(list[Layer]):
    '''
    Objeto representando peça a ser produzida por MA

    Parâmetros
        layers (list[Layer]): lista de camadas que produzem a peça
        center (tuple[float]): tupla com as coordenadas do centro da peça
    '''
    def __init__(self, layers: list[Layer], center:tuple[float]):
        self.O = center
        super().__init__(layers)
    
    def plot(self):
        ax = plt.figure().add_subplot(projection='3d')
        ax.set_zlim(self[0].z, self[-1].z)
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