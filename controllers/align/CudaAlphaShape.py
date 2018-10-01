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
Derive 2D alpha complex from scipy.spatial Delaunay
=================================================================================

:Author:
  `Sebastian Reinhard`

:Organization:
  Biophysics and Biotechnology, Julius-Maximillians-University of Würzburg

:Version: 2018.03.09

"""
import time
import pycuda
import pycuda.autoinit
import pycuda.driver as drv
import numpy as np
from pycuda.compiler import SourceModule
from scipy.spatial import Delaunay
#GPU code to construct d = 1 simplices from delaunay triangulation
mod = SourceModule("""
typedef struct{
    int* indices;
    float* points;
    int* neighbor;
    float* k_simplices;
} alpha_complex;

__device__ float calc_sigma(int* indices, float* points)
//circle radius of triangle
{
    float d[3];
    float s = 0;
    for (int i = 0; i<3; i++){
        float p1 = points[indices[i]*2] - points[indices[(i+1)%3]*2];
        float p2 = points[indices[i]*2+1]-points[indices[(i+1)%3]*2+1];
        d[i] = sqrtf(p1*p1+p2*p2);
        s += d[i];}
    s = s/2;
    float area = sqrtf(s*(s-d[0])*(s-d[1])*(s-d[2]));
    float circle_r = d[0]*d[1]*d[2]/(4.0*area);
    return circle_r;
}

