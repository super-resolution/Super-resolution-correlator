# -*- coding: utf-8 -*-
"""
Created on: 2015.01.11.

Author: turbo


"""
import numpy as numpy, datetime
import scipy
from sklearn.cluster import DBSCAN
from scipy import spatial
#from numpy import *
import numpy as np

from .util import RunnableComponent


class Filter(RunnableComponent):
    def __init__(self, *args, **kwargs):
        super(Filter, self).__init__(*args, **kwargs)

    def run(self, points):
        return points


#deletes localizations that are outside the given z range
class ZFilter(Filter):
    def __init__(self, *args, **kwargs):
        super(ZFilter, self).__init__(*args, **kwargs)

    def run(self, points):
        print("ZFilter")
        #out=[]
        pointsf1 = points[points[...,3]<=self.storm_filter_z_to]
        pointsf2 = pointsf1[pointsf1[...,3]>=self.storm_filter_z_from]
        out = numpy.array([pointsf2])
        # for k in range(len(points)):
        #
        #     indsplus=numpy.where(numpy.asarray(points[k])[:,3]>self.storm_filter_z_to)
        #     indsminus=numpy.where(numpy.asarray(points[k])[:,3]<self.storm_filter_z_from)
        #     inds2=numpy.union1d(indsplus[0],indsminus[0])
        #
        #     if list(numpy.delete(numpy.asarray(points[k]),inds2,0))==[]:
        #         out.append(numpy.asarray([]))
        #     else:
        #         out.append(list(numpy.delete(numpy.asarray(points[k]),inds2,0)))

        return out

class PhotonFilter(Filter):
    def __init__(self, *args, **kwargs):
        super(PhotonFilter, self).__init__(*args, **kwargs)

    def run(self, points):
        print('PhotonFilter')
        out = []
        #t0 =datetime.datetime.now()
        print()
        pointsf1 = points[points[...,4]>=self.storm_filter_photon_from]
        pointsf2 = pointsf1[pointsf1[...,4]<=self.storm_filter_photon_to]
        out = numpy.array([pointsf2])
        #print datetime.datetime.now() -t0
        #print len(out2)
        #t0 =datetime.datetime.now()
        #for k in range(len(points)):
            #indsplus=numpy.where(numpy.asarray(points[k])[:,4]>self.storm_filter_photon_to)

            #indsminus=numpy.where(numpy.asarray(points[k])[:,4]<self.storm_filter_photon_from)
            #inds2=numpy.union1d(indsplus[0],indsminus[0])
            #if list(numpy.delete(numpy.asarray(points[k]),inds2,0))==[]:
                #out.append(numpy.asarray([]))
            #else:
                #out.append(list(numpy.delete(numpy.asarray(points[k]),inds2,0)))
        #print datetime.datetime.now() -t0
        return out

class FrameFilter(Filter):
    def __init__(self, *args, **kwargs):
        super(FrameFilter, self).__init__(*args, **kwargs)

    def run(self, points):
        print('FrameFilter')
        pointsf1 = points[points[...,6]>self.storm_filter_frame_from]
        pointsf2 = pointsf1[pointsf1[...,4]<=self.storm_filter_photon_to]
        out= numpy.array(pointsf2)
        # outpoints=[]
        # for k in range(len(points)):
        #     indsplus=numpy.where(numpy.asarray(points[k])[:,6]>self.storm_filter_frame_to)
        #
        #     indsminus=numpy.where(numpy.asarray(points[k])[:,6]<self.storm_filter_frame_from)
        #     inds2=numpy.union1d(indsplus[0],indsminus[0])
        #     if list(numpy.delete(numpy.asarray(points[k]),inds2,0))==[]:
        #         outpoints.append(numpy.asarray([]))
        #     else:
        #         outpoints.append(list(numpy.delete(numpy.asarray(points[k]),inds2,0)))

        return out

class LocalDensityFilter(Filter):
    def __init__(self, *args, **kwargs):
        super(LocalDensityFilter, self).__init__(*args, **kwargs)

    def run(self, points):
            print("LdFilter")
            outpoints = []
            for k in range(len(points)):
                rsd=np.empty((len(points[k]), 3), dtype=np.int)
                rsd[:,0]=np.asarray(points[k])[:,0]
                rsd[:,1]=np.asarray(points[k])[:,1]
                rsd[:,2]=np.asarray(points[k])[:,3]
                filt=[]
                tree=scipy.spatial.cKDTree(rsd)
                x= tree.query_ball_point(rsd, self.storm_filter_localdensity_maxradius, n_jobs=-1)
                for i,j in enumerate(x):
                    if len(j)<=self.storm_filter_localdensity_min_num:
                        filt.append(i)
                #if list(np.delete(np.asarray(points),filt,0))==[]:
                    #outpoints.append(np.asarray([]))
                #else:
                outpoints.append(np.delete(np.asarray(points[k]),filt,0))
            outpoints = np.asarray(outpoints)
            return outpoints

def customShit(points, position):
        #position = numpy.array([10000,10000, 0])
        tree = scipy.spatial.cKDTree(points)
        indices = tree.query_ball_point(position,100000.0, n_jobs=-1)
        data = points[indices]
        indices = numpy.asarray(indices)
        print("Number of points: " + str(len(data)))
        t1 = datetime.datetime.now()
        data = DBSCAN(eps=100.0, min_samples=10,).fit(data)
        print(data.get_params())
        #print data.components_
        t2 = datetime.datetime.now()
        print("Time: " + str(t2-t1))
        labels = data.labels_
        x = [indices[data.labels_ == i] for i in range(len(set(labels)) - (1 if -1 in labels else 0))]
        y = []
        z = []
        for i, points in enumerate(x):

            for j in points:
                y.append(j)
                z.append(i)
        return y,z


class InternalizationFilter(Filter):
     def __init__(self, *args, **kwargs):
         super(InternalizationFilter, self).__init__(*args, **kwargs)

