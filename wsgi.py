from firebird.server import create_app


application = create_app()


if __name__ == '__main__':
    application.run(debug=True, use_reloader=True, use_debugger=True)