# -*- coding: utf-8 -*-
import os
import numpy as np


class Surface:
    def __init__(self, mesh_type):
        
        # data
        self.grids = None
        self.ids = None
        self.connectivity = None
        self.centers = None
        self.ngrids = 0
        self.nelements = 0
        self.area = None
        self.mesh_type = int(mesh_type)
        self.press = None
        
        # directories
        self.main_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(self.main_dir, '../resources')
        self.results_dir = os.path.join(self.main_dir, '../results')         

        
    def read_grids(self, filename):
        
        filepath = os.path.join(self.resources_dir, filename)
        
        with open(filepath, 'r') as file:
            line = file.readline()
            temp = line.split()
            self.ngrids = int(temp[0])                  # Number of grids
            print("Grids: {}".format(self.ngrids))
            self.grids = np.empty((self.ngrids, 3))
            self.ids = np.empty(self.ngrids)
            
            for i in range(self.ngrids):
                line = file.readline()
                temp = line.split()
                self.ids[i] = int(temp[0])              # Reading grid id   
                self.grids[i, 0] = float(temp[1])       # Reading grid x coordinate  
                self.grids[i, 1] = float(temp[2])       # Reading grid y coordinate 
                self.grids[i, 2] = float(temp[3])       # Reading grid z coordinate 
                
                
                
    def read_elements(self, filename):
        
        filepath = os.path.join(self.resources_dir, filename)
        
        with open(filepath, 'r') as file:
            line = file.readline()
            temp = line.split()
            self.nelements = int(temp[0])                  # Number of elements
            print("Elements: {}".format(self.nelements))
            self.connectivity = np.empty((self.nelements, self.mesh_type))
            self.centers = np.empty((self.nelements, 3))
            self.area = np.empty((self.nelements, 3))

            for i in range(self.nelements):
                line = file.readline()
                temp = line.split()
                for j in range(self.mesh_type):
                    self.connectivity[i, j] = int(temp[j])       # Reading connectivity
                    
        self.calc_panel_centers()
                    
                    
    def read_press(self, filename, ptype):
        
        filepath = os.path.join(self.resources_dir, filename)
        
        with open(filepath, 'r') as file:
            if (int(ptype) == 0):  # press on grids
                self.press = np.empty(self.ngrids)
                for i in range(self.ngrids):
                        line = file.readline()
                        temp = line.split()
                        self.press[i] = float(temp[1])
                        
            elif (int(ptype) == 1):  # press on element centers
                self.press = np.empty(self.nelements)
                for i in range(self.nelements):
                        line = file.readline()
                        temp = line.split()
                        self.press[i] = float(temp[1])
            


    def calc_panel_centers(self):
        
        for i in range(self.nelements):
            if (self.mesh_type == 3):
                self.centers[i, 0] = (self.grids[int(self.connectivity[i, 0]) - 1, 0] + self.grids[int(self.connectivity[i, 1]) - 1, 0] + self.grids[int(self.connectivity[i, 2]) - 1, 0]) / 3
                self.centers[i, 1] = (self.grids[int(self.connectivity[i, 0]) - 1, 1] + self.grids[int(self.connectivity[i, 1]) - 1, 1] + self.grids[int(self.connectivity[i, 2]) - 1, 1]) / 3
                self.centers[i, 2] = (self.grids[int(self.connectivity[i, 0]) - 1, 2] + self.grids[int(self.connectivity[i, 1]) - 1, 2] + self.grids[int(self.connectivity[i, 2]) - 1, 2]) / 3
            elif (self.mesh_type == 4):
                self.centers[i, 0] = 0.25 * (self.grids[int(self.connectivity[i, 0]) - 1, 0] + self.grids[int(self.connectivity[i, 1]) - 1, 0] + self.grids[int(self.connectivity[i, 2]) - 1, 0] + self.grids[int(self.connectivity[i, 3]) - 1, 0])
                self.centers[i, 1] = 0.25 * (self.grids[int(self.connectivity[i, 0]) - 1, 1] + self.grids[int(self.connectivity[i, 1]) - 1, 1] + self.grids[int(self.connectivity[i, 2]) - 1, 1] + self.grids[int(self.connectivity[i, 3]) - 1, 1])
                self.centers[i, 2] = 0.25 * (self.grids[int(self.connectivity[i, 0]) - 1, 2] + self.grids[int(self.connectivity[i, 1]) - 1, 2] + self.grids[int(self.connectivity[i, 2]) - 1, 2] + self.grids[int(self.connectivity[i, 3]) - 1, 2])
    


    
    def calc_area(self):
         
        for i in range(self.nelements):
            if (self.mesh_type == 3):
                points = tuple(self.grids[[int(self.connectivity[i, 0]) - 1, int(self.connectivity[i, 1]) - 1, int(self.connectivity[i, 2]) - 1], 0:2])
                self.area[i, 0:2] = self.calculate_triangle_area_3d(points)
            elif (self.mesh_type == 4):
                points = tuple(self.grids[[int(self.connectivity[i, 0]) - 1, int(self.connectivity[i, 1]) - 1, int(self.connectivity[i, 2]) - 1, int(self.connectivity[i, 3]) - 1], 0:2])
                self.area[i, 0:2] = self.calculate_quadrilateral_area_3d(points)
                
                
                
                
    def calculate_triangle_area_3d(self, points):
        A, B, C = points
        AB = np.array(B) - np.array(A)
        AC = np.array(C) - np.array(A)  

        area_vector = 0.5 * np.cross(AB, AC)
        
        return area_vector
        


    def calculate_quadrilateral_area_3d(self, points):
        A, B, C, D = points
        AC = np.array(C) - np.array(A)
        BD = np.array(D) - np.array(B)  

        area_vector = 0.5 * np.cross(AC, BD)       
        
        return area_vector
    
    
    
    def write_press_grids(self, fout):
        
        filepath = os.path.join(self.results_dir, fout)
        filepath_vtk = filepath.replace(".txt", ".vtk")
        
        with open(filepath, 'w') as file: 
            for i in range(self.ngrids):
                file.write("{:12.6f}\n".format(self.press[i]))
                
                
        with open(filepath_vtk, 'w') as file:
            
            file.write("# vtk DataFile Version 3.0\n")
            file.write("vtk output\n")
            file.write("ASCII\n")
            file.write("DATASET UNSTRUCTURED_GRID\n\n")
            file.write("POINTS {:8d} float\n".format(self.ngrids))
            
            for i in range(int(self.ngrids)):
                file.write("{:12.6f} {:12.6f} {:12.6f}\n".format(self.grids[i, 0], self.grids[i, 1], self.grids[i, 2]))
                
            file.write("\n")
            file.write("CELLS {:8d} {:8d}\n".format(self.nelements, self.nelements * (int(self.mesh_type + 1))))
            
            for i in range(self.nelements):
                if (int(self.mesh_type) == 3):
                    file.write("{:8d} {:8d} {:8d} {:8d}\n".format(int(self.mesh_type), self.elements[i, 0], self.elements[i, 1], self.elements[i, 2] ))
                elif (int(self.mesh_type) == 4):
                    file.write("{:8d} {:8d} {:8d} {:8d} {:8d}\n".format(int(self.mesh_type), int(self.connectivity[i, 0]), int(self.connectivity[i, 1]), int(self.connectivity[i, 2]), int(self.connectivity[i, 3])))
                    
            file.write("\n")
            file.write("CELL_TYPES {:8d}\n".format(self.nelements))
            
            for i in range(self.nelements):
                file.write("9\n")

            file.write("\n")
            
            file.write("POINT_DATA {:8d}\n".format(self.ngrids))
            file.write("SCALARS dcp float\n")
            file.write("LOOKUP_TABLE default\n")
            file.write("\n")
            for i in range(self.ngrids):
                file.write("{:12.6f} \n".format(self.press[i]))
            
    def write_press_elements(self, fout):
        
        filepath = os.path.join(self.results_dir, fout)
        
        
        with open(filepath, 'w') as file: 
            for i in range(self.nelements):
                file.write("{:12.6f}\n".format(self.press[i])) 