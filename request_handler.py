import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from models import Category, Post, Reaction, Tag, User
from users import get_user_by_email, create_user, get_all_users
from tags import get_tags, create_tag



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


            return ( resource, key, value )

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
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()
    
    def do_GET(self):
        self._set_headers(200)
        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "users" and id is None:
                response = get_all_users()

            if resource == "tags":            
                response = f"{get_tags()}"
     
        
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            if key == "email" and resource == "users":
                response = get_user_by_email(value)
        
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

        if resource == "tags":
            new_resource = create_tag(post_body)


        # Encode the new animal and send in response
        self.wfile.write(f"{new_resource}".encode())

    


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
