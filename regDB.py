import argparse
import sqlite3
import textwrap

# TODO Error handling, Protetction from sql injection 
# Maybe should be using dicts

class RegDB:

    # Should maybe do something similar when doing searching
    DETAILS_COLUMNS = [
        "Course Id",
        "Days",
        "Start Time",
        "End Time",
        "Building",
        "Room",
        "Department",
        "Course Number",
        "Area",
        "Title",
        "Description",
        "Prerequisites",
        "Professor"
    ]
    
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

        # Throw error if table missing certain columns
        # Error if db path is wrong

    def close(self):
        self.conn.close()


    def search(self, args):
        """ 
        Searches the database and displays the results.
        """

        query = self.get_search_query(args)
        results = self.cur.execute(query).fetchall()
        self.display_table(results)


    def get_details(self, classid):
        """ 
        Searches the database and displays the results.
        """
        # TODO Error and input handling

        query = self.get_details_query(classid)
        results = self.cur.execute(query).fetchone()
        result_dict = dict(zip(self.DETAILS_COLUMNS, results))
        self.display_details(result_dict)


    # FIXME This seems really messy
    # Should the columns be hardcoded? Or should we pass em in as args? 
    def get_search_query(self, args):
        """ 
        Returns a SQL query based on the arguments. 
        Could just join all but classes table by courseid
        """
        # TODO Error handling
        dept = args.d
        num = args.n
        area = args.a
        title = args.t

        query = """
        SELECT classid, dept, coursenum, area, title
        FROM classes
        INNER JOIN courses ON classes.courseid = courses.courseid
        INNER JOIN crosslistings ON classes.courseid = crosslistings.courseid
        """

        # Add where clauses 
        where = "WHERE "
        if dept:
            where += f"dept LIKE '%{dept}%' AND "
        if num:
            where += f"coursenum LIKE '%{num}%' AND "
        if area:
            where += f"area LIKE '%{area}%' AND "
        if title:
            where += f"title LIKE '%{title}%' AND "

        # Remove last AND
        if where != "WHERE ":
            where = where[:-5]
        else:
            # FIXME There were no conditions (Not sure what to do)
            where = ""

        # Add where to query
        query += where


        # Add order by
        query += " ORDER BY dept, coursenum, classid"

        return query


    def get_details_query(self, classid):
        """ 
        Returns a SQL query based on the arguments. 
        Could just join all but classes table by courseid
        """
        # TODO Error handling 
        query = """
        SELECT classes.courseid, days, starttime, endtime, bldg, roomnum, dept, coursenum, area, title, descrip, prereqs, profname 
        FROM classes
        INNER JOIN courses ON classes.courseid = courses.courseid
        INNER JOIN crosslistings ON classes.courseid = crosslistings.courseid
        INNER JOIN coursesprofs ON classes.courseid = coursesprofs.courseid
        INNER JOIN profs ON coursesprofs.profid = profs.profid
        """

        # Add where clauses 
        where = f"WHERE classid = {classid}"

        # Add where to query
        query += where

        return query

    # Results is a dict here    
    # This is ugly 
    def display_details(self, results):
        print(f"Course Id: {results['Course Id']}\n")
        print(f"Days: {results['Days']}")
        print(f"Start Time: {results['Start Time']}")
        print(f"End Time: {results['End Time']}")
        print(f"Building: {results['Building']}")
        print(f"Room: {results['Room']}\n")
        print(f"Department and Number: {results['Department']} {results['Course Number']}\n")
        print(f"Area: {results['Area']}\n")
        print(f"Title: {results['Title']}\n")
        print(f"Description: {results['Description']}\n") # TODO Need to wrap
        print(f"Prerequisites: {results['Prerequisites']}\n")
        print(f"Professor: {results['Professor']}")


    def display_table(self, results, maxLen=72):
        """ 
        Creates a table from the results of sql query.
        """
        # Uses textwrap to wrap long titles to multiple lines
        # Titles are underlined
        # Max width of table is 72 chars
        # Column widths are determined by the longest string in each column
        # Each line needs to end after a word not within

        # ClsId Dept CrsNum Area Title
        # ----- ---- ------ ---- -----

        header = "ClsId Dept CrsNum Area Title"
        underline = "----- ---- ------ ---- -----"
        print(header)
        print(underline)

        for r in results:
            classid, dept, coursenum, area, title = r

            # Right aligning columns except title
            line = f"{classid:>5} {dept:>4} {coursenum:>6} {area:>4} {title}"
            len_without_title = len(line) - len(title)

            line = "".join(textwrap.wrap(line, maxLen, subsequent_indent="\n" + " " * len_without_title))
            print(line)
            






        


        