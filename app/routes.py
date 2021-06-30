from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

card_bp = Blueprint("cards", __name__, url_prefix="/cards")
board_bp = Blueprint("boards", __name__, url_prefix="/boards")

###################### Part A: GET /boards endpoint ##################
# a. 
# GET /boards 
# Request: board id;
# Response:  {“board_id”, “title”, “owner”}
@board_bp.route("", methods=["GET"])
def board():
    boards = Board.query.all()
    board_response = []

    for board in boards: 
        board_response.append(board.to_json())

    return jsonify(board_response), 200

###################### Part B: POST /boards endpoint ##################
#b
# #b. POST /boards
# Request: title, owner
# Response:  update db && success code ?  

@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    try: 
        create_board = Board(title=request_body["title"],
                            owner=request_body["owner"])
    except KeyError:
        return jsonify({
            "error_message": "Invalid data"
        }), 400
    db.session.add(create_board)
    db.session.commit()
    return jsonify({
        "board": create_board.to_json()
    }), 201

###################### Part C & D: "GET", "POST" /boards/<board_id>/cards endpoint ##################
# c. GET /boards/<board_id>/cards
# Request: board_id 
# Response:  {“card_id”, “message”, “likes_count”, “board_id”}

# d. POST /boards/<board_id>/cards
# Request: board_id
# Response:  update db && success code ?
@board_bp.route("/<int:board_id>/cards", methods=["POST"])
def post_card_to_board(board_id):
    board = Board.query.get(board_id)
    if not board:
        return jsonify({
            "error_message": 'Board doesn\'t exist'
        }), 404
    request_body = request.get_json()
    card = Card (
        message=request_body["message"],
        board_id = board_id
    )
    db.session.add(card)
    db.session.commit()
    return jsonify({
        "card": card.to_json()
    }), 200
    
@board_bp.route("/<int:board_id>/cards", methods=["GET"])
def get_card_from_board(board_id):
    board = Board.query.get(board_id)
    if not board:
        return make_response('Board doesn\'t exist', 404)
    board_dict = board.to_json()
    board_dict["cards"] = [card.to_json() for card in board.cards]

    # return make_response(jsonify(board_dict), 200)
    return jsonify(board_dict), 200

###################### Part E: DELETE  /cards/<card_id> endpoint ##################
# e. DELETE /cards/<card_id>
# Request: card_id
# Response:  successfully delete message ?

@card_bp.route("/<int:id>", methods=["DELETE"])
def delete_card(id):
    card = Card.query.get(id)
    if card:
        db.session.delete(card)
        db.session.commit()
        return jsonify({"details": f"Card {id} successfully deleted"
            }), 200
    return jsonify({"error_message": f"Card {id} not found"
        }), 404



###################### Part F: PUT  /cards/<card_id>/like endpoint ##################
# f. PUT /cards/<card_id>/like
# Request: card_id
# Response:  update db && success code ? 
@card_bp.route("/<int:id>/like", methods=["PATCH"])
def update_like(id):
    card = Card.query.get(id)
    if not card:
        return jsonify({"error_message": "card not found."
                }), 404
    card.like_count += 1
    db.session.commit()
    return jsonify({'card': card.to_json()}), 200
