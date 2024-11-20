import pygame as py
from . import projection, colors, render, constants

py.init()

__all__ = ['projection', 'render', 'colors', 'constants']

def init(main, normalVector = [0, 0, 1], title = "3D Projection", size = (800, 600)):
    global screen, normal, screenSize, lastTime
    
    screen = py.display.set_mode(size)
    screenSize = size
    normal = normalVector
    lastTime = py.time.get_ticks()
    
    py.display.set_caption(title)
    projection.init(normal, screenSize)
    render.init(screen)
    
    while True:
        main()
        update()
        py.time.wait(10)
    
def update(color = colors.black):
    global lastTime

    currentTime = py.time.get_ticks()
    deltaTime = (currentTime - lastTime) / 10.0
    lastTime = currentTime   
    
    projection.updateDeltaTime(deltaTime)
    
    py.display.update()
    screen.fill(color)
    
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            quit()