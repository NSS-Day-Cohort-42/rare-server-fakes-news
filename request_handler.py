import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from models import Category, Post, Reaction, Tag
from categories import get_categories, create_category
from posts import get_all_posts, create_post, get_posts_by_category_id, get_posts_by_subscription, get_posts_by_user_id, get_single_post
from reactions import get_reactions, get_reactions_by_post_id, create_reaction
from subscriptions import get_subscriptions, create_subscription
from tags import get_tags, create_tag

class HandleRequests(BaseHTTPRequestHandler):

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()