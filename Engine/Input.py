import pygame

from Engine.Constants import posLike

class Input:
    def __init__(self):
        self.alphabet = 'q w e r t y u i o p a s d f g h j k l z x c v b n m ' \
        '1 2 3 4 5 6 7 8 9 0 ' \
        'SPACE LSHIFT RSHIFT LCTRL RCTRL LALT RALT ' \
        'PERIOD COMMA SLASH BACKSLASH TAB ESCAPE SPACE ' \
        'UP DOWN LEFT RIGHT ' \
        'F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12 F13 F14 F15 ' \
        'PAGEUP PAGEDOWN'.split()

        self.keys:dict[str,bool] = {}
        self.mousePos:tuple[int,int] = (0,0)
        self.mouseInput:tuple[bool,bool,bool] = (False,False,False)

        self.pressed = False
        self.clicked = False

    def __getitem__(self,key:str|int):
        if type(key) == str:
            return self.keys[key]
        elif type(key) == int:
            return self.mouseInput[key]

    def updateInputs(self):
        key = pygame.key.get_pressed() # type: ignore
        for character in self.alphabet:
            self.keys[character] = eval(f'key[pygame.K_{character}]')
        
        self.mousePos = pygame.mouse.get_pos()
        self.mouseInput = pygame.mouse.get_pressed()
    
    def setMousePos(self,pos:posLike):
        pygame.mouse.set_pos(pos)
    
    def setMouseVisibility(self,visible:bool):
        pygame.mouse.set_visible(visible)
    
    def updatePressed(self,keys:list[str]=[]):
        if keys:
            self.pressed = any([self.keys[k] for k in keys])
        else:
            self.pressed = any(self.keys)
    
    def updateClicked(self):
        self.clicked = any(self.mouseInput)