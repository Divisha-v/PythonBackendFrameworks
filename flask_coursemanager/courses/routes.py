from flask import Blueprint,jsonify,request

courses = []

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)

def make_response_json(data,status_code):
    return jsonify({
        "Status":"success",
        "data": data
    }),status_code



@courses_bp.route("/",methods = ["GET"])
def get_courses():
    return make_response_json(
    courses,
    200
)

@courses_bp.route("/",methods=["POST"])
def create_course():
    data = request.get_json()
    required = ["name","code","credits"]
    for field in required:
        if field not in data:
            return jsonify({
                "error":f"{field} is required"
            }),400
    course = {
        "id":len(courses)+1,
        "name":data["name"],
        "code":data["code"],
        "credits":data["credits"]

    }
    courses.append(course)
    return make_response_json(
        course,201
    )

@courses_bp.route("/<int:course_id>")
def get_course(course_id):
    for course in courses:
        if course["id"] == course_id:
            return make_response_json(
                course,200
            )
    return jsonify({
        "error":"Course not found"
    }),404    

@courses_bp.route("/<int:course_id>",methods = ["PUT"])
def update_course(course_id):
    data = request.get_json()
    for course in courses:
        if course["id"] == course_id:
            course["name"] = data["name"]
            course["code"] = data["code"]
            course["credits"] = data["credits"]

            return jsonify(course)
    return jsonify({
        "error":"course not foud"
    }),404

@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):

    for course in courses:

        if course["id"] == course_id:

            courses.remove(course)

            return "",204

    return jsonify({
        "error":"Course not found"
    }),404



    

