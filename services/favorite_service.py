from models import Favorite, db, Movie, Series


def add_to_favorites(user_id, content_id, content_type):
    favorite = Favorite(user_id=user_id, content_id=content_id, content_type=content_type)
    db.session.add(favorite)
    db.session.commit()
    return [{"message": "Content added to favorites", "favorite_id": favorite.favorite_id}]


def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    results = []
    for fav in favorites:
        content = None
        if fav.content_type == 'movie':
            content = Movie.query.get(fav.content_id)
        elif fav.content_type == 'series':
            content = Series.query.get(fav.content_id)

        if content:
            results.append({
                "favorite_id": fav.favorite_id,
                "content_id": fav.content_id,
                "content_type": fav.content_type,
                "content_title": content.title  # İçeriğin başlığını ekleyin
            })
        else:
            # İçerik bulunamazsa, başlık yerine None veya uygun bir mesaj ekleyin
            results.append({
                "favorite_id": fav.favorite_id,
                "content_id": fav.content_id,
                "content_type": fav.content_type,
                "content_title": "Content not found"
            })

    return results


def remove_from_favorites(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return {"message": "Content removed from favorites"}
    else:
        return {"message": "Favorite not found"}
