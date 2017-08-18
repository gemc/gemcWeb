from flask import Flask, render_template, session, request, redirect, g, url_for, jsonify, send_file
import os, datetime
import accounts as a
import file_handling as f
import run_project as r

PROJ_DIR = /group/clas/www/gemc2017/html/gemcWeb

application = Flask(__name__)
application.secret_key = or.urandom(24)

@application.route('/', methods=['GET' , 'POST'])
def login():
    """Renders the log in template, allows for account creation, page bounces back if credentials are incorrrect"""
    if request.method == 'POST':
        session.pop('user', None)

        u = request.form['username']
        p = request.form['password']

        if not(a.account_exists(u)):
            return "Account not found, go back and create one or try again if you do have an accout."
        else:
            pass

            if a.check_password(p) ==  a.get_password(u):
                session['user'] = u
                return redirect(url_for('home'))

    return render_template('login.html')

@application.route('/createaccount', methods=['GET' , 'POST'])
def create_account():
    """Handles account creation"""
    if request.method == 'POST':
        session.pop('user', None)

        u = request.form['username']
        p = request.form['password']

        if a.create_account(u,p):
            return render_template('login.html')
        else:
            return '''
                <p>Username taken, go back and try again</a></p>
                '''
    return render_template('createaccount.html')


@application.route('/about')
def about():
    """Renders the about page"""
    return render_template('about.html')


@application.route('/docs')
def docs():
    """ Renders the docs page"""
    return render_template('docs.html')

@application.before_request
def before_request():
    """Session handling"""
    g.user = None
    if 'user' in session:
        g.user = session['user']

@application.route('/home')
def home():
    """Renders the user's homepage, including there existing projects in tabular form"""
    if g.user:
        user = session['user']
        projects= f.get_user_projects(g.user)
        return render_template('home.html', user=user, projects=projects)
    return redirect(url_for('login'))

@application.route('/projlst')
def proj_lst():
    """Renders the user's projects in tabular form"""
    if g.user:
        user = session['user']
        projects= f.get_user_projects(g.user)
        return render_template('projectlst.html', user=user, projects=projects)
    return redirect(url_for('login'))

@application.route('/view/<project>')
def details(project):
    """Renders the details page for a user's specific project"""
    if g.user:
        abstract = f.get_experiment_data(g.user, project, 'abstract')
        return render_template('view.html', project=project, abstract=abstract)
    return redirect(url_for('login'))

@application.route('/aboutin')
def aboutin():
    """Renders the about page"""
    if g.user:
        return render_template('aboutin.html')
    return redirect(url_for('login'))

@application.route('/docsin')
def docsin():
    """ Renders the docs page"""
    if g.user:
        return render_template('docsin.html')
    return redirect(url_for('login'))

#####
#The following fetch files of existing projects
#####
@application.route('/_fetch_mc/<project>')
def fetch_mc(project):
    if g.user:
        sendme = f.get_experiment_data(g.user, project, 'gl')
        name = project  + ' out'
        if os.path.exists(sendme):
            return send_file(sendme, attachment_filename=name)
        else:
            return '''
                <p>Error: File does not exist.</p>
                '''
    return redirect(url_for('login'))

@application.route('/_fetch_g/<project>')
def fetch_g(project):
    if g.user:
        sendme = PROJ_DIR + '/users/' + g.user + '/projects/' + project + '/' + project + '.gcard'
        name = project + ' gcard'
        if os.path.exists(sendme):
            return send_file(sendme, attachment_filename=name)
        else:
            return '''
                <p>Error: File does not exist.</p>
                '''
    return redirect(url_for('login'))

@application.route('/_fetch_results/<project>')
def fetch_results(project):
    if g.user:
        sendme = PROJ_DIR + '/users/' + g.user + '/projects/' + project + '/' + project + '.ev'
        name = project + ' results'
        if os.path.exists(sendme):
            return send_file(sendme, attachment_filename=name)
        else:
            return '''
                <p>Error: File does not exist.</p>
                '''
    return redirect(url_for('login'))

@application.route('/_fetch_out/<project>')
def fetch_out(project):
    if g.user:
        sendme = PROJ_DIR + '/users/' + g.user + '/projects/' + project + '/' + project +'_out.txt'
        name = project  + ' out'
        if os.path.exists(sendme):
            return send_file(sendme, attachment_filename=name)
        else:
            return '''
                <p>Error: File does not exist.</p>
                '''
    return redirect(url_for('login'))
#####
# End of fetching methods
#####


