from .database import db

class ListType(db.Model):
    __tablename__ = "list_type"
    id = db.Column(db.Integer, primary_key=True)
    name_list = db.Column(db.String(50), unique=True, nullable=False)  # favoris, a_voir, deja_vu, en_cours


class UserList(db.Model):
    __tablename__ = "user_list"
    uid = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, nullable=False)
    id_list_type = db.Column(db.Integer, db.ForeignKey("list_type.id", ondelete="CASCADE"), nullable=False)
    id_movie = db.Column(db.Integer, nullable=False)
    
    # Contrainte d'unicité combinée
    __table_args__ = (
        db.UniqueConstraint("id_list_type", "id_movie", "id_user", name="unique_user_list_movie"),
    )
