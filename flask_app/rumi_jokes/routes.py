import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from rumi_jokes import app, db, db2, db3, bcrypt
from rumi_jokes.forms import RegistrationForm, LoginForm, MajorForm, \
                             UpdateAccountForm, JokeSelectionForm, JokeSubmissionForm, SkillSubmissionForm
from rumi_jokes.models import User, Recommendation, Major, Joke, Skill
from flask_login import login_user, current_user, logout_user, login_required
from rumi_jokes.offline_training import train_offline
import logging

logging.basicConfig(filename='logfile.log'
                    , level=logging.INFO
                    , format='%(asctime)s:%(levelname)s:%(message)s')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/shutdown', methods=['GET', 'POST'])
@login_required
def shutdown_server():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    logging.info(current_user.get_id(), ' initiated server shutdown')
    return 'Server shutting down...'


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        logging.info('user {} created an account'.format(form.username.data))
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # app.logger.info('%s logged in successfully', form.email.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # app.logger.info('%s failed to log in', form.email.data)
            abort(401)
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/joke/submit", methods=['GET', 'POST'])
@login_required
def submit_joke():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = JokeSubmissionForm()
    if form.validate_on_submit():
        app.logger.info('%s is the variable', form.content.data)
        joke = Joke(content=form.content.data, author=int(current_user.get_id()))
        joke.save()
        logging.info('user {} submitted joke: {}'.format(current_user.get_id(), form.content.data))
        flash('Your joke has been submitted!', 'success')
        return redirect(url_for('home'))
    return render_template('submit_joke.html', title='New Joke',
                           form=form, legend='Joke submission')


@app.route("/joke/recommendations", methods=['GET', 'POST'])
def recommend_joke():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if Recommendation.query.filter_by(user_id=current_user.get_id()) \
            .filter_by(expired=0) \
            .count() < 2:
        train_offline()
    form = JokeSelectionForm()
    recommendation = Recommendation.query.filter_by(user_id=current_user.get_id())\
                                         .filter_by(expired=0)\
                                         .order_by('priority').first()
    db.session.commit()
    joke_1 = Joke.query.get(recommendation.joke_1)
    joke_2 = Joke.query.get(recommendation.joke_2)
    jokes = [joke_1, joke_2]
    logging.info('{} was shown jokes: \n\t\t {} \n\t\t {}'
                 .format(current_user.get_id(), joke_1.content, joke_2.content))
    if form.validate_on_submit():
        # flash('Your choice has been submitted!', 'success')
        joke_1.views += 1
        joke_2.views += 1
        if form.jokes.data == '0':
            joke_1.score += 1
            joke_2.score -= 1
        if form.jokes.data == '1':
            joke_2.score += 1
            joke_1.score -= 1
        recommendation.winner = form.jokes.data
        joke_1.save()
        joke_2.save()
        recommendation.expired = bool(1)
        recommendation.winner = bool(form.data['jokes'])
        db.session.commit()
        logging.info('joke {} was the winner'.format(str(form.data['jokes'])))
        return redirect(url_for('leaderboards'))
    return render_template('recommendation.html', jokes=jokes, form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    try:
        skills = Skill.get(user=current_user.get_id())
    except:
        skills = []
    usermajor = Major.query.get(current_user.get_id())
    try :
        majorname = usermajor.name
    except AttributeError:
        majorname = 'None!'
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, skills=skills, major=majorname)


@app.route("/skills", methods=['GET', 'POST'])
@login_required
def submit_skills():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = SkillSubmissionForm()
    skills = Skill.filter(user=current_user.get_id())
    if form.validate_on_submit():
        skill = form.content.data
        skill = skill.split(', ')
        skill = set(skill)
        Skill.objects(user=current_user.get_id()).update(sname__add=skill)
        flash('Your skill has been added!', 'success')
        return redirect(url_for('account'))
    return render_template('skills.html', skills=skills, title='New Joke',
                           form=form, legend='Joke submission')


@app.route("/leaderboards", methods=['GET', 'POST'])
def leaderboards():
    logging.info('{} viewed leaderboards'.format(current_user.get_id()))
    table_rows = 5
    query = Joke.query.descending('score').limit(table_rows)
    users = []
    for item in query:
        user = User.query.get(item.author)
        users.append(user.username)
    jokes = [dict(content='', author='', score='') for row in range(table_rows)]
    row = 0
    for value in query:
        jokes[row]['content'] = value.content
        jokes[row]['author'] = users[row]
        jokes[row]['score'] = value.score
        row += 1
    return render_template('leaderboards.html', jokes=jokes)


@app.route('/major', methods=['GET', 'POST'])
@login_required
def major():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # a=Major(name='Engineering')
    # b=Major(name='anthropology')
    # c=Major(name='Business')
    # db.session.add(a)
    # db.session.add(b)
    # db.session.add(c)
    # db.session.commit()
    form = MajorForm()
    if request.method == 'POST':
        # major_id = Major.query.filter_by(name=form.major.data).first()
        current_user.major_id = form.major.data
        db.session.commit()
        flash('Major changed successfully', 'success')
        return redirect('account')
    return render_template('major.html', form=form)
