from app import utils
from flask import render_template, Blueprint, request, send_from_directory, jsonify, Response
from pathlib import Path
from app.models import db, Project, Task
import os
blueprint = Blueprint('resources', __name__)

import numpy as np
################
#### routes ####
################

MEDIA_FOLDER = '/mnt/e/Datasets/selfie2anime/testA'

@blueprint.route('/get-data/<path:filename>')
def download_file(filename):
    existing_project = Project.query.filter(
            Project.name == "PROJECT_NAME"
        ).first()

    MEDIA_FOLDER = existing_project.storage_location
    return send_from_directory(MEDIA_FOLDER, filename, as_attachment=False)

@blueprint.route('/add-local-storage', methods=['POST'])
def add_local_storage():
    data = request.get_json(force=True)
    status = int(Path(data['location']).is_dir())
    if status==1:
        existing_project = Project.query.filter(
            Project.name == "PROJECT_NAME"
        ).first()

        if existing_project:
            existing_project.storage_location = data['location']
            existing_project.question = data['question']
            Task.query.delete()
        for filename in os.listdir(data['location']):
            task = Task.query.filter(
            Task.image == filename).first()
            if not task:
                task = Task(
                image=filename)
                db.session.add(task)  # Adds new Project record to database
        if not existing_project.last_task_id:
            obj = db.session.query(Task).order_by(Task.id).first()
            existing_project.last_task_id = obj.id
        
        db.session.commit()  # Commits all changes
    
    return jsonify({'status': status})

@blueprint.route('/check-local-storage', methods=['POST'])
def check_local_storage():
    data = request.get_json(force=True)
    status = int(Path(data['location']).is_dir())

    return jsonify({'status': status})


@blueprint.route('/large.csv')
def generate_large_csv():
    data1 = np.load('/mnt/e/img.npy')
    def generate():
        for i in range(data1.shape[-1]):
            yield data1[:,:,i].tostring()
            
    return Response(generate(), mimetype='text/csv')


