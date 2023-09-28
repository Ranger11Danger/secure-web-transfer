import threading
import random
import string
from flask import Flask, send_from_directory, abort, request
from cmd2 import Cmd
import os
import logging

app = Flask(__name__)
server_thread = None

# Generate a random 10-character path
path_to_serve = '/' + ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '/'
chosen_file = None

@app.route(path_to_serve)
def serve_file():
    print(f"[LOG] Received request from {request.remote_addr}, Sending {chosen_file}")
    response = send_from_directory('./serve/', chosen_file)
    print(f"[LOG] Finished sending {chosen_file} to {request.remote_addr}")
    return response

@app.route('/')
def root():
    abort(404)

class ServerCmdApp(Cmd):
    prompt = "(Secure Transfer): "
    def do_choose_file(self, arg):
        """Choose a file from the 'serve' directory to be served"""
        global chosen_file
        
        # List all files in the 'serve' directory
        files = [f for f in os.listdir('serve') if os.path.isfile(os.path.join('serve', f))]
        
        # If there are no files, inform the user and return
        if not files:
            self.poutput("No files found in 'serve' directory!")
            return

        # Display the files to the user
        for idx, filename in enumerate(files, 1):
            print(f"{idx}. {filename}")

        # Get the user's choice
        choice = input("Choose a file by number: ")
        try:
            chosen_index = int(choice) - 1
            if 0 <= chosen_index < len(files):
                chosen_file = files[chosen_index]
                self.poutput(f"Chosen file to serve: {chosen_file}")
            else:
                self.poutput("Invalid choice!")
        except ValueError:
            self.poutput("Invalid input. Please enter a number.")

    def do_set_path(self, arg):
        """Set the path to serve the file"""
        global path_to_serve
        path_to_serve = arg
        self.poutput(f"Path set to: {path_to_serve}")
        app.url_map._rules.pop(0)
        app.add_url_rule(path_to_serve, 'serve_file', serve_file)
    
    def do_start(self, arg):
        """Start the web server"""
        global server_thread
        if chosen_file == None:
            self.poutput("Please select a file with `choose_file` first")
            return
        if server_thread:
            self.poutput("Server is already running!")
            return

        if not (os.path.exists('cert.pem') and os.path.exists('key.pem')):
            self.poutput(f"[LOG] Generating Fresh Certs")
            os.system('openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -subj "/CN=example.com" -keyout key.pem -out cert.pem 2> /dev/null')

        server_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem')))
        server_thread.start()
        self.poutput("Server started!")

    def do_stop(self, arg):
        """Stop the web server"""
        global server_thread
        if not server_thread:
            self.poutput("Server is not running!")
            return

        os._exit(0)  # Forcefully stops the server.

    def do_exit(self, arg):
        """Exit the cmd app"""
        return True

if __name__ == '__main__':
    app.logger.setLevel(logging.ERROR)
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    del log.handlers[:]
    print(f"Initial random path is: {path_to_serve}")
    ServerCmdApp().cmdloop()
