# Copyright (c) 2018-2022, Sebastian Reinhard
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the names of any
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""
=================================================================================
Class to efficiently perform General Hough Transformation on GPU
=================================================================================
:Author:
  `Sebastian Reinhard`

:Organization:
  Biophysics and Biotechnology, Julius-Maximillians-University of Würzburg

:Version: 2018.03.09

"""

import pycuda
import pycuda.autoinit
import pycuda.driver as drv
import numpy as np
import cv2
from pycuda.compiler import SourceModule
import time
mod = SourceModule("""
typedef struct {
    int width;
    int height;
    int stride;
    int* elements;
} Matrix;

typedef struct {
    int width;
    int height;
    int stride;
    float* elements;
} Matrixf;

 __device__ Matrix GetSubMatrix(Matrix A, int row, int col, int block_size)
{
    Matrix Asub;
    Asub.width    = block_size;
    Asub.height   = block_size;
    Asub.stride   = A.stride;
    Asub.elements = &A.elements[A.stride * block_size * row
                                         + block_size * col];
    return Asub;
}

 __device__ Matrixf GetSubMatrixf(Matrixf A, int row, int col, int block_size)
{
    Matrixf Asub;
    Asub.width    = block_size;
    Asub.height   = block_size;
    Asub.stride   = A.stride;
    Asub.elements = &A.elements[A.stride * block_size * row
                                         + block_size * col];
    return Asub;
}


