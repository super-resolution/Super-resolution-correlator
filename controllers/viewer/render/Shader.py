"""
=================================================================================
Class to create and compile a program from vertex, fragment and geometry shaders
=================================================================================

"""
from OpenGL.GL import *
from OpenGL.GL import shaders
import os.path
import numpy as np
from PyQt5 import QtGui

#todo: add Attribute support


class shader(object):
    """
    Class to create and compile a program from vertex, fragment and geometry shaders
    checks for common build errors
    :param filepath: path to vertex fragment and (optional) geometry shaders. should all have the same name
    :var m_program: reference number to program
    """
    def __init__(self, filename):
        self.filename = os.path.basename(filename)
        self.m_shaders = []
        self.m_program = glCreateProgram()
        self.m_shaders.append(self.create_shader(self.load_shader(filename + ".vs"), GL_VERTEX_SHADER))
        self.m_shaders.append(self.create_shader(self.load_shader(filename + ".fs"), GL_FRAGMENT_SHADER))
        if os.path.exists(filename + ".gs"):
            self.m_shaders.append(self.create_shader(self.load_shader(filename + ".gs"), GL_GEOMETRY_SHADER))
        self.m_uniform = {}
        for shader in self.m_shaders:
            glAttachShader(self.m_program, GLuint(shader))
        self.link_program()
        self.validate_program()

    def link_program(self):
        """
        Link program
        :raises RuntimeError:
        """
        glLinkProgram(self.m_program)
        linkstatus = glGetProgramiv(self.m_program, GL_LINK_STATUS)
        if linkstatus != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(self.m_program).decode('ASCII'))

    def validate_program(self):
        """
        Validate program
        :raises RuntimeError:
        """
        glValidateProgram(self.m_program)
        validatestatus = glGetProgramiv(self.m_program, GL_VALIDATE_STATUS)
        if validatestatus != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(self.m_program).decode('ASCII'))

    def create_shader(self, shader, type):
        """
        Compile OpenGL shaders string and check for shaders errors
        :param shader: String of shaders
        :param type: Type of shaders can be: GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_GEOMETRY_SHADER
        :return: Shader ID
        """
        try:
            shader = shaders.compileShader(shader, type)
        except (GLError, RuntimeError) as err:
            print('Example of shaders compile error', err)
        return shader

    def load_shader(self, filename):
        """
        Load shaders string from file
        :param filename: Full path to shaders
        :return: File as string
        """
        with open(filename) as shaderString:
            shader = shaderString.read()
        return shader

    def set_uniform(self, name, data):
        if np.all(data) == None :
            del self.m_uniform[name]
        else:
            self.m_uniform[name] = data

    def uniform_loc(self, name):
        return glGetUniformLocation(self.m_program, name.encode('utf_8'))

    def attribute_loc(self, name):
        return glGetAttribLocation(self.m_program, name.encode('utf_8'))

    def __enter__(self):
        glUseProgram(self.m_program)
        try:
            for uniform, data in self.m_uniform.items():
                uniform_loc = self.uniform_loc(uniform)
                if uniform_loc == -1:
                    raise Exception('Could not find uniform variable "%s"' % uniform)

                if isinstance(data, list):
                    if len(data) == 3:
                        glUniform3fv(uniform_loc, 1, data)
                    elif len(data) == 4:
                        glUniform4fv(uniform_loc, 1, data)
                elif isinstance(data, float):
                    glUniform1fv(uniform_loc, 1, data)
                elif type(data).__module__ == np.__name__:
                    if len(data.shape) == 2:
                        if data.shape[0] == 4 and data.shape[1] == 4:
                            glUniformMatrix4fv(uniform_loc, 1, False, data)
                        if data.shape[0] == 3 and data.shape[1] == 3:
                            glUniformMatrix3fv(uniform_loc, 1, False, data)
                    elif len(data.shape) == 1:
                        if data.shape[0]==4:
                            glUniform4fv(uniform_loc, 1, data)
                        if data.shape[0] == 3:
                            glUniform3fv(uniform_loc, 1, data)
                elif isinstance(data, int) or isinstance(data, bool) :
                    glUniform1i(uniform_loc, data)
                elif isinstance(data, QtGui.QMatrix4x4):
                    glUniformMatrix4fv(uniform_loc, 1, False, data.data())
                elif isinstance(data, QtGui.QMatrix3x3):
                    glUniformMatrix3fv(uniform_loc, 1, False, data.data())
        except:
            print("Uniform Error", uniform, data)
            raise Exception(glGetError())
        
    def __setitem__(self, key, value):
        """
        Uniform value to be set in shaders program
        :param key: Name of variable in shaders program
        :param value: Value to be set can be: int, float, list, numpy array, QtGui.QMatrix
        """
        self.set_uniform(key, value)

    def __delitem__(self, key):
        """
        Uniform value to be deleted from GPU
        :param key: Name of variable in shaders program
        """
        self.set_uniform(key, None)

    def __getitem__(self, item):
        """
        Get uniform or attribute location on GPU
        :param item: Name of uniform/attribute
        :return: Location
        """
        if self.uniform_loc(item) != -1:
            return self.uniform_loc(item)
        elif self.attribute_loc(item) != -1:
            return self.attribute_loc(item)
        else:
            return None

    def __exit__(self, *args):
        if len(self.m_shaders) > 0:
            glUseProgram(0)
