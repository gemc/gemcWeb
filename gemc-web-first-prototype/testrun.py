from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

#global variables that hold essential user data
experiments = []
detectors = []
adv_det_opt = []
ec = ""

@app.route('/')
def homepage():
    #must allow experiment list to be global as it needs to be rendered in each template
    global experiments
    #location of experiments directory
    exp_directory = "/home/smarky/Desktop/json_exp"

    #append to file and experiment list
    for exp in os.listdir(exp_directory):
        if exp.endswith('.json'):
            experiments.append(exp[:-5])

    #returns homepage with all available options
    return render_template('home.html', exps = experiments, i1 = "static/images/circle-xxl.png", i2 = "static/images/circle-xxl.png", i3 = "static/images/circle-xxl.png", i4 = "static/images/circle-xxl.png")

@app.route('/_process_description')
def _process_description():
    #gets experiment selection form data
    experiment_choice = request.args.get('experiment_select')

    #gets name in proper formatting
    delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())

    unscruched = str(experiment_choice)

    #applies the experiment choice globally
    global ec
    ec = unscruched.translate(None, delchars)

    #gets the description of selected experiment from json file and returns the json object
    with open('/home/smarky/Desktop/json_exp/' + ec + '.json') as data_file:
        user_json = json.load(data_file)

    experimentDescription = str(user_json["description"])

    return jsonify(result=experimentDescription)

@app.route('/aorddetectors', methods=['POST'])
def advanceddetectoroptions():
    #we must apply the experiment choice globally
    global ec

    #gets selected experiment, applies it to ec, and gets the proper information from json file
    option = request.form['expradio']

    ec = str(option)

    with open('/home/smarky/Desktop/json_exp/' + ec + '.json') as data_file:
        user_json = json.load(data_file)

    global detectors

    detectors = user_json["detectors"]

    return render_template('home.html', exps = experiments, detects = detectors, i1 = "static/images/circle-xxl.png", i2 = "static/images/green.png", i3 = "static/images/circle-xxl.png", i4 = "static/images/circle-xxl.png")

@app.route('/aodone', methods=['POST'])
def get_ao():
    #must get advanced options globally so that they can be applied later
    global adv_det_opt

    #gets the selcted checkboxes
    value = request.form.getlist('detectorcb')

    #applies it to the global value
    adv_det_opt = value

    #testing purposes (remove inproduction version)
    print adv_det_opt

    return render_template('home.html', exps = experiments, detects = detectors, i1 = "static/images/circle-xxl.png", i2 = "static/images/green.png", i3 = "static/images/circle-xxl.png", i4 = "static/images/circle-xxl.png")

if __name__ == '__main__':
    app.run(debug = True)
