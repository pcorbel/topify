#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import flask_cors
import flask_restplus as rest
from flask import Flask, send_from_directory

from topify.common.utils import expose_collectors, find_collectors


def main():
    app = Flask(__name__)
    app.logger.setLevel(logging.DEBUG)
    flask_cors.CORS(app)

    # Define root endpoint to serve frontend before APIfying Flask
    @app.route("/")
    def index():
        return send_from_directory("/app/topify/templates/topify", "index.html")

    @app.route("/<path:path>")
    def dist(path):
        return send_from_directory("/app/topify/templates/topify", path)

    # APIfying Flask
    api = rest.Api(
        version="1.0.0",
        title="topify",
        description="A user-friendly top-like monitoring",
        app=app,
        doc="/doc/",
        default="topify",
        default_label="Topify root endpoint",
        prefix="/api/v1",
    )

    # Add collectors
    for collector in find_collectors():
        expose_collectors(api, collector)

    # Start Flask server
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
