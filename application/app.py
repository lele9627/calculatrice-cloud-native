from flask import Flask, request, jsonify, send_from_directory
import redis
import uuid
import os
import json
import pika

app = Flask(__name__, static_folder=None)

# ---------------- Redis ----------------
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
TTL_SECONDS = 600

def _k_status(op_id: str) -> str:
    return f"calc:{op_id}:status"   # queued | processing | done | error

def _k_result(op_id: str) -> str:
    return f"calc:{op_id}:result"

def _k_error(op_id: str) -> str:
    return f"calc:{op_id}:error"

# -------------- RabbitMQ --------------
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT = int(os.getenv("RABBIT_PORT", "5672"))
RABBIT_QUEUE = os.getenv("RABBIT_QUEUE", "calc_jobs")

def publish_job(message: dict) -> None:
    """
    Publication simple dans RabbitMQ.
    Pour un TP, ouvrir/fermer une connexion par requête est acceptable.
    (Optimisation possible: connexion globale + retry.)
    """
    params = pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=RABBIT_QUEUE, durable=True)

    body = json.dumps(message).encode("utf-8")
    channel.basic_publish(
        exchange="",
        routing_key=RABBIT_QUEUE,
        body=body,
        properties=pika.BasicProperties(delivery_mode=2),  # message persistant
    )
    connection.close()

def newCalc(expr: str) -> str:
    op_id = str(uuid.uuid4())
    pipe = r.pipeline()
    pipe.set(_k_status(op_id), "queued", ex=TTL_SECONDS)
    pipe.set(f"calc:{op_id}:expr", expr, ex=TTL_SECONDS)  # utile pour debug
    pipe.execute()
    return op_id

def getResult(op_id: str):
    status = r.get(_k_status(op_id))
    if status is None:
        return {"id": op_id, "status": "waiting", "message": "Waiting for result"}

    if status == "done":
        val = r.get(_k_result(op_id))
        try:
            if val is None:
                return {"id": op_id, "status": "done", "result": None}
            if "." in val:
                num = float(val)
                return {"id": op_id, "status": "done", "result": int(num) if num.is_integer() else num}
            return {"id": op_id, "status": "done", "result": int(val)}
        except Exception:
            return {"id": op_id, "status": "done", "result": val}

    if status == "error":
        return {"id": op_id, "status": "error", "error": r.get(_k_error(op_id)) or "Unknown error"}

    return {"id": op_id, "status": "waiting", "message": "Waiting for result"}

# -------------- Static routes ----------
@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/css/<path:filename>")
def css_files(filename):
    return send_from_directory("css", filename)

@app.get("/js/<path:filename>")
def js_files(filename):
    return send_from_directory("js", filename)

# -------------- API --------------------
@app.post("/api/calc")
def calc():
    data = request.get_json(silent=True) or {}
    expr = (data.get("expression") or "").strip()

    # 1) Créer opération (Redis: queued)
    op_id = newCalc(expr)

    # 2) Publier job dans RabbitMQ (le consumer calculera)
    try:
        publish_job({"id": op_id, "expression": expr})
    except Exception as e:
        # Si RabbitMQ est down, on marque en erreur pour ne pas laisser "queued" indéfiniment
        r.set(_k_status(op_id), "error", ex=TTL_SECONDS)
        r.set(_k_error(op_id), f"RabbitMQ error: {e}", ex=TTL_SECONDS)
        return jsonify({"id": op_id, "status": "error", "error": "RabbitMQ unavailable"}), 503

    # 3) Répondre immédiatement
    return jsonify({"id": op_id, "status": "queued"}), 202

@app.get("/api/result/<op_id>")
def api_result(op_id: str):
    payload = getResult(op_id)
    if payload.get("status") == "error":
        return jsonify(payload), 400
    if payload.get("status") == "done":
        return jsonify(payload), 200
    return jsonify(payload), 202

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)

