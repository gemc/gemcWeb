from flask import Flask, render_template, session, request, redirect, g, url_for, jsonify, send_file
import os
import scripts as s


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        u = request.form['username']
        p = request.form['password']

        if not(s.account_exists(u)):
            return "Account not found, go back and create one"
        else:
            pass

            if s.check_password(p) ==  s.get_password(u):
                session['user'] = u
                return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/createaccount', methods=['GET' , 'POST'])
def create_account():
    if request.method == 'POST':
        session.pop('user', None)

        u = request.form['username']
        p = request.form['password']

        if s.create_account(u,p):
            return '''
                <p>Account creation successful, go to <a href="/"> log in</a></p>
                '''
        else:
            return '''
                <p>Username taken, go <a href="/createaccount"> try again</a></p>
                '''
    return render_template('createaccount.html')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/home')
def home():
    if g.user:
        user = session['user']
        projects= s.get_user_projects(g.user)
        return render_template('home.html', user=user, projects=projects)
    return redirect(url_for('login'))

@app.route('/_fetch_out/<project>')
def fetch_out(project):
    if g.user:
        sendme = basedir + '/users/' + g.user + '/projects/' + project + '/' + 'out.txt'
        name = project  + ' out'
        return send_file(sendme, attachment_filename=name)
    return redirect(url_for('login'))

@app.route('/_fetch_g/<project>')
def fetch_g(project):
    if g.user:
        sendme = basedir + '/users/' + g.user + '/projects/' + project + '/' + 'g.gcard'
        name = project + ' gcard'
        return send_file(sendme, attachment_filename=name)
    return redirect(url_for('login'))

@app.route('/_fetch_results/<project>')
def fetch_results(project):
    if g.user:
        sendme = basedir + '/users/' + g.user + '/projects/' + project + '/' + 'r.ev'
        name = project + ' results'
        return send_file(sendme, attachment_filename=name)
    return redirect(url_for('login'))


@app.route('/about')
def about():
    if g.user:
        return render_template('about.html')
    return redirect(url_for('login'))

@app.route('/docs')
def docs():
    if g.user:
        return render_template('docs.html')
    return redirect(url_for('login'))

@app.route('/_new_experiment')
def new_exp():
	if g.user:
		exps = s.get_experiment_list()
		return render_template('newexperiment.html', exps=exps)
	return redirect(url_for('login'))

@app.route('/_name_&_abstract')
def name_and_abstract():
	if g.user:
		title = request.args.get('title')
		abstract = request.args.get('abstract')
		session['exp'] = title
		s.create_project_dir(g.user, session['exp'])
		s.create_experiment_data(g.user, session['exp'])
		s.write_experiment_data(g.user, session['exp'], 'title', title)
		s.write_experiment_data(g.user, session['exp'], 'abstract', abstract)
        return jsonify(t = title, a = abstract)
	return redirect(url_for('login'))

@app.route('/_gl_upload', methods=['POST'])
def gl():
	import uuid
	from werkzeug import secure_filename
	if g.user:
		if request.method == 'POST':
			files = request.files['file']
			if files:
				fn = secure_filename(files.filename)
				filename = str(uuid.uuid4()) + secure_filename(files.filename)
				app.logger.info('FileName: ' + filename)
				updir = os.path.join(basedir, 'upload/')
				files.save(os.path.join(updir, filename))
				file_size = os.path.getsize(os.path.join(updir, filename))
				gl = basedir + "/upload/" + filename
				s.write_experiment_data(g.user, session['exp'], 'gl', gl)
				return jsonify(name=fn, size=file_size)
	return redirect(url_for('login'))

@app.route('/_ec')
def ec():
	if g.user:
		ec = s.trim_ec(request.args.get('x_sel'))
		edes = s.get_ec_info(ec, 'description')
		s.write_experiment_data(g.user, session['exp'], 'ec', ec)
		return jsonify(edes=edes)
	return redirect(url_for('login'))

@app.route('/_display_ao')
def display_ao():
	if g.user:
		t = s.get_experiment_data(g.user, session['exp'], 'ec')
		edet = s.get_ec_info(str(t), 'detectors')
		return jsonify(advanced=edet)
	return redirect(url_for('login'))

@app.route('/_ao')
def ao():
	if g.user:
		ao = s.trim_ao(request.args.get('advanced_select'))
		s.write_experiment_data(g.user, session['exp'], 'ao', ao)
		return jsonify(test=ao)
	return redirect(url_for('login'))

@app.route('/go')
def go():
    if g.user:
        s.gen_gcard(g.user, session['exp'])
        if s.run_gemc(g.user, session['exp']):
            project = session['exp']
            return render_template('results.html', project=project)
        else:
            return '''
            <p>These is an error, please go back and check generator library file.</p>
            '''
            return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
