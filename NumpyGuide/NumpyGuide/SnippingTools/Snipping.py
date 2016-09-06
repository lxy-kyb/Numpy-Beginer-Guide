import pygame
import sys,os
import ConfigParser
from pygame.locals import *
 
class Snipping():
    def __init__(self, configPath):
        self.screen = pygame.display.set_mode((800, 600))                
        self.redicon = pygame.image.load('redicon.png')
        self.blackicon = pygame.image.load('blackicon.png')
        self.greenicon = pygame.image.load('greenicon.png')
        self.settitle('red')
        self.clock = pygame.time.Clock()
        self._readConfig(configPath)

    def _readConfig(self,configPath):
        config = ConfigParser.ConfigParser()
        config.read(configPath)
        self.Infolder = config.get('Path','In')
        self.Redfolder = config.get('Path','Red')
        if os.path.exists(self.Redfolder) == False:
            os.mkdir(self.Redfolder)
        self.Blackfolder = config.get('Path','Black')
        if os.path.exists(self.Blackfolder) == False:
            os.mkdir(self.Blackfolder)
        self.Greenfolder = config.get('Path','Green')
        if os.path.exists(self.Greenfolder) == False:
            os.mkdir(self.Greenfolder)
        self.TxtPath = config.get('Path','Txt')
        if os.path.exists(self.TxtPath) == False:
            os.mkdir(self.TxtPath)
        self.postfix = config.get('Path','Postfix')
        
        self.RedTxt = open(self.TxtPath + 'r.txt', 'w+')
        self.GeenTxt = open(self.TxtPath + 'g.txt', 'w+')
        self.BlackTxt = open(self.TxtPath + 'b.txt', 'w+')
        self.list_In = []
        for pic in os.listdir(self.Infolder):
           if ''.join(pic).split('.')[1] == self.postfix:
               self.list_In.append(pic)
        self.dic_red = dict()
        self.dic_black = dict()
        self.dic_green = dict()
        self.PicIndex = 0

    def settitle(self,colorName):
        self.color = pygame.color.THECOLORS[colorName]
        if self.color == pygame.color.THECOLORS["black"]:
            pygame.display.set_caption("black")
            pygame.display.set_icon(self.blackicon)
        elif self.color == pygame.color.THECOLORS["green"]:
            pygame.display.set_caption("green")
            pygame.display.set_icon(self.greenicon)
        else:
            pygame.display.set_caption("red")
            pygame.display.set_icon(self.redicon)

    def _save(self):
        self.screen.blit(self.pic ,[0,0])
        ret = pygame.Rect(self.start[0],self.start[1], self.end[0] - self.start[0], self.end[1] - self.start[1])
        if self.color == pygame.color.THECOLORS["black"]:            
            filename = self.Blackfolder + self.list_In[self.PicIndex]
            pygame.image.save(pygame.display.get_surface().subsurface(ret), filename)
            self.dic_black[self.list_In[self.PicIndex]] = str.format(' {0} {1} {2} {3}\n',self.start[0],self.start[1],self.end[0],self.end[1])
            #self.BlackTxt.write(self.list_In[self.PicIndex] + str.format(' {0},{1} {2},{3}\n',self.start[0],self.start[1],self.end[0],self.end[1]))            
        elif self.color == pygame.color.THECOLORS["green"]:
            filename = self.Greenfolder + self.list_In[self.PicIndex]
            pygame.image.save(pygame.display.get_surface().subsurface(ret), filename)
            self.dic_green[self.list_In[self.PicIndex]] = str.format(' {0} {1} {2} {3}\n',self.start[0],self.start[1],self.end[0],self.end[1])
            #self.GreenTxt.write(self.list_In[self.PicIndex] + str.format(' {0},{1} {2},{3}\n',self.start[0],self.start[1],self.end[0],self.end[1]))
        else:
            filename = self.Redfolder + self.list_In[self.PicIndex]
            pygame.image.save(pygame.display.get_surface().subsurface(ret), filename)
            self.dic_red[self.list_In[self.PicIndex]] = str.format(' {0} {1} {2} {3}\n',self.start[0],self.start[1],self.end[0],self.end[1])
            #self.RedTxt.write(self.list_In[self.PicIndex] + str.format(' {0},{1} {2},{3}\n',self.start[0],self.start[1],self.end[0],self.end[1]))

    def _loadpic(self):
        self.pic = pygame.image.load(self.Infolder + self.list_In[self.PicIndex])
        self.screen.fill([255,255,255])
        self.screen.blit(self.pic, [0,0])    

    def stop(self):
        for red in self.dic_red:
            self.RedTxt.write(red + self.dic_red[red])
        self.RedTxt.close()
        for black in self.dic_black:
            self.BlackTxt.write(black + self.dic_black[black])
        self.BlackTxt.close()
        for green in self.dic_green:
            self.GeenTxt.write(green + self.dic_green[green])
        self.GeenTxt.close()


    def _nextpic(self):
        if self.PicIndex < len(self.list_In) - 1:
            self.PicIndex += 1
        self._loadpic()   
    def _prepic(self):
        if self.PicIndex > 0:
            self.PicIndex -= 1
        self._loadpic()
        

    def run(self):
        self.mousepos = None
        self.start = None
        self._loadpic()
        while True:
            # max fps limit
            self.clock.tick(50)   
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        self.settitle("red")
                    elif event.key == K_2:
                        self.settitle("black")
                    elif event.key == K_3:
                        self.settitle("green")
                    elif event.key == K_RETURN:
                        if self.start is not None and self.end is not None:
                            self._save()    
                            self._nextpic()                             
                    elif event.key == K_LEFT:
                        self._prepic()
                    elif event.key == K_RIGHT:
                        self._nextpic()                                     
                if event.type == QUIT:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    self.start = pygame.mouse.get_pos()
                    self.mousepos = pygame.mouse.get_pos()
                    self.end = None
                    pass
                elif event.type == MOUSEMOTION:                    
                    pos = pygame.mouse.get_pos()
                    if self.mousepos is not None:
                        self._loadpic()
                        ret = pygame.Rect(self.start[0],self.start[1], pos[0] - self.start[0], pos[1] - self.start[1])
                        pygame.draw.rect(self.screen,self.color,ret, 1)
                    pass
                elif event.type == MOUSEBUTTONUP:
                    self.end = pygame.mouse.get_pos()
                    self.mousepos = None
                    pass           
            pygame.display.update()
 
if __name__ == '__main__':
    app = Snipping('Snipping.config')
    app.run()
    app.stop()
    exit()