from __future__ import print_function
from flask import Flask, render_template, request, Response, url_for, jsonify

import socketserver
import os
import time
import sys


app = Flask(__name__)
default_port = 8500

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        lat = request.form["latitude"]
        lon = request.form["longitude"]
        #print "hello"
        #print("hello", file=sys.stderr)
        print(lat, file=sys.stderr)
        print(lon, file=sys.stderr)

        return jsonify({"latitude": lat, "longitude": lon})

    return render_template("server_home.html", latitude="na", longitude="na")

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
            with open("./data/port.txt", "w") as f:
                f.write(str(default_port))
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



if __name__ == "__main__":
    main()