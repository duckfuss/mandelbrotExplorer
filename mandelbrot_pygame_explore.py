import math as maths
import pygame
import numpy as np
import tkinter
'''
window = tkinter.Tk()
window.title("GUI")
'''
WIDTH = 400
HEIGHT = WIDTH
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = (0,0,0) #rgb(255,255,255), rgb(0,0,0)
        self.prec = 75
    def find_colour(self, prec):
        term_x, term_y = 0, 0
        self.prec = prec
        for iteration in range(self.prec):
            term_x, term_y = term_x**2 - term_y**2, 2 * term_x * term_y
            term_x += self.x
            term_y += self.y
            if term_x**2 + term_y**2 >= 4:
                colour_sum = iteration * 765/prec
                if colour_sum > 510:
                    self.colour = (255,255,colour_sum - 510)
                elif colour_sum > 255:
                    self.colour = (255, colour_sum - 255, 0)
                else:
                    self.colour = (colour_sum , 0, 0)
                break
    def draw(self, add_x, add_y, scale_x, scale_y):
        pygame.draw.circle(screen, self.colour, (((self.x+add_x)*scale_x), ((self.y+add_y)*scale_y)), 1)

class Graph():
    def __init__(self):
        self.points_dict = {}
        self.scale = 1/1
        self.xadj = 0
        self.yadj = 0
        self.speedup = 4
    def fill(self):
        global WIDTH, HEIGHT, prec_adj
        self.prec = int(50*(maths.log(1/self.scale)/maths.log(2))) + prec_adj
        self.granuality = 0.02 * self.scale
        self.granuality = self.granuality*self.speedup
        self.range_x_start = -2*self.scale + self.xadj
        self.range_x_stop = 2*self.scale + self.xadj
        self.range_y_start = -2*self.scale + self.yadj
        self.range_y_stop = 2*self.scale + self.yadj
        self.adj_add_x = 0 - self.range_x_start
        self.adj_add_y = 0 - self.range_y_start
        self.adj_scale_x = WIDTH/(self.range_x_stop+self.adj_add_x)
        self.adj_scale_y = HEIGHT/(self.range_y_stop+self.adj_add_y)
        self.points_dict = {}
        count = 0
        for x in np.arange(self.range_x_start, self.range_x_stop, self.granuality):
            count += 1
            for y in np.arange(self.range_y_start, self.range_y_stop, self.granuality):
                if (x,y) not in self.points_dict or self.points_dict[(x,y)].prec != self.prec:
                    point = Point(x,y)
                    point.find_colour(prec=self.prec)
                    if (x,y) in self.points_dict:
                        del self.points_dict[(x,y)]
                    self.points_dict[(x,y)] = point
            if count % 2 == 0:
                screen.fill((100,100,100))
                self.draw()
                pygame.display.update()
        print("done", self.granuality, self.xadj, self.yadj, 1/self.scale, self.prec)
    def draw(self):
        for item in self.points_dict:
            if item[0] > self.range_x_start and item[0] < self.range_x_stop and item[1] > self.range_y_start and item[1] < self.range_y_stop:
                point = self.points_dict[item]
                point.draw(self.adj_add_x, self.adj_add_y, self.adj_scale_x, self.adj_scale_y)

class Mouse_Rect():
    def __init__(self):
        self.scale = 1/2
        self.x_width = WIDTH * self.scale
        self.y_width = HEIGHT * self.scale
        self.pos = pygame.mouse.get_pos()
        self.TL = (self.pos[0]-self.x_width/2, self.pos[1]-self.y_width/2)
    def update(self):
        self.x_width = WIDTH * self.scale
        self.y_width = HEIGHT * self.scale
        self.pos = pygame.mouse.get_pos()
        self.TL = (self.pos[0]-self.x_width/2, self.pos[1]-self.y_width/2)
        pygame.draw.rect(screen, (0,0,255), (self.TL[0], self.TL[1], self.x_width, self.y_width), 2)
    def zoom(self):
        mandelbrot.xadj += ((self.pos[0]-(WIDTH/2))/100) * mandelbrot.scale
        mandelbrot.yadj += ((self.pos[1]-(HEIGHT/2))/100) * mandelbrot.scale
        mandelbrot.scale = mandelbrot.scale * self.scale
        mandelbrot.fill()
'''
def update_prec(v):
    global prec_adj
    prec_adj = int(v)
    actual_prec_label["text"] = str(mandelbrot.prec+int(v))
'''
font = pygame.font.SysFont(None, 24)
count_font = 0

prec_adj = 50
'''actual_prec_label = tkinter.Label(window)
actual_prec_label.pack()
prec_scale_var = tkinter.IntVar()
prec_scale = tkinter.Scale(window, variable=prec_scale_var, from_=-5000, to=5000, length=500, command=update_prec).pack()
'''

mandelbrot = Graph()
mouse = Mouse_Rect()
mandelbrot.fill()

print('''
Controls:
---------
Left Click = zoom to blue box
Scroll = change zoom level
Right Click = increase resolution
''')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                mouse.scale = mouse.scale/2
            elif event.y < 0:
                mouse.scale = mouse.scale * 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mandelbrot.speedup = 4
                mouse.zoom()
            if event.button == 3:
                mandelbrot.speedup = mandelbrot.speedup/2
                mandelbrot.fill()
    if count_font % 50 == 0:
        text = font.render("zoom: "+ str(1/mandelbrot.scale) + "x    prec: "+ str(mandelbrot.prec), True, (0,255,0))
    count_font += 1
    #window.update_idletasks()
    #window.update()
    screen.fill((100,100,100))
    mandelbrot.draw()
    mouse.update()
    screen.blit(text, (20, 20))
    pygame.display.update()
    clock.tick(60)
