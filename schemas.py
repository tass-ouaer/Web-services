from marshmallow import Schema, fields

#class CourseItemSchema(Schema):
#    course_item_id = fields.Str(dump_only=True)
#    name = fields.Str(required=True)
#    type = fields.Str(required=True)
#    specialization_id = fields.Str(required=True)
    
class PlainCourseItemSchema(Schema):
    course_item_id = fields.Int(dump_only=True, attribute="id")
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    #specialization_id = fields.Str(required=True)
    
class PlainSpecializationSchema(Schema):
    specialization_id = fields.Int(dump_only=True, attribute="id")
    name = fields.Str(required=True)
    
class CourseItemSchema(PlainCourseItemSchema):
    specialization_id = fields.Int(required=True, load_only=True)
    specialization = fields.Nested("PlainSpecializationSchema", dump_only=True)
    
class SpecializationSchema(PlainSpecializationSchema):
    course_items = fields.List(fields.Nested(PlainCourseItemSchema), dump_only=True)
    
#class SpecializationUpdateSchema(Schema):
#    name = fields.Str(required=True)