"""
=================================================================================
Class to render multiple objects on GPU(points, image2D, image3D
=================================================================================
"""
import numpy as np
import os
import math
from PIL import Image
from OpenGL.GL import *
from OpenGL.arrays import vbo
from PyQt5 import QtCore
from pyqtgraph.opengl.GLGraphicsItem import GLGraphicsItem
from .Shader import *
from .common import Textures, Objects, Surface, Buffer

class custom_graphics_item(GLGraphicsItem):
    """
    Bases on QtCore.QGraphics item should work in every Qt OpenGL context
    """
    def __init__(self, **kwds):
        super().__init__()
        basepath = os.path.dirname(os.path.realpath(__file__)) +r"\shaders"
        if "filename" in kwds.keys():
            self.filename = basepath + kwds.pop("filename")
        else:
            raise Exception("Need shaders filenames")
        self.modelview = []
        self.projection = []
        self._shader = shader(self.filename)

    def background_render(self,size, ratio, rect = (0,0,0,0)):
        self.width = int(size.x()*ratio)#int(896/322*1449)
        self.height = int(size.y()*ratio)
        if rect[3] != 0:
            rect = (rect[0]*ratio,rect[1]*ratio,rect[2]*ratio,rect[3]*ratio)
        else:
            rect = (rect[0]*ratio,rect[1]*ratio,self.width,self.height)
        #self.roi = rect
        self.backgroundRender = True
        model = QtGui.QMatrix4x4()
        X = self.position[:,0].max() #- self.position[:,0].min()
        Y = self.position[:,1].max()# - self.position[:,1].min()
        print(self.position[:,0].max())
        print(self.position[:,1].max())
        Xt = X/2 #+ self.position[:,0].min()
        Yt = Y/2 #+ self.position[:,1].min()
        glTexImage2D(GL_PROXY_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        if glGetTexLevelParameteriv(GL_PROXY_TEXTURE_2D, 0, GL_TEXTURE_WIDTH) == 0:
            raise Exception("OpenGL failed to create 2D texture (%dx%d); too large for this hardware." )
            return
        center = QtGui.QVector3D(Xt, Yt, 0)
        dist = math.tan(math.radians(60))*Y/2# Field of view in Y direction
        eye = QtGui.QVector3D(Xt, Yt, dist)#Point of eye in space
        up = QtGui.QVector3D(0, 1, 0)
        model.lookAt(eye,center,up)
        self.modelview = model
        proj = QtGui.QMatrix4x4()
        aspect  = float(self.width)/float(self.height)#aspect ratio of display
        proj.perspective(60.0, aspect, dist*0.0001, dist*10000.0)
        self.projection = proj
        #self._m_clusterTest.set_array(np.zeros(self.position.shape[0],dtype="f"))
        renderbuffer = Buffer.Renderbuffer()
        renderbuffer.build(self.width, self.height)
        texturebuffer = Buffer.Texturebuffer()
        texturebuffer.build(self.width, self.height)
        framebuffer = Buffer.Framebuffer()
        framebuffer.build(renderbuffer.handle, texturebuffer.handle)

        try:
            glBindFramebuffer(GL_FRAMEBUFFER, framebuffer.handle)
            glViewport(0, 0, self.width, self.height)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.paint()
        finally:
            glReadBuffer(GL_COLOR_ATTACHMENT0)
            buf = glReadPixels(rect[0],rect[1],rect[2], rect[3], GL_RGBA, GL_UNSIGNED_BYTE)
            image = Image.frombytes(mode="RGBA", size=(int(rect[2]), int(rect[3])), data=buf)
            self.image = image.transpose(Image.FLIP_LEFT_RIGHT)
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            renderbuffer.delete()
            texturebuffer.delete()
            framebuffer.delete()
            self.backgroundRender = False
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def paint(self):
        """
        Drawing the object:
            update buffers and uniforms
            set matrices
            set enumerators
            set buffers
            draw
            clean up
        """
        if not self.backgroundRender:
            self.modelview = self.view().viewMatrix()*self.viewTransform()
            self.projection = self.view().projectionMatrix()
        self._shader.__setitem__("u_modelview", self.modelview)
        self._shader.__setitem__("u_projection", self.projection)
        self.setupGLState()


class alpha_complex(custom_graphics_item):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        basepath = os.path.dirname(os.path.realpath(__file__)) +r"\shaders"
        if "filename" in kwds.keys():
            self.filename = basepath + kwds.pop("filename")
        else:
            raise Exception("Need shaders filenames")
        self.enums = [GL_POINT_SPRITE, GL_PROGRAM_POINT_SIZE, GL_DEPTH_TEST, GL_BLEND]
        self.position = np.array(([[0,0,0,0,0,0,0]]))
        self.simplices = np.zeros((1,5))
        self.size = 1
        self.alpha = 100.0
        #self.ratio = 1
        #self.fg_color = [0.0,0.0,0.0,0.0]
        #self.color = [1.0,1.0,1.0,1.0]
        self.image = None
        self.backgroundRender=False
        self.updateData = True
        self.args = ["position", "size", "color", "simplices","alpha" ]
        self._m_vertexarray_buffer = vbo.VBO(self.position[...,[0,1]].astype("f"), usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
        self._m_simplexarray_buffer = vbo.VBO(self.simplices.astype("f"), usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
        self.set_data(**kwds)

    def set_data(self, **kwds):
        """
        Set data for point cloud rendering
        :param kwds: allowed arguments are: position, size, color, maxEmission and cluster
        """
        for k in kwds.keys():
            if k not in self.args:
                raise Exception('Invalid keyword argument: %s (allowed arguments are %s)' % (k, str(self.args)))
        for arg in self.args:
            if arg in kwds:
                setattr(self, arg, kwds[arg])
        self.updateData = True

    def _update(self):
        self.updateData = False
        #self._shader.__setitem__("size", self.size)
        #self.alpha = (self.alpha+10)%200
        self._shader.__setitem__("alpha", self.alpha)
        #self._shader.__setitem__("color", self.color)
        self._m_vertexarray_buffer.set_array(self.position.astype("f") , size = None )
        self._m_simplexarray_buffer.set_array(self.simplices.astype("f"))

        #if type(self.position).__module__ == np.__name__:
        #    self.ratio = self.position[:,0].max()/self.position[:,1].max()

    def paint(self):
        super().paint()
        # Enable several enumerators
        for enum in self.enums:
            glEnable(enum)
        # Blending to get a smooth point cloud
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)#todo:overlapp via blend
        glLineWidth(float(1.0))
        if self.updateData:
            self._update()
            print("Updating Alpha data")
        with self._shader:
            # Bind buffer objects
            glEnableVertexAttribArray(1)
            self._m_vertexarray_buffer.bind()
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(2)
            self._m_simplexarray_buffer.bind()
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
            try:
                # Draw everything
                glDrawArrays(GL_LINES, 0, int(self.position.size/self.position.shape[-1]))
            finally:
                # Clean up
                glDisableVertexAttribArray(1)
                glDisableVertexAttribArray(2)
                self._m_vertexarray_buffer.unbind()
                self._m_simplexarray_buffer.unbind()
                # Disable enumerators
                for enum in self.enums:
                    glDisable(enum)

class points(custom_graphics_item):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        basepath = os.path.dirname(os.path.realpath(__file__)) +r"\shaders"
        if "filename" in kwds.keys():
            self.filename = basepath + kwds.pop("filename")
        else:
            raise Exception("Need shaders filenames")
        self.enums = [GL_POINT_SPRITE, GL_PROGRAM_POINT_SIZE, GL_DEPTH_TEST, GL_BLEND]
        self.position = np.array(([[0,0,0,0,0,0,0]]))
        self.cluster = np.array((0.0,0.0))
        self.size = 20.0#
        #self.ratio = 1
        #self.fg_color = [0.0,0.0,0.0,0.0]
        self.color = [1.0,1.0,1.0,1.0]
        self.maxEmission = 0
        self.image = None
        self.backgroundRender=False
        self.updateData = True
        self.args = ["position", "size", "color", "maxEmission", "cluster"]
        self._m_vertexarray_buffer = vbo.VBO(self.position[...,[0,1,3,4]].astype("f"), usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
        self._m_clusterarray_buffer = vbo.VBO(self.cluster.astype("f"), usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
        self.set_data(**kwds)

    def set_data(self, **kwds):
        """
        Set data for point cloud rendering
        :param kwds: allowed arguments are: position, size, color, maxEmission and cluster
        """
        for k in kwds.keys():
            if k not in self.args:
                raise Exception('Invalid keyword argument: %s (allowed arguments are %s)' % (k, str(self.args)))
        for arg in self.args:
            if arg in kwds:
                setattr(self, arg, kwds[arg])
        self.updateData = True

    def _update(self):
        self.updateData = False
        self._shader.__setitem__("size", self.size)
        self._shader.__setitem__("bg_color", self.color)
        self._shader.__setitem__("maxEmission", self.maxEmission)
        self._m_vertexarray_buffer.set_array(self.position[...,[0,1,3,4]].astype("f") , size = None )
        self._m_clusterarray_buffer.set_array(self.cluster.astype("f"))

        #if type(self.position).__module__ == np.__name__:
        #    self.ratio = self.position[:,0].max()/self.position[:,1].max()

    def paint(self):
        super().paint()
        # Enable several enumerators
        for enum in self.enums:
            glEnable(enum)
        # Blending to get a smooth point cloud
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if self.updateData:
            self._update()
            print("Updating dStorm data")
        with self._shader:
            # Bind buffer objects
            glEnableVertexAttribArray(1)
            self._m_vertexarray_buffer.bind()
            glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(2)
            self._m_clusterarray_buffer.bind()
            glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, 0, None)
            try:
                # Draw everything
                glDrawArrays(GL_POINTS, 0, int(self.position.size/self.position.shape[-1]))
            finally:
                # Clean up
                glDisableVertexAttribArray(1)
                glDisableVertexAttribArray(2)
                self._m_vertexarray_buffer.unbind()
                self._m_clusterarray_buffer.unbind()
                # Disable enumerators
                for enum in self.enums:
                    glDisable(enum)


class image(custom_graphics_item):
    """
    **Bases:** :class:`GLGraphicsItem <pyqtgraph.opengl.GLGraphicsItem>`

    Displays image data.
    """


    def __init__(self, smooth=False, glOptions='translucent',**kwds):
        """

        ==============  =======================================================================================
        **Arguments:**
        image            Microscope Image to be rendered.
                        *Must* contain: numpy array of shape[Color][Slice][Shape0][Shape1].
                                        indexlist of slices to be rendered.
                        (See functions.makeRGBA)
        filename        Shader path to use
        lut             Tick values between 0;1
        smooth          (bool) If True, the volume slices are rendered with linear interpolation
        ==============  =======================================================================================
        """
        super().__init__(**kwds)
        self.enums = [GL_TEXTURE_2D, GL_DEPTH_TEST, GL_BLEND]
        self.active_textures = [GL_TEXTURE0, GL_TEXTURE1, GL_TEXTURE2, GL_TEXTURE3]
        self.imageTexture = [Textures.Create2DTexture() for i in range(4)]
        self.Quad = Objects.Texture()
        self.Surface = Objects.Surface()
        self.scaled = False
        self.backgroundRender = False
        self.image = None
        self.ch_numb = 0
        self.data = 0
        self.color = 0
        self.flip_lr = False
        self.flip_ud = False

    def set_data(self, data, color, ch_numb, flip_lr=False, flip_ud=False, smooth=True):
        self.ch_numb = ch_numb
        self.data = data
        self.color = color
        self.flip_lr = flip_lr
        self.flip_ud = flip_ud
        for i in ch_numb:
            if smooth:
                self.imageTexture[i].set_texture(data[i], GL_LINEAR)
            else:
                self.imageTexture[i].set_texture(data[i], GL_NEAREST)
        self.update()

    def paint(self):
        super().paint()
        self._shader.__setitem__("u_UD", self.flip_ud)
        self._shader.__setitem__("u_LR", self.flip_lr)
        # Set uniforms
        for i in self.ch_numb:
            self._shader.__setitem__("SIM"+str(i), i)
            self._shader.__setitem__("SIMColor"+str(i), self.color[i])
        # Set Enumerators
        for enum in self.enums:
            glEnable(enum)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        with self._shader:
            for i in self.ch_numb:
                glActiveTexture(GL_TEXTURE0+i)
                glBindTexture(GL_TEXTURE_2D, self.imageTexture[i].textureHandle)
            self.Surface.vertex_vbo.bind()
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
            self.Quad.vertex_vbo.bind()
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, None)
            try:
                glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
            finally:
                # Clean up
                for enum in self.enums:
                    glDisable(enum)
                glDisableVertexAttribArray(1)
                glDisableVertexAttribArray(2)
                self.Surface.vertex_vbo.unbind()
                self.Quad.vertex_vbo.unbind()
                for i in range(4):
                    glActiveTexture(GL_TEXTURE3-i)
                    glBindTexture(GL_TEXTURE_2D, 0)


class raycast(GLGraphicsItem):
    """
    Do some crazy shit to get a 3D interpolation of your image
    """
    def __init__(self, smooth=False, glOptions='translucent', **kwds):
        GLGraphicsItem.__init__(self)
        #super().__init__(**kwds)
        glEnable(GL_TEXTURE_3D)
        self.setGLOptions(glOptions)
        self._init_structures__()
        self._init_shader_programs__()
        self.imageTexture = [Textures.Create3DTexture() for i in range(4)]
        self.noiseTexture = Textures.CreateNoise()
        self.data = []
        self.chNumb = []
        self.color = []
        self.scaled = False
        self.flipLR = False
        self.flipUD = False
        self._needUpdate = False
        self.backgroundRender = False

    def _init_structures__(self):
        self.Quad = Objects.Quad()
        self.Cube = Objects.Cube()
        self.RayEndPointsSurface = Surface.CSurface()

    def _init_shader_programs__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self._RayEndPointsProgram = shader(self.path + r"\shaders\raycast\RayEndpoints")
        self.set_raycast_shaders()

    def set_raycast_shaders(self, predefined=1, path=None):
        #if path is None:
            #if predefined == 1:
        self._RayCastProgram = shader(self.path + r"\shaders\raycast\Semitransparent")
            #if predefined == 2:
                #self._RayCastProgram = Shader(self.path + r"\shader\Lighting")
        #else:
            #if path is not None:
                #self._RayCastProgram = Shader(path)

    def set_data(self, data, color, ch_numb, flip_lr=False, flip_ud=False):

        self.color = color
        self.chNumb = ch_numb
        self.flipLR = flip_lr
        self.flipUD = flip_ud

        if not flip_ud:
            y = []
            for i in data:
                y.append([np.flipud(stack) for stack in i])
            data = np.asarray(y)
        if flip_lr:
            y = []
            for i in data:
                y.append([np.fliplr(stack) for stack in i])
            data = np.asarray(y)
        self.data = data[:,:,0:glGetIntegerv(GL_MAX_3D_TEXTURE_SIZE),0:glGetIntegerv(GL_MAX_3D_TEXTURE_SIZE)]
#        self.noiseTexture.set_texture(data[1].shape[1], data[1].shape[2])
        for i in ch_numb:
            self.imageTexture[i].set_texture(self.data[i])
        self._needUpdate = True

    def paint(self):
        self.RayEndPointsSurface.build_surface(self.view().width(), self.view().height(), 3, 2)
        #Find screen-space AABB for scissoring:
        #const float M = std::numeric_limits<float>::max()
        #M = 1
        # minCorner = QtGui.QVector3D(0, 0, 0)
        # maxCorner = QtGui.QVector3D(0, 0, 0)
        # for cornerIndex in range(8):
        #     corner = QtGui.QVector3D(
        #         -1.0 if (cornerIndex & 0x1) else +1.0,
        #         -1.0 if (cornerIndex & 0x2) else +1.0,
        #         -1.0 if (cornerIndex & 0x4) else +1.0)
        #
        #     corner = corner.toVector4D()
        #     corner.setW(1.0)
        #     v = self.view().projectionMatrix() * self.view().viewMatrix() * self.viewTransform() * corner
        #     p = v.toVector3D()/v.w()
        #     minCorner = min(p, minCorner)
        #     maxCorner = max(p, maxCorner)
        # minCorner += QtGui.QVector3D(1.0, 1.0, 0)
        # maxCorner += QtGui.QVector3D(1.0, 1.0, 0)
        # viewport = QtGui.QVector3D(self.view().width()/2,self.view().height()/2, 1.0)
        # minCorner = minCorner * viewport
        # maxCorner = maxCorner * viewport
        # extent = maxCorner - minCorner
        # glScissor(
        #      int(minCorner.x()), int(minCorner.y()),
        #      int(extent.x()), int(extent.y()))
        #Update the ray start & stop surfaces:
        glBlendFunc(GL_ONE, GL_ONE)
        glDisable(GL_DEPTH_TEST)
        self._RayEndPointsProgram.__setitem__("u_modelview", self.view().viewMatrix()*self.viewTransform())
        self._RayEndPointsProgram.__setitem__("u_projection", self.view().projectionMatrix())
        self._set_uniforms()
        with self._RayEndPointsProgram:
            glBindFramebuffer(GL_FRAMEBUFFER, self.RayEndPointsSurface.surface.FboHandle)
            glEnable(GL_BLEND)
            glDrawBuffers(n=2, bufs=(GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1))
            glClearColor(0, 0, 0, 0)
            glClear(GL_COLOR_BUFFER_BIT)
            self.Cube.index_vbo.bind()
            self.Cube.vertex_vbo.bind()
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            #glEnable(GL_SCISSOR_TEST)
            try:
                glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
            finally:
                glDisableVertexAttribArray(0)
                #glDisable(GL_SCISSOR_TEST)
                glDisable(GL_BLEND)
                self.Cube.vertex_vbo.unbind()
                self.Cube.index_vbo.unbind()
                glBindFramebuffer(GL_FRAMEBUFFER, 0)

        #Perform the raycast:
        #background render in
        if self.backgroundRender:
            glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer.handle)
            glViewport(0, 0, self.width, self.height)
        with self._RayCastProgram:
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_DST_COLOR)
            #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            #glDrawBuffers(n=2, bufs=(GL_BACK_LEFT, GL_NONE))
            #glEnable(GL_SCISSOR_TEST)
            self._load_end_points()
            self._load_textures()
            self.Quad.vertex_vbo.bind()
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
            try:
                glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
            except:
                raise
            finally:
                #glDisable(GL_SCISSOR_TEST)
                self._clear_active_textures()
                glDisableVertexAttribArray(0)
                self.Quad.vertex_vbo.unbind()

    def _set_uniforms(self):
        self._RayCastProgram.__setitem__("u_RayStart", 0)
        self._RayCastProgram.__setitem__("u_RayStop", 1)
        #self._RayEndPointsProgram.__setitem__("u_LR", self.flipLR)
        #self._RayEndPointsProgram.__setitem__("u_UD", self.flipUD)
        for i in self.chNumb:
            self._RayCastProgram.__setitem__("u_Color" + str(i), self.color[i])
            self._RayCastProgram.__setitem__("u_Volume" + str(i),i+2)
        if self._RayCastProgram.filename == "Lighting":
            self._RayCastProgram.__setitem__("u_Noise", 3)
            self._RayCastProgram.__setitem__("LightPosition", [0.25, 0.25, 1.0])
            self._RayCastProgram.__setitem__("DiffuseMaterial",[1.0, 1.0, 0.5])
            self._RayCastProgram.__setitem__("NormalMatrix",
                                              (self.view().viewMatrix()*self.viewTransform()).normalMatrix())

    def _load_end_points(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.RayEndPointsSurface.surface.TextureHandle[0])
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.RayEndPointsSurface.surface.TextureHandle[1])

    def _load_textures(self):
        for numb in self.chNumb:
            #if self.imageTexture[numb].dataSet:
                glActiveTexture(GL_TEXTURE2+numb)
                glBindTexture(GL_TEXTURE_3D, self.imageTexture[numb].textureHandle)
        if self._RayCastProgram.filename == "Lighting":
            glActiveTexture(GL_TEXTURE3)
            glBindTexture(GL_TEXTURE_2D, self.noiseTexture.textureHandle)

    def _clear_active_textures(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, 0)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_3D, 0)
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, 0)
        glActiveTexture(GL_TEXTURE0)


