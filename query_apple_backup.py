'''
Note: I replaced the sqlite3.dll in my Python 2.7 installation with the latest
32-bit version (3.24) from the SQLite site

Before doing this, I saw errors of the form
    "sqlite3.DatabaseError: file is encrypted or is not a database"
After doing this, the connection worked correctly.

The original dll has been moved to old.sqlite3.dll.old

References:
https://stackoverflow.com/questions/18589280/sqlite3-databaseerror-file-is-encrypted-or-is-not-a-database
https://www.sqlite.org/download.html
'''

################################################################################

import sqlite3
import os
from shutil import copyfile

################################################################################

backup_dir = "C:\\Users\\cdl\\AppData\\Roaming\\Apple Computer\\MobileSync\\Backup\\f2608b0f1ec4e73c9c3507d1c3c9477fccee3704"
archive_dir = "C:\\to_backup\\wens_iphone_13082018"
db_file="Manifest.db"
db_ref = backup_dir + "\\" + db_file

################################################################################

def check_db_present():
    if os.path.isfile(db_ref):
        print("Found DB file")
        return True
    else:
        print("Failed to find DB file")
        return False


def setup_connection(db_file):
    return sqlite3.connect(db_file)


def setup_querier(db_connection):
    return db_connection.cursor()


def test_connection():
    conn = setup_connection(db_ref)
    querier = setup_querier(conn)
    test_connection_cmd = "select * from Files limit 10"
    rv = querier.execute(test_connection_cmd)
    for row in rv:
        print row
    
    
def get_mp4_file_records(limit):
    conn = setup_connection(db_ref)
    querier = setup_querier(conn)
    find_movies_cmd = "select * from Files where relativePath like \"%.mp4\" LIMIT ?"
    rv = querier.execute(find_movies_cmd, [limit])
    for row in rv:
        print row


def get_jpg_file_records(app_dir, limit):
    conn = setup_connection(db_ref)
    querier = setup_querier(conn)
    find_jpgs_cmd = 'SELECT * FROM Files WHERE relativePath LIKE "%.jpg" AND domain LIKE ? LIMIT ?'
    app_str = '%' + app_dir + '%'
    print find_jpgs_cmd,(app_str)
    rv = querier.execute(find_jpgs_cmd, [app_str, str(limit)])
    return rv
    #for row in rv:
    #    print row


def make_archive_dir(app_name):
    new_dir = archive_dir + "\\" + app_name
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    return


def copy_to_photo_archive(app_name, db_rec):
    backup_file = db_rec[0]
    backup_file_dir = backup_file[:2]
    target_name = db_rec[2].split("/")[-1]
    src_file = backup_dir + "\\" + backup_file_dir + "\\" + backup_file
    make_archive_dir(app_name)
    dst_file = archive_dir +  "\\" + app_name + "\\" + target_name
    copyfile(src_file, dst_file)
    return

################################################################################

def main():
    #test_connection()
    app_list = ['viber', 'WhatsApp']
    for i in app_list:
        make_archive_dir(i)
        rv = get_jpg_file_records(i,10000)
        for rec in rv:
            copy_to_photo_archive(i, rec)
    #get_mp4_file_records(2)
    return

################################################################################

if __name__ == "__main__":
    main()

#column_names = ['fileID', 'domain', 'relativePath', 'flags', 'file']
#conn = setup_connection(db_ref)
#querier = setup_querier(conn)
#test_connection_cmd = "SELECT * FROM Files WHERE relativePath LIKE \"%.jpg%\" LIMIT 10"
#querier.execute(test_connection_cmd)
#rv = querier.fetchone()

#backup_file = rv[0]
#backup_file_dir = backup_file[:2]
#rv[2].split("/")[-1]