@application.route('/_deleteme/<project>')
def erase_proj(project):
    """DANGER: Erases a project"""
    if g.user:
        import shutil
        delete = PROJ_DIR + '/users/' + g.user + '/projects/' + project
        shutil.rmtree(delete, ignore_errors=True)
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@application.route('/_new_experiment')
def new_exp():
    """Loads a blank new experiment template"""
    if g.user:
        exps = f.get_experiment_list()
        now = datetime.datetime.now()
        tmp = now.strftime("%Y-%m-%d_%H:%M:%S")
        session['exp'] = tmp
        f.create_project_dir(g.user, tmp)
        f.create_experiment_data(g.user, session['exp'])
        return render_template('newexperiment.html', exps=exps)
    return redirect(url_for('login'))

@application.route('/_name_&_abstract')
def name_and_abstract():
    """Handles getting the name and abstract of a new experiment"""
    if g.user:
        title = request.args.get('title')
        abstract = request.args.get('abstract')
        session['exp'] = f.rename_project_dir(g.user, session['exp'], title)
        f.write_experiment_data(g.user, session['exp'], 'title', title)
        f.write_experiment_data(g.user, session['exp'], 'abstract', abstract)
        return jsonify(t = title, a = abstract)
    return redirect(url_for('login'))

@application.route('/_gl_upload', methods=['POST'])
def gl():
    """Handles getting the gl file of a new experiment"""
    import uuid
    from werkzeug import secure_filename
    if g.user:
        if request.method == 'POST':
            files = request.files['file']
            if files:
                fn = secure_filename(files.filename)
                filename = str(uuid.uuid4()) + secure_filename(files.filename)
                application.logger.info('FileName: ' + filename)
                updir = os.path.join(PROJ_DIR, 'upload/')
                files.save(os.path.join(updir, filename))
                file_size = os.path.getsize(os.path.join(updir, filename))
                gl = PROJ_DIR + '/upload/' + filename
                f.write_experiment_data(g.user, session['exp'], 'gl', gl)
                return jsonify(name=fn, size=file_size)
    return redirect(url_for('login'))

@application.route('/_ec')
def ec():
	"""Handles getting the experiment choice of a new experiment"""
	if g.user:
		ec = r.trim_ec(request.args.get('x_sel'))
		edes = r.get_ec_info(ec, 'description')
		f.write_experiment_data(g.user, session['exp'], 'ec', ec)
		return jsonify(edes=edes)
	return redirect(url_for('login'))

@application.route('/_display_ao')
def display_ao():
	"""Handles displaying the advanced options of an experiment"""
	if g.user:
		t = f.get_experiment_data(g.user, session['exp'], 'ec')
		edet = r.get_ec_info(str(t), 'detectors')
		return jsonify(advanced=edet)
	return redirect(url_for('login'))

@application.route('/_ao')
def ao():
	"""Handles getting the ao if selected of a new experiment"""
	if g.user:
		ao = r.trim_ao(request.args.get('advanced_select'))
		f.write_experiment_data(g.user, session['exp'], 'ao', ao)
		return jsonify(test=ao)
	return redirect(url_for('login'))

@application.route('/go')
def go():
    """Generates the gcard, runs gemc and returns results of a new experiment"""
    if g.user:
        r.gen_gcard(g.user, session['exp'])
        if s.run_gemc(g.user, session['exp']):
            code = "gemc run successfully"
            return jsonify(code=code)
        else:
            return '''
            <p>These is an error, please go back and check generator library file.</p>
            '''
            return redirect(url_for('login'))

@application.route('/exp_res')
def exp_res ():
    """Handles sending results for project that is just completed"""
    if g.user:
        project = session['exp']
        sendme = PROJ_DIR + '/users/' + g.user + '/projects/' + project + '/' + project + '.ev'
        name = project + ' results'
        return send_file(sendme, attachment_filename=name)
    return redirect(url_for('login'))

@application.route('/exp_g')
def exp_g ():
    """Handles sending gcard for project that is just completed"""
    if g.user:
        project = session['exp']
        sendme = PROJ_DIR + '/users/' + g.user + '/projects/' + project + '/' + project + '.gcard'
        name = project + ' gcard'
        return send_file(sendme, attachment_filename=name)
    return redirect(url_for('login'))

@application.route('/exp_log')
def exp_log ():
    """Handles sending gemc log for project that is just completed"""
    if g.user:
        project = session['exp']
        sendme = PROJ_DIR + '/users/' + g.user + '/projects/' + project + '/' + project + '_out.txt'
        name = project + ' gemc log'
        return send_file(sendme, attachment_filename=name)
    return redirect(url_for('login'))


if __name__ == '__main__':
    application.run()
