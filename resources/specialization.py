import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import SpecializationModel
from db import db
from schemas import SpecializationSchema
from marshmallow import EXCLUDE


blp = Blueprint("specializations", __name__, description="Operations on specializations")


@blp.route("/specialization/<int:specialization_id>")
class SpecializationResource(MethodView):
    @blp.response(200, SpecializationSchema)
    def get(self, specialization_id):
        specialization = SpecializationModel.query.get(specialization_id)
        if not specialization:
            abort(404, message="Specialization not found.")
        return specialization

    @blp.response(204, description="Specialization deleted successfully")
    def delete(self, specialization_id):
        specialization = SpecializationModel.query.get(specialization_id)
        if not specialization:
            abort(404, message="Specialization not found.")
        db.session.delete(specialization)
        db.session.commit()
        return {"message": "Specialization deleted."}
    
    @blp.arguments(SpecializationSchema(partial=True, unknown=EXCLUDE))
    @blp.response(200, SpecializationSchema)
    def put(self, specialization_data, specialization_id):
        specialization = SpecializationModel.query.get(specialization_id)
        if not specialization:
            abort(404, message="Specialization not found.")
        
        specialization.name = specialization_data["name"]
        db.session.commit()
        return specialization


@blp.route("/specialization")
class SpecializationList(MethodView):
    @blp.response(200, SpecializationSchema(many=True))
    def get(self):
        return SpecializationModel.query.all()

    @blp.arguments(SpecializationSchema)
    @blp.response(201, SpecializationSchema)
    def post(self, specialization_data):
        # validation handled by schema
        existing = SpecializationModel.query.filter_by(name=specialization_data["name"]).first()
        if existing:
            abort(400, message="Specialization already exists.")

        specialization = SpecializationModel(name=specialization_data["name"])
        db.session.add(specialization)
        db.session.commit()
        
    

        return specialization