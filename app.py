from flask import Flask, flash, render_template, jsonify, request
from models import connect_app, Cupcake, db
import os

username = os.environ["PGUSER"]
password = os.environ["PGPASSWORD"]
secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

app = Flask(__name__)

app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.debug = True

connect_app(app)

app.app_context().push()

@app.route('/api/cupcakes')
def get_all_cupcakes():
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake().query.all()]

    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake = cupcake.to_dict())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add cupcake, and return data about new cupcake.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    # POST requests should return HTTP status of 201 CREATED
    return (jsonify(cupcake=cupcake.to_dict()), 201)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)