__global__ void create_accum(Matrix *accum, Matrix *r_table, Matrixf *gradient_image)
{
  int idx = threadIdx.x + blockDim.x * blockIdx.x;;//height of image
  int idy = threadIdx.y + blockDim.y * blockIdx.y;//width of image
  int idz = threadIdx.z + blockDim.z * blockIdx.z;;//width of r_table
  //float phi =0;
  //if(idx<gradient_image->height && idy<gradient_image->width){
  float  phi = gradient_image->elements[idx * gradient_image->width + idy];
  //}
  int slice =0;
  float pi = 3.14159265359;
  if(phi > 0.001||phi< -0.001){
        slice = __float2int_rd(8*(phi+pi)/(2*pi));//rotate here?
        if(r_table->elements[(slice*r_table->width + idz)*2] != 0 && r_table->elements[(slice*r_table->width + idz)*2+1] != 0){

            int ix =  idx+r_table->elements[(slice*r_table->width + idz)*2];
            int iy =  idy+r_table->elements[(slice*r_table->width + idz)*2 + 1];
            if ( ix >= 0 && ix < accum->width && iy >= 0 && iy < accum->height){
               atomicAdd(&accum->elements[(ix*accum->width + iy)],1);
               //__syncthreads();
         }
        }
    }
}
""")


class hough_transform(object):
    """
    Perform a gradient weighted General Hough Transform on an image given a template and a set of rotation angles
    """
    def __init__(self,):
        self.weighted = True
        self.r_table = []
        self.gradient_image = []
        self.create_accum = mod.get_function("create_accum")

    
    def set_template(self, templ):
        #templ = cv2.cvtColor(templ, cv2.COLOR_RGBA2GRAY)
        templ = self.scale(templ.astype("uint8"), 0.5, 0.5)
        #cv2.imwrite(r"C:\Users\biophys\Desktop\Masterarbeit\src\abb\Hough_complete_templ.jpg",templ)

        canny = self.create_template(templ)
        #cv2.imwrite(r"C:\Users\biophys\Desktop\Masterarbeit\src\abb\Hough_complete_canny.jpg",canny)

        gradient = self.create_gradient(canny)
        #cv2.imwrite(r"C:\Users\biophys\Desktop\Masterarbeit\src\abb\Hough_complete_gradient.jpg",gradient.astype("uint8"))

        cv2.imshow("temp", gradient.astype("uint8"))
        self.r_table_zero = self.create_R_table(gradient, canny)
        #self.r_table = self.rot_R_table(np.pi*1/18)
    
    def create_template(self, image):
        im = cv2.blur(image, (4,4))
        canny = cv2.Canny(im, 130,200)
        cv2.imshow("ctemp", canny.astype("uint8"))
        return canny

    def rot_R_table(self, angle):
        s = np.sin(angle)
        c = np.cos(angle)
        new_table = []
        phitable = []
        [phitable.append([]) for i in range(8)]
        [new_table.append([]) for i in range(8)]
        for i, islice in enumerate(self.phi_table):
            for j, phi in enumerate(islice):
                vec = self.r_table_zero[i, j]
                phi_new = phi + angle
                slice = self.is_slice(phi_new)
                rotated = (int(round(c*vec[0]-s*vec[1])),int(round(s*vec[0]+c*vec[1])))
                new_table[slice].append(rotated)
                phitable[slice].append(phi_new)
        return self.table_to_matrix(new_table)

    def table_to_matrix(self, table):
        maximum = 0
        for i in table:
            if len(i) > maximum:
                maximum = len(i)
        R_Matrix = np.zeros([8,maximum,2])
        for i,j in enumerate(table):
            for h,k in enumerate(j):
                R_Matrix[i][h] = k
        return R_Matrix


    def create_R_table(self, gradient, canny):
        origin = np.asarray((gradient.shape[0]/2, gradient.shape[1]/2))
        Rtable = []
        phitable = []
        [phitable.append([]) for i in range(8)]
        [Rtable.append([]) for i in range(8)]
        for i in range(gradient.shape[0]):
            for j in range(gradient.shape[1]):
                if canny[i,j] == 255:
                    phi = gradient[i,j]
                    slice = self.is_slice(phi)
                    phitable[slice].append(phi)
                    Rtable[slice].append(np.array((origin[0] - i, origin[1] - j)))
        self.phi_table = phitable
        return self.table_to_matrix(Rtable)



    def is_slice(self, phi):
        #round down wanted
        return int(8*(divmod(phi+np.pi,2*np.pi)[1]/(2*np.pi)))

    def scale(self,image, d_x, d_y):
        return cv2.resize(image, (0,0), fx=d_x, fy=d_y, interpolation=cv2.INTER_CUBIC)

    def create_gradient(self, image):
        X = cv2.Sobel(image,cv2.CV_64F,1,0,ksize=5)
        Y = cv2.Sobel(image,cv2.CV_64F,0,1,ksize=5)
        gradient = np.zeros(image.shape)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                gradient[i][j] = np.arctan2(X[i,j],Y[i,j])
        return gradient
    
    def set_image(self, image):
        #image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
        image = self.scale(image.astype("uint8"), 0.5, 0.5)
        im = cv2.blur(image, (5,5))
        #cv2.imwrite(r"C:\Users\biophys\Desktop\Masterarbeit\src\abb\Hough_complete_image.jpg",image)

        self.image_canny = cv2.Canny(im, 130,180)
        #cv2.imwrite(r"C:\Users\biophys\Desktop\Masterarbeit\src\abb\Hough_complete_imcanny.jpg",self.image_canny)

        cv2.imshow("canny", self.image_canny.astype("uint8"))
        #cv2.imwrite(r"C:\Users\biophys\Desktop\Masterarbeit\src\abb\SIM_edge_canny.jpg",im.astype("uint8"))
        self.gradient_image = self.create_gradient(self.image_canny)
        #cv2.imwrite(r"C:\Users\biophys\Desktop\Masterarbeit\src\abb\Hough_complete_imgrad.jpg",self.gradient_image.astype("uint8"))

        cv2.imshow("grad", self.gradient_image.astype("uint8"))
        #cv2.waitKey(0)

    def get_weighted_maximas(self, accum, ratio=0.8):
        #done: speed up to slow
        #accum = cv2.blur(accum, (2,2))
        maxindex = np.unravel_index(accum.argmax(), accum.shape)
        #candidates = []
        result = []
        candidates = np.argwhere(accum >= (accum[maxindex]*ratio))

        #for i in range(accum.shape[0]):
        #    for j in range(accum.shape[1]):
        #        if accum[i,j]>(accum[maxindex]*ratio):
        #            candidates.append(np.array((i,j, accum[i,j])))
        accum_max = accum[candidates[...,0],candidates[...,1]]
        for i, candidate in enumerate(candidates):
            ind1 = max(candidate[0]-50,0),min(candidate[0]+50,self.image_canny.shape[0])
            ind2 = max(candidate[1]-50,0),min(candidate[1]+50,self.image_canny.shape[1])
            #maxl = accum[candidate[0],candidate[1]]+accum[candidate[0]+1,candidate[1]]+accum[candidate[0]-1,candidate[1]]+accum[candidate[0],candidate[1]+1]+accum[candidate[0],candidate[1]-1]
            subarray = self.image_canny[ind1[0]:ind1[1],ind2[0]:ind2[1]]
            weight = (subarray == 255).sum()
            result.append(np.array((candidate[0], candidate[1], accum_max[i], weight, 10000*accum_max[i]/weight+6*accum_max[i])))
        result = np.asarray(result).astype(np.int32)
        return result

    def transform(self):
        accum = np.zeros_like(self.gradient_image)

        #allocate memmory for matrices
        grad_ptr = drv.mem_alloc(Matrix.mem_size)

        #htod matrices data keep variables to prohibit python garbage cleaning
        #R = Matrix(self.r_table.astype(np.int32), r_table_ptr)# fucking python garbage collector srsly
        #A = Matrix(accum.astype(np.int32), accum_ptr)
        G = Matrix(self.gradient_image.astype(np.float32), grad_ptr)
        dev = drv.Device(0)
        attr = dev.get_attributes()

        max_threads = pycuda.tools.DeviceData(dev=None).max_threads
        print(max_threads)
        print(drv.device_attribute.MAX_BLOCK_DIM_X)
        n = max_threads/1024
        if n < 1:
            raise(EnvironmentError("Upgrade GPU"))
        block_size = (32,32,int(n))

        res = 0,np.zeros(5)
         # int(self.r_table.shape[1]/block_size[2])
        #todo: size something with modulo
        #done: iterate different angles 0:16 degree
        for i in range(10):
            #done: additive rundungsfehler lösung: rotate r_zero
            angle = i
            self.r_table = self.rot_R_table(np.pi*(angle)/180)
            accum_ptr = drv.mem_alloc(Matrix.mem_size)

            r_table_ptr = drv.mem_alloc(Matrix.mem_size)

            #print(self.r_table.shape[1])
            #t2 = time.time()

            A = Matrix(accum.astype(np.int32), accum_ptr)
            R = Matrix(self.r_table.astype(np.int32), r_table_ptr)
            #print("rotating:", time.time()-t2)

            grid = int(self.gradient_image.shape[0]/block_size[0])+0,int(self.gradient_image.shape[1]/block_size[1])+0,int(self.r_table.shape[1])
            self.create_accum(accum_ptr, r_table_ptr, grad_ptr,  block=block_size, grid=grid)
            t1 = time.time()
            acc = A.get()
            print("one run needs:", time.time()-t1)
            #cv2.imwrite(r"C:\Users\biophys\Desktop\Masterarbeit\src\abb\Hough_complete_accum.jpg",acc.astype("uint8"))
            if self.weighted:
                weighted_acc = self.get_weighted_maximas(acc, ratio=0.8)
            else:
                #todo: fix
                weighted_acc = acc
            x=np.unravel_index(weighted_acc[...,4].argmax(),weighted_acc.shape[0])
            if weighted_acc[x,4]>res[1][4]:
                res = (angle,weighted_acc[x])
            print("Rotation:"+ str(angle) +"° \n maximal weighted find"+ str(weighted_acc[x]))
        #dtoh result from gpu
        #done: get max return rotation and index
        #drv.stop_profiler()
        print("final result:" + str(res))

        #t = G.get()
        return res

class Matrix():
    """
    Wrapper class for Matrix and Matrixf struct on GPU:
    """
    mem_size = 16 + np.intp(0).nbytes
    def __init__(self, array, struct_ptr):
        self.data = drv.to_device(array)
        self.shape, self.dtype = array.shape, array.dtype
        self.width = array.shape[1]
        self.height = array.shape[0]
        self.stride = np.int32(0).nbytes
        drv.memcpy_htod(int(struct_ptr), np.int32(self.width))
        drv.memcpy_htod(int(struct_ptr)+4, np.int32(self.height))
        drv.memcpy_htod(int(struct_ptr)+8, np.int32(self.stride))
        drv.memcpy_htod(int(struct_ptr)+16, np.intp(int(self.data)))
    def get(self):
        #drv.memcpy_dtoh(array, self.data)
        return drv.from_device(self.data, self.shape, self.dtype)

def error_handling():
    t_list = []
    imgs_t = []
    points1 = []
    points2 = []


    grid=[]
    num = []
    for i,ent1 in enumerate(t_list):
        row1 = int(i/2)
        col1 = i%2
        max=0
        print(i)
        for j,ent2 in enumerate(t_list):
            row = int(j/2)
            col = j%2
            val1 = ent1[1][0]-(col1-col)*100
            val2 = ent1[1][1]-(row1-row)*100
            if np.absolute(val1-ent2[1][0])<50 and np.absolute(val2-ent2[1][1])<50:
                print(True)
                max+=1
            else:
                print(False)
        if max>4:
            num.append(i)
            grid.append(ent1)
