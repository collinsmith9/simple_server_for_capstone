import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_users, get_posts_expand_user, get_user_by_email, create_post
from views.users_requests import get_users_partner, get_user_by_id



class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        if "?" in resource:
            if "_" in resource:
                param = resource.split("?")[1] # _expand=user
                resource = resource.split("?")[0] # posts
                pair = param.split("=") # ['_expand','user']
                key = pair[0]
                value = pair[1]
            else:
                param = resource.split("?")[1]  # email=jenna@solis.com
                resource = resource.split("?")[0]  # 'customers'
                pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
                key = pair[0]  # 'email'
                value = pair[1]  # 'jenna@solis.com'
            return ( resource, key, value )
        else:
            id = None
            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response
        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handles GET requests to the server
        """
        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)
        if len(parsed) == 2:
            ( resource, id ) = parsed
            if resource == "users":
                if id is not None:
                    response = f"{get_user_by_id(id)}"
                else:
                    response = f"{get_all_users()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"

        elif len(parsed) == 3:
            ( resource, key, value ) = parsed
            if key == "partner" and resource == "users":
                response = get_users_partner()
            elif key == "_expand" and resource == "posts":
                response = get_posts_expand_user()
            elif key == "email" and resource == "users":
                response = get_user_by_email(value)
            elif key == "id" and resource == "users":
                response = get_user_by_id(int(value))

        self.wfile.write(f"{response}".encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0)) # get length of what was passed
        post_body = self.rfile.read(content_len) # read file only reads to specified character (content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_resource = None
        if resource == "posts":
            new_resource = create_post(post_body)
        elif resource == "locations":
            new_resource = create_location(post_body)
        elif resource == "employees":
            new_resource = create_employee(post_body)
        elif resource == "customers":
            new_resource = create_customer(post_body)

        self.wfile.write(f"{new_resource}".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        success = False
        if resource == "entries":
            success = update_entry(id, post_body)
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)
        if resource == "entries":
            delete_entry(id)
        elif resource == "locations":
            delete_location(id)
        elif resource == "employees":
            delete_employee(id)
        elif resource == "customers":
            delete_customer(id)
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()