from app import ma
from app.models import Task, Project
from sqlalchemy import asc


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = Task

    child_task = ma.Nested('TaskSchema', many=True, only=(
        'id', 'name', 'description', 'voting_status', 'time' , 'child_task', 'parent', 'flag'))


def getProjectTasks(id):
    allTask = [t for t in Task.query.filter_by(
        project_id=id).order_by(asc(Task.id)) if not t.parent.all()]
    sh = TaskSchema()
    tasksJson = []
    for task in allTask:
        json = sh.dump(task)
        tasksJson.append(json)
    pr = Project.query.get(id)
    project = {'id': pr.id, 'name': pr.name,
                'description': pr.description, 'child_task': tasksJson, 'flag': pr.flag}
    return project


def deleteTaskRecursion(result):
    for a in result['child_task']:
        deleteTaskRecursion(a)

        task = Task.query.get(a.get('id'))

        task.child_category = []
        db.session.commit()

        db.session.delete(task)
        db.session.commit()
