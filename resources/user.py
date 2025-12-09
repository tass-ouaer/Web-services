from flask.views import MethodView
from flask_smorest import Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from db import db
from models.user import UserModel
from schemas import UserRegisterSchema, UserLoginSchema, TokenSchema
from schemas import UserSchema


blp = Blueprint("Users", "users", description="User login & register APIs")


@blp.route("/register")
class Register(MethodView):

    @blp.arguments(UserRegisterSchema)
    @blp.response(201, TokenSchema)
    def post(self, data):

        # Check if email already exists
        if UserModel.query.filter_by(email=data["email"]).first():
            abort(400, message="Email already registered.")

        user = UserModel(
            name=data["name"],
            email=data["email"],
            password=generate_password_hash(data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return {
            "message": "User registered successfully",

        }
        

@blp.route("/login")
class Login(MethodView):

    @blp.arguments(UserLoginSchema)
    @blp.response(200, TokenSchema)
    def post(self, data):

        user = UserModel.query.filter_by(email=data["email"]).first()

        if not user or not check_password_hash(user.password, data["password"]):
            abort(401, message="Invalid credentials")

        token = create_access_token(identity=str(user.id))

        return {
            "message": "Login successful",
            "access_token": token
        }
