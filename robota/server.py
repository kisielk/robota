#!/usr/bin/env python
from flask import Flask, session, abort, request, flash, redirect, render_template, url_for, g, jsonify

from .db import connect_db

DEBUG = True
SECRET_KEY = 'secret'
USERNAME = 'kamil'
PASSWORD = 'kamil'
HOST = '0.0.0.0'
DATABASE = 'state.db'

app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.db = connect_db(app.config['DATABASE'])


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in', 'success')
            return redirect(url_for('show_jobs'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'info')
    return redirect(url_for('show_jobs'))


@app.route('/jobs/', methods=['POST'])
def create_job():
    if not session.get('logged_in'):
        abort(401)

    g.db.execute('insert into jobs (name, script) values (?, ?)',
                [request.form['name'], request.form['script']])
    g.db.commit()
    flash('New job was successfully created', 'success')
    return redirect(url_for('show_jobs'))


@app.route('/jobs/', methods=['GET'])
def show_jobs():
    cur = g.db.execute('select id, name from jobs order by id desc')
    jobs = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
    return render_template('show_jobs.html', jobs=jobs)


@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        cur = g.db.execute('delete from jobs where id = ?', job_id)
        cur.fetchall()
    except:
        return jsonify(False)
    return jsonify(True)


if __name__ == "__main__":
    app.run()
