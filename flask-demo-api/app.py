from flask import Flask, jsonify, request

app = Flask(__name__)

# 模拟数据库
users = [{"id": 1, "name": "Test User"}]

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({"users": users}),200

@app.route('/api/users', methods=['POST'])
def add_user():
    user = request.get_json()
    users.append(user)
    return jsonify({"message": "User added", "user": user}), 200

if __name__ == '__main__':
    app.run(debug=True)

