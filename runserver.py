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
        print(results)
        return render_template('reg_details.html', course=results)


if __name__ == '__main__':
    main()
