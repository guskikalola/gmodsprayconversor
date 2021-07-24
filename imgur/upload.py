import configparser, os, sys, time, getopt, glob, datetime
from imgur_python import Imgur

helpText = """
GMODSprayConversor/Imgur by guskikalola

This script uploads images to imgur and outputs a file
with every link to the uploaded files

-f, --folder <folder> Input folder for images 
-o, --output <folder> Output folder for results
-h, --help            Help about the script

"""

# Load config file
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__),"../config.cfg")
config.read(config_path)

# Client auth
client_id = config["Imgur"]["client_id"]
client_secret = config["Imgur"]["client_secret"]
access_token = config["Imgur"]["access_token"]

client = Imgur({'client_id':client_id,'client_secret':client_secret,'access_token':access_token})

# Parse parameters
argv = sys.argv[1:]
try:
    opts,args = getopt.getopt(argv, "hf:o:",["help","folder=","output="])
except:
    sys.exit("Error while parsing arguments")

input_folder = None
output_folder = None

for opt,value in opts:
    if opt in ["-h","--help"]:
        print(helpText)
        sys.exit()
    elif opt in ["-f","--folder"]:
        input_folder = value
    elif opt in ["-o","--output"]:
        output_folder = value

# Check if required parameters are given, else use defaults
if input_folder == None:
    sys.exit("Input folder must be given (-f path/to/folder)")
if output_folder == None:
    output_folder = os.path.join(os.path.dirname(__file__), "./output")
print(output_folder)
# Get the file names 
filenames = glob.glob(os.path.join(input_folder,"*"))

# Start updating the images
links = {}
for filename in filenames:
    file = os.path.realpath(filename)

    title = "UltimateSprayConversor"
    description = "Updated using UltimateSprayConversor"
    album = config["Imgur"]["album_id"]
    disable_audio = 0

    try:
        response = client.image_upload(file,title,description,album,disable_audio)
        if response["status"] == 200:
            image = response["response"]["data"]["link"]
            links[file] = image
            print(image)
    except (KeyError,TypeError):
        sys.exit("""
Error while uploading image located at ({image_path}) .
Maybe the error is due to a missing or invald access_token, 
follow the steps below to get a valid access_token. 
1.Authorize the app: {auth_link}
2.After the redirect, from the URL copy the access_token
3.Paste it at the config file 
""".format(auth_link=client.authorize(),image_path=file))

# Create the output file
output_file = os.path.realpath(output_folder+"/"+datetime.datetime.now().strftime("%I.%M.%S%p-%B-%d-%Y")) + ".txt"

if not os.path.exists(output_folder): 
    os.makedirs(output_folder)


f = open(output_file, "w+")
for key in links:
    f.write("{key} -> {value} \n".format(key=key,value=links[key]))
f.close()
