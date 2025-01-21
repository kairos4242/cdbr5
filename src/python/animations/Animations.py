from abc import abstractmethod
from typing import Type
import pygame
import os
        

class Animation:

    def __init__(self, file_path: str, num_frames: int, size: tuple[int, int]):
        self.num_frames = num_frames
        self.file_path = file_path
        self.size = size
        self.sprites = []
        self.initialized = False #should these all be always initialized at game start? would it be helpful or hurtful to do so dynamically?

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def get_sprite(self, index: int):
        pass
    
class FrameAnimation(Animation):
    def __init__(self, file_path: str, num_frames: int, size: tuple[int, int]):
        super().__init__(file_path, num_frames, size)

    def initialize(self):
        self.initialized = True
        for i in range(self.num_frames - 1):
            number = f"{i:05d}" #leading zeros
            image = pygame.image.load(self.file_path + f'_{number}.png')
            self.sprites.append(image)


class SpritesheetAnimation(Animation):

    def __init__(self, file_path: str, num_frames: int, size: tuple[int, int]):
        super().__init__(file_path, num_frames, size)

    def initialize(self):
        self.initialized = True
        self.sprites = self.sprite_sheet(self.file_path, self.num_frames, self.size, True)

    def get_sprite(self, index: int):
        return self.sprites[index]

    def sprite_sheet(self, file_path, num_frames, size: tuple[int, int], has_transparency: bool):
        #modified https://stackoverflow.com/questions/10560446/how-do-you-select-a-sprite-image-from-a-sprite-sheet-in-python
        len_sprt_x,len_sprt_y = size #sprite size
        sprt_rect_x,sprt_rect_y = (0,0) #where to find first sprite on sheet

        curr_frame = 0
        
        sheet = pygame.image.load(file_path) #Load the sheet
        if has_transparency:
            sheet = sheet.convert_alpha()
        else:
            sheet = sheet.convert()
        sheet_rect = sheet.get_rect()
        sprites = []
        try:
            for i in range(0,sheet_rect.height,size[1]):#rows
                for j in range(0,sheet_rect.width,size[0]):#columns
                    sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
                    sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
                    sprites.append(sprite)
                    sprt_rect_x += len_sprt_x
                    curr_frame += 1
                    if curr_frame >= num_frames - 1:
                        raise Exception("Exiting loop") #this isn't perfect but its fin
                sprt_rect_y += len_sprt_y
                sprt_rect_x = 0

        except:
            pass

        return sprites
    
class AnimationManager:

    def __init__(self):
        self.animations = dict()

    def get_animation(self, animation_name: Type[Animation]) -> Animation:
        animation = self.animations.get(animation_name, None)
        if animation == None:
            animation = animation_name()
            animation.initialize() #right place for this?
            self.animations[animation_name] = animation
        return animation
    
class StormAnimation(SpritesheetAnimation):

    def __init__(self):
        super().__init__(os.path.join('assets', 'testing', 'Storm', 'StormSheet.png'), 480, (256, 256))