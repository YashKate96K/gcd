import os
import json
from flask import Flask, request
from google.cloud import pubsub_v1

app = Flask(__name__)
publisher = pubsub_v1.PublisherClient()

# TOPIC_ID must be set as an env var in Cloud Run
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
topic_id = os.environ["TOPIC_ID"]
topic_path = publisher.topic_path(project_id, topic_id)

@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        return "No input", 400

    # Extract file info from the event
    name = envelope["name"]
    size = envelope["size"]
    content_type = envelope.get("contentType", "unknown")

    data = {
        "file_name": name,
        "file_size": size,
        "file_type": content_type
    }

    publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
    return f"Published file info for: {name}", 200
