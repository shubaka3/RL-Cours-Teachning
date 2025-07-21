# api.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Course, Lesson, Enrollment, QuizAttempt, Submission
from rl_agent import BanditAgent

agent = BanditAgent()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/lessons")
def get_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()

@router.get("/enrollments")
def get_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()

@router.get("/quizattempts")
def get_quizattempts(db: Session = Depends(get_db)):
    return db.query(QuizAttempt).all()

@router.get("/submissions")
def get_submissions(db: Session = Depends(get_db)):
    return db.query(Submission).all()

from fastapi import HTTPException

@router.get("/users/{user_id}/learning-path")
def get_learning_path(user_id: int, db: Session = Depends(get_db)):
    # 1. Tìm user
    user = db.query(User).filter(User.Id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 2. Lấy các khoá học mà user đã enroll
    enrollments = db.query(Enrollment).filter(Enrollment.UserId == user_id).all()
    if not enrollments:
        return []

    learning_path = []
    for enrollment in enrollments:
        course = db.query(Course).filter(Course.Id == enrollment.CourseId).first()
        if not course:
            continue

        lessons = (
            db.query(Lesson)
            .filter(Lesson.CourseId == course.Id)
            .order_by(Lesson.LessonOrder)
            .all()
        )

        lessons_data = [
            {
                "LessonId": lesson.Id,
                "Title": lesson.Title,
                "LessonOrder": lesson.LessonOrder,
            }
            for lesson in lessons
        ]

        learning_path.append({
            "CourseId": course.Id,
            "CourseTitle": course.Title,
            "Lessons": lessons_data
        })

    return learning_path


@router.get("/users/{user_id}/personalized-learning-path")
def get_personalized_learning_path(user_id: int, db: Session = Depends(get_db)):
    # 1. Tìm user
    user = db.query(User).filter(User.Id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 2. Lấy các khoá học mà user đã enroll
    enrollments = db.query(Enrollment).filter(Enrollment.UserId == user_id).all()
    if not enrollments:
        return []

    personalized_path = []

    for enrollment in enrollments:
        course = db.query(Course).filter(Course.Id == enrollment.CourseId).first()
        if not course:
            continue

        lessons = (
            db.query(Lesson)
            .filter(Lesson.CourseId == course.Id)
            .order_by(Lesson.LessonOrder)
            .all()
        )

        lessons_data = []

        for lesson in lessons:
            # Lấy attempt gần nhất của user cho lesson này
            attempt = (
                db.query(QuizAttempt)
                .filter(QuizAttempt.UserId == user_id, QuizAttempt.LessonId == lesson.Id)
                .order_by(QuizAttempt.AttemptedAt.desc())
                .first()
            )

            # Quy tắc "ML giả lập":
            if attempt:
                if attempt.Score >= 80:
                    status = "mastered"  # Có thể bỏ qua
                else:
                    status = "retry"     # Nên học lại
            else:
                status = "not_attempted"  # Nên học tiếp

            lessons_data.append({
                "LessonId": lesson.Id,
                "Title": lesson.Title,
                "LessonOrder": lesson.LessonOrder,
                "Status": status
            })

        personalized_path.append({
            "CourseId": course.Id,
            "CourseTitle": course.Title,
            "Lessons": lessons_data
        })

    return personalized_path


@router.get("/users/{user_id}/recommendations2")
def get_recommendations2(user_id: int, k: int = 5, db: Session = Depends(get_db)):
    # 1. Kiểm tra user tồn tại
    user = db.query(User).filter(User.Id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Lấy Q-values của user
    q_values = (
        db.query(UserLessonQValue)
        .filter(UserLessonQValue.UserId == user_id)
        .order_by(UserLessonQValue.QValue.desc())
        .limit(k)
        .all()
    )

    if not q_values:
        return {"message": "No recommendations yet"}

    recommendations = []

    for qv in q_values:
        lesson = db.query(Lesson).filter(Lesson.Id == qv.LessonId).first()
        if lesson:
            course = db.query(Course).filter(Course.Id == lesson.CourseId).first()
            recommendations.append({
                "LessonId": lesson.Id,
                "LessonTitle": lesson.Title,
                "CourseId": course.Id if course else None,
                "CourseTitle": course.Title if course else None,
                "QValue": qv.QValue
            })

    return recommendations

# Lấy hành vi user (UserActions)


@router.get("/users/{user_id}/actions")
def get_user_actions(user_id: int, db: Session = Depends(get_db)):
    actions = db.query(UserAction).filter(UserAction.UserId == user_id).all()
    return [{"Action": a.Action, "LessonId": a.LessonId, "Metadata": a.Metadata} for a in actions]

# Xem Q-values
@router.get("/users/{user_id}/qvalues")
def get_user_qvalues(user_id: int, db: Session = Depends(get_db)):
    qvalues = db.query(UserLessonQValue).filter(UserLessonQValue.UserId == user_id).all()
    return [{"LessonId": q.LessonId, "QValue": q.QValue} for q in qvalues]


# RLModels
@router.get("/rlmodels")
def get_rl_models(db: Session = Depends(get_db)):
    models = db.query(RLModel).all()
    return [{"Version": m.Version, "FilePath": m.FilePath, "Note": m.Note} for m in models]

# Lấy embedding của user

@router.get("/users/{user_id}/embedding")
def get_user_embedding(user_id: int, db: Session = Depends(get_db)):
    embedding = db.query(UserEmbedding).filter(UserEmbedding.UserId == user_id).first()
    if not embedding:
        raise HTTPException(status_code=404, detail="Embedding not found")
    return {"UserId": embedding.UserId, "Embedding": embedding.Embedding}

@router.post("/users/{user_id}/lessons/{lesson_id}/reward")
def update_q_value(user_id: int, lesson_id: int, reward: float, db: Session = Depends(get_db)):
    # Load Q-values hiện tại từ DB
    q_entry = db.query(UserLessonQValue).filter(
        UserLessonQValue.UserId == user_id,
        UserLessonQValue.LessonId == lesson_id
    ).first()

    agent.Q = {}
    if q_entry:
        agent.Q[lesson_id] = q_entry.QValue

    # Update bằng agent logic
    agent.update(lesson_id, reward)

    # Ghi lại DB
    if q_entry:
        q_entry.QValue = agent.Q[lesson_id]
    else:
        from models import UserLessonQValue
        new_q = UserLessonQValue(UserId=user_id, LessonId=lesson_id, QValue=agent.Q[lesson_id])
        db.add(new_q)

    db.commit()
    return {"LessonId": lesson_id, "UpdatedQValue": agent.Q[lesson_id]}