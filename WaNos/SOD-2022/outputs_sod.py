import yaml, os, shutil
from ase import Atoms
import tarfile, zipfile
from ase import io


def tar_folder(out_dir_name, source_dir):
    sourcefiles = os.listdir(source_dir)
    files_names = []

    for file in sourcefiles:
        if file.endswith('.vasp'):
            files_names.append(file)
            file = source_dir + file
            shutil.copy2(file, '.')


    with tarfile.open(out_dir_name, "w") as tar:
        for name in files_names:
            tar.add(name)
            os.remove(name)    

if __name__ == '__main__':
    
    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)

    source_dir = "CALCS/"
    out_dir = "calcs.tar"
    tar_folder(out_dir, source_dir) 

 
    sod_dict = {}
    
    with open("OUTSOD") as file_in:
        Lines = file_in.readlines()
        sod_dict["substitutions"] = Lines[0].strip('\n')
        sod_dict["configurations"] = Lines[1].strip('\n')
        for line in Lines:
            items = line.split()
            key, values = items[0], items[1:]
            sod_dict[int(key)] = values 

    with open("outsod_results.yml",'w') as out:
        yaml.dump(sod_dict, out,default_flow_style=False)