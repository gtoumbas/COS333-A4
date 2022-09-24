import argparse
import sqlite3
import textwrap
import sys

# TODO Error handling, Protetction from sql injection


class RegDB:

    DB_URL = 'file:reg.sqlite?mode=ro'

    def __init__(self):
        self.conn = sqlite3.connect(
            self.DB_URL, isolation_level=None, uri=True)
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

    def get_details(self, args):
        """ 
        Searches the database and displays the results.
        """
        # TODO Checks on args
        classID = args.classID

        query = self.get_details_query(classID)
        results = self.cur.execute(query).fetchall()
        self.display_details(results)



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
        """
        # TODO Error handling
        query = """
        SELECT classes.courseid, days, starttime, endtime, bldg, roomnum, dept, coursenum, area, title, descrip, prereqs, profname 
        FROM classes
        INNER JOIN courses ON classes.courseid = courses.courseid
        INNER JOIN crosslistings ON classes.courseid = crosslistings.courseid
        LEFT JOIN coursesprofs ON classes.courseid = coursesprofs.courseid
        LEFT JOIN profs ON coursesprofs.profid = profs.profid
        """

        # Add where clauses
        where = f"WHERE classid = {classid}"

        # Add where to query
        query += where

        # Add order by
        query += " ORDER BY dept, coursenum"
        return query

    def display_details(self, results):
        # TODO need to handle multiple profs
        NUM_COLUMNS = 13
        res = results[0]

        # Check length of results. This should never happen, as errors should
        # be caught be when query executed
        if len(res) != NUM_COLUMNS:
            sys.stderr.write("Error: Invalid number items in details display")
            sys.exit(1)

        # multiple depts and profs
        dept_num = ""
        profs = []
        for r in results:
            new_dept_num = f"{r[6]} {r[7]}"
            if new_dept_num not in dept_num:
                dept_num += f"Dept and Number: {new_dept_num}\n"

            profs.append(r[12])
        
        profs = list(set(profs))
        profs.sort()
        prof_str = ""
        for p in profs:
            prof_str += f"Professor: {p}\n"
        # Remove last newline
        prof_str = prof_str[:-1]
        
        wrapped_descrip = textwrap.fill(f"Description: {res[10]}", 72, break_long_words=False)
        wrapped_title = textwrap.fill(f"Title: {res[9]}", 72, break_long_words=False)

        print(f"Course Id: {res[0]}\n")
        print(f"Days: {res[1]}")
        print(f"Start time: {res[2]}")
        print(f"End time: {res[3]}")
        print(f"Building: {res[4]}")
        print(f"Room: {res[5]}\n")
        print(dept_num)
        print(f"Area: {res[8]}\n")
        print(f"{wrapped_title}\n")
        print(f"{wrapped_descrip}\n")
        if len(res[11]) > 0:
            print(f"Prerequisites: {res[11]}\n")
        else:
            print(f"Prerequisites:\n")
        if profs[0] != None:
            print(f"{prof_str}")

    def display_table(self, results, max_len=72):
        """ 
        Creates a table from the results of sql query.
        """

        header = "ClsId Dept CrsNum Area Title"
        underline = "----- ---- ------ ---- -----"
        print(header)
        print(underline)

        for r in results:
            classid, dept, coursenum, area, title = r

            # Right aligning columns except title. Info from https://docs.python.org/3/library/string.html
            line = f"{classid:>5} {dept:>4} {coursenum:>6} {area:>4} {title}"
            len_without_title = len(line) - len(title)

            line = textwrap.fill(line, max_len, subsequent_indent=" " *
                                 len_without_title, break_long_words=False)

            print(line)
