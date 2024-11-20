import math
import pygame as py
import numpy as np
import parteeprojection as pp

def init(window):
    global screen
    screen = window

def renderArrow(color, start, end, arrow_size=10):
    start = pp.projection.projectPoint(start)
    end = pp.projection.projectPoint(end)
    angle = np.arctan2(end[1] - start[1], end[0] - start[0])
    arrow_points = [
        (end[0] - arrow_size * np.cos(angle - np.pi / 6), end[1] - arrow_size * np.sin(angle - np.pi / 6)),
        (end[0] - arrow_size * np.cos(angle + np.pi / 6), end[1] - arrow_size * np.sin(angle + np.pi / 6))
    ]
    py.draw.polygon(screen, color, [end, *arrow_points])
    
def renderLine(color, start, end, size = 2):
    py.draw.line(screen, color, pp.projection.projectPoint(start), pp.projection.projectPoint(end), size)
    
def renderAxies():
    pp.render.renderLine(pp.colors.red, (0,0,0), (0,0,100))
    pp.render.renderLine(pp.colors.green, (0,0,0), (0,100,0))
    pp.render.renderLine(pp.colors.blue, (0,0,0), (100,0,0))

    pp.render.renderArrow(pp.colors.red, (0,0,0), (0,0,100))
    pp.render.renderArrow(pp.colors.green, (0,0,0), (0,100,0))
    pp.render.renderArrow(pp.colors.blue, (0,0,0), (100,0,0))
    pp.render.renderCircle(pp.colors.white, (0,0,0))
    
def renderCircle(color, center, radius = 3, size = 3):
    py.draw.circle(screen, color, pp.projection.projectPoint(center), radius, size)
    
def renderText(text, color, origin, size = 20):
    font = py.font.Font(None, size)
    text = font.render(text, True, color)
    screen.blit(text, pp.projection.projectPoint(origin))
    
def renderIsosahedron(color, radius, thickness = 2):
    points = pp.constants.icosahedronPoints
    edges = pp.constants.icosahedronEdges
    
    points = [[radius * x / math.sqrt(x**2 + y**2 + z**2),
                radius * y / math.sqrt(x**2 + y**2 + z**2),
                radius * z / math.sqrt(x**2 + y**2 + z**2)] for x, y, z in points]
    
    for edge in edges:
        pp.render.renderLine(color, points[edge[0]], points[edge[1]], thickness)
        
def renderDodecahedron(color, radius, thickness = 2):
    points = pp.constants.dodecahedronPoints
    edges = pp.constants.dodecahedronEdges
    
    points = [[radius * x / math.sqrt(x**2 + y**2 + z**2),
                radius * y / math.sqrt(x**2 + y**2 + z**2),
                radius * z / math.sqrt(x**2 + y**2 + z**2)] for x, y, z in points]
    
    for edge in edges:
        pp.render.renderLine(color, points[edge[0]] , points[edge[1]], thickness)
        

    
def rotateY(theta_per_second = 0.25):
    
    # Calculate the rotation angle based on deltaTime
    angle = np.radians(theta_per_second * pp.projection.deltaTime)
    
    rotation_matrix = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    
    pp.normal = np.dot(rotation_matrix, pp.normal)
    
def rotateX(theta_per_second = 0.25):
    # Calculate the rotation angle based on deltaTime
    angle = np.radians(theta_per_second * pp.projection.deltaTime)
    
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])
    
    normal = np.dot(rotation_matrix, normal)