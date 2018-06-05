from OpenGL.GL import *
import numpy as np


class CSurface:
    def __init__(self,):
        self.surface = Surface()

    def build_surface(self, width, height, numComponents, numTargets):
        self.surface.FboHandle = glGenFramebuffers(1)
        glEnable(GL_TEXTURE_2D)
        glBindFramebuffer(GL_FRAMEBUFFER, self.surface.FboHandle)
        # switch = [
        #         glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, width, height, 0, GL_RED, GL_FLOAT, None),
        #         glTexImage2D(GL_TEXTURE_2D, 0, GL_RG32F, width, height, 0, GL_RG, GL_FLOAT, None),
        #         glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, width, height, 0, GL_RGB, GL_FLOAT, None),
        #         glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGBA, GL_FLOAT, None),
        #     ]

        for attachment in range(numTargets):
            textureHandle = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, textureHandle)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            self.surface.TextureHandle[attachment] = textureHandle
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, width, height, 0, GL_RGB, GL_FLOAT, None)
            glBindTexture(GL_TEXTURE_2D, 0)
            if GL_NO_ERROR != glGetError():
                print("Unable to create FBO texture")

            colorbuffer  = glGenRenderbuffers(1)
            glBindRenderbuffer(GL_RENDERBUFFER, colorbuffer)
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + attachment, GL_TEXTURE_2D, textureHandle, 0)
            if(GL_NO_ERROR != glGetError()):
                print("Unable to attach color buffer")
            glBindRenderbuffer(GL_RENDERBUFFER, 0)

        if GL_FRAMEBUFFER_COMPLETE != glCheckFramebufferStatus(GL_FRAMEBUFFER):
            print("Unable to create FBO.")

        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)


class Volume:
    def __init__(self, width,height, depth):
        self.surface = Surface
        self.surface.FboHandle = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.surface.FboHandle)

        self.textureHandle = glGenTextures(1)
        glBindTexture(GL_TEXTURE_3D, self.textureHandle)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.surface.TextureHandle[0] = self.textureHandle

        glTexImage3D(GL_TEXTURE_3D, 0, GL_RGB16F, width, height, depth, 0, GL_RGB, GL_HALF_FLOAT, 0)

        miplevel = 0

        self.colorbuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.colorbuffer)
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.textureHandle, miplevel)
        if(GL_NO_ERROR == glGetError()):
            print("Unable to attach color buffer")

        if GL_FRAMEBUFFER_COMPLETE == glCheckFramebufferStatus(GL_FRAMEBUFFER):
            print("Unable to create FBO.")

        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)


class Surface:
    def __init__(self):
        self.FboHandle = 0
        self.TextureHandle = [0, 0]