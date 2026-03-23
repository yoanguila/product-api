# Product REST API

REST API built with Flask and SQLite to manage products and pricing data. 
Returns JSON responses with proper HTTP status codes.

## Features
- Get all products or a single product by ID
- Add and delete products
- Price summary: minimum, maximum and average
- Proper error handling with 400 and 404 responses
- Data persistence with SQLite

## Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/products | Get all products |
| GET | /api/products/`<id>` | Get product by ID |
| POST | /api/products | Add a new product |
| DELETE | /api/products/`<id>` | Delete a product |
| GET | /api/summary | Get price statistics |

## How to use
1. Clone this repository
2. Install dependencies:
```
pip3 install -r requirements.txt
```
3. Run the API:
```
python3 app.py
```
4. API will be available at `http://127.0.0.1:5000`

## Example requests
```
curl http://127.0.0.1:5000/api/products

curl -X POST http://127.0.0.1:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99}'

curl -X DELETE http://127.0.0.1:5000/api/products/1
```

## Tech stack
- Python 3
- Flask
- SQLite3