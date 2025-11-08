from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('reviews', description='Review operations')

user_model = api.model('ReviewUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email'),
})

place_model = api.model('ReviewPlace', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Place title'),
    'price': fields.Float(description='Price per night'),
})

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID'),
})

@api.route('/')
class ReviewList(Resource):

    @api.expect(review_model)
    @api.response(201, 'Review creado con éxito')
    @api.response(400, 'Datos inválidos')
    def post(self):
        data = api.payload or {}

        user = facade.get_user(data.get("user_id"))
        if not user:
            return {"error": "User no existe"}, 400

        place = facade.get_place(data.get("place_id"))
        if not place:
            return {"error": "Place no existe"}, 400

        new_review = facade.create_review(data)

        return {
            "id": new_review.id,
            "text": new_review.text,
            "created_at": new_review.created_at,
            "user": {
                "id": user.id,
                "first_name": getattr(user, "first_name", None),
                "last_name": getattr(user, "last_name", None),
                "email": getattr(user, "email", None),
            },
            "place": {
                "id": place.id,
                "title": getattr(place, "title", None),
                "price": getattr(place, "price", None),
            },
        }, 201

    @api.response(200, 'Lista de reviews recuperada')
    def get(self):
        reviews = facade.get_all_reviews() or []

        return [
            {
                "id": r.id,
                "text": r.text,
                "created_at": r.created_at,
                "user": {
                    "id": r.user.id,
                    "first_name": getattr(r.user, "first_name", None),
                    "last_name": getattr(r.user, "last_name", None),
                    "email": getattr(r.user, "email", None),
                },
                "place": {
                    "id": r.place.id,
                    "title": getattr(r.place, "title", None),
                    "price": getattr(r.place, "price", None),
                },
            }
            for r in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):

    @api.response(200, 'Review encontrado')
    @api.response(404, 'Review no encontrado')
    def get(self, review_id):
        """Obtener un review por ID"""
        r = facade.get_review(review_id)
        if not r:
            return {"error": "Review no encontrado"}, 404

        return {
            "id": r.id,
            "text": r.text,
            "created_at": r.created_at,
            "user": {
                "id": r.user.id,
                "first_name": getattr(r.user, "first_name", None),
                "last_name": getattr(r.user, "last_name", None),
                "email": getattr(r.user, "email", None),
            },
            "place": {
                "id": r.place.id,
                "title": getattr(r.place, "title", None),
                "price": getattr(r.place, "price", None),
            },
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review actualizado')
    @api.response(404, 'Review no encontrado')
    def put(self, review_id):
        """Actualizar review"""
        r = facade.get_review(review_id)
        if not r:
            return {"error": "Review no encontrado"}, 404

        data = api.payload or {}

        try:
            facade.update_review(review_id, data)
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

        r = facade.get_review(review_id)

        return {
            "id": r.id,
            "text": r.text,
            "created_at": r.created_at,
            "user": {
                "id": r.user.id,
                "first_name": getattr(r.user, "first_name", None),
                "last_name": getattr(r.user, "last_name", None),
                "email": getattr(r.user, "email", None),
            },
            "place": {
                "id": r.place.id,
                "title": getattr(r.place, "title", None),
                "price": getattr(r.place, "price", None),
            },
        }, 200

    @api.response(204, 'Review borrado')
    @api.response(404, 'Review no encontrado')
    def delete(self, review_id):
        ok = facade.delete_review(review_id)
        if not ok:
            return {"error": "Review no encontrado"}, 404
        return "", 204
