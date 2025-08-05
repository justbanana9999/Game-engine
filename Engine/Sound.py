from pygame import mixer
mixer.init()

class Sound:
    def __init__(self,path:str,volume:float=1):
        self.sound = mixer.Sound(path)
        self.volume = volume
    
    def play(self,volume:float=-1):
        if volume == -1:
            volume = self.volume
        self.sound.set_volume(volume)
        self.sound.play()
    
    def stop(self):
        self.sound.stop()

    def fadeout(self,seconds:float):
        self.sound.fadeout(int(seconds*1000))