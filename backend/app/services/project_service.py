from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate

def create_project(db: Session, user_id: int, project_data: ProjectCreate):
    project = Project(
        user_id=user_id,
        name=project_data.name,
        description=project_data.description
    )

    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_user_projects(db: Session, user_id: int):
    return (
        db.query(Project)
        .filter(Project.user_id == user_id)
        .order_by(Project.created_at.desc())
        .all()
    )

def get_project_by_id(db: Session, project_id: int, user_id: int):
    return (
        db.query(Project)
        .filter(Project.project_id == project_id, Project.user_id == user_id)
        .first()
    )