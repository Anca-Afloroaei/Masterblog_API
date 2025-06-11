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


# @app.route('/api/posts', methods=['GET'])
# def get_posts():
#     return jsonify(POSTS)


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


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    for post in POSTS:
        if post["id"] == post_id:
            # Update the post with new title/content if provided
            title = data.get("title")
            content = data.get("content")

            if title is not None:
                post["title"] = title
            if content is not None:
                post["content"] = content

            return jsonify(post), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    # Return an empty list if both queries are blank
    if title_query == '' and content_query == '':
        return jsonify([]), 200

    filtered_posts = []
    for post in POSTS:
        title_matches = title_query in post['title'].lower() if title_query else True
        content_matches = content_query in post['content'].lower() if content_query else True

        if title_matches and content_matches:
            filtered_posts.append(post)

    return jsonify(filtered_posts), 200


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    sort_direction = request.args.get('direction', 'asc')

    # Validate sort field
    if sort_field and sort_field not in ['title', 'content']:
        return jsonify({"error": "Invalid sort field. Must be 'title' or 'content'."}), 400

    # Validate direction
    if sort_direction and sort_direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid sort direction. Must be 'asc' or 'desc'."}), 400

    sorted_posts = POSTS.copy()

    # Apply sorting if valid parameters are provided
    if sort_field:
        reverse = (sort_direction == 'desc')
        sorted_posts.sort(key=lambda x: x[sort_field].lower(), reverse=reverse)

    return jsonify(sorted_posts), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
