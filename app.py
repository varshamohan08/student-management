from flask import Flask
from views import student_bp, auth_bp

app = Flask(__name__)
app.config.from_object("config.Config")

app.register_blueprint(student_bp, url_prefix="/students")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)
