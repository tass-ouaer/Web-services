from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import CourseItemModel
from db import db
from schemas import CourseItemSchema
from marshmallow import EXCLUDE
from flask_jwt_extended import jwt_required


blp = Blueprint("Course_Items", __name__, description="Operations on course_items")


@blp.route("/course_item/<int:course_item_id>")
class CourseItemResource(MethodView):

    @blp.response(200, CourseItemSchema)
    def get(self, course_item_id):
        course_item = CourseItemModel.query.get(course_item_id)
        if not course_item:
            abort(404, message="Course item not found.")
        return course_item

    @jwt_required()  # requires token
    @blp.response(204, description="Course item deleted successfully")
    def delete(self, course_item_id):
        course_item = CourseItemModel.query.get(course_item_id)
        if not course_item:
            abort(404, message="Course item not found.")
        db.session.delete(course_item)
        db.session.commit()
        return {"message": "Course item deleted."}

    @jwt_required()  # requires token
    @blp.arguments(CourseItemSchema(partial=True, unknown=EXCLUDE))
    @blp.response(200, CourseItemSchema)
    def put(self, course_item_data, course_item_id):
        course_item = CourseItemModel.query.get(course_item_id)
        if not course_item:
            abort(404, message="Course item not found.")
        
        if "name" in course_item_data:
            course_item.name = course_item_data["name"]
        if "type" in course_item_data:
            course_item.type = course_item_data["type"]
        
        db.session.commit()
        return course_item


@blp.route("/course_item")
class CourseItemList(MethodView):

    @blp.response(200, CourseItemSchema(many=True))
    def get(self):
        return CourseItemModel.query.all()

    @jwt_required()  # requires token
    @blp.arguments(CourseItemSchema)
    @blp.response(201, CourseItemSchema)
    def post(self, course_item_data):
        # Validation: check if course item already exists for this specialization
        existing = CourseItemModel.query.filter_by(
            name=course_item_data["name"],
            specialization_id=course_item_data["specialization_id"]
        ).first()
        if existing:
            abort(400, message="Course item already exists for this specialization.")

        course_item = CourseItemModel(
            name=course_item_data["name"],
            type=course_item_data["type"],
            specialization_id=course_item_data["specialization_id"]
        )
        db.session.add(course_item)
        db.session.commit()
        
        return course_item
