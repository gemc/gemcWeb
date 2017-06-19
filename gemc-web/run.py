from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

#global variables that hold essential user data
gl_part = ""
experiments = []
ec = ""
advOps = ""

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

#gets gl input
@app.route('/_process_glinput')
def glsetup():
    #globally set gl part
    global gl_part

    #getting it from form
    gl_step = request.args.get('glin', 0, type=str)

    gl_part = gl_step

    return jsonify(yesss=gl_step)


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

    return jsonify(result=experimentDescription)

#gets data for advanced options modal
@app.route('/_adv_detect_su')
def ad_cb():
    #gets the description of selected experiment from json file and returns the json object
    with open('/home/smarky/active_dev/components/' + ec + '.json') as data_file:
        user_json = json.load(data_file)

    experimentDetectors = user_json["detectors"]

    return jsonify(advanced=experimentDetectors)

#save advanced options
@app.route('/_process_advanced')
def get_ao():
    global advOps
    #gets advanced options selections from form data
    advOps= request.args.get('advanced_select')

    return jsonify(test="All set")

if __name__ == '__main__':
    app.run(debug = True)
