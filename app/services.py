from app import ma, db
from app.models import Task, Project, TaskVoting
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
                'description': pr.description, 'child_task': tasksJson, 'flag': pr.flag, 'time': pr.time}
    return project


def deleteTaskRecursion(result):
    for a in result['child_task']:
        deleteTaskRecursion(a)

        task = Task.query.get(a.get('id'))
        TaskVoting.query.filter_by(task_id=a.get('id')).delete()
        task.child_category = []
        db.session.commit()

        db.session.delete(task)
        db.session.commit()


def recursiveCalcTimeTasks(task):
    total = 0
    for t in task['child_task']:
        recursiveCalcTimeTasks(t)
        time = t['time']
        total = total + t['time']
    if task['child_task']:
        task['time'] = total
        parentTask = Task.query.get(task['id'])
        parentTask.time = total
        db.session.commit()


def taskCalcTime(id):
    t = Task.query.get(id)
    if not id:
        return None
    time = [x.time for x in t.voting]
    time = sum(time) / len(time)
    return time


def projectTimeCalc(id):
    pr = Project.query.get(id)
    if not pr:
        return None
    total = 0
    for t in pr.tasks.filter_by(parent = None):
        sh = TaskSchema()
        shTask = sh.dump(Task.query.get(t.id))
        recursiveCalcTimeTasks(shTask)
        total = total + t.time
    pr.time = total
    db.session.commit()

