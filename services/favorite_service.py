from models import Favorite, db


def add_to_favorites(user_id, content_id, content_type):
    favorite = Favorite(user_id=user_id, content_id=content_id, content_type=content_type)
    db.session.add(favorite)
    db.session.commit()
    return {"message": "Content added to favorites"}


def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return [{"favorite_id": fav.favorite_id, "content_id": fav.content_id, "content_type": fav.content_type} for fav in favorites]

def remove_from_favorites(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return {"message": "Content removed from favorites"}
    return {"message": "Favorite not found"}

