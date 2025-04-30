import subprocess
import time
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello World')
    
    def log_message(self, format, *args):
        print(f"Request received: {args[0]}")

def run_http_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

def run_command(command):
    try:
        subprocess.call(command, shell=True)
        time.sleep(5)  # Wait for 5 seconds
    except subprocess.CalledProcessError as e:
        print(f"Error executing '{command}': {e}")
        print("Continuing with the script.")

# Start HTTP server in a separate thread
server_thread = threading.Thread(target=run_http_server)
server_thread.daemon = True  # Set as daemon so it exits when the main program exits
server_thread.start()
print("HTTP server started in background")

# Update package lists
# run_command("apt-get update")
# Install procps
# run_command("apt-get install -y procps")
# Install curl
# run_command("apt-get install -y curl")

# Set execute permissions for start.sh
start_script = "/work/start.sh"
try:
    os.chmod(start_script, 0o755)
    print(f"Set execute permissions for '{start_script}'")
    time.sleep(5)  # Wait for 5 seconds
except Exception as e:
    print(f"Error setting execute permissions for '{start_script}': {e}")
    print("Continuing with the script.")

# Execute start.sh
run_command("/work/start.sh")
print("Script execution completed.")

# Keep the main thread running to allow the HTTP server to continue
try:
    # This is just to keep the main thread alive while the HTTP server runs
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("Script terminated by user")
