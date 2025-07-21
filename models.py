# models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    Role = Column(String(50), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

class Course(Base):
    __tablename__ = 'Courses'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(255), nullable=False)
    Description = Column(Text)
    Level = Column(String(50))
    CreatedAt = Column(DateTime, default=datetime.utcnow)

class Lesson(Base):
    __tablename__ = 'Lessons'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    CourseId = Column(Integer, ForeignKey('Courses.Id'), nullable=False)
    Title = Column(String(255), nullable=False)
    Content = Column(Text)
    LessonOrder = Column(Integer)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

class Enrollment(Base):
    __tablename__ = 'Enrollments'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer, ForeignKey('Users.Id'), nullable=False)
    CourseId = Column(Integer, ForeignKey('Courses.Id'), nullable=False)
    EnrolledAt = Column(DateTime, default=datetime.utcnow)
    Progress = Column(Float, default=0)

class QuizAttempt(Base):
    __tablename__ = 'QuizAttempts'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    LessonId = Column(Integer, ForeignKey('Lessons.Id'), nullable=False)
    UserId = Column(Integer, ForeignKey('Users.Id'), nullable=False)
    Score = Column(Float, default=0)
    AttemptedAt = Column(DateTime, default=datetime.utcnow)

class Submission(Base):
    __tablename__ = 'Submissions'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    LessonId = Column(Integer, ForeignKey('Lessons.Id'), nullable=False)
    UserId = Column(Integer, ForeignKey('Users.Id'), nullable=False)
    Content = Column(Text)
    Grade = Column(Float)
    SubmittedAt = Column(DateTime, default=datetime.utcnow)


class UserAction(Base):
    __tablename__ = 'UserActions'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer, ForeignKey('Users.Id'), nullable=False)
    LessonId = Column(Integer, ForeignKey('Lessons.Id'))
    Action = Column(String(255), nullable=False)
    Metadata = Column(Text)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

class UserLessonQValue(Base):
    __tablename__ = 'UserLessonQValues'

    UserId = Column(Integer, ForeignKey('Users.Id'), primary_key=True)
    LessonId = Column(Integer, ForeignKey('Lessons.Id'), primary_key=True)
    QValue = Column(Float, default=0)
    LastUpdated = Column(DateTime, default=datetime.utcnow)

class RLModel(Base):
    __tablename__ = 'RLModels'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Version = Column(String(50), nullable=False)
    FilePath = Column(String(255), nullable=False)
    Note = Column(Text)
    CreatedAt = Column(DateTime, default=datetime.utcnow)


class UserEmbedding(Base):
    __tablename__ = 'UserEmbeddings'

    UserId = Column(Integer, ForeignKey('Users.Id'), primary_key=True)
    Embedding = Column(String)  # Hoặc LargeBinary nếu bạn dùng VARBINARY
    UpdatedAt = Column(DateTime, default=datetime.utcnow)
