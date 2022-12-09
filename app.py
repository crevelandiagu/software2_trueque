# from flaskwebgui import FlaskUI
import socket

from app import create_app

server_port: int = 57777

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = s.getsockname()[0] # Get local IP address
s.close()

app = create_app(ip_addr=ip_addr, server_port=server_port)

# ui = FlaskUI(app, host=ip_addr, port=server_port, maximized=True, close_server_on_exit=True)


if __name__ == "__main__":
    # app.run(host=ip_addr, port=server_port, debug=True)
    app.run()
