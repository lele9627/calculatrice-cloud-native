from flask import Flask, request, jsonify, send_from_directory
import ast
import operator as op

app = Flask(__name__, static_folder=None)

import math

def safe_eval(expr: str) -> float:
    expr = (expr or "").strip()
    if not expr:
        raise ValueError("Expression vide")
    
    try:
        result = eval(expr, {"__builtins__": {}})
    except Exception as e:
        raise ValueError(f"Expression invalide: {e}") from e

    if not isinstance(result, (int, float)):
        raise ValueError("Le résultat n'est pas un nombre")

    return float(result)


@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/css/<path:filename>")
def css_files(filename):
    return send_from_directory("css", filename)

@app.get("/js/<path:filename>")
def js_files(filename):
    return send_from_directory("js", filename)

@app.post("/api/calc")
def calc():
    data = request.get_json(silent=True) or {}
    expr = data.get("expression", "")

    try:
        result = safe_eval(expr)

        if result.is_integer():
            return jsonify({"result": int(result)})
        return jsonify({"result": result})

    except ZeroDivisionError:
        return jsonify({"error": "Division par zéro"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)