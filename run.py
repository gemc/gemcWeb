from flask import Flask, render_template, request, jsonify, url_for, request
from datetime import datetime
from werkzeug import secure_filename
import json, os

#global variables that hold essential user data
glfile = ""
experiments = []
experimentDetectors = []
ec = ""
advOps = ""

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#homepage
@app.route('/')
def homepage():
    #must allow experiment list to be global as it needs to be rendered in each template
    global experiments
    #location of experiments directory
    exp_directory = "/home/smarky/active_dev/components"

    #append to file and experiment list
    for exp in os.listdir(exp_directory):
        if exp.endswith('experiment.json'):
            experiments.append(exp[:-16])

    #returns homepage with all available options
    return render_template('home.html', exps = experiments)

#this gets the glfileupload
@app.route('/uploadajax', methods=['POST'])
def upldfile():
    if request.method == 'POST':
        files = request.files['file']
        if files:
            filename = secure_filename(files.filename)
            app.logger.info('FileName: ' + filename)
            updir = os.path.join(basedir, 'upload/')
            files.save(os.path.join(updir, filename))
            file_size = os.path.getsize(os.path.join(updir, filename))
            global glfile
            glfile = filename
            return jsonify(name=filename, size=file_size)

#get more info and load adanced options from experiment selection
@app.route('/_process_description')
def _process_description():
    #gets experiment selection form data
    experiment_choice = request.args.get('experiment_select')

    #gets name in proper formattingautocompleteautocomplete
    delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())

    unscruched = str(experiment_choice)

    #applies the experiment choice globally
    global ec
    ec = unscruched.translate(None, delchars)

    #gets the description of selected experiment from json file and returns the json object
    with open('/home/smarky/active_dev/components/' + ec + '_experiment.json') as data_file:
        user_json = json.load(data_file)

    experimentDescription = str(user_json["description"])

    return jsonify(result=experimentDescription)

#gets data for advanced options modal
@app.route('/_adv_detect_su')
def ad_cb():
    #gets the description of selected experiment from json file and returns the json object
    with open('/home/smarky/active_dev/components/' + ec + '_experiment.json') as data_file:
        user_json = json.load(data_file)

    global experimentDetectors

    experimentDetectors = user_json["detectors"]

    return jsonify(advanced=experimentDetectors)

#save advanced options
@app.route('/_process_advanced')
def get_ao():
    global advOps
    #gets advanced options selections
    advOps= request.args.get('advanced_select')

    return jsonify(test="All set")

@app.route('/testresults')
def the_finisher():
    #location of test experiment
    loc_directory = "/home/smarky/Desktop/clas12Tags-master/4a.1.0"

    #change the directory to the working directory
    os.chdir(loc_directory)

    #run gemc for test scenario
    p = subprocess.Popen(args=['/bin/csh', '-c', "gemc clas12.gcard -USE_GUI=0"])

    #check to see if gemc is done and exit when it is
    while True:
        if os.path.isfile("/home/smarky/Desktop/clas12Tags-master/4a.1.0/out.ev"):
            break
        else:
            pass

    #kill gemc amd subprocess
    os.system("pkill -HUP gemc");
    p.kill()

    #get the contents of the ouput file
    x = os.system("cat out.ev")

    return x



if __name__ == '__main__':
    app.run(debug = True)
