from flask import render_template, Blueprint, request ,redirect,jsonify,send_from_directory
from app.forms import *
from app.models import db, Project, Task, serialize
from datetime import datetime as dt
import json
import os
from config import Config
import pandas as pd
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter
blueprint = Blueprint('pages', __name__)


################
#### routes ####
################

@blueprint.route('/tasks/label/', methods=["GET", "POST"])
@login_required
def label_tasks():
    existing_project = Project.query.filter(
            Project.name == "PROJECT_NAME"
        ).first()
    if request.method=="POST":
        data = request.get_json(force=True)
        

        unlabeld_task = Task.query.filter(
            Task.id == data['task_id']
        ).first()

        unlabeld_task.label = data['label']
        unlabeld_task.question = existing_project.question
        unlabeld_task.user_name = current_user.user_name
        unlabeld_task.date = dt.now()
        if data['next_task']!=0:
            existing_project.last_task_id = data['next_task']
        db.session.commit()  # Commits all changes

        return jsonify({'status': 1})

        
    task_id = request.args.get('task')
    if task_id is not None:
        unlabeld_task = Task.query.filter(
            Task.id == task_id
        ).first()

        if unlabeld_task:
            
            prev_task = db.session.query(Task).order_by(Task.id.desc()).filter(Task.id < unlabeld_task.id).first()

            next_task = db.session.query(Task).order_by(Task.id.asc()).filter(Task.id > unlabeld_task.id).first()
            if not prev_task:
                prev_task = 0
            else:
                prev_task = prev_task.id

            if not next_task:
                next_task = 0
            else:
                next_task = next_task.id

            return render_template('pages/placeholder.label-task.html', task = unlabeld_task, prev_task = prev_task, next_task = next_task, project = existing_project)
    return redirect('/tasks')

@blueprint.route('/tasks/export/')
@login_required
def export_tasks():
    
    type = request.args.get('type')
    tasks = Task.query.all()
    tasks_json = [serialize(task) for task in tasks if task.label]

    if type=='json':
        with open(os.path.join(Config.TEMP_DIR,'result.json'), 'w') as f:
            json.dump(tasks_json , f)
        return send_from_directory(Config.TEMP_DIR, 'result.json', as_attachment=True)

    else:
        df = pd.DataFrame(tasks_json)
        df.to_csv(os.path.join(Config.TEMP_DIR,'result.csv'),index=False)
        return send_from_directory(Config.TEMP_DIR, 'result.csv', as_attachment=True)


@blueprint.route('/tasks')
@login_required
def get_tasks():
    existing_project = Project.query.filter(
            Project.name == "PROJECT_NAME"
        ).first()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    tasks = Task.query.paginate(page,per_page,error_out=False).items
    total = db.session.query(Task).count()
    pagination = Pagination(page=page, total=total, record_name='tasks',css_framework='bootstrap4')
    return render_template('pages/placeholder.tasks.html', tasks = tasks, project = existing_project, pagination=pagination)


@blueprint.route('/about')
@login_required
def about():
    return render_template('pages/placeholder.about.html')

@blueprint.route('/add-storage', methods=('GET', 'POST'))
@login_required
def add_storage():
    return render_template('pages/placeholder.add-storage.html')


