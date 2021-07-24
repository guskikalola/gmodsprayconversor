import configparser,os,sys,getopt,glob

helpText = """
GMODSprayConversor/VTF by guskikalola

This script converts PNG and JPEG ( not tested
with other image types ) to VTF files

-f, --folder <folder> Input folder for images
-o, --output <folder> Output folder for results
-h, --help            Help about the script

"""

# Load config file
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "../config.cfg")
config.read(config_path)

VTFCmd = config["VTF"]["vtfcmd"]
VTFParam = config["VTF"]["vtfcmd_param"]

# Parse parameters
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hf:o:", ["help", "folder=", "output="])
except:
    sys.exit("Error while parsing arguments")

input_folder = None
output_folder = None

for opt, value in opts:
    if opt in ["-h", "--help"]:
        print(helpText)
        sys.exit()
    elif opt in ["-f", "--folder"]:
        input_folder = value
    elif opt in ["-o", "--output"]:
        output_folder = value

# Check if required parameters are given, else use defaults
if input_folder == None:
    sys.exit("Input folder must be given (-f path/to/folder)")
if output_folder == None:
    output_folder = os.path.join(os.path.dirname(__file__), "./out")

# Get the file names
filenames = glob.glob(os.path.join(input_folder, "*"))

# Start converting the files to VTF
if not os.path.exists(output_folder): 
    os.makedirs(output_folder)

for filename in filenames:
    file = os.path.realpath(filename)
    os.system(VTFCmd + " " + VTFParam.strip() + " -output " + output_folder + " -file " + file)
