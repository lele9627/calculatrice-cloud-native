from flask import Flask, request, jsonify
import redis
import uuid
import os
import json
import pika

app = Flask(__name__)

# ======================
# Redis configuration
# ======================
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
TTL_SECONDS = 600

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True
)

def key_status(op_id): return f"calc:{op_id}:status"
def key_result(op_id): return f"calc:{op_id}:result"
def key_error(op_id):  return f"calc:{op_id}:error"

# ======================
# RabbitMQ configuration
# ======================
RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq-service")
RABBIT_PORT = int(os.getenv("RABBIT_PORT", "5672"))
RABBIT_QUEUE = os.getenv("RABBIT_QUEUE", "calc_jobs")

def publish_job(message: dict):
    params = pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=RABBIT_QUEUE, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=RABBIT_QUEUE,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

# ======================
# API ROUTES
# ======================

@app.post("/api/calc")
def create_calc():
    """
    Reçoit une expression (ex: "2+3"),
    enregistre la demande,
    envoie le job à RabbitMQ,
    retourne un ID.
    """
    data = request.get_json(silent=True) or {}
    expression = data.get("expression", "").strip()

    if not expression:
        return jsonify({"error": "Expression missing"}), 400

    op_id = str(uuid.uuid4())

    # Stockage initial
    r.set(key_status(op_id), "queued", ex=TTL_SECONDS)

    try:
        publish_job({
            "id": op_id,
            "expression": expression
        })
    except Exception as e:
        r.set(key_status(op_id), "error", ex=TTL_SECONDS)
        r.set(key_error(op_id), str(e), ex=TTL_SECONDS)
        return jsonify({"error": "RabbitMQ unavailable"}), 503

    return jsonify({
        "id": op_id,
        "status": "queued"
    }), 202


@app.get("/api/result/<op_id>")
def get_result(op_id):
    status = r.get(key_status(op_id))

    if status is None:
        return jsonify({"status": "unknown"}), 404

    if status == "done":
        return jsonify({
            "status": "done",
            "result": r.get(key_result(op_id))
        }), 200

    if status == "error":
        return jsonify({
            "status": "error",
            "error": r.get(key_error(op_id))
        }), 400

    return jsonify({
        "status": status
    }), 202


# ======================
# Health checks (très bien pour le projet)
# ======================

@app.get("/api/health/redis")
def health_redis():
    try:
        r.ping()
        return jsonify({"redis": "ok"}), 200
    except Exception as e:
        return jsonify({"redis": "down", "error": str(e)}), 500


@app.get("/api/health/rabbit")
def health_rabbit():
    try:
        params = pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
        conn = pika.BlockingConnection(params)
        conn.close()
        return jsonify({"rabbitmq": "ok"}), 200
    except Exception as e:
        return jsonify({"rabbitmq": "down", "error": str(e)}), 500


# ======================
# ENTRYPOINT KUBERNETES
# ======================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # OBLIGATOIRE en Kubernetes
        port=5000,        # DOIT matcher Service + nginx
        debug=False
    )
