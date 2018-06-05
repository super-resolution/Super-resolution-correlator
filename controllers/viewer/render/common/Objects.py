from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy as np


class Cube:
    def __init__(self):
        O = -1.0
        X = 1.0
        positions = np.array([O, O, O, O, O, X, O, X, O, O, X, X, X, O, O, X, O, X, X, X, O, X, X, X,],dtype="f")
        indices = np.array([
        7, 3, 1, 1, 5, 7,
        0, 2, 6, 6, 4, 0,
        6, 2, 3, 3, 7, 6,
        1, 0, 4, 4, 5, 1,
        3, 2, 0, 0, 1, 3,
        4, 6, 7, 7, 5, 4,
        ], dtype=np.int32)
        #Create the VBO for positions:
        self.vertex_vbo = vbo.VBO(data=positions, usage=GL_STATIC_DRAW, target=GL_ARRAY_BUFFER)
        #Create the VBO for indices:
        self.index_vbo = vbo.VBO(data=indices ,usage=GL_STATIC_DRAW, target=GL_ELEMENT_ARRAY_BUFFER)


class Quad:
    def __init__(self):
        positions = np.array([
        [-1, -1],
         [-1, 1],
        [1,  -1],
         [1,  1],
        ], dtype="f")
        self.vertex_vbo = vbo.VBO(data=positions, usage=GL_STATIC_DRAW, target=GL_ARRAY_BUFFER)


class Texture:
    def __init__(self):
        positions = np.array([
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            ], dtype="f")
        self.vertex_vbo = vbo.VBO(data=positions, usage=GL_STATIC_DRAW, target=GL_ARRAY_BUFFER)


class Surface:
    def __init__(self):
        positions = np.array([
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            ],dtype="f")
        #indices = np.array([
        #    0, 1, 2,
        #    2, 1, 3
        #], dtype=np.int32)
        #Create the VBO for positions:
        self.vertex_vbo = vbo.VBO(data=positions, usage=GL_STATIC_DRAW, target=GL_ARRAY_BUFFER)
        #Create the VBO for indices:
        #self.index_vbo = vbo.VBO(data=indices, usage=GL_STATIC_DRAW, target=GL_ELEMENT_ARRAY_BUFFER)