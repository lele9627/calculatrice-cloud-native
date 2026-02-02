import os
import json
import redis
import pika

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
TTL_SECONDS = 600

def _k_status(op_id: str) -> str:
    return f"calc:{op_id}:status"

def _k_result(op_id: str) -> str:
    return f"calc:{op_id}:result"

def _k_error(op_id: str) -> str:
    return f"calc:{op_id}:error"

# RabbitMQ
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT = int(os.getenv("RABBIT_PORT", "5672"))
RABBIT_QUEUE = os.getenv("RABBIT_QUEUE", "calc_jobs")

def on_message(ch, method, properties, body: bytes):
    msg = None  # Initialiser msg au début
    try:
        msg = json.loads(body.decode("utf-8"))
        op_id = msg["id"]
        expr = (msg.get("expression") or "").strip()

        r.set(_k_status(op_id), "processing", ex=TTL_SECONDS)

        if not expr:
            raise ValueError("Expression vide")

        # Évaluation intégrée (comme demandé)
        result = eval(expr, {"__builtins__": {}})
        if not isinstance(result, (int, float)):
            raise ValueError("Le résultat n'est pas un nombre")

        result = float(result)
        out = int(result) if result.is_integer() else result

        pipe = r.pipeline()
        pipe.set(_k_result(op_id), str(out), ex=TTL_SECONDS)
        pipe.set(_k_status(op_id), "done", ex=TTL_SECONDS)
        pipe.delete(_k_error(op_id))
        pipe.execute()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except ZeroDivisionError:
        # erreur fonctionnelle -> ack (on ne veut pas retry en boucle)
        try:
            op_id = msg.get("id", "unknown") if msg else "unknown"
            r.set(_k_status(op_id), "error", ex=TTL_SECONDS)
            r.set(_k_error(op_id), "Division par zéro", ex=TTL_SECONDS)
        except Exception as e:
            print(f"[consumer] Erreur lors du marquage d'erreur ZeroDivisionError: {e}")
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        # erreur de contenu -> ack
        try:
            op_id = msg.get("id", "unknown") if msg and isinstance(msg, dict) else "unknown"
            r.set(_k_status(op_id), "error", ex=TTL_SECONDS)
            r.set(_k_error(op_id), str(e), ex=TTL_SECONDS)
        except Exception as err:
            print(f"[consumer] Erreur lors du marquage d'erreur générale: {err}")
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    params = pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=RABBIT_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)  # 1 job à la fois par worker

    channel.basic_consume(queue=RABBIT_QUEUE, on_message_callback=on_message)
    print(f"[consumer] Listening on queue '{RABBIT_QUEUE}' (RabbitMQ {RABBIT_HOST}:{RABBIT_PORT})")
    channel.start_consuming()

if __name__ == "__main__":
    main()
