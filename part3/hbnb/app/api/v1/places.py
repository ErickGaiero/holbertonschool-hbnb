from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# --- MODELOS ---
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenity IDs")
})


# --- ENDPOINT /api/v1/places ---
@api.route('/')
class PlaceList(Resource):

    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place (only logged-in users)"""
        current_user_id = get_jwt_identity()
        place_data = api.payload

        # Validar usuario autenticado
        owner = facade.get_user(current_user_id)
        if not owner:
            return {'error': "User does not exist"}, 400

        # Validar amenities
        amenities = []
        for amenity_id in place_data.get("amenities", []):
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenities.append(amenity)
        place_data["amenities"] = amenities
        place_data["owner_id"] = current_user_id

        # Crear el lugar
        new_place = facade.create_place(place_data)

        return {
            "id": new_place.id,
            "owner": new_place.owner.to_dict() if hasattr(new_place.owner, 'to_dict') else new_place.owner_id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "amenities": [
                {
                    "id": amenity.id,
                    "name": getattr(amenity, "name", None)
                } for amenity in new_place.amenities
            ]
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            "id": place.id,
            "owner": place.owner.to_dict() if hasattr(place.owner, 'to_dict') else place.owner_id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "amenities": [
                {
                    "id": amenity.id,
                    "name": getattr(amenity, "name", None)
                } for amenity in place.amenities
            ]
        } for place in places], 200


# --- ENDPOINT /api/v1/places/<place_id> ---
@api.route('/<place_id>')
class PlaceResource(Resource):

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            "id": place.id,
            "owner": place.owner.to_dict() if hasattr(place.owner, 'to_dict') else place.owner_id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "amenities": [
                {
                    "id": amenity.id,
                    "name": getattr(amenity, "name", None)
                } for amenity in place.amenities
            ]
        }, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Forbidden: you do not own this place')
    def put(self, place_id):
        """Update a place's information (only by owner)"""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        # Solo el dueño puede modificar su propio lugar
        if str(place.owner_id) != str(current_user_id):
            return {'error': 'You are not allowed to modify this place'}, 403

        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

        return {
            "id": updated_place.id,
            "owner": updated_place.owner.to_dict() if hasattr(updated_place.owner, 'to_dict') else updated_place.owner_id,
            "title": updated_place.title,
            "description": updated_place.description,
            "price": updated_place.price,
            "latitude": updated_place.latitude,
            "longitude": updated_place.longitude,
            "amenities": [
                {
                    "id": amenity.id,
                    "name": getattr(amenity, "name", None)
                } for amenity in updated_place.amenities
            ]
        }, 200
