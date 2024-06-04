import sqlite3, sys

class CIS:
    def __init__(self):
        self.conn=""
        self.crsr=""
        self.err=""

    def ConnectDB(self):
        try:
            self.conn=sqlite3.connect("unotes.db")
            self.crsr=self.conn.cursor()

        except sqlite3.Error as e:
            self.err="Error connecting to Database."+str(e)+"\n"
            sys.exit(1)

    def CreateTableContact(self):
        try:
            createq='CREATE TABLE IF NOT EXISTS cinfo'
            createq+='(Pno integer primary key, Fname text, Lname text, Email text)'
            self.crsr.execute(createq)

        except sqlite3.Error as e:
            self.err="There is an error creating the table "+str(e)
            #CIS.CloseDB(self)   #IT IS PART OF THE CLASS SO TO CALL THIS FUNTION YOU HAVE TO WRITE CLASS.FUNCTION()
            #sys.exit(1)

    def CloseDB(self):
        try:
            self.conn.close()

        except sqlite3.Error as e:
            self.err="There was an error closing the connection- "+str(e)

    def AddB(self,fname,lname,phoneno,emailid):
        try:

            addq="INSERT INTO cinfo (Pno, Fname, Lname, Email) VALUES (?, ?, ?, ?)"
            self.crsr.execute(addq, (phoneno,fname, lname, emailid))
            self.conn.commit()

        except sqlite3.Error as er:
            self.err="There was an error inserting record "+str(er)

    def AddInfo(self,fname,lname,phoneno,emailid):

        try:
            searchq="SELECT * FROM cinfo WHERE Pno=?"

            self.crsr.execute(searchq,(phoneno,))

            rdbks=self.crsr.fetchall()
            if rdbks:
                self.UpdateB(fname,lname,phoneno,emailid)

            else:
                self.AddB(fname,lname,phoneno,emailid)
        
        except sqlite3.Error as er:
                self.err="There was an error searching for record "+str(er)

    def UpdateB(self,fname,lname,phoneno,emailid):

        try:
            q1="UPDATE cinfo SET "
            if(fname and lname and emailid):
                q1+="Fname = '{0}', Lname='{1}',Email='{2}' where Pno = {3}".format(fname,lname,emailid,phoneno)
                self.crsr.execute(q1)
                self.conn.commit()

            elif (fname and emailid ):
                q1+="Fname = '{0}', Email='{1}'where Pno = {2}".format(fname,emailid,phoneno)
                self.crsr.execute(q1)
                self.conn.commit()

            elif (lname and emailid):
                q1+="Lname = '{0}',Email='{1}' where Pno = {2}".format(lname,emailid,phoneno)
                self.crsr.execute(q1)
                self.conn.commit()

            elif(fname and lname):
                q1+="Fname='{0}',Lname='{1}' where Pno = {2}".format(fname,lname,phoneno)
                self.crsr.execute(q1)
                self.conn.commit()
            
            elif(fname):
                q1+="Fname = '{0}' where Pno = {1}".format(fname,phoneno)
                self.crsr.execute(q1)
                self.conn.commit()

            elif(lname):
                q1+="Lname='{0}' where Pno = {1}".format(lname,phoneno)
                self.crsr.execute(q1)
                self.conn.commit()

            elif(emailid):
                q1+="Email='{0}' where Pno = {1}".format(emailid,phoneno)
                self.crsr.execute(q1)
                self.conn.commit()

        except sqlite3.Error as er:
            self.err="There was an error updating record "+str(er)
            #return(self.err)
            #CIS.CloseDB(self)
            #sys.exit(1)

    def CreateTableNotes(self):
        try:
            createq='CREATE TABLE IF NOT EXISTS nts'
            createq+='(ID primary key, Author text, Subject text, Topic text, Content text)'
            self.crsr.execute(createq)

        except sqlite3.Error as e:
            self.err="There is an error creating the table "+str(e)

    def AddN(self,author,subject,topic,content):
        try:
            addq="INSERT INTO nts (Author, Subject, Topic, Content) VALUES (?, ?, ?,?)"
            self.crsr.execute(addq, (author,subject,topic,content))
            self.conn.commit()
            msg="Note added successfully."
            return(msg)

        except sqlite3.Error as er:
            self.err="There was an error inserting record "+str(er)
            return(self.err)

    def SearchN(self,skw):
        try:
            #searchq="Select * from nts where subject like ? or topic like ? or content like ? values (?,?,?)"
            searchq="SELECT * FROM nts WHERE Subject LIKE ? OR Topic LIKE ? OR Content like ? "
            self.crsr.execute(searchq, ('%'+skw+'%', '%'+skw+'%','%'+skw+'%'))
            rdnts = self.crsr.fetchall()
            if rdnts:
                return rdnts
            else:
                return "No notes."

        except sqlite3.Error as er:
            self.err="There was an error searching for record "+str(er)
            return(self.err)
