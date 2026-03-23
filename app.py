from flask import Flask, jsonify, request
from database import get_connection, init_db

app = Flask(__name__)

def row_to_dict(cursor, row):
    columns = [description[0] for description in cursor.description]
    return dict(zip(columns, row))

@app.route("/api/products", methods=["GET"])
def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    products = [row_to_dict(cursor, row) for row in rows]
    conn.close()
    return jsonify([dict(p) for p in products]), 200

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return jsonify({"error": "Product not found"}), 404
    
    product = row_to_dict(cursor, row)
    conn.close()
    return jsonify(product), 200

@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Name and price are required"}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (data["name"], data["price"]))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": new_id, "name": data["name"], "price": data["price"]}), 201

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return jsonify({"error": "Product not found"}), 404
    
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Product deleted"}), 200

@app.route("/api/summary", methods=["GET"])
def get_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(price), MAX(price), AVG(price), COUNT(*) FROM products")
    row = cursor.fetchone()
    conn.close()

    return jsonify({
        "total_products": row[3],
        "min_price": row[0],
        "max_price": row[1],
        "avg_price": round(row[2],2)
    }), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

        