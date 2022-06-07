from .dashboard import create_app

if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True, host="0.0.0.0")
