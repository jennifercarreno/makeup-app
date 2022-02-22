from makeup_app.extensions import app, db
from makeup_app.routes import main

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)