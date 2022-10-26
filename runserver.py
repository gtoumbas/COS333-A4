import argparse
from flask import Flask, render_template, request, json
from reg_db import RegDB
# Flask home route
# test json data of classes with dept, number, area, title
test_dict = [
        {
            "id": "1234",
            "dept": "CS",
            "num": "111",
            "area": "A",
            "title": "Intro to Computer Science"
        },
        {
            "id": "12214",
            "dept": "CS",
            "num": "112",
            "area": "A",
            "title": "Intro to Computer Science II"
        },
    ]

app = Flask(__name__)
db = RegDB()


def main():
    parser = argparse.ArgumentParser(description='Client for the registrar application')
    parser.add_argument('port', metavar='port', type=int, help='the port at which the server is listening')

    args = parser.parse_args()

    # Start flask server 
    app.run(debug=True, port=args.port)
    # app.run(port=args.port, debug=True)


@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        # Check the form data
        dept = request.args.get('dept')
        num = request.args.get('num')
        area = request.args.get('area')
        title = request.args.get('title')

        params = [dept, num, area, title]
        db.connect()
        results = db.search(params)
        db.close()


        return render_template('reg_search.html', courses=results)
    
    # return render_template('reg_search.html')

@app.route('/regdetails', methods=['GET'])
def details():
    if request.method == 'GET':
        # Check the form data
        class_id = request.args.get('classid')
        
        db.connect()
        # Right now the results are a list 
        # Should probably turn into dict - need to handle 
        # multiple teacher 
        results = db.get_details(class_id, as_string=False)
        db.close()

        for item in results:
            for i in item:
                print(i)

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
        
        return render_template('reg_details.html', course=course_results)


if __name__ == '__main__':
    main()
