import os
import platform
import subprocess
import shutil

def add_bin_to_path():
    # Get the user's home directory
    home_directory = os.path.expanduser("~")

    # Determine the 'bin' directory path based on the OS
    if platform.system() == "Windows":
        bin_directory = os.path.join(home_directory, "bin")
    else:
        bin_directory = os.path.join(home_directory, "bin")

    # Get the current PATH variable value and split it into a list of directories
    current_path = os.environ.get("PATH", "").split(os.pathsep)

    # Check if the 'bin' directory is already in the PATH
    if bin_directory not in current_path:
        # Add the 'bin' directory to the beginning of the PATH list
        updated_path = [bin_directory] + current_path

        # Join the directories back into a string with the appropriate separator
        updated_path_str = os.pathsep.join(updated_path)

        # Update the PATH environment variable
        os.environ["PATH"] = updated_path_str

def create_youtube_downloads_folder():
    # Create the Youtube_Downloads folder in the user's Downloads directory
    downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
    youtube_downloads_folder = os.path.join(downloads_directory, "Youtube_Downloads")
    os.makedirs(youtube_downloads_folder, exist_ok=True)

def create_single_file_executable(script_name, output_dir=None):
    # Check if the script file exists
    if not os.path.isfile(script_name):
        print(f"Error: '{script_name}' not found. Make sure the script exists in the current directory.")
        return

    # Set the default output directory if not provided
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), 'dist')

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Determine the executable name based on the OS
    if platform.system() == 'Windows':
        executable_name = os.path.splitext(script_name)[0] + '.exe'
    else:
        executable_name = os.path.splitext(script_name)[0]

    # Run PyInstaller to create the single-file executable
    cmd = f'pyinstaller --onefile {script_name} --distpath "{output_dir}" --noconfirm --log-level ERROR'
    subprocess.run(cmd, shell=True)

    # Copy the executable to the 'bin' folder of the user
    target_directory = os.path.expanduser('~/bin')  # Change this to your desired target directory

    # Use the appropriate path separator for the current OS
    target_path = os.path.join(target_directory, executable_name).replace('/', os.sep)

    os.makedirs(target_directory, exist_ok=True)  # Create 'bin' folder if it doesn't exist
    shutil.copy(os.path.join(output_dir, executable_name), target_path)

    # Add execute permissions (Linux/macOS only)
    if os.name != 'nt':
        st = os.stat(target_path)
        os.chmod(target_path, st.st_mode | 0o111)

    print(f"Single-file executable created and copied to: {target_path}")

if __name__ == '__main__':

    print("")

    print(r"""
          
     /$$$$$$                       /$$               /$$ /$$                    
    |_  $$_/                      | $$              | $$| $$                    
      | $$   /$$$$$$$   /$$$$$$$ /$$$$$$    /$$$$$$ | $$| $$  /$$$$$$   /$$$$$$ 
      | $$  | $$__  $$ /$$_____/|_  $$_/   |____  $$| $$| $$ /$$__  $$ /$$__  $$
      | $$  | $$  \ $$|  $$$$$$   | $$      /$$$$$$$| $$| $$| $$$$$$$$| $$  \__/
      | $$  | $$  | $$ \____  $$  | $$ /$$ /$$__  $$| $$| $$| $$_____/| $$      
     /$$$$$$| $$  | $$ /$$$$$$$/  |  $$$$/|  $$$$$$$| $$| $$|  $$$$$$$| $$      
    |______/|__/  |__/|_______/    \___/   \_______/|__/|__/ \_______/|__/  

    """)

    print("Creating the Youtube_Downloads Folder in your Downloads dir ...")
    create_youtube_downloads_folder()

    script_name = 'ytdl.py'  # Replace with your YouTube downloader script name
    output_directory = None  # Set this to the desired output directory or leave it as None for the default

    print("Creating single-file executable...")
    create_single_file_executable(script_name, output_directory)
    print("Adding the environment variable...")
    add_bin_to_path()
    print("Done.")
