import argparse
import sqlite3
import textwrap

# TODO Error handling, Protetction from sql injection 

class RegDB:
    
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

        # Throw error if table missing certain columns
        # Error if db path is wrong
    

    def close(self):
        self.conn.close()


    def args_to_SQL(self, args):
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
            # There were no conditions (Not sure what to do)
            where = ""

        # Add where to query
        query += where


        # Add order by
        query += " ORDER BY dept, coursenum, classid"

        return query



        
    def query(self, args):
        """ 
        Queries the database and returns the results.
        """
        query = self.args_to_SQL(args)
        # TODO protect from sql injection

        result = self.cur.execute(query)
        return result.fetchall() 


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
            







        


        