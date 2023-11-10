from surface import Surface
from config import Config
from idw_interpolation import IDWInterpolator
from kriging import kriging

config = Config()  

# Origin mesh data

origin_data = config.get_mesh_info("origin")

if origin_data != "Mesh not found in the config file.":
    grids_file, elements_file, mesh_type, origin_press_type = origin_data
    print(f"Origin: Grids file: {grids_file}, Elements file: {elements_file}, Mesh type: {mesh_type}, Press type: {origin_press_type}")

origin= Surface(int(mesh_type))
origin.read_grids(grids_file)
origin.read_elements(elements_file)
origin.calc_area()


# Target mesh data

target_data = config.get_mesh_info("target")

if target_data != "Mesh not found in the config file.":
    grids_file, elements_file, mesh_type, target_press_type = target_data
    print(f"Target: Grids file: {grids_file}, Elements file: {elements_file}, Mesh type: {mesh_type}, Press type: {target_press_type}")

target = Surface(int(mesh_type))
target.read_grids(grids_file)
target.read_elements(elements_file)
target.allocate_press(target.ngrids)
target.calc_area()

# Pressure files
config.get_press_file_info()


# Mapping


for i in range(config.ifiles):
    origin.read_press(config.press_i[i], origin_press_type)
    
    if (int(config.plane) == 0):     # Plane xy
        c1 = 0
        c2 = 1
    elif (int(config.plane) == 1):   # Plane xz
        c1 = 0
        c2 = 2
    
    if (int(config.method) == 0):
        if (int(origin_press_type) == 0):     # Pressure on grids 
            if (int(target_press_type) == 0):     # Pressure on grids
                temp = kriging(origin.grids[:, int(c1)], origin.grids[:, int(c2)], origin.press[:], target.grids[:, int(c1)], target.grids[:, int(c2)])
                for i1 in range(len(temp)):
                    target.press[i1] = float(temp[i1])
                target.write_press_grids(config.press_o[i])
            
            if (int(target_press_type) == 1):     # Pressure on element centers
                temp = kriging(origin.grids[:, int(c1)], origin.grids[:, int(c2)], origin.press[:], target.centers[:, int(c1)], target.center[:, int(c2)])
                for i1 in range(len(temp)):
                    target.press[i1] = float(temp[i1])
                target.write_press_elements(config.press_o[i])
        elif (int(origin_press_type) == 1):     # Pressure on element centers
            if (int(target_press_type) == 0):     # Pressure on grids
                temp = kriging(origin.centers[:, int(c1)], origin.centers[:, int(c2)], origin.press[:], target.grids[:, int(c1)], target.grids[:, int(c2)])
                print(temp)
                for i1 in range(len(temp)):
                    target.press[i1] = float(temp[i1])
                target.write_press_grids(config.press_o[i])
            
            if (int(target_press_type) == 1):     # Pressure on element centers
                temp = kriging(origin.centers[:, int(c1)], origin.centers[:, int(c2)], origin.press[:], target.centers[:, int(c1)], target.center[:, int(c2)])
                for i1 in range(len(temp)):
                    target.press[i1] = float(temp[i1])                
                target.write_press_elements(config.press_o[i])        
    elif (int(config.method) == 1):
        
        if (int(origin_press_type) == 0):     # Pressure on grids
            origin_idw = IDWInterpolator(origin.ngrids, 4, 10)
            origin_idw.set_mesh(origin.grids[:, int(c1)], origin.grids[:, int(c2)], origin.press[:])
            origin.write_press_grids(config.press_i[i])
            
        if (int(origin_press_type) == 1):     # Pressure on element centers
            origin_idw = IDWInterpolator(origin.nelements, 4, 10)
            origin_idw.set_mesh(origin.centers[:, int(c1)], origin.centers[:, int(c2)], origin.press[:])
            origin.write_press_elements(config.press_i[i])
            
        if (int(target_press_type) == 0):     # Pressure on grids
            target.press = origin_idw.eval_mesh(target.grids, int(config.plane), target.ngrids)
            target.write_press_grids(config.press_o[i])
        
        if (int(target_press_type) == 1):     # Pressure on element centers
            target.press = origin_idw.eval_mesh(target.centers, int(config.plane), target.nelements)
            target.write_press_elements(config.press_o[i])
    
    i_intmesh_out = config.press_i[i].replace(".txt", "_int.txt")
    origin.intmesh(i_intmesh_out)
    o_intmesh_out = config.press_o[i].replace(".txt", "_int.txt")
    target.intmesh(o_intmesh_out)
