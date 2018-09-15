import socketserver
import os
import sys

from flask import Flask, render_template, request, url_for, jsonify

app = Flask(__name__)
default_port = 8500

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("server_home.html")

# For starting the server
def main():
    # Globals because flask doesn't have regular function calls
    global default_port
    global app

    # Finding an open port to use
    while True:
        if default_port >= 9000:
            default_port = 8001
        try:
            app.run(debug=True, host="0.0.0.0", port=default_port)
        except socketserver.socket.error as sse:
            # Port didn't work, trying another
            default_port += 3
            print(repr(sse))
            continue
        except BaseException as ex:
            print(repr(ex))
            print("Critical error finding port, try again or write better code you fool")
            return
        break

    with open("./data/port.txt", "w") as f:
        f.write(str(default_port))


if __name__ == "__main__":
    main()