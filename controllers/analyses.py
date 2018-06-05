# -*- coding: utf-8 -*-
"""
Created on: 2015.01.11.

Author: turbo


"""
import os
from .util import RunnableComponent
import numpy
import string
import scipy
from scipy import stats
from scipy import spatial
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from matplotlib import colors
import math
import copy
from scipy.optimize import minimize
import random
from scipy import ndimage
from pyqtgraph.Qt import QtCore, QtGui



class Analysis(RunnableComponent):
    def __init__(self, *args, **kwargs):
        super(Analysis, self).__init__(*args, **kwargs)

        self.storm_channel_list=[]  # names of all STORM channels
        self.storm_channels_visible = [False, False, False, False] # True if the nth STORM channel is checked in GUI
        self.storm_channels_colors = [(), (), (), ()]  # colors selected for displaying STORM channels
        self.visible_storm_channel_names = [] # names of visible STORM channels

        self.confocal_channel_list=['0','1','2','3'] # numbers of confocal channels
        self.confocal_channels_visible = [False, False, False, False] # True if the nth conf. channel is checked in GUI
        self.confocal_channels_colors = [(), (), (), ()] # colors selected for displaying confocal channels
        self.visible_confocal_channel_names = [] # names of visible STORM channels
        self.z_position=0 # number of the image from confocal check selected for visualization
        self.confocal_image=None # original confocal image stack
        self.ConfocalMetaData = {} # metadata of original confocal image
        self.confocal_offset=[0,0] # confocal offset: y,x
        self.confocal_file_name=''

        self.DisplayPlotCheckBox=[] # display plot checkbox in analysis GUI
        self.storm_file_name = '' # displayed STORM filename
        self.ROI = None # ROI instance
        self.ROI_tag = None # name of ROI
        self.roi_perimeter = None # perimeter of ROI
        self.roi_area = None # area of ROI
        self.storm_file_path='' # file path of displayed STORM file
        self.working_directory='' # path of selected working directory
        self.display_plots=None # true if display plots checkbox in analysis GUI is selected

        """Pre-requirements for the analysis to be able to run it"""
        self.requirements_channels_num_min = 0 # minimum STORM channel number to be able to run the analysis
        self.requirements_dimensions_num_list_any = ['2d', '3d'] # minimal dimension of STORM data

        """Stuff for simple values"""
        self.computed_values_simple = [] # components of the simple results file

        """Stuff for complex computed values"""
        self.output_file_extension = 'txt'
        self.output_file = ''
        self.computed_values_multiple = '' # components of the complex results files of each analysis

        """Stuff for other exported values"""
        self.output_file_export_extension = ''
        self.computed_values_export = None
        self.output_file_export = ''



    def setup_data(self, storm_channel_list, storm_channels_visible, storm_channels_colors,
                   confocal_channels_visible, confocal_channels_colors,
                   z_position, confocal_image, confocal_meta_data,
                   ROI, ROI_tag, roi_perimeter, roi_area, confocal_offset, display_plots, euc_conf, StormDisplay):
        self.storm_channel_list=storm_channel_list
        self.storm_channels_visible = storm_channels_visible
        self.storm_channels_colors = storm_channels_colors
        self.confocal_channels_visible=confocal_channels_visible
        self.confocal_channels_colors=confocal_channels_colors
        self.z_position=z_position
        self.confocal_image=confocal_image
        self.ConfocalMetaData = confocal_meta_data
        self.ROI = ROI
        self.ROI_tag = ROI_tag
        self.roi_perimeter = roi_perimeter
        self.roi_area = roi_area
        self.confocal_offset=confocal_offset
        self.StormDisplay=StormDisplay
        self.visible_storm_channel_names = \
            [ch for i, ch in enumerate(storm_channel_list) if storm_channels_visible[i]]
        for combo_box in self.combo_boxes:
            while combo_box.count() > 0:
                combo_box.removeItem(0)
            combo_box.addItems(self.visible_storm_channel_names)
        self.DisplayPlotCheckBox=display_plots
        self.analysis_euclidean_between_confocal=euc_conf

    def setup_filenames(self, working_directory, storm_file_path, confocal_file_path):
        self.storm_file_name = os.path.basename(storm_file_path).split('.')[0]

        if confocal_file_path!=None:
            self.confocal_file_name=os.path.basename(confocal_file_path.file_path)



        self.storm_file_path=storm_file_path
        self.working_directory=working_directory
        self.output_file = os.path.join(
            working_directory,
            self.storm_file_name + '_' + self.ROI_tag + '_' + type(self).__name__ + '.' + self.output_file_extension
        )
        self.output_file_export = os.path.join(
            working_directory,
            self.storm_file_name + '_' + self.ROI_tag + '_' + type(self).__name__ + '.'
            + self.output_file_export_extension
        )

    def compute(self, points):
        pass

    def _write_results_to_file(self, save_all_data, export_data):
        # write to the own file of the given analyse, complex values
        if save_all_data:
            f = open(self.output_file, 'w')
            f.write(str(self.computed_values_multiple) + '\n')
            f.close()

        if export_data:
            # Save the exported data file
            f = open(self.output_file_export, 'w')
            for line in self.computed_values_export:
                f.write(line + '\n')
            f.close()


    def run(self, points, channels_num, dimensions):
        self.display_plots=self.DisplayPlotCheckBox.isChecked()
        if channels_num >= self.requirements_channels_num_min and dimensions in self.requirements_dimensions_num_list_any:
            self.computed_values_simple = []
            self.compute(points)

            save_all_data = False
            export_data = False
            if self.computed_values_multiple is not None:
                save_all_data = getattr(self, self.name_prefix + '_save_all')
            if self.computed_values_export is not None:
                export_data = getattr(self, self.name_prefix + '_export_' + self.output_file_export_extension)
            self._write_results_to_file(save_all_data, export_data)

            return self.computed_values_simple
        else:
            print(str(type(self).__name__) + ' analysis requirements are not met!')
            return None

