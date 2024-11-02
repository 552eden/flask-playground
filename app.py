from flask import Flask, render_template, request, redirect, url_for, jsonify
import boto3
from boto3.dynamodb.conditions import Key
import uuid
import datetime
import json, os, signal


from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env

app = Flask(__name__)

# AWS DynamoDB Setup
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('falsk_test')

@app.route('/')
def index():
    # Fetch all blog posts
    response = table.scan()
    return render_template('index.html', posts=response['Items'])

@app.route('/post/<id>')
def post(id):
    # Fetch a single post
    response = table.query(
        KeyConditionExpression=Key('post_id').eq(id)
    )
    return render_template('post.html', post=response['Items'][0])

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Generate a unique ID for the new post
        post_id = str(uuid.uuid4())

        # Get form data
        title = request.form['title']
        content = request.form['content']
        author = request.form.get('author', 'Anonymous')  # Default to 'Anonymous' if no author provided
        tags = request.form['tags']
        date = datetime.datetime.now().isoformat()

        # Insert new post into DynamoDB
        table.put_item(
          Item={
              'post_id': post_id,
              'title': title,
              'content': content,
              'author': author,
              'date': date,
              'status': 'published',
              'tags': tags
          }
        )

        return redirect(url_for('index'))

    return render_template('create.html')

# Add more routes for update and delete
@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })

if __name__ == '__main__':
    app.run(debug=True)
