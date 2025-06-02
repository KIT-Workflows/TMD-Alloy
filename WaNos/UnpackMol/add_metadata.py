import getpass
import socket
import datetime
import platform
import sys
import os
import logging
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class UtilTricks:
    """
    Utility class containing helper functions for collecting metadata.
    """

    @staticmethod
    def add_metadata():
        """
        Collects metadata including user, system, and job scheduler information.

        Returns:
            dict: The collected metadata.
        """
        properties_dict = {}

        # Basic user and system information
        properties_dict['user'] = getpass.getuser()
        properties_dict['hostname'] = socket.gethostname()

        # Get IP address
        try:
            properties_dict['ip_address'] = socket.gethostbyname(properties_dict['hostname'])
        except socket.gaierror:
            properties_dict['ip_address'] = 'Unavailable'

        properties_dict['datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        properties_dict['working_directory'] = os.getcwd()
        properties_dict['os'] = platform.system()
        properties_dict['os_version'] = platform.version()
        properties_dict['python_version'] = sys.version.split()[0]
        properties_dict['processor'] = platform.processor()
        properties_dict['machine'] = platform.machine()
        properties_dict['script_name'] = os.path.basename(sys.argv[0])

        # Detect job scheduler and collect scheduler-specific metadata
        scheduler = UtilTricks.detect_scheduler()
        properties_dict['scheduler'] = scheduler

        if scheduler == 'SLURM':
            # SLURM environment variables
            properties_dict['job_id'] = os.environ.get('SLURM_JOB_ID', 'N/A')
            properties_dict['job_name'] = os.environ.get('SLURM_JOB_NAME', 'N/A')
            properties_dict['node_list'] = os.environ.get('SLURM_NODELIST', 'N/A')
            properties_dict['num_nodes'] = os.environ.get('SLURM_NNODES', 'N/A')
            properties_dict['num_tasks'] = os.environ.get('SLURM_NTASKS', 'N/A')
            properties_dict['tasks_per_node'] = os.environ.get('SLURM_TASKS_PER_NODE', 'N/A')
        elif scheduler == 'PBS/Torque':
            # PBS/Torque environment variables
            properties_dict['job_id'] = os.environ.get('PBS_JOBID', 'N/A')
            properties_dict['job_name'] = os.environ.get('PBS_JOBNAME', 'N/A')
            properties_dict['node_list'] = UtilTricks.get_pbs_node_list()
            properties_dict['num_nodes'] = os.environ.get('PBS_NUM_NODES', 'N/A')
            properties_dict['num_tasks'] = os.environ.get('PBS_NP', 'N/A')
        else:
            properties_dict['job_id'] = 'N/A'
            properties_dict['job_name'] = 'N/A'
            properties_dict['node_list'] = 'N/A'
            properties_dict['num_nodes'] = 'N/A'
            properties_dict['num_tasks'] = 'N/A'

        # Loaded modules
        properties_dict['loaded_modules'] = UtilTricks.get_loaded_modules()

        # Memory information
        total_memory, available_memory = UtilTricks.get_memory_info()
        properties_dict['total_memory_gb'] = total_memory
        properties_dict['available_memory_gb'] = available_memory

        return properties_dict

    @staticmethod
    def detect_scheduler():
        """
        Detects the job scheduler system in use (SLURM, PBS/Torque, or Unknown).

        Returns:
            str: The name of the scheduler system.
        """
        if 'SLURM_JOB_ID' in os.environ:
            return 'SLURM'
        elif 'PBS_JOBID' in os.environ:
            return 'PBS/Torque'
        else:
            return 'Unknown'

    @staticmethod
    def get_pbs_node_list():
        """
        Retrieves the node list for PBS/Torque scheduler.

        Returns:
            str: A comma-separated list of nodes.
        """
        nodefile = os.environ.get('PBS_NODEFILE')
        if nodefile and os.path.isfile(nodefile):
            try:
                with open(nodefile, 'r') as f:
                    nodes = f.read().splitlines()
                    unique_nodes = sorted(set(nodes))
                    return ','.join(unique_nodes)
            except Exception as e:
                logging.error(f"Error reading PBS_NODEFILE: {e}")
                return 'Error reading PBS_NODEFILE'
        else:
            return 'N/A'

    @staticmethod
    def get_loaded_modules():
        """
        Retrieves the list of loaded modules.

        Returns:
            str: A string representation of the loaded modules.
        """
        try:
            import subprocess
            # Using 'module' command and capturing stderr because module outputs to stderr
            loaded_modules = subprocess.check_output(['module', 'list'], stderr=subprocess.STDOUT, universal_newlines=True)
            return loaded_modules.strip()
        except Exception as e:
            logging.warning(f"Could not retrieve loaded modules: {e}")
            return 'Could not retrieve loaded modules'

    @staticmethod
    def get_memory_info():
        """
        Retrieves total and available memory using psutil.

        Returns:
            tuple: (total_memory_in_gb, available_memory_in_gb)
        """
        try:
            import psutil
            mem = psutil.virtual_memory()
            total_gb = mem.total / (1024 ** 3)  # Convert bytes to GB
            available_gb = mem.available / (1024 ** 3)
            return round(total_gb, 2), round(available_gb, 2)
        except ImportError:
            logging.warning("psutil not installed. Memory information not available.")
            return 'psutil not installed', 'psutil not installed'
        except Exception as e:
            logging.error(f"Error retrieving memory info: {e}")
            return 'Error retrieving memory info', 'Error retrieving memory info'

    @staticmethod
    def write_metadata_to_yaml(metadata, filename='metadata.yml'):
        """
        Writes the collected metadata to a YAML file.

        Parameters:
            metadata (dict): The metadata dictionary to write.
            filename (str): The name of the output YAML file.
        """
        try:
            with open(filename, 'w') as outfile:
                yaml.dump(metadata, outfile, default_flow_style=False)
            logging.info(f"Metadata successfully written to {filename}")
        except Exception as e:
            logging.error(f"Error writing metadata to YAML file: {e}")

# Example usage
if __name__ == '__main__':
    metadata = UtilTricks.add_metadata()

    # # Print the collected metadata
    # for key, value in metadata.items():
    #     print(f"{key}: {value}")

    # Write metadata to YAML file
    UtilTricks.write_metadata_to_yaml(metadata, filename='metadata.yml')
