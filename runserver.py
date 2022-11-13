"""
Authors: Shanzay Waseem, George Toumbas

Source for jinja implementation idea:
https://stackoverflow.com/questions/40701973/create-dynamically-html-div-jinja2-and-ajax


"""
import argparse
import sys
from flask import (
    Flask,
    render_template,
    request,
    make_response,
    jsonify
)
from reg_db import RegDB

app = Flask(__name__, template_folder='.')
db = RegDB()

ADMIN_ERROR_MSG = "A server error occurred. " + \
    "Please contact the system administrator."

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

        try:
            # Handle db error
            connected = db.connect()
            results = db.search(params)
            db.close()
        except Exception as exception:
            print(f"Exception: \n {exception}", file=sys.stderr)
            error_response = make_response(ADMIN_ERROR_MSG, 500)
            return error_response


        if not connected or (results and results[0] == 'ERROR'):
            error_response  = make_response(ADMIN_ERROR_MSG, 500)
            return error_response


        json_html = jsonify(render_template(
            'dynamic_results.html',
            courses=results
            ))
        response = make_response(json_html, 200)
        return response


@app.route('/', methods=['GET'])
def home():
    return render_template('reg_search.html')


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

        try:
            connected = db.connect()
            results = db.get_details(class_id, as_string=False)
            db.close()
        except Exception as exception:
            print(f"Exception: \n {exception}", file=sys.stderr)
            return render_template(
                'error.html',
                error_message=ADMIN_ERROR_MSG
            )

        if not connected or (results and results[0] == 'ERROR'):
            return render_template(
                'error.html',
                error_message=ADMIN_ERROR_MSG
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
