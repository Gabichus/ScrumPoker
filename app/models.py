from app import db


task_child = db.Table('task_child',
    db.Column('task_parent_id', db.Integer, db.ForeignKey('task.id')),
    db.Column('task_child_id', db.Integer, db.ForeignKey('task.id'))
)

member = db.Table('member',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    description = db.Column(db.Text, nullable=True)
    time = db.Column(db.Integer, nullable=False, default=0)
    voting_status = db.Column(db.Boolean, nullable=False, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    flag = db.Column(db.Boolean, nullable=False, default=False)
    voting = db.relationship('TaskVoting', backref='task', lazy='dynamic')

    child_task = db.relationship(
        'Task', secondary=task_child,
        primaryjoin=(task_child.c.task_parent_id == id),
        secondaryjoin=(task_child.c.task_child_id == id),
        backref=db.backref('parent', lazy='dynamic'), lazy='dynamic')


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    description = db.Column(db.Text, nullable=True)
    tasks = db.relationship('Task', backref='project', lazy='dynamic')
    time = db.Column(db.Integer, nullable=False, default=0)
    flag = db.Column(db.Boolean, nullable=False, default=False)
    members = db.relationship('User', secondary=member, backref=db.backref('projects', lazy='dynamic'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gmail = db.Column(db.String(64), nullable=False)
    token = db.Column(db.Text, nullable=True)
    old_token = db.Column(db.Text, nullable=True)
    voting = db.relationship('TaskVoting', backref='user', lazy='dynamic')
    admin = db.Column(db.Boolean, nullable=False, default=False)


class TaskVoting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    time = db.Column(db.Integer, nullable=False)