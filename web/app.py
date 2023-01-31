"""
Cece Smith's Flask API.
"""
import os
import configparser
from flask import Flask, abort, send_from_directory

app = Flask(__name__)

# opens first valid file in the given array and parses it.
def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

@app.route("/<string:request>")
# reads the given request and checks if there is a valid file name in /pages.
# if so, it returns that page. if there are forbidden characters or the
# page does not exist, it returns the appropriate error page instead.
def respond(request):
    if (".." in request or "~" in request):
        abort(403)
    else:
        if os.path.isfile('./pages/{}'.format(request)):
            return send_from_directory('./pages/', '{}'.format(request)), 200
        else:
            abort(404)

@app.errorhandler(403)
@app.errorhandler(404)
def display(error):
    parseError = str(error).split()
    return send_from_directory('./pages/', '{}.html'.format(parseError[0])), \
    int(parseError[0])

if __name__ == "__main__":
    config = parse_config(["credentials.ini", "default.ini"])
    app.run(debug=config["SERVER"]["DEBUG"], host='0.0.0.0', \
	port=config["SERVER"]["PORT"])
