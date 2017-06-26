from flask import Flask, render_template, request, jsonify, url_for, request, send_file
from datetime import datetime
from werkzeug import secure_filename
import json, os, subprocess, uuid

#global variables that hold essential user data
glfile = ""
experiments = []
experimentDetectors = []
ec = ""
advOps = ""
user_gcard=""

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
        if exp.endswith('.json'):
            experiments.append(exp[:-5])

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
            glfile = "/home/smarky/active_dev/gemc-web/upload/" + filename
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
    with open('/home/smarky/active_dev/components/' + ec + '.json') as data_file:
        user_json = json.load(data_file)

    experimentDescription = str(user_json["description"])

    global experimentDetectors

    experimentDetectors = user_json["detectors"]

    return jsonify(result=experimentDescription)

#gets data for advanced options modal
@app.route('/_adv_detect_su')
def ad_cb():
    #gets the description of selected experiment from json file and returns the json object
    with open('/home/smarky/active_dev/components/' + ec + '.json') as data_file:
        user_json = json.load(data_file)

    global experimentDetectors

    return jsonify(advanced=experimentDetectors)

#save advanced options
@app.route('/_process_advanced')
def get_ao():
    global advOps
    #gets advanced options selections
    trat = request.args.get('advanced_select')

    tret = trat[1:-1]

    advOps = str(tret)

    print(advOps)

    return jsonify(test=tret)

@app.route('/testresults', methods = ['POST', 'GET'])
def the_finisher():
    if request.method == 'POST':
        global user_gcard
        global advOps
        global experimentDetectors
        global glfile

        loc_directory = '/home/smarky/active_dev/gemc-web/output'
        os.chdir(loc_directory)

        #generate unique gcard and output file for user
        user_gcard = str(uuid.uuid4()) + ".gcard"
        user_out =str(uuid.uuid4()) + ".ev"

        #generate the gcard
        if advOps == "":
            fo = open(user_gcard, "wb")
            fo.write("<gcard>" + '\n')
            for e in experimentDetectors:
                fo.write(e["tag"] + '\n')
            fo.write("<option name ='INPUT_GEN_FILE' value='lund,"+ glfile +"'/>" + '\n')
            fo.write("<option name='OUTPUT' value='evio," + user_out + "'/>" +'\n')
            fo.write("</gcard>" + '\n')
            fo.close()
        else:
            fo = open(user_gcard, "wb")
            fo.write("<gcard>" + '\n')
            for e in experimentDetectors:
                if e["name"] in advOps:
                    fo.write(e["tag"] + '\n')
                else:
                    pass
            fo.write("<option name ='INPUT_GEN_FILE' value='lund,"+ glfile +"'/>" + '\n')
            fo.write("<option name='OUTPUT' value='evio," + user_out + "'/>" +'\n')
            fo.write("</gcard>" + '\n')
            fo.close()

        #run gemc for test scenario
        p = subprocess.Popen(args=['/bin/csh', '-c', "gemc "+ user_gcard +" -USE_GUI=0"])

        #check to see if gemc is done and exit when it is
        while True:
            if os.path.isfile(user_out):
                break
            else:
                pass

        #kill gemc amd subprocess
        os.system("pkill -HUP gemc");
        p.kill()
        sendthis = "/home/smarky/active_dev/gemc-web/output/" + user_out

        return send_file(sendthis,  attachment_filename='Output File')

if __name__ == '__main__':
    app.run(debug = True)
