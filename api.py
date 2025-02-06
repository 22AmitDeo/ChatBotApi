from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# User Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

# Debate Model
class DebateModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Debate(topic={self.topic}, description={self.description})"

# Request Parser for Debate Submission
debate_args = reqparse.RequestParser()
debate_args.add_argument('topic', type=str, help="Debate topic is required", required=True)
debate_args.add_argument('description', type=str, help="Debate description is required", required=True)

# Fields for Marshaling Response
debate_fields = {
    'id': fields.Integer,
    'topic': fields.String,
    'description': fields.String
}

# Debate Resource
class Debates(Resource):
    @marshal_with(debate_fields)
    def get(self):
        debates = DebateModel.query.all()
        return debates

    @marshal_with(debate_fields)
    def post(self):
        args = debate_args.parse_args()
        new_debate = DebateModel(topic=args["topic"], description=args["description"])
        db.session.add(new_debate)
        db.session.commit()
        return new_debate, 201

api.add_resource(Debates, '/api/debates/')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
