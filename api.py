from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'User( name = {self.name}, email = {self.email})'

@app.route('/')
def home():
    return '<div style="margin: 5%; text-align: center;"><h1>🐍 Welcome Home, O Python Traveller! 🐍</h1><h2>This Is Our Python Flask Server REST API</h2></div>'
  
if __name__ == '__main__':
    app.run(debug=True)