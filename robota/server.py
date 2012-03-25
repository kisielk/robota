#!/usr/bin/env python
from .app import app, db
from .db import Job
from flask import session, abort, request, flash, redirect, render_template, url_for, g, jsonify


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

    job = Job(**request.form.to_dict(flat=True))
    db.session.add(job)
    db.session.commit()

    flash('New job was successfully created', 'success')
    return redirect(url_for('show_jobs'))


@app.route('/jobs/', methods=['GET'])
def show_jobs():
    jobs = Job.query.all()
    return render_template('show_jobs.html', jobs=jobs)


@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        Job.query(id=job_id).delete()
    except:
        return jsonify(False)
    return jsonify(True)


if __name__ == "__main__":
    app.run()
