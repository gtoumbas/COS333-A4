import argparse
import sqlite3
import textwrap

# TODO Error handling, Protetction from sql injectio, table, query creation, 

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

        # Want the title, coursenum, classid, area


        
    def query(self, args):
        """ 
        Queries the database and returns the results.
        """
        query = self.args_to_SQL(args)
        # TODO protect from sql injection

        result = self.cur.execute(query)
        return result.fetchall() 


    def create_table(self, results, maxLen=72, col_names=["Title", "Course Number", "Area", "Class ID"]):
        """ 
        Creates a table from the results of sql query.
        """
        # Uses textwrap to wrap long titles to multiple lines
        # Titles are underlined
        # Max width of table is 72 chars
        # Column widths are determined by the longest string in each column
        # Each line needs to end after a word not within

        # Something like
        # ----------------------------------------------
        # | Title | Course Number | Area | Class ID |
        # ----------------------------------------------


        


        