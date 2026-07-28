from flask import Flask
from requests.exceptions import ConnectionError
app = Flask(__name__)

@app.get("/api/courses/")
def get_courses():
    return [
        {
            "id":1,
            "name":"Python"
        }
    ]

@app.get("/api/courses/<int:id>")
def get_course(id):
    return {
        "id":id,
        "name":"Python"
    }


@app.route("/api/courses/", methods=["GET"])
def gateway_courses():

    response = requests.get(
        "http://localhost:5001/api/courses/"
    )

    return (
        response.json(),
        response.status_code
    )

@app.route("/api/students/", methods=["GET"])
def gateway_students():

    response = requests.get(
        "http://localhost:5002/api/students/"
    )

    return (
        response.json(),
        response.status_code
    )

if __name__=="__main__":
    app.run(port=5000)

if __name__ == "__main__":
    app.run(port=5001)