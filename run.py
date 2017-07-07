from flask import Flask, render_template, request, jsonify, url_for, redirect, send_from_directory
from datetime import datetime
from werkzeug import secure_filename
import json, os, subprocess, uuid, time

#global variables that hold essential user data
glfile = ""
experiments = []
experimentDetectors = []
ec = ""
advOps = ""
user_out=""
user_exp_name=""
user_exp_abstract=""
piped_out = ""

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#homepage
@app.route('/')
def homepage():
    #must allow experiment list to be global as it needs to be rendered in each template
    global experiments
    #location of experiments directory
    exp_directory = basedir + "/components/expjson"

    #append to file and experiment list
    for exp in os.listdir(exp_directory):
        if exp.endswith('.json'):
            experiments.append(exp[:-5])

    #returns homepage with all available options
    return render_template('home.html', exps = experiments)

#this gets the user's provided name
@app.route('/_process_username')
def processname():
    drat = request.args.get('uexpname')

    global user_exp_name

    user_exp_name = str(drat)

    return jsonify(yyy=user_exp_name)

#this gets the user's provided abstract
@app.route('/_process_abstract')
def processabstract():
    wrat = request.args.get('uexpab')

    print(wrat)

    global user_exp_abstract

    user_exp_abstract = str(wrat)

    return jsonify(nnn=user_exp_abstract)

#this gets the glfileupload
@app.route('/uploadajax', methods=['POST'])
def upldfile():
    if request.method == 'POST':
        files = request.files['file']
        if files:
            fn = secure_filename(files.filename)
            filename = str(uuid.uuid4()) + secure_filename(files.filename)
            app.logger.info('FileName: ' + filename)
            updir = os.path.join(basedir, 'upload/')
            files.save(os.path.join(updir, filename))
            file_size = os.path.getsize(os.path.join(updir, filename))
            global glfile
            glfile = basedir + "/upload/" + filename
            return jsonify(name=fn, size=file_size)

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
    with open(basedir + '/components/expjson/' + ec + '.json') as data_file:
        user_json = json.load(data_file)

    experimentDescription = str(user_json["description"])

    global experimentDetectors

    experimentDetectors = user_json["detectors"]

    return jsonify(result=experimentDescription)

#gets data for advanced options modal
@app.route('/_adv_detect_su')
def ad_cb():
    #gets the description of selected experiment from json file and returns the json object
    with open(basedir + '/components/expjson/' + ec + '.json') as data_file:
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

#generates gcard and runs gemc
@app.route('/gogogo', methods = ['POST', 'GET'])
def gengcardandgo():
    if request.method == 'POST':
        global user_out
        global advOps
        global experimentDetectors
        global glfile

        os.chdir(basedir + "/output")

        #generate unique gcard and output file for user
        user_gcard = str(uuid.uuid4()) + ".gcard"
        user_out = str(uuid.uuid4()) + ".ev"

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

        global piped_out
        piped_out = str(uuid.uuid4()) + "out.txt"

        with open(piped_out,"wb+") as out:
            p = subprocess.Popen(args=['/bin/csh', '-c', "gemc " +  user_gcard + " -USE_GUI=0 -N=10"], stdout=out)

            while True:
                while 1:
                    where = out.tell()
                    line = out.readline()
                    if not line:
                        time.sleep(1)
                        out.seek(where)
                    else:
                        if "Event Action: >>  Begin of event" in line:
                            print line
                        elif "> Total gemc time:" in line:
                            print line
                            break
                        elif "> Number of events to be simulated set to:" in line:
                            print line
                        elif "> Initializing GEant4 MonteCarlo:" in line:
                            print line
                        elif "> Loading field map" in line:
                            print line
                        elif "Beam Settings >>" in line:
                            print line
                        elif ">> Registering experiment" in line:
                            print line
                        elif ">> Parsing clas12.gcard for options:" in line:
                            print line
                        elif "> Choice of Physics" in line:
                            print line
                        elif "Aborted" in line:
                            print "ERROR!" + line
                            break
                        else:
                            pass
                break

            #kill gemc amd subprocess
            os.system("pkill -HUP gemc");
            p.kill()
            out.close()

            return redirect(url_for('user_res'))


#returns results
@app.route('/theresults')
def user_res():
    global user_out

    sendthis = user_out

    return render_template('results.html', filename=sendthis)

@app.route('/ur_download/<filename>')
def results_download(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True)
