from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User( name = {self.name}, email = {self.email}, password = {self.password})"


user_args = reqparse.RequestParser()
user_args.add_argument(
    "name", type=str, help="Name is required and cannot be left blank.", required=True
)
user_args.add_argument(
    "email", type=str, help="Email is required and cannot be left blank.", required=True
)
user_args.add_argument(
    "password",
    type=str,
    help="Password is required and cannot be left blank.",
    required=True,
)

userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
}


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        return UserModel.query.all()

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(
            name=args["name"], email=args["email"], password=args["password"]
        )
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201


class User(Resource):

    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with this ID {id} not found.")
        return user

    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with this ID {id} not found.")
        user.name = args["name"]
        user.email = args["email"]
        user.password = args["password"]
        db.session.commit()
        return user

    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with this ID {id} not found.")
        db.session.delete(user)
        db.session.commit()
        return UserModel.query.all()


api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/users/<int:id>")


@app.route("/")
def home():
    return '<div style="margin: 5%; text-align: center;"><h1>🐍 Welcome Home, O Python Traveller! 🐍</h1><h2>This Is Our Python Flask Server REST API</h2></div>'


if __name__ == "__main__":
    app.run(debug=True)
