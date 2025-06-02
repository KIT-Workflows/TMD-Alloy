import os
import shutil
import tarfile
import zipfile
import numpy as np
import yaml


def get_relative_file_paths(folder):
    """
    Returns a list of relative file paths under the given folder.
    """
    relative_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            absolute_path = os.path.join(root, file)
            relative_path = os.path.relpath(absolute_path, folder)
            relative_paths.append(relative_path)
    return relative_paths


def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    """
    Safely extracts tar files, preventing path traversal attacks.
    """
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        abs_member_path = os.path.abspath(member_path)
        abs_extract_path = os.path.abspath(path)
        if not abs_member_path.startswith(abs_extract_path):
            raise Exception("Attempted Path Traversal in Tar File")
    tar.extractall(path, members=members, numeric_owner=numeric_owner)


def extract_archive(archive_file, extract_to):
    """
    Extracts tar or zip archives to the specified directory.
    """
    try:
        if tarfile.is_tarfile(archive_file):
            with tarfile.open(archive_file) as tar:
                safe_extract(tar, path=extract_to)
        elif zipfile.is_zipfile(archive_file):
            with zipfile.ZipFile(archive_file, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        else:
            print("The file you entered is not a recognized archive format (tar or zip).")
    except (tarfile.TarError, zipfile.BadZipFile) as e:
        print(f"Error extracting archive {archive_file}: {e}")


def archive_directory(path, archive_name):
    """
    Archives the specified directory into a tar or zip file.
    """
    if archive_name.endswith(('.tar.gz', '.tar.xz', '.tar')):
        with tarfile.open(archive_name, "w:gz") as tar_handle:
            # Add the directory itself to the archive
            tar_handle.add(path, arcname=os.path.basename(path))
    elif archive_name.endswith('.zip'):
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Include empty directories
            for root, dirs, files in os.walk(path):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    zipf.write(dir_path, os.path.relpath(dir_path, os.path.join(path, '..')))
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, os.path.join(path, '..')))
    else:
        print("Unsupported archive format. Please use .tar, .tar.gz, .tar.xz, or .zip")


def process_float_variables(wano_file):
    """
    Processes float variables based on the wano_file configuration.
    Generates float_output_dict.yml and copies it to output_dict.yml.
    """
    try:
        varF_begin = wano_file['VarF-begin']
        varF_end = wano_file['VarF-end']
        n_points = wano_file['N-points']
    except KeyError as e:
        print(f"Missing required key in wano_file for float variables: {e}")
        return
    temp_var = np.linspace(varF_begin, varF_end, n_points)
    float_outdict = {'iter': [float(i) for i in temp_var]}
    print(float_outdict)
    with open('float_output_dict.yml', 'w') as out:
        yaml.dump(float_outdict, out, default_flow_style=False)
    shutil.copy2('float_output_dict.yml', 'output_dict.yml')


def process_int_variables(wano_file):
    """
    Processes integer variables based on the wano_file configuration.
    Generates int_output_dict.yml and copies it to output_dict.yml.
    """
    try:
        varI_begin = wano_file['VarF-begin']
        varI_end = wano_file['VarF-end']
        step_var = wano_file['Step']
    except KeyError as e:
        print(f"Missing required key in wano_file for integer variables: {e}")
        return
    temp_var = np.arange(varI_begin, varI_end, step_var)
    int_outdict = {'iter': [int(i) for i in temp_var]}
    with open('int_output_dict.yml', 'w') as out:
        yaml.dump(int_outdict, out, default_flow_style=False)
    shutil.copy2('int_output_dict.yml', 'output_dict.yml')


def process_structures(wano_file):
    """
    Processes structures based on the wano_file configuration.
    Extracts structures from archives if available and writes the structure output dictionaries.
    If no structures are provided, creates an empty 'Structures' directory and archives it.
    """
    if wano_file.get('Structures'):
        if os.path.isdir('Structures'):
            shutil.rmtree('Structures')

        # Check for archive files
        archive_found = False
        archive_name = ''
        for fname in ['Structures.tar', 'Structures.tar.gz', 'Structures.tar.xz', 'Structures.zip']:
            if os.path.isfile(fname):
                archive_name = fname
                archive_found = True
                break

        if archive_found:
            extract_archive(archive_name, 'Structures')
        else:
            print("No archive file found (Structures.tar, Structures.tar.gz, Structures.tar.xz, Structures.zip)")

        folder = os.path.join(os.getcwd(), 'Structures')
        my_list = get_relative_file_paths(folder)
        structure_outdict = {'iter': my_list, 'struct_len': len(my_list)}

        with open('structure_output_dict.yml', 'w') as out:
            yaml.dump(structure_outdict, out, default_flow_style=False)
        with open('output_dict.yml', 'w') as out:
            yaml.dump(structure_outdict, out, default_flow_style=False)
    else:
        print("Structure directory does not exist. Creating an empty directory.")
        if not os.path.isdir('Structures'):
            os.mkdir('Structures')

        # Choose archive format (tar or zip)
        archive_name = 'Structures.tar'  # You can change this to 'Structures.zip' if needed
        archive_directory('./Structures', archive_name)
        shutil.rmtree('Structures')
        structure_outdict = {'iter': []}
        with open('structure_output_dict.yml', 'w') as out:
            yaml.dump(structure_outdict, out, default_flow_style=False)
        with open('output_dict.yml', 'w') as out:
            yaml.dump(structure_outdict, out, default_flow_style=False)


def main():
    """
    Main function to process variables and structures based on the rendered_wano.yml configuration.
    """
    # Initialize empty dictionaries
    empty_outdict = {'iter': []}
    for filename in ['float_output_dict.yml', 'int_output_dict.yml', 'structure_output_dict.yml', 'output_dict.yml']:
        with open(filename, 'w') as out:
            yaml.dump(empty_outdict, out, default_flow_style=False)

    # Read input parameters
    try:
        with open('rendered_wano.yml') as file:
            wano_file = yaml.full_load(file)
    except FileNotFoundError:
        print("The 'rendered_wano.yml' file was not found.")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing 'rendered_wano.yml': {e}")
        return

    # Process variables based on wano_file configuration
    if wano_file.get('Float'):
        process_float_variables(wano_file)

    if wano_file.get('Int'):
        process_int_variables(wano_file)

    process_structures(wano_file)


if __name__ == '__main__':
    main()
