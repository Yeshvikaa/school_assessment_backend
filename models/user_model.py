from database.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    age = db.Column(db.String(10))
    qualification = db.Column(db.String(100))
    school = db.Column(db.String(100))
    years_exp = db.Column(db.String(10))
    father_occ = db.Column(db.String(100))
    father_phone = db.Column(db.String(20))
    mother_occ = db.Column(db.String(100))
    mother_phone = db.Column(db.String(20))
    security_destination = db.Column(db.String(100))
    security_food = db.Column(db.String(100))
    security_hobby = db.Column(db.String(100))
    student_id = db.Column(db.String(50))

    def __init__(self, role, name, email, password, phone=None, age=None, qualification=None,
                 school=None, years_exp=None, father_occ=None, father_phone=None,
                 mother_occ=None, mother_phone=None, security_destination=None,
                 security_food=None, security_hobby=None,student_id=None):
        self.role = role
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.age = age
        self.qualification = qualification
        self.school = school
        self.years_exp = years_exp
        self.father_occ = father_occ
        self.father_phone = father_phone
        self.mother_occ = mother_occ
        self.mother_phone = mother_phone
        self.security_destination = security_destination
        self.security_food = security_food
        self.security_hobby = security_hobby
        self.student_id = student_id