from tessera import db
from werkzeug import check_password_hash, generate_password_hash

class Base(db.Model):
    """Base class that all models are derived from.
    
    It defines the id, created_at, and updated_at fields for all models.
    """

    __abstract__ = True

    id         = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                        onupdate=db.func.current_timestamp())

class User(Base):
    """User represents a user of our application."""

    full_name = db.Column(db.String(250), nullable=False)
    email     = db.Column(db.String(128),  nullable=False, unique=True)

    username  = db.Column(db.String(128),  nullable=False, unique=True)
    password  = db.Column(db.String(192),  nullable=False)

    def __init__(self, username, email, password, full_name):
        self.full_name = full_name
        self.username  = username
        self.email     = email
        self.set_password(password)

    def set_password(pw):
        self.password = generate_password_hash(pw)

    def check_password(pw):
        return check_password_hash(self.password, pw)

    def __repr__(self):
        return "<User %r>" % (self.name)

class Ticket(Base):
    """Ticket represents a project's ticket."""

    ticket_key  = db.Column(db.String(100), nullable=False, unique=True) # I mean jesus christ how many digits
    summary     = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text())

    def __init__(self, ticket_key, summary, description):
        self.ticket_key  = ticket_key
        self.summary     = summary
        self.description = description

    def __repr__(self):
        return "<Ticket %r>" % (self.ticket_key)

class Project(Base):
    """Project is a container for tickets."""
    pkey     = db.Column(db.String(6), nullable=False, unique=True)
    name     = db.Column(db.String(250), nullable=False)
    repo     = db.Column(db.String(250))
    homepage = db.Column(db.String(250))
    team_id  = db.Column(db.Integer, db.foreignkey('team.id'))

    tickets = db.relationship('Ticket', backref='project', lazy='dynamic')
    members = db.relationship('Membership', backref='project', lazy='dynamic')

    def __init__(self, pkey, name, repo='', homepage=''):
        self.pkey     = pkey
        self.name     = name
        self.repo     = repo
        self.homepage = homepage

    def __repr__(self):
        return "<Project %r>" % (self.pkey)

class Team(Base):
    """Team is a container for projects."""
    name     = db.Column(db.String(120), nullable=False, unique=True)
    url_stub = db.Column(db.String(150), nullable=False, unique=True)
    icon     = db.Column(db.String(150))    

    projects = db.relationship('Project', backref='team', lazy='dynamic')
    
    def __init__(self, name, icon=""):
        self.name     = name
        self.url_stub = name.lower().replace(" ", "-")
        icon          = icon

    def __repr__(self):
        return "<Team %r>" % (self.name)


class Membership(Base):
    """Membership is used to control access and permissions for a project or
    team.
    
    Permission levels are stored as Integers and there are three permission
    levels.

    0 = User
    1 = Contributor
    2 = Administrator
    """
    team_id     = db.Column(db.Integer, db.foreignkey('team.id'))
    project_id  = db.Column(db.Integer, db.foreignkey('project.id'))
    user_id     = db.Column(db.Integer, db.foreignkey('user.id'))

    permission_level = db.Column(db.Integer)

    def __init__(self, perm):
        permission_level = perm

    def __repr__(self):
        return "<Membership %r %r %r %r>"  % (self.team_id, self.project_id,
                                              self.user_id,
                                              self.permission_level)
