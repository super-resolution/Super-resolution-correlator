from OpenGL.GL import *
import numpy as np

class Renderbuffer:
    def __init__(self):
        self.handle = glGenRenderbuffers(1)

    def build(self, width, height):
        glBindRenderbuffer(GL_RENDERBUFFER,self.handle)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
        glBindRenderbuffer(GL_RENDERBUFFER,0)

    def delete(self):
        glDeleteRenderbuffers(1, int(self.handle)) #edit if more than one buffer

class Framebuffer:
    def __init__(self):
        self.handle = glGenFramebuffers(1)

    def build(self, renderbuf, texbuf):
        glBindFramebuffer(GL_FRAMEBUFFER, self.handle)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D,
        texbuf, 0)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, renderbuf)
        if(glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE):
           print ("Framebuffer Error")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def delete(self):
        glDeleteFramebuffers(1, int(self.handle))

class Texturebuffer:
    def __init__(self):
        self.handle = glGenTextures(1)

    def build(self, width, height):
        glBindTexture(GL_TEXTURE_2D, self.handle)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8,  width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE,None)
        glBindTexture(GL_TEXTURE_2D, 0)

    def delete(self):
        glDeleteTextures(int(self.handle))