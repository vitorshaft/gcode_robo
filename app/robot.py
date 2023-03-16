from _collections_abc import Callable
from airspeed import Template
from model import Body

class Robot:
    def __init__(self,
                 template_path: str,
                 adjust_function: Callable,
                 robot_constants: dict):
        with open(template_path, 'r') as file:
            self.template = Template(file.read())
        self.adjust_function = adjust_function
        self.constants = robot_constants
    
    def generate_code(self, body:Body, params:dict):
        velocity_params = {**body.gen_velocity_dict(self.adjust_function, params),
                           **params,
                           **self.constants}
        return self.template.merge(velocity_params)


def adjust_coords_yask(coords, layer_z, params):
    x = params['x'] + coords[0]
    y = params['y'] + coords[1]
    z = params['z'] + params['dbcp'] + layer_z
    return x,y,z


Yaskawa = Robot("yaskawa_jbi_template.vm", adjust_coords_yask,
                {"ang": [-179.3958, -7.3004, 0.7371]})
