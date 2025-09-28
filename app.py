from flask import Flask
from flask import render_template , request , redirect , url_for
import json , os



app = Flask(__name__)

def load_posts():
    if not os.path.exists("posts.json"):
        return []
    with open("posts.json", "r") as f:
        return json.load(f)

def save_posts(posts):
    with open("posts.json", "w") as f:
        json.dump(posts, f, indent=4)

def get_post_by_id(post_id):
    posts = load_posts()
    return next((p for p in posts if p.get("id") == post_id), None)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()

        # get form data
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        new_id = max([p["id"] for p in posts], default=0) + 1

        # create new post with an ID
        new_post = {
            "id": new_id ,
            "author": author,
            "title": title,
            "content": content
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    posts = load_posts()
    posts = [p for p in posts if p["id"] != post_id]  # filter out the deleted post
    save_posts(posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post = next((p for p in posts if p.get('id') == post_id), None)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # read updated values from form
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()

        # basic validation (optional)
        if not title or not content:
            # simple error handling - re-render form with message
            return render_template('update.html', post=post, error="Title and content are required.")

        # update the in-memory dict (post is a reference into posts list)
        post['title'] = title
        post['author'] = author
        post['content'] = content

        # save updated posts list
        save_posts(posts)
        return redirect(url_for('index'))

    # GET -> show update form with existing post values
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)