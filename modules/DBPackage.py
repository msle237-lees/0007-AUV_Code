from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from typing import List, Dict, Any
import argparse

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Inputs class to store the submarine's input data (X, Y, Z, Roll, Pitch, Yaw, Arm, S1, S2, S3)
class Inputs(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Z = db.Column(db.Float, nullable=False)
    Roll = db.Column(db.Float, nullable=False)
    Pitch = db.Column(db.Float, nullable=False)
    Yaw = db.Column(db.Float, nullable=False)
    Arm = db.Column(db.Float, nullable=False)
    S1 = db.Column(db.Float, nullable=False)
    S2 = db.Column(db.Float, nullable=False)
    S3 = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Inputs {self.datetime}, {self.X}, {self.Y}, {self.Z}, {self.Roll}, {self.Pitch}, {self.Yaw}, {self.Arm}, {self.S1}, {self.S2}, {self.S3}>'

# Position class to store the submarine's position data (X, Y, Z)
class Position(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Z = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Position {self.datetime}, {self.X}, {self.Y}, {self.Z}>'

# Rotation class to store the submarine's rotation data (Roll, Pitch, Yaw)
class Rotation(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True)
    Roll = db.Column(db.Float, nullable=False)
    Pitch = db.Column(db.Float, nullable=False)
    Yaw = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Rotation {self.datetime}, {self.Roll}, {self.Pitch}, {self.Yaw}>'

# Velocity class to store the submarine's velocity data (Vx, Vy, Vz)  
class Velocity(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True)
    Vx = db.Column(db.Float, nullable=False)
    Vy = db.Column(db.Float, nullable=False)
    Vz = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Velocity {self.datetime}, {self.Vx}, {self.Vy}, {self.Vz}>'
    
# Routes for inputs data
@app.route('/inputs', methods=['GET'])
def get_inputs():
    latest_input = Inputs.query.order_by(Inputs.datetime.desc()).first()
    if latest_input:
        return jsonify({
            'datetime': latest_input.datetime,
            'X': latest_input.X,
            'Y': latest_input.Y,
            'Z': latest_input.Z,
            'Roll': latest_input.Roll,
            'Pitch': latest_input.Pitch,
            'Yaw': latest_input.Yaw,
            'Arm': latest_input.Arm,
            'S1': latest_input.S1,
            'S2': latest_input.S2,
            'S3': latest_input.S3
        })
    else:
        return jsonify({'message': 'No data available'}), 404

@app.route('/inputs', methods=['POST'])
def add_input():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    try:
        new_input = Inputs(
            datetime=datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S'),
            X=data['X'],
            Y=data['Y'],
            Z=data['Z'],
            Roll=data['Roll'],
            Pitch=data['Pitch'],
            Yaw=data['Yaw'],
            Arm=data['Arm'],
            S1=data['S1'],
            S2=data['S2'],
            S3=data['S3']
        )
        db.session.add(new_input)
        db.session.commit()
        return jsonify({'message': 'Input data added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    
# Routes for position data
@app.route('/position', methods=['GET'])
def get_position():
    latest_position = Position.query.order_by(Position.datetime.desc()).first()
    if latest_position:
        return jsonify({
            'datetime': latest_position.datetime,
            'X': latest_position.X,
            'Y': latest_position.Y,
            'Z': latest_position.Z
        })
    else:
        return jsonify({'message': 'No data available'}), 404

@app.route('/position', methods=['POST'])
def add_position():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    try:
        new_position = Position(
            datetime=datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S'),
            X=data['X'],
            Y=data['Y'],
            Z=data['Z']
        )
        db.session.add(new_position)
        db.session.commit()
        return jsonify({'message': 'Position data added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    
# Routes for rotation data
@app.route('/rotation', methods=['GET'])
def get_rotation():
    latest_rotation = Rotation.query.order_by(Rotation.datetime.desc()).first()
    if latest_rotation:
        return jsonify({
            'datetime': latest_rotation.datetime,
            'Roll': latest_rotation.Roll,
            'Pitch': latest_rotation.Pitch,
            'Yaw': latest_rotation.Yaw
        })
    else:
        return jsonify({'message': 'No data available'}), 404
    
@app.route('/rotation', methods=['POST'])
def add_rotation():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    try:
        new_rotation = Rotation(
            datetime=datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S'),
            Roll=data['Roll'],
            Pitch=data['Pitch'],
            Yaw=data['Yaw']
        )
        db.session.add(new_rotation)
        db.session.commit()
        return jsonify({'message': 'Rotation data added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    
# Routes for velocity data
@app.route('/velocity', methods=['GET'])
def get_velocity():
    latest_velocity = Velocity.query.order_by(Velocity.datetime.desc()).first()
    if latest_velocity:
        return jsonify({
            'datetime': latest_velocity.datetime,
            'Vx': latest_velocity.Vx,
            'Vy': latest_velocity.Vy,
            'Vz': latest_velocity.Vz
        })
    else:
        return jsonify({'message': 'No data available'}), 404
    
@app.route('/velocity', methods=['POST'])
def add_velocity():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    try:
        new_velocity = Velocity(
            datetime=datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S'),
            Vx=data['Vx'],
            Vy=data['Vy'],
            Vz=data['Vz']
        )
        db.session.add(new_velocity)
        db.session.commit()
        return jsonify({'message': 'Velocity data added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    
# Initialize the database and create tables
@app.before_first_request
def create_tables():
    db.create_all()

# Configure the arguments for the Flask app
parser = argparse.ArgumentParser(description="Flask API for Unity Interface")
parser.add_argument("--port", type=int, default=5000, help="Port for Flask API")
parser.add_argument("--host", type=str, default="localhost", help="Host for Flask API")
args = parser.parse_args()

if __name__ == "__main__":
    app.run(host=args.host, port=args.port, debug=True)
