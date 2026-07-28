from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    code = db.Column(
        db.String(20),
        unique=True
    )

    credits = db.Column(
        db.Integer
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("department.id")
    )

    department = db.relationship("Department",back_population="courses")

class Department(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    courses = db.relationship("Course",back_populates="department")

