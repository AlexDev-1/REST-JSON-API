from flask import Flask, flash, render_template, jsonify, request
from models import connect_app, Cupcake, db
import os

username = os.environ['PGUSER']
password = os.environ['PGPASSWORD']
secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@localhost:5432/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.debug = True

connect_app(app)

app.app_context().push()

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_all_cupcakes():
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake().query.all()]

    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake = cupcake.to_dict())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Add cupcake, and return data about new cupcake.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    '''

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data.get('image', None))

    db.session.add(cupcake)
    db.session.commit()

    # POST requests should return HTTP status of 201 CREATED
    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ['PATCH'])
def update_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    cupcake.flavor = data.get('flavor',cupcake.flavor)
    cupcake.rating = data.get('rating',cupcake.rating)
    cupcake.size = data.get('size',cupcake.size)
    cupcake.image = data.get('image',cupcake.image)

    db.session.add(cupcake)
    db.session.commit()


    return jsonify(cupcake = cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ['DELETE'])
def delete_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(msg = "Deleted")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)