# commonly used functions

    def EucDistance2D(self, point1, point2):
        # simple Euclidean distance calculation in 2D
        dist = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        return dist

    def EucDistance3D(self, point1, point2):
        # simple Euclidean distance calculation in 3D
        dist = numpy.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)
        return dist

    def tetrahedron_volume(self, a, b, c, d):
        # calculate the volume of the tetrahedron
        return numpy.abs(numpy.einsum('ij,ij->i', a - d, numpy.cross(b - d, c - d))) / 6

    def TriangleArea2D(self, point1, point2, point3):
        # calculates area of the triangle of 2D points
        a = self.EucDistance2D(point1, point2)
        b = self.EucDistance2D(point2, point3)
        c = self.EucDistance2D(point3, point1)
        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return area

    def TriangleArea3D(self, point1, point2, point3):
        # calculates area of the triangle of 3D points
        a = self.EucDistance3D(point1, point2)
        b = self.EucDistance3D(point2, point3)
        c = self.EucDistance3D(point3, point1)
        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return area

    def ClosestHullSurfPoint_2(self, hull, point):
        # Translate all points with vector 'point'
        trans_points = numpy.copy(hull.points)
        for k in range(len(trans_points)):
            trans_points[k][0] = trans_points[k][0] - point[0]
            trans_points[k][1] = trans_points[k][1] - point[1]
            trans_points[k][2] = trans_points[k][2] - point[2]

            # CALCULATING THE CLOSEST HULL DISTANCES, AND HULL SURFACE POINT
        distance = 100000000
        for triang in hull.simplices:  # Calculate the distance from all the hull triangles hull_points contains
        # the hull points
            constraint = 0  # 0 :If constrains satisfied 1: if constr not satisfied
            cround = 1
            x0 = [0.3, 0.3, 0.4]
            while constraint == 0:
                P1 = trans_points[triang[0]]
                P2 = trans_points[triang[1]]
                P3 = trans_points[triang[2]]

                def func(x):
                    """ Objective function """
                    return ((x[0] * P1[0] + x[1] * P2[0] + x[2] * P3[0]) ** 2 + (
                        x[0] * P1[1] + x[1] * P2[1] + x[2] * P3[1]) ** 2 + (
                                x[0] * P1[2] + x[1] * P2[2] + x[2] * P3[2]) ** 2 )

                cons = ({'type': 'eq', 'fun': lambda x: numpy.array([x[0] + x[1] + x[2] - 1])},
                        {'type': 'ineq', 'fun': lambda x: numpy.array([x[0]])},
                        {'type': 'ineq', 'fun': lambda x: numpy.array([x[1]])},
                        {'type': 'ineq', 'fun': lambda x: numpy.array([x[2]])})

                res = scipy.optimize.minimize(func, x0, constraints=cons, method='SLSQP', options={'disp': False})
                qtmp = res.x  # The optimized parameter values
                constraint = 1
                if qtmp[0] > 1.001 or qtmp[0] < -0.001 or qtmp[1] > 1.001 or qtmp[1] < -0.001 or qtmp[2] > 1.001 or \
                                qtmp[2] < -0.001:
                    constraint = 0
                    # Make a starting guess
                    x0a = random.randint(0, 90)
                    x0b = random.randint(0, 95 - x0a)
                    x0c = 100 - x0a - x0b
                    x0 = [float(x0a) / 100, float(x0b) / 100, float(x0c) / 100]

                # Select the smallest triangle distance
                Q = [0, 0, 0]
                Q[0] = qtmp[0] * P1[0] + qtmp[1] * P2[0] + qtmp[2] * P3[
                    0]  # The coordinates of the closest point on the hull (Q)
                Q[1] = qtmp[0] * P1[1] + qtmp[1] * P2[1] + qtmp[2] * P3[1]
                Q[2] = qtmp[0] * P1[2] + qtmp[1] * P2[2] + qtmp[2] * P3[2]
                distmp = math.sqrt(Q[0] ** 2 + Q[1] ** 2 + Q[2] ** 2)
                if distmp < distance and constraint == 1:
                    distance = distmp
                    qpoint_tr = Q
                    tri = triang
                cround = cround + 1
        qpoint = [qpoint_tr[0] + point[0], qpoint_tr[1] + point[1],
                  qpoint_tr[2] + point[2]]  # Closest point on the surface in the original coordinates
        return ([qpoint, distance, tri])

        # points_f are the points interested and pts_4_hull points forming the hull

    def Loc_Distances_from_Hull_Surface_2(self, points_f, pts_4_hull):
        hull = ConvexHull(pts_4_hull)
        close_points = []
        i = 0
        for pt in points_f[:]:
            # print i, '/', len(points_f)
            i = i + 1
            [cl_point, dist_fs, triang] = self.ClosestHullSurfPoint_2(hull, pt)
            close_points.append(list(pt) + cl_point + [dist_fs] + list(triang))
        return (close_points)



    # Returns the sheet third point but in the translated coordinates with centr_cord
    def rot_sheet_calc(self, a, b):
        # Calculate the rotating sheets
        # Center of point a and b
        centr_cord = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2]
        a = [a[0] - centr_cord[0], a[1] - centr_cord[1], a[2] - centr_cord[2]]
        b = [b[0] - centr_cord[0], b[1] - centr_cord[1], b[2] - centr_cord[2]]
        # Random point on the sheet perpendicular to a-b quadrant
        q = [-40, -20, 0]
        q[2] = -1 * (
            ( (a[0] - b[0]) * q[0] + (a[1] - b[1]) * q[1]) / (
                a[2] - b[2] + 0.001)  )  # +0.001 to avoid division by zero
        l_ab = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
        v1 = [(a[0] - b[0]) / l_ab, (a[1] - b[1]) / l_ab, (a[2] - b[2]) / l_ab]
        l_q = math.sqrt(q[0] ** 2 + q[1] ** 2 + q[2] ** 2)
        v2 = [q[0] / l_q, q[1] / l_q, q[2] / l_q]
        # Cross product of v1 and v2 = v3
        v3 = [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]
        # The third point of triangle in sheet S perpendicular to a-b
        v4 = [(v2[0] + v3[0]) / -2, (v2[1] + v3[1]) / -2, (v2[2] + v3[2]) / -2]
        numb_of_sheets = 20  # must be even number!
        # sheet_points = [0 0 0;v1;v2;v3;v4;a;b;q]
        sheet_points = []
        b1 = [v2[0] - v4[0], v2[1] - v4[1], v2[2] - v4[2]]
        b2 = [v3[0] - v2[0], v3[1] - v2[1], v3[2] - v2[2]]
        multiple = 100
        for k in range(numb_of_sheets):
            t = float(k) * (1 / float(numb_of_sheets))
            p1 = [(v4[0] + t * b1[0]) * multiple, (v4[1] + t * b1[1]) * multiple, (v4[2] + t * b1[2]) * multiple]
            sheet_points.append(p1)
        for k in range(numb_of_sheets / 2):
            t = float(k) * (1 / float(numb_of_sheets))
            p2 = [(v2[0] + t * b2[0]) * multiple, (v2[1] + t * b2[1]) * multiple, (v2[2] + t * b2[2]) * multiple]
            sheet_points.append(p2)

        return (sheet_points)

        # Shortest distance on convex hull
    def shortest_distance_on_hull_surface(self, conv_hull, poi_a, poi_b):
        # Generate the edges of the hull
        edges = []
        for i in range(len(conv_hull.simplices)):
            edges.append([conv_hull.simplices[i][0], conv_hull.simplices[i][1]])
            edges.append([conv_hull.simplices[i][1], conv_hull.simplices[i][2]])
            edges.append([conv_hull.simplices[i][2], conv_hull.simplices[i][0]])
        # Delete duplicated edges
        tmp = [edges[0]]
        for i in range(len(edges)):
            ins = 1
            for k in range(len(tmp)):
                if edges[i] == [tmp[k][0], tmp[k][1]] or edges[i] == [tmp[k][1], tmp[k][0]]:
                    ins = 0
            if ins == 1:
                tmp.append(edges[i])
        edges_sort = tmp

        a_vertex = 0
        b_vertex = 0
        a_triangles = []
        b_triangles = []
        for i in range(len(conv_hull.simplices)):
            # Points of the actual triangle h1,h2,h3
            h1 = conv_hull.points[conv_hull.simplices[i][0]]
            h2 = conv_hull.points[conv_hull.simplices[i][1]]
            h3 = conv_hull.points[conv_hull.simplices[i][2]]
            # Distance of the poi_a and poi_b from the actual Vertex of the hull
            d1_a = math.sqrt((poi_a[0] - h1[0]) ** 2 + (poi_a[1] - h1[1]) ** 2 + (poi_a[2] - h1[2]) ** 2)
            d2_a = math.sqrt((poi_a[0] - h2[0]) ** 2 + (poi_a[1] - h2[1]) ** 2 + (poi_a[2] - h2[2]) ** 2)
            d3_a = math.sqrt((poi_a[0] - h3[0]) ** 2 + (poi_a[1] - h3[1]) ** 2 + (poi_a[2] - h3[2]) ** 2)
            d1_b = math.sqrt((poi_b[0] - h1[0]) ** 2 + (poi_b[1] - h1[1]) ** 2 + (poi_b[2] - h1[2]) ** 2)
            d2_b = math.sqrt((poi_b[0] - h2[0]) ** 2 + (poi_b[1] - h2[1]) ** 2 + (poi_b[2] - h2[2]) ** 2)
            d3_b = math.sqrt((poi_b[0] - h3[0]) ** 2 + (poi_b[1] - h3[1]) ** 2 + (poi_b[2] - h3[2]) ** 2)
            if d1_a < 0.01 or d2_a < 0.01 or d3_a < 0.01:
                a_vertex = 1
                a_triangles.append(sorted(conv_hull.simplices[i]))
            # Which point is identical with poi_a on the actual triangle  ?
            if d1_a < 0.01:
                a_ver = conv_hull.simplices[i][0]
            if d2_a < 0.01:
                a_ver = conv_hull.simplices[i][1]
            if d3_a < 0.01:
                a_ver = conv_hull.simplices[i][2]
            if d1_b < 0.01 or d2_b < 0.01 or d3_b < 0.01:
                b_vertex = 1
                b_triangles.append(sorted(conv_hull.simplices[i]))
            #Which point is identical with poi_b on the actual triangle ?
            if d1_b < 0.01:
                b_ver = conv_hull.simplices[i][0]
            if d2_b < 0.01:
                b_ver = conv_hull.simplices[i][1]
            if d3_b < 0.01:
                b_ver = conv_hull.simplices[i][2]

        # Rotating sheet generation
        sheet_points = self.rot_sheet_calc(poi_a, poi_b)

        # Center point and translation of the two surface point a and b
        centr_cord = [(float(poi_a[0] + poi_b[0])) / 2, (float(poi_a[1] + poi_b[1])) / 2,
                      (float(poi_a[2] + poi_b[2])) / 2]
        poi_a = [poi_a[0] - centr_cord[0], poi_a[1] - centr_cord[1], poi_a[2] - centr_cord[2]]
        poi_b = [poi_b[0] - centr_cord[0], poi_b[1] - centr_cord[1], poi_b[2] - centr_cord[2]]

        #A Translate the points with the centrum point of poi_a - poi_b (centr_cord)
        tmp = numpy.copy(conv_hull.points)
        for i in range(len(tmp)):
            tmp[i] = [tmp[i][0] - centr_cord[0], tmp[i][1] - centr_cord[1], tmp[i][2] - centr_cord[2]]
        all_centered = tmp
        conv_hull_trans = scipy.spatial.ConvexHull(all_centered)  #Convex hull for the translated points

        #Closest hull triangle for the a and b points
        [xxxx, yyyy, closest_triangle_a] = self.ClosestHullSurfPoint_2(conv_hull_trans, poi_a)
        [xxxx, yyyz, closest_triangle_b] = self.ClosestHullSurfPoint_2(conv_hull_trans, poi_b)
        closest_triangle_a = sorted(closest_triangle_a)
        closest_triangle_b = sorted(closest_triangle_b)
        #Check the special point a and b coordinate cases.
        if a_vertex == 1 and b_vertex == 0:
            for i in range(len(a_triangles)):
                if closest_triangle_b == a_triangles[i]:
                    #print('On the same triangle poi_a vertex a1 b0')
                    closest_triangle_a = closest_triangle_b
        if a_vertex == 0 and b_vertex == 1:
            for i in range(len(b_triangles)):
                if closest_triangle_a == b_triangles[i]:
                    #print('On the same triangle poi_b vertex  a0 b1')
                    closest_triangle_a = closest_triangle_b
        if a_vertex == 1 and b_vertex == 1:
            for i in range(len(a_triangles)):
                for k in range(len(b_triangles)):
                    if a_triangles[i] == b_triangles[k]:
                        #print('Both vertex on same triangle')
                        closest_triangle_b = a_triangles[i]
                        closest_triangle_a = b_triangles[k]
        if closest_triangle_a == closest_triangle_b:
            #print('On the same triangle')
            min_root_length = math.sqrt(
                (poi_a[0] - poi_b[0]) ** 2 + (poi_a[1] - poi_b[1]) ** 2 + (poi_a[2] - poi_b[2]) ** 2)
            min_root_trans = [poi_a, poi_b]
            cb1_edges_cross = [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
        # IF the two points on different triangles
        else:
            min_root_length = 10000000
            #Rotating the S sheet
            for plane in range(len(sheet_points)):
                p = sheet_points[plane]
                #Calculation the edge crossing points
                cb1_edges_cross = []
                for i in range(len(edges_sort)):
                    w = all_centered[edges_sort[i][0]]
                    r = all_centered[edges_sort[i][1]]
                    # x=r_1+tw_1-tr_1, y=r_2+tw_2-tr_2, z=r_3+tw_3-tr_3 p_1x+p_2y+p_3z=0
                    t_param = -( p[0] * r[0] + p[1] * r[1] + p[2] * r[2] ) / (
                        p[0] * (w[0] - r[0]) + p[1] * (w[1] - r[1]) + p[2] * (w[2] - r[2]) )
                    if t_param >= 0 and t_param <= 1:
                        cross_point = [r[0] + t_param * (w[0] - r[0]), r[1] + t_param * (w[1] - r[1]),
                                       r[2] + t_param * (w[2] - r[2])]
                        cb1_edges_cross.append(list(w) + list(r) + cross_point + edges_sort[i])
                #It there is no edges with the actual S sheet continue with the next S sheet.
                if len(cb1_edges_cross) == 0:
                   # print('No edges')
                    continue
                    # Finding first edges if poi a or poi_b vertex point
                next_edge_a = []
                next_edge_b = []
                # poi_a
                if a_vertex == 1:  # Searching for non-vertex cutoff
                    for i in range(len(a_triangles)):
                        for k in range(len(cb1_edges_cross)):
                            ab = [a_triangles[i][0], a_triangles[i][1]]  # 1st edge of the actual neighbouring triangle
                            ac = [a_triangles[i][0], a_triangles[i][2]]  # 2st edge of the actual neighbouring triangle
                            bc = [a_triangles[i][1], a_triangles[i][2]]  # 3st edge of the actual neighbouring triangle
                            ee = sorted(cb1_edges_cross[k][9:])  # The k th crossing edge
                            if ab == ee:
                                if ab[0] != a_ver and ab[1] != a_ver:
                                    next_edge_a.append(ab)
                            if ac == ee:
                                if ac[0] != a_ver and ac[1] != a_ver:
                                    next_edge_a.append(ac)
                            if bc == ee:
                                if bc[0] != a_ver and bc[1] != a_ver:
                                    next_edge_a.append(bc)

                if b_vertex == 1:
                    for i in range(len(b_triangles)):
                        for k in range(len(cb1_edges_cross)):
                            ab = [b_triangles[i][0], b_triangles[i][1]]
                            ac = [b_triangles[i][0], b_triangles[i][2]]
                            bc = [b_triangles[i][1], b_triangles[i][2]]
                            ee = sorted(cb1_edges_cross[k][9:])  # The k th crossing edge
                            if ab == ee:
                                if ab[0] != b_ver and ab[1] != b_ver:
                                    next_edge_b.append(ab)

                            if ac == ee:
                                if ac[0] != b_ver and ac[1] != b_ver:
                                    next_edge_b.append(ac)

                            if bc == ee:
                                if bc[0] != b_ver and bc[1] != b_ver:
                                    next_edge_b.append(bc)
                if a_vertex != 1:
                    next_edge_a = []
                    for i in range(len(cb1_edges_cross)):
                        ab = [closest_triangle_a[0],
                              closest_triangle_a[1]]  # 1st edge of the actual neighbouring triangle
                        ac = [closest_triangle_a[0],
                              closest_triangle_a[2]]  # 2st edge of the actual neighbouring triangle
                        bc = [closest_triangle_a[1],
                              closest_triangle_a[2]]  # 3st edge of the actual neighbouring triangle

                        ee = sorted(cb1_edges_cross[i][9:])  # The k th crossing edge
                        if ab == ee or ac == ee or bc == ee:
                            next_edge_a.append(ee)

                if b_vertex != 1:
                    next_edge_b = []
                    for i in range(len(cb1_edges_cross)):
                        ab = [closest_triangle_b[0],
                              closest_triangle_b[1]]  # 1st edge of the actual neighbouring triangle
                        ac = [closest_triangle_b[0],
                              closest_triangle_b[2]]  # 2st edge of the actual neighbouring triangle
                        bc = [closest_triangle_b[1],
                              closest_triangle_b[2]]  # 3st edge of the actual neighbouring triangle

                        ee = sorted(cb1_edges_cross[i][9:])  # The k th crossing edge
                        if ab == ee or ac == ee or bc == ee:
                            next_edge_b.append(ee)

                if len(next_edge_a) < 2 or len(next_edge_b) < 2:
                    #print 'There is no neighbor edge'
                    continue

                #The two root
                for k in [0, 1]:
                    con = 1
                    ee = next_edge_a[k]

                    if a_vertex == 1:
                        for i in range(len(a_triangles)):
                            ab = [a_triangles[i][0], a_triangles[i][1]]  # 1st edge of the actual neighbouring triangle
                            ac = [a_triangles[i][0], a_triangles[i][2]]  # 2st edge of the actual neighbouring triangle
                            bc = [a_triangles[i][1], a_triangles[i][2]]  # 3st edge of the actual neighbouring triangle
                            if ab == ee or ac == ee or bc == ee:
                                closest_triangle_a = a_triangles[i]
                    et = sorted(closest_triangle_a)

                    #                     sort(next_edge_b(1,:))
                    #                     sort(next_edge_b(2,:))
                    if k == 0:
                        root_a = [ee]

                    if k == 1:
                        root_b = [ee]

                    # Finding the root all the way from poi_a to poi_b
                    exxxit = 0
                    while con == 1:
                        # If the root returned to poi_b break the while
                        if ee == sorted(next_edge_b[0]):
                            break

                        if ee == sorted(next_edge_b[1]):
                            break

                        # Stop finding root after 5000 trial
                        exxxit = exxxit + 1
                        if exxxit == 5000:
                            # print 'missed side \n'
                            root_a = [0, 0]
                            root_b = [0, 0]
                            break

                        # Finding the next triangle on the actual root
                        for i in range(len(conv_hull.simplices)):
                            ab = sorted([conv_hull.simplices[i][0], conv_hull.simplices[i][1]])
                            ac = sorted([conv_hull.simplices[i][0], conv_hull.simplices[i][2]])
                            bc = sorted([conv_hull.simplices[i][1], conv_hull.simplices[i][2]])
                            abc = sorted(conv_hull.simplices[i])
                            if ee == ab or ee == ac or ee == bc:  #ee is the actual edge
                                if abc == et:
                                    tttt = 'aasd'
                                else:
                                    et_tmp = abc

                        et = et_tmp  # the new triangle
                        del et_tmp
                        ee_tmp = []

                        # Searching for next edge
                        for i in range(len(cb1_edges_cross)):
                            ab = sorted([et[0], et[1]])
                            ac = sorted([et[0], et[2]])
                            bc = sorted([et[1], et[2]])
                            tmp = sorted(cb1_edges_cross[i][9:])

                            if ab == tmp or ac == tmp or bc == tmp:
                                if ee == tmp:
                                    tttt = 'aasd'
                                else:
                                    ee_tmp.append(sorted(cb1_edges_cross[i][9:]))

                        if len(ee_tmp) > 1:
                            # print 'bifurcation   at ' + str(i) + 'element'
                            break

                        ee = ee_tmp[0]
                        del ee_tmp

                        if k == 0:
                            root_a.append(ee)

                        if k == 1:
                            root_b.append(ee)

                        if ee == sorted(next_edge_b[0]):
                            con = 0

                        if ee == sorted(next_edge_b[1]):
                            con = 0

                if len(root_a) > 0:
                    # Calculate route length 0
                    root_a_coord = [list(numpy.copy(poi_a))]
                    for r_a in range(len(root_a)):
                        for cross_p in range(len(cb1_edges_cross)):
                            if root_a[r_a] == sorted(cb1_edges_cross[cross_p][9:]):
                                root_a_coord.append(cb1_edges_cross[cross_p][6:9])
                    root_a_coord.append(list(numpy.copy(poi_b)))

                    # Calculate route length 0
                    root_b_coord = [list(numpy.copy(poi_a))]
                    for r_b in range(len(root_b)):
                        for cross_p in range(len(cb1_edges_cross)):
                            if root_b[r_b] == sorted(cb1_edges_cross[cross_p][9:]):
                                root_b_coord.append(cb1_edges_cross[cross_p][6:9])
                    root_b_coord.append(list(numpy.copy(poi_b)))

                full_root_a_length = 0
                full_root_b_length = 0
                for i in range(len(root_a_coord) - 1):
                    distmp = math.sqrt((root_a_coord[i][0] - root_a_coord[i + 1][0]) ** 2 + (
                        root_a_coord[i][1] - root_a_coord[i + 1][1]) ** 2 + (
                                           root_a_coord[i][2] - root_a_coord[i + 1][2]) ** 2)
                    full_root_a_length = full_root_a_length + distmp

                for i in range(len(root_b_coord) - 1):
                    distmp = math.sqrt((root_b_coord[i][0] - root_b_coord[i + 1][0]) ** 2 + (
                        root_b_coord[i][1] - root_b_coord[i + 1][1]) ** 2 + (
                                           root_b_coord[i][2] - root_b_coord[i + 1][2]) ** 2)
                    full_root_b_length = full_root_b_length + distmp

                if min_root_length > full_root_a_length:
                    min_root_length = full_root_a_length
                    min_root_trans = root_a_coord

                if min_root_length > full_root_b_length:
                    min_root_length = full_root_b_length
                    min_root_trans = root_b_coord

        # print min_root_length
        try:
            min_root_trans
        except NameError:
            min_root_trans = [[0, 0, 0], [0, 0, 0]]

        if min_root_trans == [[0, 0, 0], [0, 0, 0]]:
            print('Failed to calculate shortest dist')
        else:
            for i in range(len(min_root_trans)):
                min_root_trans[i][0] = min_root_trans[i][0] + centr_cord[0]
                min_root_trans[i][1] = min_root_trans[i][1] + centr_cord[1]
                min_root_trans[i][2] = min_root_trans[i][2] + centr_cord[2]
                # return(edges_sort,cb1_edges_cross,root_a_coord,root_b_coord)
        return (min_root_length, min_root_trans)

        # Return a list of PDB formatted string

    def PDB_format(self, cord, atomt, cname, star_numb):
        # creates PDB format
        k = star_numb
        pdb_format = []
        for coo in cord:
            x = int(float(coo[0]))
            y = int(float(coo[1]))
            z = int(float(coo[2]))
            line = 'ATOM      1   B  CB1 X   1                                                                                                                           '
            a = list(line)
            a[14:16] = atomt
            a[21] = cname
            a[17:20] = 'LOC'
            a[32:len(str(x))] = str(x)
            a[40:len(str(y))] = str(y)
            a[47:len(str(z))] = str(z)
            a[11 - len(str(k)):11] = str(k)
            k = k + 1
            pdb_format.append(string.join(a, ''))
        return pdb_format

    def random_points_on_triangle(self, triangle, den):
        # The area of the triangle
        a = numpy.linalg.norm(triangle[0] - triangle[1])
        b = numpy.linalg.norm(triangle[0] - triangle[2])
        c = numpy.linalg.norm(triangle[1] - triangle[2])

        # The Heron's formula for triangle area
        s = (a + b + c) / 2
        triangle_area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        point_number = int(triangle_area * den)

        random_points = []
        for i in range(point_number):
            A = triangle[0]
            AB = [triangle[1][0] - triangle[0][0], triangle[1][1] - triangle[0][1], triangle[1][2] - triangle[0][2]]
            AC = [triangle[2][0] - triangle[0][0], triangle[2][1] - triangle[0][1], triangle[2][2] - triangle[0][2]]
            R = random.random()
            S = random.random()
            if (R + S) >= 1:
                R = 1 - R
                S = 1 - S
            RandomPointPosition = [A[0] + R * AB[0] + S * AC[0], A[1] + R * AB[1] + S * AC[1],
                                   A[2] + R * AB[2] + S * AC[2]]
            random_points.append(RandomPointPosition)

        return (random_points)


class NlpAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(NlpAnalysis, self).__init__(*args, **kwargs)
        self.computed_values_multiple = None

    def compute(self, points):
        print('Nlp_analysis')

        if self.roi_area is not None:
            RoiArea = self.roi_area
            RoiPerimeter = self.roi_perimeter
            self.computed_values_simple.append(['ROI_perimeter(um)', str(RoiPerimeter / 1000)])
            self.computed_values_simple.append(['ROI_area(um^2)', str(RoiArea / 1000000)])

        channel_nr= numpy.where(numpy.asarray(self.storm_channels_visible) == True)
        visible_channel_nr=numpy.asarray(channel_nr)[0]

        for k in visible_channel_nr:
            if len(points[k])>0:
                coords = numpy.empty((len(points[k]), 3), dtype=numpy.int)
                coords[:, 0] = numpy.asarray(points[k])[:, 0]
                coords[:, 1] = numpy.asarray(points[k])[:, 1]
                coords[:, 2] = numpy.asarray(points[k])[:, 3]
                nlp = len(coords)  # Number of Localization in the channel

                self.computed_values_simple.append([self.storm_channel_list[k] + '_NLP', str(nlp)])

            else:
                self.computed_values_simple.append([self.storm_channel_list[k] + '_NLP', str(0)])


        print('Nlp_analysis ready')


class ConvexHullAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(ConvexHullAnalysis, self).__init__(*args, **kwargs)
        self.computed_values_multiple = None

    def compute(self, points):
        print('ConvexHull_Analysis')

        # 2D matplotlib hull figure properties
        fig2Dhull = plt.figure(facecolor=(0, 0, 0), edgecolor=(0, 0, 0))

        fig2Dhull.patch.set_facecolor((0, 0, 0))
        #fig2Dhull.patch.set_alpha(1)

        axes2Dhull = fig2Dhull.add_subplot(111, axisbg='k', aspect='equal')
        axes2Dhull.set_title('2D Convex hull', color='w')
        fig2Dhull.hold(True)
        axes2Dhull.grid(False)
        axes2Dhull.set_axis_off()
        axes2Dhull.set_frame_on(False)

        # 3D matplotlib hull figure properties
        fig3Dhull = plt.figure(facecolor=(0, 0, 0), edgecolor=(0, 0, 0))
        fig3Dhull.patch.set_facecolor((0, 0, 0))
        #fig3Dhull.patch.set_alpha(1)

        axes3Dhull = fig3Dhull.add_subplot(111, axisbg='k', projection='3d', aspect='equal')
        axes3Dhull.set_title('3D Convex hull', color='w')
        fig3Dhull.hold(True)
        axes3Dhull.grid(False)
        axes3Dhull.set_axis_off()
        axes3Dhull.set_frame_on(False)

        visible_storm_channel_colors = []
        for s in range(len(self.storm_channels_colors)):
            colortuple = [x / 255.0 for x in self.storm_channels_colors[s]]
            visible_storm_channel_colors.append(colortuple)
        coords=None

        channel_nr= numpy.where(numpy.asarray(self.storm_channels_visible) == True)
        visible_channel_nr=numpy.asarray(channel_nr)[0]

        for k in visible_channel_nr:
            if len(points[k])>0:
                coords = numpy.empty((len(points[k]), 3), dtype=numpy.int)
                coords[:, 0] = numpy.asarray(points[k])[:, 0]
                coords[:, 1] = numpy.asarray(points[k])[:, 1]
                coords[:, 2] = numpy.asarray(points[k])[:, 3]

                # calculating 2D hull
                if len(coords) < 4:
                    print("not enough LPs to form a convex hull")

                else:
                    hull2D = scipy.spatial.ConvexHull(coords[:, :2])
                    # calculating perimeter
                    hull2D_perimeter = 0.0

                    for m in range(len(hull2D.vertices) - 1):
                        side = self.EucDistance2D(hull2D.points[hull2D.vertices[m]], hull2D.points[hull2D.vertices[m + 1]])
                        hull2D_perimeter += side

                    hull2D_perimeter += self.EucDistance2D(hull2D.points[hull2D.vertices[0]],
                                                           hull2D.points[hull2D.vertices[-1]])
                    # converting to um
                    hull2D_perimeter = hull2D_perimeter / 1000

                    self.computed_values_simple.append(
                        [self.storm_channel_list[k] + '_2D_hull_perimeter(um)', str(hull2D_perimeter)])

                    # calculating area
                    hull2D_area = 0.0
                    for n in range(len(hull2D.vertices) - 2):
                        hull2D_area += self.TriangleArea2D(hull2D.points[hull2D.vertices[-1]],
                                                           hull2D.points[hull2D.vertices[n]],
                                                           hull2D.points[hull2D.vertices[n + 1]])

                    # converting to um^2
                    hull2D_area = hull2D_area / 1000000

                    self.computed_values_simple.append(
                        [self.storm_channel_list[k] + '_2D_hull_area(um^2)', str(hull2D_area)])

                    # displaying 2D hull
                    axes2Dhull.plot(coords[:, 0], coords[:, 1], 'o', color=visible_storm_channel_colors[k])

                    for simplex in hull2D.simplices:
                        axes2Dhull.plot(coords[simplex, 0], coords[simplex, 1], '-w')

                    if numpy.sum(coords[:, 2]) == 0:
                        print("not 3D data")

                    else:
                        # calculating 3D hull
                        hull3D = scipy.spatial.ConvexHull(coords, incremental=False, qhull_options=None)

                        # calculating surface
                        hull3D_surface = 0.0
                        for simplex in hull3D.simplices:
                            hull3D_surface += self.TriangleArea3D(hull3D.points[simplex[0]], hull3D.points[simplex[1]],
                                                                  hull3D.points[simplex[2]])

                        # converting to um^2
                        hull3D_surface = hull3D_surface / 1000000
                        self.computed_values_simple.append(
                            [self.storm_channel_list[k] + '_3D_hull_surface(um^2)', str(hull3D_surface)])

                        # calculating volume
                        simplices = numpy.column_stack(
                            (numpy.repeat(hull3D.vertices[0], hull3D.nsimplex), hull3D.simplices))
                        tets = hull3D.points[simplices]
                        hull3D_volume = numpy.sum(self.tetrahedron_volume(tets[:, 0], tets[:, 1], tets[:, 2], tets[:, 3]))

                        # converting to um^3
                        hull3D_volume = hull3D_volume / 1000000000

                        self.computed_values_simple.append(
                            [self.storm_channel_list[k] + '_3D_hull_volume(um^3)', str(hull3D_volume)])

                        # displaying 3D hull
                        axes3Dhull.scatter(coords[:, 0], coords[:, 1], zs=coords[:, 2], zdir='z', marker='.',
                                           color=visible_storm_channel_colors[k])
                        axes3Dhull.plot_trisurf(coords[:, 0], coords[:, 1], coords[:, 2], triangles=hull3D.simplices,
                                                color=visible_storm_channel_colors[k], shade=1)
                        axes3Dhull.elev = -96
                        axes3Dhull.azim = -86
                        axes3Dhull.dist = 5


            else:
                print("Not enough points for Convex hull analysis")

        if self.display_plots == True:
            # set origin to upper left corner
            if coords!=None:
                ylim = axes2Dhull.get_ylim()
                axes2Dhull.set_ylim(ylim[1], ylim[0])
                #plt.ion()
                plt.show()
                plt.close()
        else:
            plt.close("all")

        print("ConvexHull_Analysis ready")

class QualityControlAnalysis(Analysis):
     def __init__(self, *args, **kwargs):
         super(QualityControlAnalysis, self).__init__(*args, **kwargs)
         self.computed_values_multiple = None

     def compute(self, points):
         print('QualityControlAnalysis')
         channel_nr= numpy.where(numpy.asarray(self.storm_channels_visible) == True)
         visible_channel_nr=numpy.asarray(channel_nr)[0]

         for k in visible_channel_nr:
             if len(points[k])>0:
                 coords = numpy.empty((len(points[k]), 3), dtype=numpy.int)
                 coords[:, 0] = numpy.asarray(points[k])[:, 0]
                 coords[:, 1] = numpy.asarray(points[k])[:, 1]
                 coords[:, 2] = numpy.asarray(points[k])[:, 3]
                 nlp = len(coords)  # Number of Localization in the channel
                 mean_loc_acc=numpy.mean(numpy.asarray(points[k])[:, 2])

                 tree = scipy.spatial.KDTree(coords)

                 neighbor_nrs=numpy.zeros(nlp)

                 for b in range(nlp):
                     neighbor_nrs[b]=len((tree.query_ball_point(coords[b], 160)))

                 mean_neighbor_number=numpy.mean(neighbor_nrs)-1

                 if all( numpy.asarray(points[k])[:, 2]==numpy.asarray(points[k])[:, 2][0]):
                     self.computed_values_simple.append([self.storm_channel_list[k] + '_mean_localization_accuracy', str(0)])
                 else:
                     self.computed_values_simple.append([self.storm_channel_list[k] + '_mean_localization_accuracy',
                                                    str(mean_loc_acc)])
                 self.computed_values_simple.append([self.storm_channel_list[k] + '_mean_neighbor_number_160nm',
                                                    str(mean_neighbor_number)])
             else:
                 self.computed_values_simple.append([self.storm_channel_list[k] + '_mean_localization_accuracy', str(0)])
                 self.computed_values_simple.append([self.storm_channel_list[k] + '_mean_neighbor_number_160nm',
                                                     str(0)])
         print('QualityControlAnalysis ready')

class DBScanAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(DBScanAnalysis, self).__init__(*args, **kwargs)
        self.computed_values_export = []
        self.output_file_export_extension = 'pdb'

    def Region_Query(self, p, eps, dataset):
        neig_list = []
        for k in range(len(dataset)):
            dist = numpy.linalg.norm(numpy.array(p) - numpy.array(dataset[k]))
            if dist < eps and dist > 0.001:
                neig_list.append(k)
        return neig_list

    def PDB_Print_beta(self, coords, atom_type, chain_id, start_number):
        k = start_number
        pdb_format = []
        for coo in coords:
            # if coo[4] == 0:
            # atom_type = ' O'
            #chain_id = 'A'
            #else:
            #atom_type = ' H'
            #chain_id = 'B'

            x = int(float(coo[0]))
            y = int(float(coo[1]))
            z = int(float(coo[2]))
            line = 'ATOM      1   B  CB1 X   1                                                                                                                           '
            a = list(line)
            a[14:16] = atom_type
            a[21] = chain_id
            a[17:20] = 'LOC'
            a[32:len(str(x))] = str(x)
            a[40:len(str(y))] = str(y)
            a[47:len(str(z))] = str(z)
            a[11 - len(str(k)):11] = str(k)
            a[26 - len(str(k)):26] = str(k)  # resid
            a[60:60 + len(str(coo[4] * 10))] = str(coo[4] * 10)  # Beta Factor
            k = k + 1
            pdb_format.append(string.join(a, ''))

        return (pdb_format)

    def compute(self, points):
        print('DBSCAN_analysis')


        # Big output file header
        self.computed_values_multiple = 'storm_file\tROI_tag\tchannel_ID\tcluster_ID\tNLP_per_cluster' \
                                        '\tV_hull_per_cluster(um^3)\tmax_distance_per_cluster(um)\n'
        fig = plt.figure(facecolor=(0, 0, 0), edgecolor=(0, 0, 0))
        fig.hold(True)
        fig.patch.set_facecolor((0, 0, 0))
        # fig.patch.set_alpha(1)
        axes = fig.add_subplot(111, axisbg='k', projection='3d', aspect='equal')
        axes.grid(False)
        axes.set_axis_off()
        axes.set_frame_on(False)

        axes.set_title('DBSCAN', color='w')

        self.computed_values_simple.append(
            ['DBSCAN_parameters[Eps(nm),MinN] ', str(self.analysis_dbscan_eps) + ',' + str(self.analysis_dbscan_minn)])
        coords=None

        channel_nr= numpy.where(numpy.asarray(self.storm_channels_visible) == True)
        visible_channel_nr=numpy.asarray(channel_nr)[0]
        print(len(points[0]))
        for m in visible_channel_nr:
            if len(points[m])>0:
                coords = numpy.empty((len(points[m]), 3), dtype=numpy.int)
                coords[:, 0] = numpy.asarray(points[m])[:, 0]
                coords[:, 1] = numpy.asarray(points[m])[:, 1]
                coords[:, 2] = numpy.asarray(points[m])[:, 3]
                coords = coords.tolist()
                nlp = len(coords)  # Number of Localization in the bouton
                clusters = []
                for i in range(len(coords)):
                    clusters.append(coords[i] + [0, 0])  # coordinates, visited(1), clusternumber (0 noise)
                clust_number = 0

                for i in range(len(clusters)):
                    if clusters[i][3] == 0:  # Not visited jet
                        neig = self.Region_Query(clusters[i][:3], self.analysis_dbscan_eps, coords)

                        if len(neig) < self.analysis_dbscan_minn:
                            clusters[i][3:] = [1, 0]  # Visited and noise
                        else:
                            clust_number = clust_number + 1
                            clusters[i][3:] = [1, clust_number]  # add P to cluster C

                            neig_numb = len(neig)  #Expand the cluster
                            k = 0
                            while k <= neig_numb - 1:
                                if clusters[neig[k]][3] == 0 or clusters[neig[k]][
                                    4] == 0:  # if P' is not visited or it's noise
                                    clusters[neig[k]][3] = 1  # mark P' as visited
                                    neig2 = self.Region_Query(clusters[neig[k]][:3], self.analysis_dbscan_eps,
                                                              coords)  # Neighbors of P'
                                    if len(neig2) >= self.analysis_dbscan_minn:
                                        neig = neig + neig2  #NeighborPts joined with NeighborPts'
                                        neig_numb = len(neig)
                                    if clusters[neig[k]][4] == 0:  # if P' is not yet member of any cluster
                                        clusters[neig[k]][4] = clust_number  # add P' to cluster C
                                k += 1

                self.computed_values_simple.append([self.storm_channel_list[m] + '_cluster#', str(clust_number)])
                sumvolume = 0

                # calculating cluster properties
                for c in range(clust_number + 1):
                    inds = numpy.where(numpy.asarray(clusters)[:, 4] != c)
                    cluster = numpy.delete(numpy.asarray(clusters), inds, 0)
                    # calculating nlp per cluster
                    nlp_per_cluster = len(cluster)
                    # calculating 3D hulls and volumes for clusters
                    hull3D_volume = 0
                    if c > 0:
                        if len(cluster) > 3:
                            hull3D = scipy.spatial.ConvexHull(cluster[:, :3], incremental=False, qhull_options=None)
                            # calculating volume
                            simplices = numpy.column_stack(
                                (numpy.repeat(hull3D.vertices[0], hull3D.nsimplex), hull3D.simplices))
                            tets = hull3D.points[simplices]
                            hull3D_volume = numpy.sum(
                                self.tetrahedron_volume(tets[:, 0], tets[:, 1], tets[:, 2], tets[:, 3]))
                            sumvolume += hull3D_volume

                        # calculating maximum distance
                        maxdistance = 0
                        for cm in range(len(cluster)):
                            for om in range(len(cluster)):
                                if self.EucDistance3D(cluster[cm, :3], cluster[om, :3]) > maxdistance:
                                    maxdistance = self.EucDistance3D(cluster[cm, :3], cluster[om, :3])

                        self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' + \
                                                         self.storm_channel_list[m] + '\t' + str(c) + '\t' + str(
                            nlp_per_cluster) + '\t' + str(hull3D_volume / 1000000000) + '\t' + str(
                            maxdistance / 1000) + '\n'
                    else:
                        self.computed_values_simple.append(
                            [self.storm_channel_list[m] + '_clustered_NLP#', str(len(clusters) - nlp_per_cluster)])
                        self.computed_values_simple.append(
                            [self.storm_channel_list[m] + '_noise#', str(nlp_per_cluster)])

                self.computed_values_simple.append(
                    [self.storm_channel_list[m] + '_sum_V_hull(um^3)', str(sumvolume / 1000000000)])

                # Displaying coordinates in 3D

                # marking unclastered dots with white
                inds = numpy.where(numpy.asarray(clusters)[:, 4] == 0)
                clusters_wo_noise = numpy.delete(numpy.asarray(clusters), inds, 0)
                colorlist = numpy.ones((len(clusters_wo_noise), 3))

                for s in range(clust_number):
                    inds = numpy.where(numpy.asarray(clusters_wo_noise)[:, 4] == s + 1)
                    assignedcolor = matplotlib.colors.hsv_to_rgb([(s / 1.0) / clust_number, 1.0, 1.0])
                    colorlist[inds, :] = numpy.asarray(assignedcolor)

                scalefactor = 50

                if m == 0:
                    axes.scatter(numpy.asarray(clusters_wo_noise)[:, 0], numpy.asarray(clusters_wo_noise)[:, 1],
                                 zs=numpy.asarray(clusters_wo_noise)[:, 2], zdir='z', s=scalefactor * 2,
                                 c=numpy.asarray(colorlist), marker='.')
                elif m == 1:
                    axes.scatter(numpy.asarray(clusters_wo_noise)[:, 0], numpy.asarray(clusters_wo_noise)[:, 1],
                                 zs=numpy.asarray(clusters_wo_noise)[:, 2], zdir='z', s=scalefactor,
                                 c=numpy.asarray(colorlist), marker='s')
                elif m == 2:
                    axes.scatter(numpy.asarray(clusters_wo_noise)[:, 0], numpy.asarray(clusters_wo_noise)[:, 1],
                                 zs=numpy.asarray(clusters_wo_noise)[:, 2], zdir='z', s=scalefactor,
                                 c=numpy.asarray(colorlist), marker='V')
                else:
                    axes.scatter(numpy.asarray(clusters_wo_noise)[:, 0], numpy.asarray(clusters_wo_noise)[:, 1],
                                 zs=numpy.asarray(clusters_wo_noise)[:, 2], zdir='z', s=scalefactor,
                                 c=numpy.asarray(colorlist), marker='D')
                # Saving clustered coordinates to PDB file

                if self.analysis_dbscan_export_pdb == True:
                    if m == 0:
                        self.computed_values_export += self.PDB_Print_beta(clusters, ' C', 'A', 1)
                    elif m == 1:
                        self.computed_values_export += self.PDB_Print_beta(clusters, ' N', 'A', 1)
                    elif m == 2:
                        self.computed_values_export += self.PDB_Print_beta(clusters, ' P', 'A', 1)
                    else:
                        self.computed_values_export += self.PDB_Print_beta(clusters, ' S', 'A', 1)

            else:
                print('not enough LPs for DBSCAN analysis') \

        if self.display_plots == True:
            # ylim=axes.get_ylim()
            # axes.set_ylim(ylim[1], ylim[0])
            if coords!=None:
                axes.elev =- 96
                axes.azim =- 86
                axes.dist = 5
                #plt.ion()
                plt.show()

        else:
            plt.close("all")

        print('DBSCAN_analysis ready')


class InternalizationDrAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(InternalizationDrAnalysis, self).__init__(*args, **kwargs)
        self.requirements_dimensions_num_list_any = ['3d']

    def compute(self, points):

        print("d/r analysis")
        dist_channel_nr = self.visible_storm_channel_names.index(
            self.analysis_internalization_dr_channel_distance)

        # Big output file header
        self.computed_values_multiple = 'storm_file\tROI_tag\tchannel_ID\tXPoint\tYPoint\tZPoint\td/r\n'
        if len(points[dist_channel_nr])>3:
            points_4_distances = numpy.empty((len(points[dist_channel_nr]), 3), dtype=numpy.float)
            points_4_distances[:, 0] = numpy.asarray(points[dist_channel_nr])[:, 0]
            points_4_distances[:, 1] = numpy.asarray(points[dist_channel_nr])[:, 1]
            points_4_distances[:, 2] = numpy.asarray(points[dist_channel_nr])[:, 3]

            # calculating center of gravity
            M = numpy.mean(points_4_distances, axis=0)
            hull2D = ConvexHull(points_4_distances[:, :2])
            hull2D_area = 0.0
            for k in range(len(hull2D.vertices) - 2):
                hull2D_area += self.TriangleArea2D(hull2D.points[hull2D.vertices[-1]], hull2D.points[hull2D.vertices[k]],
                                                   hull2D.points[hull2D.vertices[k + 1]])
            r = math.sqrt(hull2D_area / math.pi)

            # Calculating distances form center of gravity
            dist_from_cg = []
            for m in range(len(points_4_distances)):
                dist_from_cg.append(self.EucDistance3D(points_4_distances[m, :], M) / r)
            average_dr = numpy.mean(numpy.asarray(dist_from_cg))

            # Generating output
            self.computed_values_simple.append(
                [str(self.analysis_internalization_dr_channel_distance) + '_mean_d/r', str(average_dr)])

            for c in range(len(points_4_distances)):
                self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' + str(
                    self.analysis_internalization_dr_channel_distance) + '\t' + str(points_4_distances[c, 0]) + '\t' + str(
                    points_4_distances[c, 1]) + '\t' + str(points_4_distances[c, 2]) + '\t' + str(dist_from_cg[c]) + '\n'
        else:
            print("not enough LPs for d/r analysis")
        print("d/r analysis ready")


class InternalizationSurfaceAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(InternalizationSurfaceAnalysis, self).__init__(*args, **kwargs)
        self.requirements_dimensions_num_list_any = ['3d']

    def compute(self, points):

        print("Internalization Analysis/surface")
        hull_channel_nr = self.visible_storm_channel_names.index(
            self.analysis_internalization_surface_channel_convex)
        dist_channel_nr = self.visible_storm_channel_names.index(
            self.analysis_internalization_surface_channel_distance)

        int_threshold = self.analysis_internalization_surface_treshold

        if (len(points[dist_channel_nr])>0 and len(points[hull_channel_nr])>3):
            # Big output file header
            self.computed_values_multiple = 'storm_file\tROI_tag\tchannel_IDs(distance,hull)\tXPoint\tYPoint\tZPoint' \
                                            '\tXHullPoint\tYHullPoint\tZHullPoint\tdistance(um)\n'

            points_4_distances = numpy.empty((len(points[dist_channel_nr]), 3), dtype=numpy.float)
            points_4_distances[:, 0] = numpy.asarray(points[dist_channel_nr])[:, 0]
            points_4_distances[:, 1] = numpy.asarray(points[dist_channel_nr])[:, 1]
            points_4_distances[:, 2] = numpy.asarray(points[dist_channel_nr])[:, 3]

            points_4_hull = numpy.empty((len(points[hull_channel_nr]), 3), dtype=numpy.float)
            points_4_hull[:, 0] = numpy.asarray(points[hull_channel_nr])[:, 0]
            points_4_hull[:, 1] = numpy.asarray(points[hull_channel_nr])[:, 1]
            points_4_hull[:, 2] = numpy.asarray(points[hull_channel_nr])[:, 3]
            points_4_hull = points_4_hull.tolist()


            qpoint_vector = []
            distance_vector = []
            # Convex hull of the points
            conv_hull = ConvexHull(points_4_hull)
            for s in range(len(points_4_distances)):
                [qpoint, distance, tri] = self.ClosestHullSurfPoint_2(conv_hull, points_4_distances[s, :])
                qpoint_vector.append(qpoint)
                distance_vector.append(distance)
                # print str(s) + '/' + str(len(points_4_distances))

            # Generate small output file
            internalized_nr = numpy.asarray(numpy.where(numpy.asarray(distance_vector) > int_threshold)).size

            self.computed_values_simple.append(['surface_internalization_parameters[distance_channel, hull_channel,'
                                                ' threshold(um)]',
                                                str(self.analysis_internalization_surface_channel_distance)+','+
                                               str(self.analysis_internalization_surface_channel_convex)+','+
            str(int_threshold / 1000.0)])

            self.computed_values_simple.append(['internalized_NLP_surface_distance', str(internalized_nr)])
            # Generate big output file
            for c in range(len(distance_vector)):
                self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' + str(
                    self.analysis_internalization_surface_channel_distance) + ',' + str(
                    self.analysis_internalization_surface_channel_convex) + '\t' + str(
                    points_4_distances[c, 0]) + '\t' + str(points_4_distances[c, 1]) + '\t' + str(
                    points_4_distances[c, 2]) + '\t' + str(qpoint_vector[c][0]) + '\t' + str(
                    qpoint_vector[c][1]) + '\t' + str(qpoint_vector[c][2]) + '\t' + str(
                    round(distance_vector[c] / 1000, ndigits=3)) + '\n'
        else:
            print('not enough LPs for Surface Internalization Analysis')
        print('Internalization Analysis/surface ready')


class EuclideanDistanceWithinChannelAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(EuclideanDistanceWithinChannelAnalysis, self).__init__(*args, **kwargs)

    def compute(self, points):
        print("EuclideanDistanceWithinChannelAnalysis")

        # Big output file header
        self.computed_values_multiple = 'storm_file\tROI_tag\tchannel_ID\tLP_ID\tmin_neighbor_distance(um)\n'
        channel_nr= numpy.where(numpy.asarray(self.storm_channels_visible) == True)
        visible_channel_nr=numpy.asarray(channel_nr)[0]

        for k in visible_channel_nr:
            if len(points[k])>0:

                rsd = numpy.empty((len(points[k]), 3), dtype=numpy.float)
                rsd[:, 0] = numpy.asarray(points[k])[:, 0]
                rsd[:, 1] = numpy.asarray(points[k])[:, 1]
                rsd[:, 2] = numpy.asarray(points[k])[:, 3]

                tree = scipy.spatial.KDTree(rsd)
                NNvector, NNs = tree.query(rsd, k=2, p=2)
                meanNN = numpy.mean(NNvector[:, 1] / 1000.0)
                varNN = scipy.stats.variation(NNvector[:, 1] / 1000.0, axis=0)
                # Creating big outfile
                for i in range(len(NNvector)):
                    self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' + \
                                                     self.storm_channel_list[k] + '\t' + str(
                        NNs[i, 0]) + '\t' + str(NNvector[i, 1] / 1000.0) + '\n'
                # Creating small outfile
                self.computed_values_simple.append(
                    [self.storm_channel_list[k] + '_mean_NN_distance(um)', str(meanNN)])
                self.computed_values_simple.append([self.storm_channel_list[k] + '_CV_NN_distance', str(varNN)])
            else:
                print("not enough LPs for Euclidean Distance within channel analysis")
        print("EuclideanDistanceWithinChannelAnalysis ready")


class EuclideanDistanceBetweenChannelsAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(EuclideanDistanceBetweenChannelsAnalysis, self).__init__(*args, **kwargs)
        self.requirements_channels_num_min = 1

    def compute(self, points):
        print("EuclideanDistanceBetweenChannelAnalysis")
        base_channel_nr = self.visible_storm_channel_names.index(
                self.analysis_euclidean_between_channel_minimum_dist)
        from_channel_nr = self.visible_storm_channel_names.index(self.analysis_euclidean_between_channel_from)


        if self.analysis_euclidean_between_confocal.isChecked():
            ConfocalSizeMultiplier=self.StormDisplay.ConfocalSizeMultiplier
            channel=int(self.analysis_euclidean_between_channel_from_confocal)
            channelstr=str(channel)
            img=self.StormDisplay.ConfChannelToShow[channel]

            im=scipy.ndimage.zoom(img,(0.1,0.1),order=0)/ 255.0
            #fig2 = plt.figure(facecolor=(0, 0, 0), edgecolor=(0, 0, 0))
            #axes3 = fig2.add_subplot(111, axisbg='k', aspect='equal')
            #axes3.imshow(im, cmap=plt.cm.gray)
            #plt.show()



            # selecting and resizing STORM channel to confocal channel
            if (len(points[base_channel_nr])>0):
                #todo get it from GUI
                pix_size=self.ConfocalMetaData['SizeX']*1000 #in nm
                offset=[self.confocal_offset[1]/ConfocalSizeMultiplier, self.confocal_offset[0]/ConfocalSizeMultiplier]

                base_coords = numpy.empty((len(points[base_channel_nr]), 3), dtype=numpy.float)
                base_coords[:, 0] = (numpy.asarray(points[base_channel_nr])[:, 0])/pix_size-offset[0]
                base_coords[:, 1] = (numpy.asarray(points[base_channel_nr])[:, 1])/pix_size-offset[1]
                base_coords[:, 2] = numpy.asarray(points[base_channel_nr])[:, 3]/pix_size

                image_max = ndimage.maximum_filter(im, size=3, mode='constant')
                maxima = (im == image_max)
                image_min = ndimage.minimum_filter(im, size=3, mode='constant')
                threshold=numpy.mean(im)+(numpy.amax(im)-numpy.mean(im))\
                                         *self.analysis_euclidean_between_channel_peak_threshold/100.0
                diff = ((image_max - image_min) > threshold)
                maxima[diff == 0] = 0
                labeled, num_objects = ndimage.label(maxima)
                xy_switched = numpy.array(ndimage.center_of_mass(im, labeled, list(range(1, num_objects+1))))

                coordinates=numpy.copy(xy_switched)
                coordinates[:,1]=xy_switched[:,0]
                coordinates[:,0]=xy_switched[:,1]

                ## display results
                fig = plt.figure(facecolor=(0, 0, 0), edgecolor=(0, 0, 0))
                axes = fig.add_subplot(121, axisbg='k', aspect='equal')
                axes2= fig.add_subplot(122, axisbg='k', aspect='equal')
                axes2.set_title('Distance from confocal channel', color='w')
                axes.imshow(im, cmap=plt.cm.gray)
                axes.autoscale(False)
                loc_max_intensities=[]
                for coord in coordinates:
                    loc_max_intensities.append(im[coord[1],coord[0]])

                distance_threshold=self.analysis_euclidean_between_channel_distance_threshold/pix_size #nm
                boundaries=numpy.zeros(4)
                boundaries[0]=numpy.amin(base_coords[:, 0])
                boundaries[1]=numpy.amax(base_coords[:, 0])
                boundaries[2]=numpy.amin(base_coords[:, 1])
                boundaries[3]=numpy.amax(base_coords[:, 1])

                # deleting local maxima which have a bigger distance from the bouton than the 2*threshold

                distant_inds = numpy.where(numpy.asarray(coordinates[:,0]) < (boundaries[0]-2*distance_threshold))
                coordinates = numpy.delete(coordinates, distant_inds, 0)

                distant_inds = numpy.where(numpy.asarray(coordinates[:,0]) > (boundaries[1]+2*distance_threshold))
                coordinates = numpy.delete(coordinates, distant_inds, 0)

                distant_inds = numpy.where(numpy.asarray(coordinates[:,1]) < (boundaries[2]-2*distance_threshold))
                coordinates = numpy.delete(coordinates, distant_inds, 0)

                distant_inds = numpy.where(numpy.asarray(coordinates[:,1]) > (boundaries[3]+2*distance_threshold))
                coordinates = numpy.delete(coordinates, distant_inds, 0)

                near_coordinates=[]

                for nlg_coord in coordinates:
                    for storm_coord in base_coords:
                        nlg_distance=self.EucDistance2D([storm_coord[0],storm_coord[1]], nlg_coord)
                        if nlg_distance<distance_threshold:
                            near_coordinates.append(nlg_coord)
                            break

                near_coords=numpy.asarray(near_coordinates)

                ext_near_coords=[]
                if len(near_coords)>0:
                    for near_coord in near_coords:
                        pix_int_thresh=im[(near_coord[1]),(near_coord[0])]*self.analysis_euclidean_between_channel_pixel_threshold/100.0
                        for k in range(-3,3):
                            for n in range(-3,3):
                                if (im[(near_coord[1]+k),(near_coord[0]+n)]>pix_int_thresh):
                                    ext_near_coords.append([(near_coord[0]+n),(near_coord[1]+k)])

                if len(ext_near_coords)>0:
                    ext_near_coords=numpy.asarray(ext_near_coords)

                    axes.plot(base_coords[:, 0], base_coords[:, 1], 'y.')
                    axes.plot(ext_near_coords[:, 0], ext_near_coords[:, 1], 'mo')
                    axes.plot(coordinates[:, 0], coordinates[:, 1], 'ro')
                    axes.plot(near_coords[:, 0], near_coords[:, 1], 'bo')

                    axes.axis('off')
                    axes.set_title('Peak local max')

                    from_coords = numpy.empty((len(ext_near_coords), 3), dtype=numpy.float)
                    from_coords[:, 0] = (ext_near_coords[:, 0]+offset[0]+0.5)*pix_size
                    from_coords[:, 1] = (ext_near_coords[:, 1]+offset[1]+0.5)*pix_size
                    from_coords[:, 2] = numpy.zeros(len(ext_near_coords))

                else:
                    from_coords=[]
                    print("no points in reference channel")

        else:

            if (len(points[from_channel_nr])>0):
                from_coords = numpy.empty((len(points[from_channel_nr]), 3), dtype=numpy.float)
                from_coords[:, 0] = numpy.asarray(points[from_channel_nr])[:, 0]
                from_coords[:, 1] = numpy.asarray(points[from_channel_nr])[:, 1]
                from_coords[:, 2] = numpy.asarray(points[from_channel_nr])[:, 3]
            channelstr=self.visible_storm_channel_names[from_channel_nr]




        if (len(points[base_channel_nr])>0 and len(from_coords)>0):
            # Big output file header
            self.computed_values_multiple = 'storm_file\tROI_tag\tchannel_IDs(base,ref)\t' \
                                            'LP_ID\tXBase\tYBase\tZBase\tXRef' \
                                            '\tYRef\tZRef\tmin_neighbor_distance(um)\n'

            base_coords = numpy.empty((len(points[base_channel_nr]), 3), dtype=numpy.float)
            base_coords[:, 0] = numpy.asarray(points[base_channel_nr])[:, 0]
            base_coords[:, 1] = numpy.asarray(points[base_channel_nr])[:, 1]
            base_coords[:, 2] = numpy.asarray(points[base_channel_nr])[:, 3]

            if self.display_plots == True and self.analysis_euclidean_between_confocal.isChecked():
                axes2.plot(base_coords[:, 0], base_coords[:, 1], 'y.')
                axes2.plot(from_coords[:, 0], from_coords[:, 1], 'mo')
                ylim = axes2.get_ylim()
                axes2.set_ylim(ylim[1], ylim[0])
                axes2.axis('off')
                # axes2.set_axis_bgcolor('k')
                # axes.set_aspect('equal')
                # axes2.set_aspect('equal')
                plt.show()
            else:
                plt.close("all")


            tree = scipy.spatial.KDTree(from_coords)
            NNvector, NNs = tree.query(base_coords, k=1, p=2)
            meanNN = numpy.mean(NNvector / 1000.0)
            varNN = scipy.stats.variation(NNvector / 1000.0, axis=0)

            # Creating big outfile
            for i in range(len(NNvector)):
                self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' \
                                                  + \
                                                 self.visible_storm_channel_names[
                                                     base_channel_nr] + ',' + \
                                                 channelstr + '\t' +str(i) + '\t' \
                                                 +str(base_coords[i,0])+'\t'\
                                                 +str(base_coords[i,1])+'\t'\
                                                 +str(base_coords[i,2])+'\t'\
                                                 +str(from_coords[NNs[i],0])+'\t'\
                                                 +str(from_coords[NNs[i],1])+'\t'\
                                                 +str(from_coords[NNs[i],2])+'\t'+ str(NNvector[i] / 1000.0) + '\n'

            for v in range(len(from_coords)):
                self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' \
                                                  + \
                                                 self.visible_storm_channel_names[base_channel_nr] +',' + \
                                                 channelstr + '\t' +'ref_'+str(v) + '\t' \
                                                 +'_'+'\t'\
                                                 +'_'+'\t'\
                                                 +'_'+'\t'\
                                                 +str(from_coords[v,0])+'\t'\
                                                 +str(from_coords[v,1])+'\t'\
                                                 +str(from_coords[v,2])+'\t_\n'

            # Creating small outfile
            self.computed_values_simple.append(['Euclidean_distance_between_parameters[distance_channel,'
                                                'reference_channel]',self.visible_storm_channel_names[base_channel_nr]
                                                +','+channelstr])

            if self.analysis_euclidean_between_confocal.isChecked():
                self.computed_values_simple.append([
                'Reference_from_confocal_parameters[peak_threshold(%), distance_threshold(nm), pixel_threshold(%)]',
                str(self.analysis_euclidean_between_channel_peak_threshold)+','
                +str(self.analysis_euclidean_between_channel_distance_threshold)+','
                +str(self.analysis_euclidean_between_channel_pixel_threshold)])

            self.computed_values_simple.append([
                'mean_NN_distance_between(um)', str(meanNN)])
            self.computed_values_simple.append([
                'CV_NN_distance_between', str(varNN)])
        else:
            print("Not enough LPs for EuclideanDistanceBetweenChannelAnalysis")
        print("EuclideanDistanceBetweenChannelAnalysis ready")


class SurfaceDistanceBetweenChannelsAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(SurfaceDistanceBetweenChannelsAnalysis, self).__init__(*args, **kwargs)
        self.requirements_channels_num_min = 2
        self.requirements_dimensions_num_list_any = ['3d']
        self.computed_values_export = []
        self.output_file_export_extension = 'pdb'

    # Return the Hull points in order of the surface triangles
    def Hull_Points(self, hull):
        hullpoints = []
        for trian in hull.simplices:
            hullpoints = hullpoints + [hull.points[trian[0]], hull.points[trian[1]], hull.points[trian[2]]]

        return (hullpoints)

    # Connect the LOC in PDB format
    def PDB_Connect_Edges(self, coords, start_atom, rep_type):
        conn = []

        if rep_type == 'root':
            for i in range(start_atom, len(coords) - 1 + start_atom):
                a = list(
                    'CONECT                                                                                                              ')
                a[11 - len(str(i)):10] = str(i)
                a[16 - len(str(i + 1)):15] = str(i + 1)
                conn.append(string.join(a, ''))

        if rep_type == 'hull':
            for i in range(start_atom, len(coords) + start_atom, 3):
                a = list(
                    'CONECT                                                                                                              ')
                a[11 - len(str(i)):10] = str(i)
                a[16 - len(str(i + 1)):15] = str(i + 1)
                a[21 - len(str(i + 2)):20] = str(i + 2)
                conn.append(string.join(a, ''))
                a = list(
                    'CONECT                                                                                                              ')
                a[11 - len(str(i)):10] = str(i + 1)
                a[16 - len(str(i + 1)):15] = str(i + 2)
                conn.append(string.join(a, ''))

        if rep_type == 'pair':
            for i in range(start_atom, len(coords) - 1 + start_atom, 2):
                a = list(
                    'CONECT                                                                                                              ')
                a[11 - len(str(i)):10] = str(i)
                a[16 - len(str(i + 1)):15] = str(i + 1)
                conn.append(string.join(a, ''))

        return (conn)


    def compute(self, points):
        print("SurfaceDistanceBetweenChannelAnalysis")

        hull_channel_nr = self.visible_storm_channel_names.index(self.analysis_euclidean_surface_between_channel_convex)
        ref_channel_nr = self.visible_storm_channel_names.index(
            self.analysis_euclidean_surface_between_channel_reference)
        dist_channel_nr = self.visible_storm_channel_names.index(
            self.analysis_euclidean_surface_between_channel_distance)

        dist_limit = self.analysis_euclidean_surface_between_distance_limit
        isPDBChecked = self.analysis_euclidean_surface_between_export_pdb

        visible_storm_channel_colors = []
        for s in range(len(self.storm_channels_colors)):
            colortuple = [x / 255.0 for x in self.storm_channels_colors[s]]
            visible_storm_channel_colors.append(colortuple)
        if (len(points[hull_channel_nr])>3 and len(points[ref_channel_nr])>3 and len(points[ref_channel_nr])>0):
            # generating input matrices
            points_4_hull = numpy.empty((len(points[hull_channel_nr]), 3), dtype=numpy.float)
            points_4_hull[:, 0] = numpy.asarray(points[hull_channel_nr])[:, 0]
            points_4_hull[:, 1] = numpy.asarray(points[hull_channel_nr])[:, 1]
            points_4_hull[:, 2] = numpy.asarray(points[hull_channel_nr])[:, 3]
            points_4_hull = points_4_hull.tolist()

            points_4_reference = numpy.empty((len(points[ref_channel_nr]), 3), dtype=numpy.float)
            points_4_reference[:, 0] = numpy.asarray(points[ref_channel_nr])[:, 0]
            points_4_reference[:, 1] = numpy.asarray(points[ref_channel_nr])[:, 1]
            points_4_reference[:, 2] = numpy.asarray(points[ref_channel_nr])[:, 3]
            points_4_reference = points_4_reference.tolist()

            points_4_distances = numpy.empty((len(points[dist_channel_nr]), 3), dtype=numpy.float)
            points_4_distances[:, 0] = numpy.asarray(points[dist_channel_nr])[:, 0]
            points_4_distances[:, 1] = numpy.asarray(points[dist_channel_nr])[:, 1]
            points_4_distances[:, 2] = numpy.asarray(points[dist_channel_nr])[:, 3]
            points_4_distances = points_4_distances.tolist()

            # Big output file header
            self.computed_values_multiple = 'storm_file\tROI_tag\tchannel_IDs(hull,reference,distance)\tXPoint1\tYPoint1' \
                                            '\tZPoint1\tXPoint2\tYPoint2\tZPoint2\tsurface_distance(um)\n'

            points_4_distances_dist_proj = self.Loc_Distances_from_Hull_Surface_2(numpy.array(points_4_distances),
                                                                                  numpy.array(points_4_hull))

            # Distance cutoff
            # in nm
            # Only LOC closer than dist_limit
            tmp = []
            for i in range(len(points_4_distances_dist_proj)):
                if points_4_distances_dist_proj[i][6] < dist_limit:
                    tmp.append(points_4_distances_dist_proj[i])
            closer_localizations = copy.deepcopy(tmp)

            #Calculate the distance from the reference hull
            points_4_distances_dist_from_ref_hull = self.Loc_Distances_from_Hull_Surface_2(
                numpy.array([s[3:6] for s in closer_localizations]), numpy.array(points_4_reference))

            ref_proj_points_proj_to_hull_surf = self.Loc_Distances_from_Hull_Surface_2(
                numpy.array([s[3:6] for s in points_4_distances_dist_from_ref_hull]), numpy.array(points_4_hull))

            for i in range(len(closer_localizations)):
                closer_localizations[i] = closer_localizations[i] + ref_proj_points_proj_to_hull_surf[i][3:6]

            conv_hull_reference = ConvexHull(points_4_reference)

            # Convex hull of the points
            conv_hull = ConvexHull(points_4_hull)

            ## calculation of the shortest route
            all_distances = []
            all_roots = []
            for i in range(len(closer_localizations)):
                A = closer_localizations[i][10:]  #Points on reference hul
                B = closer_localizations[i][3:6]  #Points on hull 4 distances
                [min_dist_on_hull, min_dist_on_hull_root] = self.shortest_distance_on_hull_surface(conv_hull, A, B)
                all_roots.append(min_dist_on_hull_root)
                all_distances.append(A + B + [min_dist_on_hull])

            # Generate small output file
            distance_vector = numpy.asarray(all_distances)[:, 6]

            meanDV = numpy.mean(distance_vector / 1000.0)
            varDV = scipy.stats.variation(distance_vector / 1000.0, axis=0)

            self.computed_values_simple.append(['surface_distance_between_parameters[hull_channel,reference_channel,'
                                                'distance_channel,distance_limit(um)',
                                                self.visible_storm_channel_names[hull_channel_nr]
                                                + ',' + self.visible_storm_channel_names[ref_channel_nr]
                                                + ',' + self.visible_storm_channel_names[
                                                    dist_channel_nr] + ',' + str(dist_limit / 1000.0)])

            self.computed_values_simple.append(['mean_surface_distance(um)', str(meanDV)])
            self.computed_values_simple.append(['CV_surface_distance', str(varDV)])

            # Generate big output file
            for c in range(len(all_distances)):
                self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' \
                                                 + self.visible_storm_channel_names[hull_channel_nr] + ',' \
                                                 + self.visible_storm_channel_names[ref_channel_nr] + ',' \
                                                 + self.visible_storm_channel_names[dist_channel_nr] \
                                                 + '\t' + str(all_distances[c][0]) + '\t' \
                                                 + str(all_distances[c][1]) + '\t' + str(all_distances[c][2]) \
                                                 + '\t' + str(all_distances[c][3]) + '\t' + str(all_distances[c][4]) \
                                                 + '\t' + str(all_distances[c][5]) + '\t' + str(
                    all_distances[c][6] / 1000.0) \
                                                 + '\n'

            # Visualize in matplotlib

            points_refer_draw = numpy.copy(numpy.array(points_4_reference))
            points_orig_draw = numpy.copy(numpy.array(points_4_distances))
            closer_localizations_draw = numpy.copy(closer_localizations)
            points_4_distances_dist_proj_draw = numpy.copy(closer_localizations)
            points_4_distances_dist_proj_all_draw = numpy.copy(points_4_distances_dist_proj)

            fig = plt.figure(facecolor=(0, 0, 0), edgecolor=(0, 0, 0))
            fig.hold(True)
            fig.patch.set_facecolor((0, 0, 0))
            # fig.patch.set_alpha(1)
            axes = fig.add_subplot(111, axisbg='k', projection='3d', aspect='equal')
            axes.grid(False)
            axes.set_axis_off()
            axes.set_frame_on(False)

            axes.set_title('Surface distances', color='w')


            # All points
            axes.plot(points_orig_draw[:, 0], points_orig_draw[:, 1], points_orig_draw[:, 2], linestyle='none',
                      marker='o', markerfacecolor=visible_storm_channel_colors[dist_channel_nr], markersize=3)
            # Hull
            for simplex in conv_hull.simplices:
                simplex = numpy.append(simplex, simplex[0])
                axes.plot(conv_hull.points[simplex, 0], conv_hull.points[simplex, 1], conv_hull.points[simplex, 2],
                          color=visible_storm_channel_colors[hull_channel_nr], linestyle='-',
                          markeredgecolor=visible_storm_channel_colors[hull_channel_nr], marker='o',
                          markerfacecolor=visible_storm_channel_colors[hull_channel_nr],
                          markersize=3)

            # Hull_reference
            for simplex in conv_hull_reference.simplices:
                simplex = numpy.append(simplex, simplex[0])
                axes.plot(conv_hull_reference.points[simplex, 0], conv_hull_reference.points[simplex, 1],
                          conv_hull_reference.points[simplex, 2], color=visible_storm_channel_colors[ref_channel_nr],
                          linestyle='-', markeredgecolor=visible_storm_channel_colors[ref_channel_nr],
                          marker='o', markerfacecolor=visible_storm_channel_colors[ref_channel_nr], markersize=3)

                ##reference points
                #plt.plot(points_4_distances_dist_proj_draw[:, 3], points_4_distances_dist_proj_draw[:, 4],
                #points_4_distances_dist_proj_draw[:, 5], color='blue', linestyle='none', marker='^',
                #markerfacecolor='blue', markersize=3)
                #plt.plot(points_4_distances_dist_proj_draw[:, 0], points_4_distances_dist_proj_draw[:, 1],
                #points_4_distances_dist_proj_draw[:, 2], color='green', linestyle='none', marker='o',
                #markerfacecolor='green', markersize=3)
                #plt.plot(points_4_distances_dist_proj_all_draw[:, 3], points_4_distances_dist_proj_all_draw[:, 4],
                #points_4_distances_dist_proj_all_draw[:, 5], color='gray', linestyle='none', marker='^',
                #markerfacecolor='gray', markersize=3)
                #plt.plot(closer_localizations_draw[:, 0], closer_localizations_draw[:, 1], closer_localizations_draw[:, 2],
                #color='yellow', linestyle='none', marker='^', markerfacecolor='yellow', markersize=3)

            # Shortest routes on surface
            for i in range(len(all_roots)):
                min_root_draw = numpy.copy(numpy.array(all_roots[i]))
                axes.plot(min_root_draw[:, 0], min_root_draw[:, 1], min_root_draw[:, 2], color='grey', linestyle='-',
                          linewidth='1',
                          marker='o', markerfacecolor='grey', markersize=1)

            if self.display_plots == True:
                axes.elev = -96
                axes.azim = -86
                axes.dist = 5
                #plt.ion()
                plt.show()

            else:
                plt.close("all")

            if isPDBChecked == 1:
                ##Visualization in pdb
                # All LOC for distance calculation
                all_pdb = self.PDB_format(points_4_distances, ' H', 'A', 1)
                # Reference point's conv hull
                all_pdb = all_pdb + self.PDB_format(self.Hull_Points(conv_hull_reference), ' K', 'B', 300)
                all_pdb = all_pdb + self.PDB_Connect_Edges(self.Hull_Points(conv_hull_reference), 300, 'hull')
                # Hull for shortest distance
                all_pdb = all_pdb + self.PDB_format(self.Hull_Points(conv_hull), ' S', 'E', 2000)
                all_pdb = all_pdb + self.PDB_Connect_Edges(self.Hull_Points(conv_hull), 2000, 'hull')
                # Shortest distances trajectories
                root_start_atom = 3000
                for i in range(len(all_roots)):
                    all_pdb = all_pdb + self.PDB_format(all_roots[i], ' S', 'F', root_start_atom)
                    all_pdb = all_pdb + self.PDB_Connect_Edges(all_roots[i], root_start_atom, 'root')
                    root_start_atom = root_start_atom + len(all_roots[i])
                self.computed_values_export = all_pdb
        else:
            print("not enough LPs for SurfaceDistanceBetweenChannelAnalysis")
        print("SurfaceDistanceBetweenChannelAnalysis ready")


class SurfaceDensityAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(SurfaceDensityAnalysis, self).__init__(*args, **kwargs)
        self.requirements_dimensions_num_list_any = ['3d']

    def compute(self, points):
        print("SurfaceDensityAnalysis")

        hull_channel_nr = self.visible_storm_channel_names.index(self.analysis_surface_density_channel_convex)
        dens_channel_nr = self.visible_storm_channel_names.index(self.analysis_surface_density_channel_density)

        sampl_density = self.analysis_surface_density_density/1000000.0  # Sampling density
        eps = self.analysis_surface_density_treshold  # The density probe radius in nm

        visible_storm_channel_colors = []
        for s in range(len(self.storm_channels_colors)):
            colortuple = [x / 255.0 for x in self.storm_channels_colors[s]]
            visible_storm_channel_colors.append(colortuple)


        if (len(points[hull_channel_nr])>3 and len(points[dens_channel_nr])>0):
            # generating input matrices
            points_4_hull = numpy.empty((len(points[hull_channel_nr]), 3), dtype=numpy.float)
            points_4_hull[:, 0] = numpy.asarray(points[hull_channel_nr])[:, 0]
            points_4_hull[:, 1] = numpy.asarray(points[hull_channel_nr])[:, 1]
            points_4_hull[:, 2] = numpy.asarray(points[hull_channel_nr])[:, 3]
            points_4_hull = points_4_hull.tolist()

            points_4_density = numpy.empty((len(points[dens_channel_nr]), 3), dtype=numpy.float)
            points_4_density[:, 0] = numpy.asarray(points[dens_channel_nr])[:, 0]
            points_4_density[:, 1] = numpy.asarray(points[dens_channel_nr])[:, 1]
            points_4_density[:, 2] = numpy.asarray(points[dens_channel_nr])[:, 3]
            points_4_density = points_4_density.tolist()

            # Big output file header
            self.computed_values_multiple = 'storm_file\tROI_tag\tchannel_IDs(hull,density)\tXRandPoint\tYRandPoint' \
                                            '\tZRandPoint\tsurface_density(NLP/um^2)\n'
            hull = ConvexHull(points_4_hull)
            rand_sampling_point_on_hull = []
            for i in range(len(hull.simplices)):
                trian = numpy.array([hull.points[hull.simplices[i][0]], hull.points[hull.simplices[i][1]],
                                     hull.points[hull.simplices[i][2]]])
                rand_sampling_point_on_hull = rand_sampling_point_on_hull + self.random_points_on_triangle(trian,
                                                                                                           sampl_density)

            density = []
            tree = scipy.spatial.cKDTree(points_4_density)
            for i in range(len(rand_sampling_point_on_hull)):
                volume = 4 / 3 * 3.141592 * eps ** 3
                density.append(float(len(tree.query_ball_point(rand_sampling_point_on_hull[i], eps)) / volume))

            # Generating output
            mean_density = numpy.mean(numpy.asarray(density[:]) * 1000000)
            var_density = scipy.stats.variation(numpy.asarray(density) * 1000000, axis=0)

            self.computed_values_simple.append(
                ['surface_density_parameters[hull_channel,density_channel,sampling_density(NLP/um^2),'
                 'density_probe_radius(nm)]'
                    ,self.visible_storm_channel_names[hull_channel_nr]+ ','+
                 self.visible_storm_channel_names[dens_channel_nr]+','
                 +str(sampl_density*1000000) + ',' + str(eps)])

            self.computed_values_simple.append(['mean_surface_density(NLP/um^2)',
                                                str(mean_density)])

            self.computed_values_simple.append(['CV_surface_density',str(var_density)])

            # Generate big output file
            for c in range(len(density)):
                self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' \
                                                 + self.visible_storm_channel_names[hull_channel_nr] + ',' \
                                                 + self.visible_storm_channel_names[dens_channel_nr] \
                                                 + '\t' + str(rand_sampling_point_on_hull[c][0]) + '\t' \
                                                 + str(rand_sampling_point_on_hull[c][1]) + '\t' \
                                                 + str(rand_sampling_point_on_hull[c][2]) + '\t' + str(
                    density[c] * 1000000) \
                                                 + '\n'

            # Visualization: matplotlib
            rand_sampling_point_on_hull = numpy.array(rand_sampling_point_on_hull)
            points_refer_draw = numpy.copy(numpy.array(points_4_hull))

            fig = plt.figure(facecolor=(0, 0, 0), edgecolor=(0, 0, 0))
            fig.hold(True)
            fig.patch.set_facecolor((0, 0, 0))
            #fig.patch.set_alpha(1)
            axes = fig.add_subplot(111, axisbg='k', projection='3d', aspect='equal')
            axes.grid(False)
            axes.set_axis_off()
            axes.set_frame_on(False)

            axes.set_title('Surface density', color='w')

            ###Hull
            #for simplex in hull.simplices:
                #simplex = numpy.append(simplex, simplex[0])
                #axes.plot(hull.points[simplex, 0], hull.points[simplex, 1], hull.points[simplex, 2],
                          #color=visible_storm_channel_colors[hull_channel_nr],
                          #linestyle='-', markeredgecolor=visible_storm_channel_colors[hull_channel_nr], marker='o',
                          #markerfacecolor=visible_storm_channel_colors[hull_channel_nr], markersize=1)

            #trian = numpy.vstack((trian, trian[0]))
            #♪axes.plot(rand_sampling_point_on_hull[:, 0], rand_sampling_point_on_hull[:, 1],
                      #rand_sampling_point_on_hull[:, 2], linestyle='none', marker='o', markerfacecolor='white',
                      #markersize=3)
            cm = plt.cm.get_cmap('autumn')
            axes.scatter(rand_sampling_point_on_hull[:, 0], rand_sampling_point_on_hull[:, 1],
                      rand_sampling_point_on_hull[:, 2], c=density, marker='o', cmap=cm )
            #axes.plot(trian[:, 0], trian[:, 1], trian[:, 2], linestyle='solid', marker='o', markerfacecolor='gray',
                      #markersize=1)

            if self.display_plots == True:
                axes.elev = -96
                axes.azim = -86
                axes.dist = 5
                #plt.ion()
                plt.show()

            else:
                plt.close("all")
        else:
            print('Not enough LPs for SurfaceDensityAnalysis')
        print('SurfaceDensityAnalysis ready')


class SurfaceDensityDistributionAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(SurfaceDensityDistributionAnalysis, self).__init__(*args, **kwargs)
        self.requirements_channels_num_min = 2
        self.requirements_dimensions_num_list_any = ['3d']

    def compute(self, points):
        print("SurfaceDensityDistributionAnalysis")

        hull_channel_nr = self.visible_storm_channel_names.index(
            self.analysis_surface_density_distribution_channel_convex)
        dens_channel_nr = self.visible_storm_channel_names.index(
            self.analysis_surface_density_distribution_channel_density)
        ref_channel_nr = self.visible_storm_channel_names.index(
            self.analysis_surface_density_distribution_channel_reference)

        sampl_density = self.analysis_surface_density_distribution_density/1000000.0  # Sampling density
        eps = self.analysis_surface_density_distribution_treshold  # The density probe radius in nm




        visible_storm_channel_colors = []
        for s in range(len(self.storm_channels_colors)):
            colortuple = [x / 255.0 for x in self.storm_channels_colors[s]]
            visible_storm_channel_colors.append(colortuple)

        if (len(points[hull_channel_nr])>3 and len(points[dens_channel_nr])>0 and len(points[ref_channel_nr])>3):
            # Big output file header
            self.computed_values_multiple = 'storm_file\tROI_tag\tchannel_IDs(hull,density,reference)\tXRandPoint\tYRandPoint' \
                                            '\tZRandPoint\tXRefPoint\tYRefPoint' \
                                            '\tZRefPoint\tmin_distance(um)\tsurface_density(LP/um^2)\n'

            # #generating input matrices
            points_4_hull = numpy.empty((len(points[hull_channel_nr]), 3), dtype=numpy.float)
            points_4_hull[:, 0] = numpy.asarray(points[hull_channel_nr])[:, 0]
            points_4_hull[:, 1] = numpy.asarray(points[hull_channel_nr])[:, 1]
            points_4_hull[:, 2] = numpy.asarray(points[hull_channel_nr])[:, 3]
            points_4_hull = points_4_hull.tolist()

            points_4_density = numpy.empty((len(points[dens_channel_nr]), 3), dtype=numpy.float)
            points_4_density[:, 0] = numpy.asarray(points[dens_channel_nr])[:, 0]
            points_4_density[:, 1] = numpy.asarray(points[dens_channel_nr])[:, 1]
            points_4_density[:, 2] = numpy.asarray(points[dens_channel_nr])[:, 3]
            points_4_density = points_4_density.tolist()

            points_4_reference = numpy.empty((len(points[ref_channel_nr]), 3), dtype=numpy.float)
            points_4_reference[:, 0] = numpy.asarray(points[ref_channel_nr])[:, 0]
            points_4_reference[:, 1] = numpy.asarray(points[ref_channel_nr])[:, 1]
            points_4_reference[:, 2] = numpy.asarray(points[ref_channel_nr])[:, 3]
            points_4_reference = points_4_reference.tolist()


            hull = ConvexHull(points_4_hull)

            # Generate random points on the hull surface
            rand_sampling_point_on_hull = []
            for i in range(len(hull.simplices)):
                trian = numpy.array([hull.points[hull.simplices[i][0]], hull.points[hull.simplices[i][1]],
                                     hull.points[hull.simplices[i][2]]])
                rand_sampling_point_on_hull = rand_sampling_point_on_hull \
                                              + self.random_points_on_triangle(trian, sampl_density)

            # calculate the surface distance of the density sampling points (rand_sampling_point_on_hull) from the points_4_reference
            hull_reference = ConvexHull(points_4_reference)

            # Calculate the distance from the reference hull
            points_4_distances_dist_from_ref_hull = \
                self.Loc_Distances_from_Hull_Surface_2(numpy.array(rand_sampling_point_on_hull),
                                                       numpy.array(points_4_reference))

            # Project reference points on the points_4_hull's hull
            ref_proj_points_proj_to_hull_surf = \
                self.Loc_Distances_from_Hull_Surface_2(numpy.array([s[3:6] for s in points_4_distances_dist_from_ref_hull]),
                                                       numpy.array(points_4_hull))

            for i in range(len(rand_sampling_point_on_hull)):
                rand_sampling_point_on_hull[i] = rand_sampling_point_on_hull[i] \
                                                 + ref_proj_points_proj_to_hull_surf[i][3:6]

            # Calculation of the shortest route
            all_distances = []
            all_roots = []
            for i in range(len(rand_sampling_point_on_hull)):
                # print i, '/', len(rand_sampling_point_on_hull)
                A = rand_sampling_point_on_hull[i][:3]  #Points on reference hull (random density measure points)
                B = rand_sampling_point_on_hull[i][3:6]  #Points on hull 4 distances (reference hull projection)
                [min_dist_on_hull, min_dist_on_hull_root] = self.shortest_distance_on_hull_surface(hull, A, B)
                all_roots.append(min_dist_on_hull_root)
                all_distances.append(A + B + [min_dist_on_hull])

            #Calculate the density in the sampling points
            tree = scipy.spatial.cKDTree(points_4_density)
            for i in range(len(all_distances)):
                # print i
                volume = 4 / 3 * 3.141592 * eps ** 3
                all_distances[i] = all_distances[i] + [
                    float(len(tree.query_ball_point(rand_sampling_point_on_hull[i][:3], eps)) / volume)]
            #    rand_sampling_point_on_hull[i].append(float(len(tree.query_ball_point(rand_sampling_point_on_hull[i], eps))/volume))

            #Visualization: matplotlib
            hull_4_reference_2 = ConvexHull([s[3:6] for s in ref_proj_points_proj_to_hull_surf])

            rand_sampling_point_on_hull = numpy.array(rand_sampling_point_on_hull)
            points_refer_draw = numpy.copy(numpy.array(points_4_hull))
            points_4_distances_dist_from_ref_hull_draw = numpy.array(points_4_distances_dist_from_ref_hull)
            ref_proj_points_proj_to_hull_surf_draw = numpy.array(ref_proj_points_proj_to_hull_surf)


            # Generating output
            # prune the rows where error occured
            all_distances_pruned = numpy.copy(numpy.asarray(all_distances))
            error_inds = numpy.where(numpy.asarray(all_distances)[:, 6] == 10000000)
            all_distances = numpy.delete(all_distances_pruned, error_inds, 0)

            mean_density = numpy.mean(all_distances_pruned[:, 7] * 1000000.0)
            var_density = scipy.stats.variation(all_distances_pruned[:, 7] * 1000000.0, axis=0)

            self.computed_values_simple.append(
                ['surface_density_distribution_parameters[hull_channel,density_channel,ref_channel,'
                 'sampling_density(NLP/um^2),density_probe_radius(nm))'
                    , self.visible_storm_channel_names[hull_channel_nr]+','
                 +self.visible_storm_channel_names[dens_channel_nr]+','+
                self.visible_storm_channel_names[ref_channel_nr] +','+
                 str(sampl_density) + ',' + str(eps)])

            self.computed_values_simple.append(['mean_surface_density_to_ref(NLP/um^2)',
                                                str(mean_density)])

            self.computed_values_simple.append(['CV_surface_density_to_ref',
                                                str(var_density)])
            # Generate big output file
            for c in range(len(all_distances)):
                if numpy.asarray(all_distances[c][6] == 10000000):
                    self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' \
                                                     + self.visible_storm_channel_names[hull_channel_nr] + ',' \
                                                     + self.visible_storm_channel_names[dens_channel_nr] + ',' \
                                                     + self.visible_storm_channel_names[ref_channel_nr] \
                                                     + '\t' + str(numpy.asarray(all_distances)[c][0]) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][1])) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][2])) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][3])) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][4])) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][5])) + '\t' \
                                                     + 'error' + '\t' \
                                                     + 'error' + '\t' \
                                                     + '\n'
                else:
                    self.computed_values_multiple += self.storm_file_name + '\t' + self.ROI_tag + '\t' \
                                                     + self.visible_storm_channel_names[hull_channel_nr] + ',' \
                                                     + self.visible_storm_channel_names[dens_channel_nr] + ',' \
                                                     + self.visible_storm_channel_names[ref_channel_nr] \
                                                     + '\t' + str(numpy.asarray(all_distances)[c][0]) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][1])) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][2])) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][3])) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][4])) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][5])) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][6]) / 1000.0) + '\t' \
                                                     + str(numpy.asarray(all_distances[c][7]) * 1000000.0) + '\t' \
                                                     + '\n'


            #visualization in matplotlib

            fig = plt.figure(facecolor=(0, 0, 0), edgecolor=(0, 0, 0))
            fig.hold(True)
            fig.patch.set_facecolor((0, 0, 0))
            #fig.patch.set_alpha(1)
            axes = fig.add_subplot(111, axisbg='k', projection='3d', aspect='equal')
            axes.grid(False)
            axes.set_axis_off()
            axes.set_frame_on(False)

            axes.set_title('Surface density distribution to reference', color='w')


            # Hull
            for simplex in hull.simplices:
                simplex = numpy.append(simplex, simplex[0])
                axes.plot(hull.points[simplex, 0], hull.points[simplex, 1], hull.points[simplex, 2],
                          color=visible_storm_channel_colors[hull_channel_nr], linestyle='-', linewidth='2',
                          markeredgecolor=visible_storm_channel_colors[hull_channel_nr], marker='o',
                          markerfacecolor='red', markersize=3)
            # Reference hull
            for simplex in hull_reference.simplices:
                simplex = numpy.append(simplex, simplex[0])
                axes.plot(hull_reference.points[simplex, 0], hull_reference.points[simplex, 1],
                          hull_reference.points[simplex, 2], color=visible_storm_channel_colors[ref_channel_nr],
                          linestyle='-', linewidth='2', markeredgecolor=visible_storm_channel_colors[ref_channel_nr],
                          marker='o', markerfacecolor=visible_storm_channel_colors[ref_channel_nr], markersize=3)
            # Reference hull on hull 4 hull
            #for simplex in hull_4_reference_2.simplices:
            #    simplex = np.append(simplex, simplex[0])
            #    plt.plot(hull_4_reference_2.points[simplex,0], hull_4_reference_2.points[simplex,1],hull_4_reference_2.points[simplex,2],color='blue', linestyle='-', markeredgecolor='green', marker='o', markerfacecolor='green', markersize=3)

            # Shortest routes on surface
            for i in range(len(all_roots)):
                min_root_draw = numpy.copy(numpy.array(all_roots[i]))
                axes.plot(min_root_draw[:, 0], min_root_draw[:, 1], min_root_draw[:, 2], color='gray', linestyle='-',
                          linewidth='1', marker='o', markerfacecolor='gray', markersize=2)

            #trian = np.vstack((trian,trian[0]))
            axes.plot(rand_sampling_point_on_hull[:, 0], rand_sampling_point_on_hull[:, 1],
                      rand_sampling_point_on_hull[:, 2], linestyle='none', marker='o', markerfacecolor='white',
                      markersize=2)
            axes.plot(points_4_distances_dist_from_ref_hull_draw[:, 3],
                      points_4_distances_dist_from_ref_hull_draw[:, 4],
                      points_4_distances_dist_from_ref_hull_draw[:, 5], linestyle='none', marker='^',
                      markerfacecolor='white', markersize=2)
            #plt.plot(ref_proj_points_proj_to_hull_surf_draw[:,3], ref_proj_points_proj_to_hull_surf_draw[:,4], ref_proj_points_proj_to_hull_surf_draw[:,5], linestyle='none', marker='^', markerfacecolor='black', markersize=5)

            #plt.plot(trian[:,0], trian[:,1], trian[:,2], linestyle='solid', marker='o', markerfacecolor='red', markersize=9)

            if self.display_plots == True:
                axes.elev = -96
                axes.azim = -86
                axes.dist = 5
                #plt.ion()
                plt.show()

            else:
                plt.close("all")
        else:
            print("Not enough LPs for SurfaceDensityDistributionAnalysis")
        print("SurfaceDensityDistributionAnalysis ready")


class ExportCoordinatesTxtAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(ExportCoordinatesTxtAnalysis, self).__init__(*args, **kwargs)
        self.computed_values_multiple = None


    def compute(self, points):
        print("ExportCoordinatesTxtAnalysis")

        infilename = self.storm_file_path
        outfilename = os.path.join(
            self.working_directory,
            self.storm_file_name + '_' + self.ROI_tag + '_RoiCoords.txt' )

        f_in = open(infilename, 'r')
        f_out = open(outfilename, 'w')
        header = f_in.readline()
        f_in.close()
        f_out.write(header)

        # StormChannelVisible
        channel_nr= numpy.where(numpy.asarray(self.storm_channels_visible) == True)
        visible_channel_nr=numpy.asarray(channel_nr)[0]

        for k in visible_channel_nr:
            f_in = open(infilename, 'r')
            if len(points[k])>0:
                linestoexport = numpy.empty((len(points[k]), 1), dtype=numpy.int)
                linestoexport = numpy.asarray(points[k])[:, 6]
                #print linestoexport
                n = 0
                m = 0
                for line in f_in:
                    if linestoexport[m] == n:
                        f_out.write(line)
                        m += 1
                        if m >= len(linestoexport):
                            break
                    n += 1
                f_in.close()
            else:
                print("empty channel")
        f_out.close()
        #print 'ROI Coordinate export ready'

        # exporting ROI attributes
        ConfocalSizeMultiplier=self.StormDisplay.ConfocalSizeMultiplier


        offset=[self.confocal_offset[1]/ConfocalSizeMultiplier, self.confocal_offset[0]/ConfocalSizeMultiplier]
        # print ConfocalSizeMultiplier



        if self.ROI:
            roifilename = os.path.join(
                self.working_directory,
                self.storm_file_name + '_' + self.ROI_tag + '_RoiAttr.txt' )
            f_roi = open(roifilename, 'w')
            #f_roi.write('confocal offset (nm)\n'+str(self.confocal_offset[1])+'\t'+str(self.confocal_offset[0])+'\n')

            if self.confocal_image!=[]:
                f_roi.write('confocal offset (nm)\n'+str(offset[0]*1000.0*self.StormDisplay.ConfocalMetaData['SizeX'])+
                            '\t'+str(offset[1]*1000.0*self.StormDisplay.ConfocalMetaData['SizeX'])+'\n')
            else:
                f_roi.write('confocal offset (nm)\n'+str(0)+
                            '\t'+str(0)+'\n')


            f_roi.write('ROI type'+'\n')
            if type(self.ROI).__name__ == 'CircleRoi':
                f_roi.write('CircleROI'+'\n')

                if self.confocal_image!=[]:
                    [Intensities,NumPixels]=self.StormDisplay.getPixelIntensityInRoi(self.ROI.roi,'Circle', offset)

                    f_roi.write('ROI confocal pixel number'+'\n')
                    f_roi.write(str(NumPixels)+'\n')
                    f_roi.write('ROI sum of confocal intensity per channel'+'\n')
                    for intensity in Intensities:
                        f_roi.write(str(intensity)+'\t')
                    f_roi.write('\n')
                    f_roi.write('confocal file name\n'+self.confocal_file_name+'\n')

                f_roi.write('ROI X, Y coordinates (nm)'+'\n')

                roi=self.ROI.roi.mapToParent(self.ROI.roi.shape())
                element_nr=roi.elementCount()
                for k in range(element_nr):
                    f_roi.write(str(roi.elementAt(k).x)+'\t'+str(roi.elementAt(k).y)+'\n')

            if type(self.ROI).__name__ == 'EllipseRoi':
                f_roi.write('EllipseROI'+'\n')
                if self.confocal_image!=[]:
                    [Intensities,NumPixels]=self.StormDisplay.getPixelIntensityInRoi(self.ROI.roi,'Ellipse', offset)
                    f_roi.write('ROI confocal pixel number'+'\n')
                    f_roi.write(str(NumPixels)+'\n')
                    f_roi.write('ROI sum of confocal intensity per channel'+'\n')
                    for intensity in Intensities:
                        f_roi.write(str(intensity)+'\t')
                    f_roi.write('\n')
                    f_roi.write('confocal file name\n'+self.confocal_file_name+'\n')
                f_roi.write('ROI X, Y coordinates (nm)'+'\n')

                roi=self.ROI.roi.mapToParent(self.ROI.roi.shape())
                element_nr=roi.elementCount()
                for k in range(element_nr):
                    f_roi.write(str(roi.elementAt(k).x)+'\t'+str(roi.elementAt(k).y)+'\n')


            if type(self.ROI).__name__ == 'FreehandRoi':
                f_roi.write('FreehandROI'+'\n')
                if self.confocal_image!=[]:
                    [Intensities,NumPixels]=self.StormDisplay.getPixelIntensityInRoi(self.ROI.roi,'Freehand', offset)
                    f_roi.write('ROI confocal pixel number'+'\n')
                    f_roi.write(str(NumPixels)+'\n')
                    f_roi.write('ROI sum of confocal intensity per channel'+'\n')
                    for intensity in Intensities:
                        f_roi.write(str(intensity)+'\t')
                    f_roi.write('\n')
                    f_roi.write('confocal file name\n'+self.confocal_file_name+'\n')
                f_roi.write('ROI X, Y coordinates (nm)'+'\n')

                roi=self.ROI.roi.shape()
                element_nr=roi.elementCount()
                for k in range(element_nr):
                    f_roi.write(str(roi.elementAt(k).x)+'\t'+str(roi.elementAt(k).y)+'\n')


            if type(self.ROI).__name__ == 'ActiveContourRoi':
                f_roi.write('ActiveContourROI'+'\n')
                if self.confocal_image!=[]:
                    [Intensities,NumPixels]=self.StormDisplay.getPixelIntensityInRoi(self.ROI.roi,'Activecontour', offset)
                    f_roi.write('ROI confocal pixel number'+'\n')
                    f_roi.write(str(NumPixels)+'\n')
                    f_roi.write('ROI sum of confocal intensity per channel'+'\n')
                    for intensity in Intensities:
                        f_roi.write(str(intensity)+'\t')
                    f_roi.write('\n')
                    f_roi.write('confocal file name\n'+self.confocal_file_name+'\n')
                f_roi.write('ROI X, Y coordinates (nm)'+'\n')

                PolygonItem = self.ROI.roi[0]
                roi=PolygonItem.shape()
                element_nr=roi.elementCount()
                for k in range(element_nr):
                    f_roi.write(str(roi.elementAt(k).x)+'\t'+str(roi.elementAt(k).y)+'\n')

            f_roi.close()
        print('ExportCoordinatesTxtAnalysis ready')



class ExportCoordinatesPdbAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(ExportCoordinatesPdbAnalysis, self).__init__(*args, **kwargs)
        self.computed_values_multiple = None
        self.computed_values_export = []
        self.analysis_export_pdb_export_pdb = True # small hack to emulate checked export pdb checkbox
        self.output_file_export_extension = 'pdb'

    def compute(self, points):

        print("ExportCoordinatesPdbAnalysis")

        channel_nr= numpy.where(numpy.asarray(self.storm_channels_visible) == True)
        visible_channel_nr=numpy.asarray(channel_nr)[0]

        for k in visible_channel_nr:
            if len(points[k])>0:
                coord = numpy.empty((len(points[k]), 3), dtype=numpy.float)
                coord[:, 0] = numpy.asarray(points[k])[:, 0]
                coord[:, 1] = numpy.asarray(points[k])[:, 1]
                coord[:, 2] = numpy.asarray(points[k])[:, 3]
                ##Visualization in pdb

                if k == 0:
                    self.computed_values_export += self.PDB_format(coord, ' H', 'A', 1)
                elif k == 1:
                    self.computed_values_export += self.PDB_format(coord, ' C', 'A', 1)
                elif k == 2:
                    self.computed_values_export += self.PDB_format(coord, ' N', 'A', 1)
                else:
                    self.computed_values_export += self.PDB_format(coord, ' O', 'A', 1)
            else:
                print("empty channel")
        print("ExportCoordinatesPdbAnalysis ready")


class ExportCoordinatesVmdAnalysis(Analysis):
    def __init__(self, *args, **kwargs):
        super(ExportCoordinatesVmdAnalysis, self).__init__(*args, **kwargs)
        self.computed_values_multiple = None
        self.output_file_export_extension = 'vmd'

    def compute(self, points):
        pass





# in case of adding new analysis function:
# class NewAnalysis(Analysis):
#     def __init__(self, *args, **kwargs):
#         super(NewAnalysis, self).__init__(*args, **kwargs)
#         self.computed_values_multiple = None
#
#     def compute(self, points):
#         print 'New_analysis'
# GUI elements: checkable analysis groupbox named groupBox_analysis_new,
# an example spinbox named spinBox_analysis_new_example
# an export checkbox named checkBox_analysis_new_save_all

#         print self.analysis_new_example # value of a spinbox named spinBox_analysis_new_example
#
#         self.computed_values_simple.append(['new_result_name','new_result_value']) # export results to common file
#         self.computed_values_multiple='new_result_name_1'+ '\t' +'new_result_name_2'+ '\n' # separate results file
# heading
#
#         self.computed_values_multiple +='new_result_value_1'+ '\t' +'new_result_value_2'+ '\n' # separate results
# file values
