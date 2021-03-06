import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from tagPosts import create_tagPost, get_tagPosts, delete_tag_post
from posts import create_post, get_all_posts, delete_post, get_posts_by_category_id, get_posts_by_user_id, get_single_post_tags, get_single_post, edit_post, get_posts_by_tag_id
from categories import get_categories, create_category
from reactions import get_reactions, get_reactions_by_post_id, create_reaction
from subscriptions import get_subscriptions, create_subscription, edit_subscription
from tags import get_tags, create_tag
from models import Category, Post, Reaction, Tag, User, TagPost, ReactionPost, Subscription
from users import get_user_by_email, create_user, get_all_users
from categories import get_categories
from tags import get_tags, create_tag
from reactionPosts import create_reactionPost, get_reactionPosts
from users import get_user_by_email, create_user, get_all_users, get_single_user


# This function is not inside the class. It is the starting
# point of this application.

class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return (resource, key, value)

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE, PATCH')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)
        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "categories" and id is None:
                response = get_categories()
            if resource == "tags":
                response = get_tags()
            if resource == "reactions":
                response = get_reactions()
            if resource == "tagPosts" and id is None:
                response = get_tagPosts()
            if resource == "subscriptions" and id is None:
                response = get_subscriptions()
            if resource == "posts":
                if id is not None:
                    response = get_single_post(id)
                else:
                    response = get_all_posts()

            if resource == "tagPosts" and id is None:
                response = get_tagPosts()

            if resource == "reactionPosts" and id is None:
                response = get_reactionPosts()
            if resource == "users":
                if id is not None:
                    response = get_single_user(id)
                else:
                    response = get_all_users()

        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "email" and resource == "users":
                response = get_user_by_email(value)

            if key == "category_id" and resource == "posts":
                response = get_posts_by_category_id(value)

            if key == "user_id" and resource == "posts":
                response = get_posts_by_user_id(value)
        
            if key == "tag_id" and resource == "posts":
                response = get_posts_by_tag_id(value)
            if key == "post_id" and resource == "tags":
                response = get_single_post_tags(value)

        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_resource = None

        # Add a new items to the list.
        if resource == "users":
            new_resource = create_user(post_body)
        if resource == "categories":
            new_resource = create_category(post_body)
        if resource == "tags":
            new_resource = create_tag(post_body)
        if resource == "posts":
            new_resource = create_post(post_body)
        if resource == "tagPosts":
            new_resource = create_tagPost(post_body)
        if resource == "reactions":
            new_resource = create_reaction(post_body)
        if resource == "subscriptions":
            new_resource = create_subscription(post_body)
        if resource == "reactionPosts":
            new_resource = create_reactionPost(post_body)

        # Encode the new object and send in response
        self.wfile.write(f"{new_resource}".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single post or tagPost from the list
        if resource == "posts":
            delete_post(id)
        if resource == "TagPosts":
            delete_tag_post(id)

        # Encode the new object and send in response
        self.wfile.write("".encode())

    def do_PATCH(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)

        if resource == "subscriptions":
            edit_subscription(id, post_body)

        self.wfile.write("".encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)

        if resource == "posts":
            edit_post(id, post_body)

        self.wfile.write("".encode())


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
