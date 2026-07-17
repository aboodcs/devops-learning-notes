import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)

# Redis connection settings come from environment variables
# (injected via a Kubernetes ConfigMap in this project)
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
COUNTER_KEY = "visit_counter"

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.route("/")
def index():
    count = redis_client.incr(COUNTER_KEY)
    return jsonify(
        message="Welcome to the visit counter app!",
        visits=count
    )


@app.route("/health")
def health():
    try:
        redis_client.ping()
        return jsonify(status="healthy", redis="connected"), 200
    except redis.exceptions.ConnectionError:
        return jsonify(status="unhealthy", redis="unreachable"), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
