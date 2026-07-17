import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
    socket_connect_timeout=5,
)

VISIT_COUNTER_KEY = "visit_counter"


@app.route("/")
def index():
    try:
        visits = redis_client.incr(VISIT_COUNTER_KEY)
    except redis.exceptions.RedisError as exc:
        return jsonify({
            "message": "Welcome! (Redis unavailable, count not tracked)",
            "error": str(exc)
        }), 503

    return jsonify({
        "message": "Welcome to the Flask + Redis visit counter app!",
        "visits": visits
    })


@app.route("/health")
def health():
    try:
        redis_client.ping()
        redis_status = "connected"
        status_code = 200
    except redis.exceptions.RedisError:
        redis_status = "unavailable"
        status_code = 503

    return jsonify({
        "status": "ok" if redis_status == "connected" else "degraded",
        "redis": redis_status
    }), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)