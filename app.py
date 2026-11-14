from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


@app.route("/events", methods=["POST"])
def create_event():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data provided"
        }), 400

    title = data.get("title")

    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    new_id = max(
        event.id for event in events
    ) + 1 if events else 1

    new_event = Event(
        new_id,
        title
    )

    events.append(new_event)

    return jsonify(
        new_event.to_dict()
    ), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data provided"
        }), 400

    for event in events:

        if event.id == event_id:

            if "title" in data:
                event.title = data["title"]

            return jsonify(
                event.to_dict()
            ), 200

    return jsonify({
        "error": "Event not found"
    }), 404


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):

    for index, event in enumerate(events):

        if event.id == event_id:

            deleted_event = event.to_dict()

            del events[index]

            return jsonify({
                "message": "Event deleted",
                "event": deleted_event
            }), 200

    return jsonify({
        "error": "Event not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)