__global__ void create_simplices(alpha_complex* complex){
    int idx = threadIdx.x + blockDim.x * blockIdx.x;
    int indices[3];
    int indices2[3];
    float *points = complex->points;
    float *k_sim = complex->k_simplices;

        for (int i = 0; i<3; i++){
            indices[i] = complex->indices[idx*3+i];
        }
        for (int i = 0; i<3; i++){

            k_sim[idx*15 + i*5 + 0] = (float)complex->indices[idx*3+i];
            k_sim[idx*15 + i*5 + 1] = (float)complex->indices[idx*3+(i+1)%3];
            float p1 = points[indices[i]*2] - points[indices[(i+1)%3]*2];
            float p2 = points[indices[i]*2+1] - points[indices[(i+1)%3]*2+1];
            float sigma = sqrtf(p1*p1+p2*p2);
            k_sim[idx*15 + i*5 +2] = sigma;
            if(complex->neighbor[idx*3+(i+2)%3] == -1)
            //only calc one radius if no neighbor
            {
                float dist1 = calc_sigma(indices, points);
                k_sim[idx*15 + i*5 + 3] = fminf(dist1,sigma);
                k_sim[idx*15 + i*5 + 4] = 99999.0;
            }
            else
            //calc radius of nearest neighbor triangles and line distance
            {
                //todo: set neighbor to -1 to avoid double processing
                for(int j = 0;j<3;j++){
                    indices2[j] = complex->indices[complex->neighbor[idx*3+(i+2)%3]*3+j];
                    //weird indexing from scipy delaunay
                }
                float dist1 = calc_sigma(indices, points);
                float dist2 = calc_sigma(indices2, points);
                k_sim[idx*15 +  i*5 + 3] = fminf(sigma,fminf(dist1, dist2));
                k_sim[idx*15 +  i*5 + 4] = fmaxf(dist1, dist2);
            }
    }

}
""")
class alpha_complex():
    """
    Class to create a alpha complex structure on GPU.
    :param struct_ptr: pointer to allocated memmory for structure
    :param numpy.array indices: nx3 array containing point indices of the delaunay triangulation simplices
    :param numpy.array neighbors: nx3 array containing the indices of neighboring simplices
    :param numpy.array points: nx2 array of the points used for delaunay triangulation
    """
    #size of pointers in struct = memmory size needed
    memsize = 4* np.intp(0).nbytes
    def __init__(self, struct_ptr, indices,points, neighbors ):
        #pointer to allocated memmory
        self.struct_ptr = int(struct_ptr)
        #indices per simplex
        self.indices = indices.astype(np.int32)
        #empty array for k_simplices
        self.k_simplices = np.zeros((neighbors.shape[0]*3,5)).astype(np.float32)
        #neighboring simplices
        self.neighbors = neighbors.astype(np.int32)
        #list of triangulation points
        self.points = points.astype(np.float32)
        #self.shape = indices.shape
        #copy arrays to device get pointers for struct
        self.indices_ptr = drv.to_device(self.indices)
        self.points_ptr = drv.to_device(self.points)
        self.neighbor_ptr = drv.to_device(self.neighbors)
        self.k_simplices_ptr = drv.to_device(self.k_simplices)

        #create struct from pointers
        drv.memcpy_htod(self.struct_ptr, np.intp(int(self.indices_ptr)))
        #sizeof(pointer) offset per element
        drv.memcpy_htod(self.struct_ptr+np.intp(0).nbytes, np.intp(int(self.points_ptr)))
        drv.memcpy_htod(self.struct_ptr+np.intp(0).nbytes*2, np.intp(int(self.neighbor_ptr)))
        drv.memcpy_htod(self.struct_ptr+np.intp(0).nbytes*3, np.intp(int(self.k_simplices_ptr)))




    def get(self):
        """
        :return numpy.array nx5 of d=1 simplices
        containing: [index1, index2, dist, sigma1, sigma2] with sigma 1 < sigma 2
        """
        self.result = drv.from_device(self.k_simplices_ptr, self.k_simplices.shape, np.float32)
        return self.result

    def merge(self):
        indices = self.result[...,0:2].astype(np.int32)
        indices_sorted = np.sort(indices,axis=1)
        a,index = np.unique(indices_sorted,return_index=True, axis=0)
        merged = self.result[index]
        return merged


class simplex():
    """
     deprecated: Simplex struct for GPU
    """
    memsize = 16 + np.intp(0).nbytes
    def __init__(self, struct_ptr, indices, n):
        self.sub = []
        self.super = []
        self.struct_ptr = int(struct_ptr)+n*simplex.memsize
        self.indices = indices
        self.shape = indices.shape
        self.indices_ptr = drv.to_device(indices)
        self.sigma =0
        self.exterior = False
        self.interior = False
        self.surface = False
        self.line = False
        drv.memcpy_htod(self.struct_ptr, np.float32(self.sigma))
        #drv.memcpy_htod(int(struct_ptr)+4, np.int32(0))
        #drv.memcpy_htod(int(struct_ptr)+8, np.int32(self.stride))
        drv.memcpy_htod(self.struct_ptr + 16, np.intp(int(self.indices_ptr)))

    def set_alpha(self, alpha):
        if alpha < self.c:
            self.exterior = True
        elif alpha < self.b:
            self.line = True
        elif alpha < self.a:
            self.surface = True
        else:
            self.interior = True

    def get(self):
        sigma = np.empty((3))
        sigma = drv.from_device(self.struct_ptr, 1, np.float32)
        return sigma


def get_k_simplices(points):
    """
    :param numpy.array points: nx2 array of points to use for alpha complex
    :returns numpy.array alpha complex: mx5 array of d=1 simplices
    """
    t1 = time.time()
    tri = Delaunay(points)
    _tdel = time.time()-t1
    print("Delaunay " + str(points.shape[0]) + " points in " + str(_tdel) + " seconds")
    t1 = time.time()
    simplices = tri.simplices.copy()
    neighbors = tri.neighbors.copy()

    alpha_complex_ptr = drv.mem_alloc(alpha_complex.memsize)

    alpha_comp = alpha_complex(alpha_complex_ptr,simplices,points, neighbors)

    func = mod.get_function("create_simplices")
    func(alpha_complex_ptr, block=(500,1,1), grid=(int(simplices.shape[0]/500),1,1))
    alpha_comp.get()#todo: merge duplicated simplices
    _talph = time.time()-t1
    print("created alpha complex of " + str(points.shape[0]) + " points in " + str(_talph) + " seconds")
    res = alpha_comp.merge()
    _tmerg = time.time()-t1
    print("merging needs: " + str(_tmerg) + " seconds")
    return res ,_talph, _tdel, _tmerg

if __name__ == "__main__":
    points = (np.random.randn(1000000, 2)*100).astype(np.float32)
    tri = Delaunay(points)
    simplices = tri.simplices.copy()
    neighbors = tri.neighbors.copy()

    #points = tri.points.copy()

    alpha_complex_ptr = drv.mem_alloc(alpha_complex.memsize)

    alpha_comp = alpha_complex(alpha_complex_ptr, simplices, points, neighbors)

    func = mod.get_function("create_simplices")
    func(alpha_complex_ptr, block=(500,1,1), grid=(int(simplices.shape[0]/500),1,1))
    a = alpha_comp.get()
    drv.stop_profiler()

