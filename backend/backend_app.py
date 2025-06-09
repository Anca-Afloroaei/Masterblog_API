from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


# Initial testing
# @app.route('/')
# def home():
#     return 'Masterblog API is running!'


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


from flask import request  # Make sure this import is at the top if not already

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    # Validate input
    if not data:
        print("Error: Missing JSON data")  # <-- log
        return jsonify({"error": "Missing JSON data"}), 400

    # if 'title' not in data:
    #     return jsonify({"error": "Missing field: title"}), 400
    # if 'content' not in data:
    #     return jsonify({"error": "Missing field: content"}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    # Validate required fields are not empty
    if not title:
        print("Error: Missing or empty field: title")  # <-- log
        return jsonify({"error": "Missing or empty field: title"}), 400
    if not content:
        print("Error: Missing or empty field: content")  # <-- log
        return jsonify({"error": "Missing or empty field: content"}), 400

    # Generate a new unique ID
    new_id = max([post['id'] for post in POSTS], default=0) + 1

    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }

    POSTS.append(new_post)

    print(f"New post created: {new_post}")  # <-- log success
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for post in POSTS:
        if post["id"] == post_id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {post_id} has been deleted successfully."
            }), 200

    return jsonify({
        "error": f"Post with id {post_id} not found."
    }), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
