from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/api/students/")
def students():
    return []

@app.post("/api/students/<int:id>/enroll")
def enroll(id):

    course_id = request.json["course_id"]

    response = requests.get(
        f"http://localhost:5001/api/courses/{course_id}"
    )

    if response.status_code != 200:
        return jsonify(
            {"message":"Course not found"}
        ),404

    return jsonify(
        {
            "student":id,
            "course":course_id,
            "status":"Enrolled"
        }
    )

if __name__ == "__main__":
    app.run(port=5002)


