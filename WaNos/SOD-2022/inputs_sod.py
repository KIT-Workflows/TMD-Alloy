import yaml, os, shutil, subprocess
from ase import Atoms
import tarfile, zipfile
from ase import io


if __name__ == '__main__':
    
    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)

    #if wano_file["Load INSOD file"]:
    indod = wano_file["INSOD-input"]["INSOD file"]
    
    #if wano_file["Load SGO file"]:
    in_sgo = wano_file["SGO-input"]["SGO file"]
    
    os.system('sod_comb.sh')

    
    fname = "sod-master.zip"

    
    with open('INSOD1', 'w') as f:
        f.write("#Title \n")
        f.write("Ca-doped MgO \n")
        f.write("\n")

        f.write("# a,b,c,alpha,beta,gamma \n")
        f.write("4.22  4.22  4.22  90.000  90.000  90.000 \n")
        f.write("\n")

        f.write("# nsp: Number of species\n")
        f.write("2\n")
        f.write("\n")

        f.write("# symbol(1:nsp): Atom symbols\n")
        f.write("Mg O \n")
        f.write("\n")
        
        f.write("# natsp0(1:nsp): Number of atoms for each species in the assymetric unit \n")
        f.write("1 1\n")
        f.write("\n")
        
        f.write("# coords0(1:nat0,1:3): Coordinates of each atom (one line per atom) \n")
        f.write("0.0  0.0  0.0 \n")
        f.write("0.5  0.5  0.5 \n")
        f.write("\n")

        f.write("# na,nb,nc (supercell definition) \n")
        f.write("2 2 2 \n")
        f.write("\n")

        f.write("# sptarget: Species to be substituted \n")
        f.write("Ca Mg\n")
        f.write("\n")

        f.write("# FILER, MAPPER\n")
        f.write("# # FILER:   0 (no calc files generated), 1 (GULP), 2 (METADISE), 11 (VASP) \n")
        f.write("# # MAPPER:  0 (no mapping, use currect structure), >0 (map to structure in MAPTO file) \n")
        f.write("# # (each position in old structure is mapped to MAPPER positions in new structure) \n")
        f.write("11 0 \n")
        
        f.write("\n")
        f.write("# This section is not read if VASP files are being created \n")
        f.write("# If FILER=1 then: \n")
        f.write("# ishell(1:nsp) 0 core only / 1 core and shell (for the species listed in symbol(1:nsp)) \n")
        f.write("0 1 \n")
        f.write("# newshell(1:2) 0 core only / 1 core and shell (for the species listed in newsymbol(1:2)) \n")
        f.write("0 0 \n")    


    fname = "sod-master.zip"

    if fname.endswith("tar.gz"):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall()
        tar.close()
    elif fname.endswith("zip"):
        with zipfile.ZipFile(fname,"r") as zip_ref:
            zip_ref.extractall()
    elif fname.endswith("tar"):
        tar = tarfile.open(fname, "r:")
        tar.extractall()
        tar.close()

    temp_dir = "bin/"
    current_folder = os.getcwd()
    os.chdir("sod-master/")
    cmd = "make all"
    os.system(cmd)

    os.chdir(temp_dir)
    bin_path = os.getcwd()
    cmd = "chmod +x *.sh"
    os.system(cmd)
    os.chdir(current_folder)

    cmd = "export PATH=$PATH:" + bin_path
    file_exp = "exp.sh"
    with open(file_exp, 'w') as f:
        f.write(cmd)

    cmd = "chmod +x *.sh"
    os.system("source " + file_exp)
    os.system(cmd)
    os.system('sod_comb.sh')
    
    