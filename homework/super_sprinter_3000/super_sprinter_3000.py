import os
from peewee import *
from super_sprinter_3000.connectdatabase import ConnectDatabase
from super_sprinter_3000.models import UserStories
from flask import Flask, request, g, redirect, url_for, \
    render_template, flash


app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'super_sprinter_3000.db'),
    SECRET_KEY='development key'
))
app.config.from_envvar('SUPER_SPRINTER_3000_SETTINGS', silent=True)


def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([UserStories], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
def go_to_list_page():
    return redirect(url_for('list_stories'))


@app.route('/and/list')
def list_stories():
    table = UserStories.select().order_by(UserStories.id.asc())
    return render_template('list.html', table=table)


@app.route('/story')
def add_new_story():
    title = "- Add new story"
    return render_template('form.html', title=title)


@app.route('/create', methods=['POST'])
def create_story():
    new_story = UserStories.create(story_title=request.form['story_title'],
                                   user_story=request.form['user_story'],
                                   acceptance_criteria=request.form['acceptance_criteria'],
                                   business_value=request.form['business_value'],
                                   estimation=request.form['estimation'],
                                   status=request.form['status'])
    new_story.save()
    flash('New story was successfully saved.')
    return redirect(url_for('list_stories'))


@app.route('/story/<int:story_id>', methods=['GET', 'POST'])
def get_story_for_edit(story_id):
    story_query = UserStories.select().where(UserStories.id == story_id)
    title = "- Edit story"
    return render_template('form.html', story=story_query[0], title=title)


@app.route('/edit/<int:story_id>', methods=['POST'])
def edit_story(story_id):
    updated_story = UserStories.update(story_title=request.form['story_title'],
                                       user_story=request.form['user_story'],
                                       acceptance_criteria=request.form['acceptance_criteria'],
                                       business_value=request.form['business_value'],
                                       status=request.form['status']).where(UserStories.id == story_id)
    updated_story.execute()
    flash('The story was successfully updated.')
    return redirect(url_for('list_stories'))


@app.route('/delete/<int:story_id>', methods=['GET', 'POST'])
def delete_story(story_id):
    del_story = UserStories.delete().where(UserStories.id == story_id)
    del_story.execute()
    return redirect(url_for('list_stories'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)