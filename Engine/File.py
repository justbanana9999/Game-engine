from ast import literal_eval

class File:
    def __init__(self,path:str):
        self.path = path
    
    def load(self):
        vars = []
        with open(self.path,'r') as file:
            lines = file.read().split('\n')
            lines = [line for line in lines if not (line.isspace() or len(line) == 0)]
            for line in lines:
                vars.append(literal_eval(line))

        return vars
    
    def save(self,*vars):
        with open(self.path,'w') as file:
            vars = [f'{repr(var)}' for var in vars]
            file.write('\n'.join(vars))