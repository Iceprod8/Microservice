from .database import db

class ListType(db.Model):
    __tablename__ = "type_list"
    id = db.Column(db.Integer, primary_key=True)
    name_list = db.Column(db.String(50), unique=True, nullable=False)  # favoris, a_voir, deja_vu, en_cours
    lists = db.relationship("UserList", back_populates="type_list")


class UserList(db.Model):
    __tablename__ = "user_list"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.uid", ondelete="CASCADE"))
    id_list_type = db.Column(db.Integer, db.ForeignKey("list_type.id", ondelete="CASCADE"))
    user = db.relationship("User", back_populates="lists")
    list_type = db.relationship("ListType", back_populates="type")
    movies = db.relationship("ListMovie", back_populates="user_list", cascade="all, delete-orphan")


class ListMovie(db.Model):
    __tablename__ = "movie_list"
    id = db.Column(db.Integer, primary_key=True)
    id_user_list = db.Column(db.Integer, db.ForeignKey("user_list.id", ondelete="CASCADE"))
    id_movie = db.Column(db.Integer, nullable=False)  # Référence l'ID d'un film dans la base Movie
    user_list = db.relationship("UserList", back_populates="movies")