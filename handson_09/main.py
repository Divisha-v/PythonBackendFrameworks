from fastapi import FastAPI,BackgroundTasks
from schemas import CourseCreate
from schemas import CourseResponse
from database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy import select
from models import Course,Student,Enrollment
from schemas import StudentCreate,StudentResponse
from models import Enrollment
from schemas import EnrollmentCreate, EnrollmentResponse
from fastapi import Request
from sqlalchemy import func,or_
from typing import Optional

from fastapi import FastAPI

app = FastAPI(
    title="Course Management API",
    description="REST API for managing departments, courses, students and enrollments.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    }
)

@app.post("/api/v1/auth/register/")
async def register(
    user: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
    select(User).where(
        User.email == user.email
    )
)

existing = result.scalar_one_or_none()

if existing:
    raise HTTPException(
        status_code=409,
        detail="Email already registered"
    )
hashed = get_password_hash(
    user.password
)
new_user = User(
    email=user.email,
    hashed_password=hashed
)
db.add(new_user)

await db.commit()

await db.refresh(new_user)

return new_user
@app.get("/")
def home():
    return{
        "message":"API running"
    }
@app.post("/api/v1/courses/",response_model=CourseResponse,status_code=status.HTTP_201_CREATED)
async def create_course(
    course:CourseCreate,
    db: AsyncSession = Depends(get_db)
):
    db_course = Course(
        name= course.name,
        code= course.code,
        credits = course.credits,
        department_id = course.department_id
    )
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@app.patch("/api/v1/courses/{id}")
async def patch_course(
    id: int,
    course: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == id)
    )

    existing_course = result.scalar_one_or_none()

    if existing_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    update_data = course.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_course, key, value)

    await db.commit()
    await db.refresh(existing_course)

    return existing_course

@app.get("/api/v1/courses/{id}",response_model=CourseResponse)
async def get_courses(
    request: Request,
    page: int = 1,
    page_size: int = 2,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == id)
    )
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="course not found"
        )
    return course

@app.get("/api/v1/courses/")
async def get_courses(skip:int=0,limit:int=10):
    return{
        "skip" : skip,
        "limit":limit
    }

@app.put("/api/v1/courses/{id}",response_model=CourseResponse)
async def update_course(
    id:int,
    course:CourseCreate,
    db:AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == id)
    )

    db_course = result.scalar_one_or_none()
    if db_course is None:
        raise HTTPException(
            status_code=404,
            detail="not found"
        )
    db_course.name = course.name
    db_course.code = course.code
    db_course.department_id = course.department_id

    await db.commit()
    await db.refresh(db_course)
    return db_course

@app.delete("/api/v1/courses/{id}")
async def delete_course(
    id :int,
    db:AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == id)
    )
    course = result.scalar_one_or_more()
    if course is None:
        raise HTTPException(
            status_code = 404,
            detail="COURSE NOT FOUND"
        )
    await db.delete(course)
    await db.commit()

    return{
        "message":"course dleted succesfulluy"
    }

@app.get("/api/v1/course/{id}/students")
async def get_course_students(
    id : int,
    db: AsyncSessions = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id ==  id)

    )
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    result = await db.execute(
        select(Student).join(Enrollment).where(Enrollment.course_id == id)

    )
    students = result.scalars().all()
    return students

@app.post(
    "/api/v1/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):

    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        department_id=student.department_id,
        enrollment_year=student.enrollment_year
    )

    db.add(db_student)

    await db.commit()

    await db.refresh(db_student)

    return db_student

@app.get(
    "/api/v1/students/",
    response_model=list[StudentResponse]
)
async def get_students(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student)
    )

    students = result.scalars().all()

    return students


@app.get(
    "/api/v1/students/{id}",
    response_model=StudentResponse
)
async def get_student(
    id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(Student.id == id)
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


@app.put(
    "/api/students/{id}",
    response_model=StudentResponse
)
async def update_student(
    id: int,
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(Student.id == id)
    )

    db_student = result.scalar_one_or_none()

    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    db_student.first_name = student.first_name
    db_student.last_name = student.last_name
    db_student.email = student.email
    db_student.department_id = student.department_id
    db_student.enrollment_year = student.enrollment_year

    await db.commit()

    await db.refresh(db_student)

    return db_student


@app.delete(
    "/api/v1/students/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_student(
    id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(Student.id == id)
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    await db.delete(student)

    await db.commit()

@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks
):

    db_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    )

    db.add(db_enrollment)

    await db.commit()

    await db.refresh(db_enrollment)

    background_tasks.add_task(
        send_confirmation_email,
        "student@example.com"
    )

    return db_enrollment

@app.post("/api/v1/auth/login/")
async def login(
    user: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == user.email)
    )

    existing_user = result.scalar_one_or_none()

    if (
        existing_user is None or
        not verify_password(
            user.password,
            existing_user.hashed_password
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {"sub": existing_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    result = await db.execute(
        select(User).where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user