from OpenGL.GL import *
import numpy as np


class Create2DTexture:
    def __init__(self):
        self.textureHandle = glGenTextures(1)
        self.dataSet = False

    def set_texture(self, data, interpolation):
        glEnable(GL_TEXTURE_2D)
        glTexImage2D(GL_PROXY_TEXTURE_2D, 0, GL_RGBA, data.shape[0], data.shape[1], 0, GL_RED, GL_UNSIGNED_BYTE, None)
        if glGetTexLevelParameteriv(GL_PROXY_TEXTURE_2D, 0, GL_TEXTURE_WIDTH) == 0:
            raise Exception("OpenGL failed to create 2D texture (%dx%d); too large for this hardware." % data.shape[:2])

        glBindTexture(GL_TEXTURE_2D, self.textureHandle)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, interpolation)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, interpolation)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 2)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, data.shape[0],
                     data.shape[1], 0, GL_RED, GL_UNSIGNED_BYTE, data.astype(np.uint8))
        glBindTexture(GL_TEXTURE_2D,0)
        self.dataSet = True


class Create3DTexture:
    def __init__(self):
        self.textureHandle = glGenTextures(1)
        self.dataSet = False

    def set_texture(self, data):
        width = data.shape[1]
        height = data.shape[2]
        depth = data.shape[0]

        glTexImage3D(GL_PROXY_TEXTURE_3D, 0, GL_RGBA, width, height, depth, 0, GL_RED, GL_UNSIGNED_BYTE, data)
        if glGetTexLevelParameteriv(GL_PROXY_TEXTURE_3D, 0, GL_TEXTURE_WIDTH) == 0:
            raise Exception("OpenGL failed to create 3D texture (%dx%d); too large for this hardware."
                            % data.shape[:2]+ " max = "+str(glGetIntegerv(GL_MAX_3D_TEXTURE_SIZE)))

        glBindTexture(GL_TEXTURE_3D, self.textureHandle)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_WRAP_S,GL_CLAMP)
        glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_WRAP_T,GL_CLAMP)
        glTexParameteri(GL_TEXTURE_3D,GL_TEXTURE_WRAP_R,GL_CLAMP)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 2)
        glTexImage3D(GL_TEXTURE_3D, 0, GL_RGBA, width, height, depth, 0,
                     GL_RED, GL_UNSIGNED_BYTE, data.astype(np.uint8))
        glBindTexture(GL_TEXTURE_3D,0)
        self.dataSet = True

class CreateNoise:
    def __init__(self):
        self.textureHandle = glGenTextures(1)

    def set_texture(self, width, height):
        pixels = np.random.rand(width, height)*255
        glBindTexture(GL_TEXTURE_2D, self.textureHandle)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_R8, width, height, 0, GL_RED, GL_UNSIGNED_BYTE, pixels.astype(np.uint8))

    def get_texture_handle(self):
        return self.textureHandle