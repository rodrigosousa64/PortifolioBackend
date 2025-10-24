from datetime import datetime
from app import db  # Importa a instância db do app




class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    technologies = db.Column(db.JSON, nullable=False)  
    description = db.Column(db.String(500), nullable=False)
    git_link = db.Column(db.String(200), nullable=True)
    hosted_link = db.Column(db.String(200), nullable=True)
    post_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Project id={self.id} name='{self.name}'>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "technologies": self.technologies,
            "description": self.description,
            "git_link": self.git_link,
            "hosted_link": self.hosted_link,
            "post_date": self.post_date.isoformat() if self.post_date else None,
            "image_url": self.image_url
        }