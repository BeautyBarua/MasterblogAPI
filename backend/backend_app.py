from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """this will give information for posts"""
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """To add a new blog post"""
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({'error': 'Invalid request'}), 400

    # Retrieve the title and content from the request body
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    # Check if the tittle or content is missing
    if not title or not content:
        missing_fields = []
        if not title:
            missing_fields.append('title')
        if not content:
            missing_fields.append('content')
        return jsonify({'error': 'Missing fields', 'missing_fields': missing_fields}), 400

    # Generate a new unique identifier for the post
    post_id = str(uuid.uuid4())

    # Generate a new post to object
    post = {
        'id': post_id,
        'title': title,
        'content': content
    }

    # add the post to the list
    POSTS.append(post)

    return jsonify(post), 201


@app.route('/api/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Validate the post_id format
    try:
        # Attempt to convert post_id to integer
        post_id = int(post_id)
    except ValueError:
        # Return an error response for invalid ID format
        return jsonify({'error': 'Invalid ID format'}), 400

    # Find the post with the given id
    for post in POSTS:
        if post['id'] == post_id:
            # Remove the post from the list
            POSTS.remove(post)
            return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200

    # If the post is not found, return a 404 response
    return jsonify({'error': 'Post not found'}), 404


@app.route('/api/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    """To update an existing blog post"""

    # Find the post with the given id
    for post in POSTS:
        if post['id'] == int(post_id):
            # Retrieve the updated title and content from the request body
            data = request.get_json()
            new_title = data.get('title', post['title'])
            new_content = data.get('content', post['content'])

            # Update the post with the new values
            post['title'] = new_title
            post['content'] = new_content

            # Return the updated post
            return jsonify({
                'id': post['id'],
                'title': new_title,
                'content': new_content
            }), 200

    # If the post is not found, return a 404 response
    return jsonify({'error': 'Post not found'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """TThis will allow clients to search for posts by their title or content"""
    # Retrieve the search terms from the query parameters
    search_title = request.args.get('title', '')
    search_content = request.args.get('content', '')

    # Filter posts based on search criteria
    matched_posts = []
    for post in POSTS:
        if search_title.lower() in post['title'].lower() or search_content.lower() in post['content'].lower():
            matched_posts.append(post)

    # Return the matched posts
    return jsonify(matched_posts)


@app.route('/api/posts', methods=['GET'])
def list_posts():
    """This functionality provides flexibility to users to organize the posts as per their needs"""
    # Retrieve the sort and direction parameters from the query string
    sort_by = request.args.get('sort')
    direction = request.args.get('direction')

    # Validate the sort and direction parameters
    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    if sort_by and sort_by not in valid_sort_fields:
        return jsonify({'error': 'Invalid sort field'}), 400

    if direction and direction not in valid_directions:
        return jsonify({'error': 'Invalid direction'}), 400

    # Sort the posts if valid sort and direction parameters are provided
    if sort_by and direction:
        POSTS.sort(key=lambda post: post[sort_by], reverse=(direction == 'desc'))

    # Return the list of posts
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
