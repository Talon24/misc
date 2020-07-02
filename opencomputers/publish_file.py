"""Start a webserver with a file so opencomputers can download it."""

import argparse

from flask import Flask


def main():
    """main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    app = Flask(__name__)
    @app.route('/')
    def hello_world():
        with open(args.file, "r") as file:
            data = file.read()
        return data

    app.run("127.0.0.1")


if __name__ == '__main__':
    main()
