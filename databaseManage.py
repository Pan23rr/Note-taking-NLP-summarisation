import sqlite3 as sql


def get_db_connection():
    return sql.connect('applicationDB.db')


def newUser(userName, userEmail, hash_password, appdb):
    try:
        cursor = appdb.cursor()
        cursor.execute('''
            INSERT INTO USERS (NAME, EMAIL, PASSWORD)
            VALUES (?, ?, ?)
        ''', (userName, userEmail, hash_password))
        appdb.commit()
        return True
    except sql.IntegrityError:
        return False  
    
def validUser(email, hash_password, appdb):
    cursor = appdb.cursor()
    cursor.execute('''
        SELECT USERID FROM USERS WHERE EMAIL = ? AND PASSWORD = ?
    ''', (email, hash_password))
    user = cursor.fetchone()
    if user:
        return True, user[0] 
    else:
        return False, None  



def getNoteID(CurrentUser, title, appdb):
    cursor = appdb.cursor()
    cursor.execute('''
        SELECT NOTESID FROM NOTES WHERE UID = (SELECT USERID FROM USERS WHERE USERID = ?) AND TITLE = ?
    ''', (CurrentUser, title))
    return cursor.fetchall()


def updateNote(CurrentUser, noteID, content, appdb):
    cursor = appdb.cursor()
    cursor.execute('''
        UPDATE NOTES
        SET CONTENT = ?
        WHERE NOTESID = ? AND UID = ?
    ''', (content, noteID, CurrentUser))
    appdb.commit()


def addNote(CurrentUser, content, title, appdb):
    cursor = appdb.cursor()
    cursor.execute('''
        INSERT INTO NOTES (UID, CONTENT, TITLE)
        VALUES (?, ?, ?)
    ''', (CurrentUser, content, title))
    appdb.commit()


def getallNotes(CurrentUser, appdb):
    cursor = appdb.cursor()
    cursor.execute('''
        SELECT NOTESID, TITLE FROM NOTES WHERE UID = ?
    ''', (CurrentUser,))
    return cursor.fetchall()


def getNote(CurrentUser, noteID, appdb):
    cursor = appdb.cursor()
    cursor.execute('''
        SELECT CONTENT FROM NOTES WHERE NOTESID = ? AND UID = ?
    ''', (noteID, CurrentUser))
    return cursor.fetchall()
