# -*- coding: utf-8 -*-
import configparser
import os


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.press_i = []
        self.press_o = []
        self.ifiles = 0
        self.method = 0
        self.plane = 0
        
        # directories
        self.main_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(self.main_dir, '../resources')
        self.results = os.path.join(self.main_dir, '../results')
        self.configpath = os.path.join(self.resources_dir, "config.txt")
        self.dpresspath = os.path.join(self.resources_dir, "dp_config.txt")

        # reading config file         
        self.config.read(self.configpath)
        
        
    def get_mesh_info(self, mesh_name):
        if mesh_name not in self.config:
            return "Mesh not found in the config file."
        
        grids_file = self.config[mesh_name]['grids']
        connectivities_file = self.config[mesh_name]['elements']
        mesh_type = self.config[mesh_name]['mesh_type']
        press_type = self.config[mesh_name]['press_type']

        return grids_file, connectivities_file, mesh_type, press_type
    
    
    
    def get_press_file_info(self):
        
        with open(self.dpresspath, 'r') as file:
            line = file.readline()
            temp = line.split()
            self.ifiles = int(temp[0])
            
            line = file.readline()
            temp = line.split()
            self.method = int(temp[0])      
            
            line = file.readline()
            temp = line.split()
            self.plane = int(temp[0])              
            
            for i in range(self.ifiles):
                line = file.readline()
                temp = line.split()
                self.press_i.append(temp[0])
                self.press_o.append(temp[1])