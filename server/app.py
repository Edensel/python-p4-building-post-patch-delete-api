#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)  # Initialize Flask application

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Set the database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.json.compact = False  # Configure JSON serialization

migrate = Migrate(app, db)  # Initialize Flask-Migrate extension

db.init_app(app)  # Initialize SQLAlchemy extension

# Define route for the root endpoint
@app.route('/')
def index():
    return "Index for Game/Review/User API"  # Return a simple message for the root endpoint

# Define route for retrieving all games
@app.route('/games')
def games():
    # Retrieve all games from the database
    games = [game.to_dict() for game in Game.query.all()]
    
    # Create a response containing the list of games
    response = make_response(games, 200)
    return response

# Define route for retrieving a specific game by its ID
@app.route('/games/<int:id>')
def game_by_id(id):
    # Query the database for the game with the specified ID
    game = Game.query.filter(Game.id == id).first()
    
    # Convert the game object to a dictionary
    game_dict = game.to_dict()
    
    # Create a response containing the game information
    response = make_response(game_dict, 200)
    return response

# Define route for handling reviews (GET - retrieve all reviews, POST - create a new review)
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':  # If the request method is GET
        # Retrieve all reviews from the database
        reviews = [review.to_dict() for review in Review.query.all()]
        
        # Create a response containing the list of reviews
        response = make_response(reviews, 200)
        return response
    elif request.method == 'POST':  # If the request method is POST
        # Create a new review object using data from the request
        new_review = Review(
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            game_id=request.form.get("game_id"),
            user_id=request.form.get("user_id"),
        )
        
        # Add the new review to the database and commit the transaction
        db.session.add(new_review)
        db.session.commit()
        
        # Convert the new review object to a dictionary
        review_dict = new_review.to_dict()
        
        # Create a response containing the newly created review
        response = make_response(review_dict, 201)
        return response

# Define route for retrieving, updating, or deleting a review by its ID
@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    # Query the database for the review with the specified ID
    review = Review.query.filter(Review.id == id).first()

    if review == None:  # If the review does not exist
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)
        return response
    else:  # If the review exists
        if request.method == 'GET':  # If the request method is GET
            # Convert the review object to a dictionary
            review_dict = review.to_dict()
            
            # Create a response containing the review information
            response = make_response(review_dict, 200)
            return response
        elif request.method == 'PATCH':  # If the request method is PATCH
            # Update the review attributes based on the data in the request
            for attr in request.form:
                setattr(review, attr, request.form.get(attr))

            # Add the updated review to the database and commit the transaction
            db.session.add(review)
            db.session.commit()

            # Convert the updated review object to a dictionary
            review_dict = review.to_dict()

            # Create a response containing the updated review information
            response = make_response(review_dict, 200)
            return response
        elif request.method == 'DELETE':  # If the request method is DELETE
            # Delete the review from the database and commit the transaction
            db.session.delete(review)
            db.session.commit()

            # Create a response indicating that the review was successfully deleted
            response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }
            response = make_response(response_body, 200)
            return response

# Define route for retrieving all users
@app.route('/users')
def users():
    # Retrieve all users from the database
    users = [user.to_dict() for user in User.query.all()]

    # Create a response containing the list of users
    response = make_response(users, 200)
    return response

#Decided to add comments for explaination