class roi(custom_graphics_item):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.position = np.array(())
        self.start = QtGui.QVector2D()
        self.end = QtGui.QVector2D()
        self.filename = ""
        self.size = 40.0#
        self.u_color = [1.0,1.0,1.0,1.0]
        self.rect = QtCore.QRect()
        self.modelview = []
        self.projection = []
        if "filename" in kwds.keys():
            kwds.pop("filename")
        self.backgroundRender = False


        self.args = ["start", "end", "size", "u_color"]

        self._m_VertexarrayBuffer  = glGenBuffers(1)
        self.set_data(**kwds)


    def set_data(self, **kwds):
        for k in list(kwds.keys()):
            if k not in self.args:
                raise Exception('Invalid keyword argument: %s (allowed arguments are %s)' % (k, str(self.args)))
        for arg in self.args:
            if arg in kwds:
                setattr(self, arg, kwds[arg])
        #self._shader.__setitem__("size", self.size)
        self._shader.__setitem__("u_color", self.u_color)
        self.createRect(self.start, self.end)

        glBindBuffer(GL_ARRAY_BUFFER, self._m_VertexarrayBuffer)
        glBufferData(GL_ARRAY_BUFFER, self.position.astype("f"), GL_STREAM_DRAW,)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def createRect(self, start, end):
        self.rect.setCoords(start.x(),
                            start.y(),
                            end.x(),
                            end.y())
        self.rect = self.rect.normalized()
        self.position = np.array([(start.x(),  start.y()),
                                  (start.x(),  end.y()),
                                  (end.x(),    end.y()),
                                  (end.x(), start.y()),
                                  (start.x(),  start.y())]
                                 )

    def paint(self):
        super().paint()
        self.setupGLState()
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE)

        with self._shader:
            glEnableVertexAttribArray(1)
            glBindBuffer(GL_ARRAY_BUFFER, self._m_VertexarrayBuffer)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
            try:
                glDrawArrays(GL_LINE_STRIP, 0, int(self.position.size/self.position.shape[-1]))
            finally:
                glDisableVertexAttribArray(1)
                glBindBuffer(GL_ARRAY_BUFFER, 0)
                glDisable(GL_BLEND)
                #glDeleteBuffers(1, self._m_VertexarrayBuffer)