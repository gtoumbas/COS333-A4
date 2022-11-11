"""
Authors: Shanzay Waseem, George Toumbas   

Source for jinja implementation idea: 
https://stackoverflow.com/questions/40701973/create-dynamically-html-div-jinja2-and-ajax


"""
import argparse
from flask import Flask, render_template, request, make_response, jsonify
from reg_db import RegDB

app = Flask(__name__, template_folder='.')
db = RegDB()


def main():
    parser = argparse.ArgumentParser(
        description='The registrar application')
    parser.add_argument('port', metavar='port',type=int, \
        help='the port at which the server should listen')

    args = parser.parse_args()

    # Start flask server
    app.run(host="0.0.0.0", port=args.port)

@app.route('/_get_search_results', methods=['GET'])
def get_search_results():
    if request.method == 'GET':
    # Check the form data
        dept = request.args.get('dept')
        num = request.args.get('num')
        area = request.args.get('area')
        title = request.args.get('title')

        params = [dept, num, area, title]

        # Handle db error
        try:
            db.connect()
            results = db.search(params)
            db.close()
        except:
            error_msg = "A server error occurred. " + \
                "Please contact the system administrator."
            return make_response(render_template("error.html", error_message=error_msg))

    json_html = jsonify(render_template('dynamic_results.html', courses=results))
    return json_html

@app.route('/', methods=['GET'])
def home():
    return render_template('reg_search.html') 


def get_prevcookies():
    dept = request.cookies.get("dept") or None
    num = request.cookies.get("num") or None
    area = request.cookies.get("area") or None
    title = request.cookies.get("title") or None
    inputs = {"dept": dept, "num":num,"area":area, "title":title}
    return inputs


def set_newcookies(response, inputs):
    if inputs["dept"] is not None:
        response.set_cookie("dept", inputs["dept"])
    if inputs["num"] is not None:
        response.set_cookie("num", inputs["num"])
    if inputs["area"] is not None:
        response.set_cookie("area", inputs["area"])
    if inputs["title"] is not None:
        response.set_cookie("title", inputs["title"])



@app.route('/regdetails', methods=['GET'])
def details():
    if request.method == 'GET':
        class_id = request.args.get('classid')

        # Handle missing class_id
        if not class_id:
            error_message = "missing classid"
            return render_template(
                'error.html',
                error_message=error_message
            )

        # Handle non-integer class_id
        for char in class_id:
            if not char.isdigit():
                error_message = "non-integer classid"
                return render_template(
                    'error.html',
                    error_message=error_message
                )

        # Handles DB errors
        try:
            db.connect()
            results = db.get_details(class_id, as_string=False)
            db.close()
        except:
            error_message = "A server error occurred. " + \
            "Please contact the system administrator."
            return render_template(
                'error.html',
                error_message=error_message
            )


        # Handles invalid class id
        if results[0]== "INVALID_CLASSID":
            error_message = f"no class with classid {class_id} exists"
            return render_template(
                'error.html',
                error_message=error_message
            )

        # turning results into a dict
        course_results = {}
        first_result = results[0]
        course_results["course_id"] = first_result[0]
        course_results["days"] = first_result[1]
        course_results["start_time"] = first_result[2]
        course_results["end_time"] = first_result[3]
        course_results["building"] = first_result[4]
        course_results["room"] = first_result[5]
        course_results["area"] = first_result[8]
        course_results["title"] = first_result[9]
        course_results["description"] = first_result[10]
        course_results["prereqs"] = first_result[11]
        course_results["class_id"] = class_id

        course_results.setdefault("dept_num", [])
        course_results.setdefault("profs", [])

        for items in results:
            course_results["dept_num"].append(items[6] + " " + items[7])
            course_results["profs"].append(items[12])

        course_results["dept_num"] = set(course_results["dept_num"])
        course_results["profs"] = set(course_results["profs"])

        # Sort the dept_num and profs by alphabetical order
        course_results["dept_num"] = sorted(course_results["dept_num"])
        course_results["profs"] = sorted(course_results["profs"])


        return render_template('reg_details.html', \
            course=course_results)


if __name__ == '__main__':
    main()
