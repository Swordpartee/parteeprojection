import math
import numpy as np
import pygame as py

deltaTime = 0

def updateDeltaTime(newDeltaTime):
    global deltaTime
    deltaTime = newDeltaTime

def init(normalVector, size):
    global normal, screenSize
    
    # Normalize the normal vector
    # normal = np.array(normalVector) / np.linalg.norm(normalVector)
    normal = np.array(normalVector)
    screenSize = size

def projectOntoNormal(point):
    global normal
    
    # Find the dot product of the point and the normal
    dotProduct = sum([point[i] * normal[i] for i in range(3)])
    
    # Multiply the dot product by the normal
    scaledNormal = [dotProduct * normal[i] for i in range(3)]
    
    # Subtract the scaled normal from the point
    return [point[i] - scaledNormal[i] for i in range(3)]

def findOrthogonalVectors():
    global normal
    
    # Check if the normal vector is not aligned with the z-axis
    if normal[0] != 0 or normal[1] != 0:
        # Create a vector orthogonal to the normal in the xy-plane
        o1 = np.array([-normal[1], normal[0], 0])
    else:
        # If the normal is aligned with the z-axis, choose an arbitrary orthogonal vector
        o1 = np.array([1, 0, 0])
    
    # Normalize the first orthogonal vector
    o1 = o1 / np.linalg.norm(o1)
    
    # Find the second orthogonal vector using the cross product
    o2 = np.cross(normal, o1)
    
    # Normalize the second orthogonal vector
    o2 = o2 / np.linalg.norm(o2)
    
    return o1, o2
    
def projectPoint(point):
    global normal
    
    # Project the point onto the plane
    projected_point = projectOntoNormal(point)
    
    # Find orthogonal vectors to define the screen's coordinate system
    o1, o2 = findOrthogonalVectors()
    
    # Transform the projected point to the screen's 2D coordinate system and translate the origin to the center of the screen
    x = -np.dot(projected_point, o1) + screenSize[0] / 2
    y = -np.dot(projected_point, o2) + screenSize[1] / 2
    
    return [x, y]

def addPoints(point1, point2):
    return [point1[i] + point2[i] for i in range(3)]

def calculate_distance(point):
    # Calculate the Euclidean distance from the origin (camera)
    return np.linalg.norm(point)

def sort_points_by_distance(points, normal):
    # Project points and calculate their distances
    projectedPoints = [(projectPoint(point, normal), calculate_distance(point)) for point in points]
    
    # Sort points by distance (farthest to closest)
    projectedPoints.sort(key=lambda x: x[1], reverse=True)
    
    return [p[0] for p in projectedPoints]

def rotateZ(theta_per_second = 0.25): 
    global normal
       
    # Calculate the rotation angle based on deltaTime
    angle = np.radians(theta_per_second * deltaTime)
    
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    
    normal = np.dot(rotation_matrix, normal)