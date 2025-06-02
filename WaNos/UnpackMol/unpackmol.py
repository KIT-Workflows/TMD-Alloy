import os
import tarfile
import shutil
import yaml


def load_wano_file(filename='rendered_wano.yml'):
    """
    Load the WANO configuration from a YAML file.

    Parameters:
        filename (str): The name of the YAML file to load.

    Returns:
        dict: The loaded WANO configuration.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    try:
        with open(filename) as file:
            return yaml.full_load(file)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{filename}': {e}")
        raise


def get_structure_name(wano_file):
    """
    Determine the structure name to extract based on the WANO configuration.

    Parameters:
        wano_file (dict): The WANO configuration dictionary.

    Returns:
        str: The name of the structure to extract.

    Raises:
        KeyError: If required keys are missing in the configuration.
        IndexError: If the structure index is out of range.
        ValueError: If there is a type conversion error.
    """
    if wano_file.get("Multivariable-mode"):
        try:
            structure_index = int(wano_file['Structures-int'])
            input_file = wano_file['Input-file']
            with open(input_file) as file:
                input_struct = yaml.full_load(file)
            structure_name = input_struct['iter'][structure_index]
        except (KeyError, IndexError, ValueError) as e:
            print(f"Error accessing structure information: {e}")
            raise
    else:
        structure_name = str(wano_file.get('Structures-name'))
    return structure_name


def extract_structure_from_archive(archive_name, structure_name):
    """
    Extract a specific structure from a tar archive.

    Parameters:
        archive_name (str): The name of the archive file.
        structure_name (str): The name of the structure to extract.

    Raises:
        FileNotFoundError: If the archive file does not exist.
        tarfile.TarError: If the file is not a valid tar archive or extraction fails.
        KeyError: If the structure is not found in the archive.
    """
    if not os.path.isfile(archive_name):
        print(f"Error: Archive file '{archive_name}' does not exist.")
        raise FileNotFoundError(f"Archive file '{archive_name}' does not exist.")

    if not tarfile.is_tarfile(archive_name):
        print(f"Error: File '{archive_name}' is not a valid tar archive.")
        raise tarfile.TarError(f"File '{archive_name}' is not a valid tar archive.")

    try:
        with tarfile.open(archive_name) as tar:
            if structure_name in tar.getnames():
                tar.extract(structure_name)
            else:
                print(f"Error: Structure '{structure_name}' not found in archive '{archive_name}'.")
                raise KeyError(f"Structure '{structure_name}' not found in archive.")
    except tarfile.TarError as e:
        print(f"Error extracting from tar archive '{archive_name}': {e}")
        raise


def rename_structure_file(original_name, new_name='Mol_geom.xyz'):
    """
    Rename the extracted structure file.

    Parameters:
        original_name (str): The current name of the structure file.
        new_name (str): The new name for the structure file.

    Raises:
        FileNotFoundError: If the original file does not exist.
        OSError: If renaming fails.
    """
    if not os.path.exists(original_name):
        print(f"Error: File '{original_name}' does not exist.")
        raise FileNotFoundError(f"File '{original_name}' does not exist.")
    try:
        os.rename(original_name, new_name)
    except OSError as e:
        print(f"Error renaming file '{original_name}' to '{new_name}': {e}")
        raise


def write_unpackmol_results(structure_name, output_file='unpackmol_results.yml'):
    """
    Write the unpackmol results to a YAML file.

    Parameters:
        structure_name (str): The name of the structure.
        output_file (str): The name of the output YAML file.

    Raises:
        IOError: If writing to the file fails.
    """
    unpackmol_results = {'structure': structure_name}
    try:
        with open(output_file, 'w') as out:
            yaml.dump(unpackmol_results, out, default_flow_style=False)
    except IOError as e:
        print(f"Error writing to file '{output_file}': {e}")
        raise


def cleanup_files(archive_name, directories=None):
    """
    Clean up the archive file and specified directories.

    Parameters:
        archive_name (str): The name of the archive file to remove.
        directories (list): A list of directory names to remove.

    Raises:
        OSError: If removal of files or directories fails.
    """
    if directories is None:
        directories = ['Structures']

    for directory in directories:
        if os.path.isdir(directory):
            try:
                shutil.rmtree(directory)
            except OSError as e:
                print(f"Error removing directory '{directory}': {e}")
                raise

    if os.path.isfile(archive_name):
        try:
            os.remove(archive_name)
        except OSError as e:
            print(f"Error removing file '{archive_name}': {e}")
            raise


def main():
    """
    Main function to execute the script logic.
    """
    try:
        # Load WANO configuration
        wano_file = load_wano_file()
        structure_name = get_structure_name(wano_file)
        archive_name = wano_file.get('Structures')

        if not archive_name:
            print("Error: 'Structures' key not found in WANO configuration.")
            return

        # Extract the structure from the archive
        extract_structure_from_archive(archive_name, structure_name)

        # Rename the extracted structure file
        rename_structure_file(structure_name)
        print(f"Extracted and renamed structure file: '{structure_name}' -> 'Mol_geom.xyz'")

        # Write unpackmol results
        write_unpackmol_results(structure_name)

        # Clean up files and directories
        cleanup_files(archive_name)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
