from flask import Flask, render_template, request, jsonify
import json
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Mock user data and global lock

lock = {"is_locked": False, "accepted_by": None, "accepted_role": None}


@app.route("/", methods=["POST", "GET"])
def respond():
    """
    Handles response from any responder role and broadcasts real-time updates.
    """
    if request.method == "GET":
        return render_template(
            "respond.html",
            responder_role=None,
            response=None,
            message="Waiting for responder input",
        )

    responder_role = request.form.get("responder_role")
    response = request.form.get("response")

    if not responder_role:
        return jsonify({"message": "Responder role is required"}), 400

    if response == "accept":
        if not lock["is_locked"]:
            # Update lock to mark the request as accepted
            lock["is_locked"] = True
            lock["accepted_by"] = responder_role
            lock["accepted_role"] = responder_role

            # Emit acceptance update to all connected clients
            socketio.emit(
                "response_update",
                {
                    "responder": responder_role, 
                    "response": "accepted",
                    "redirect": True  # Add redirect flag
                },
                to="/"
            )

            return jsonify({"message": f"Request accepted by {responder_role}"}), 200
        else:
            return jsonify(
                {
                    "message": f"Request already accepted by {lock['accepted_by']}"
                }
            ), 403

    elif response == "reject":
        # Emit rejection update to all connected clients
        socketio.emit(
            "response_update",
            {"responder": responder_role, "response": "rejected"},
            to="/",  # Broadcast to all clients
        )
        return jsonify({"message": f"Request declined by {responder_role}"}), 200

    return jsonify({"message": "Invalid response"}), 400



if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=800, debug=True)