import os
from os import listdir, stat
import time
import mysql.connector
from mysql.connector import Error
# import sh
from mimetypes import MimeTypes
import datetime

mime = MimeTypes()


def convertToBinaryData(filename):
    # Convert digital data to binary format
    try:
        with open(filename, 'rb+') as file:
            binaryData = file.read()
            # print(binaryData)
        return binaryData

    except (OSError, IOError, MemoryError) as e:
        print(e)


# def read_file(filename):
#     with open(filename, 'rb') as f:
#         photo = f.read()
#     return photo


def insertBLOB(id, data):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO data_blocks
                          (id, seq, data) VALUES (%s,%s,%s)"""

        # empPicture = convertToBinaryData(photo)
        # file = convertToBinaryData(biodataFile)

        # Convert data into tuple format
        insert_blob_tuple = (id, 1, data)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into data_blocks table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into data_blocks table MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_folders(folder_id, parent_id, path, folder_name, file_name, LinkId):
    print("Inserting into Folders table {0} {1} {2}".format(path, folder_name, file_name))
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')

        cursor = connection.cursor()
        sql_insert_folder_query = """ INSERT INTO folder
                                  (id,parent_id,path,folder_name,file_name, LinkId) VALUES 
                                  (%s,%s,%s,%s,%s,%s)"""

        insert_folder_tuple = (folder_id, parent_id, path, folder_name, file_name, LinkId)
        result = cursor.execute(sql_insert_folder_query, insert_folder_tuple)
        connection.commit()
        print("inserted successfully into Folders table {0} {1} {2}".format(path, folder_name, file_name))

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into folder MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_files(file_id, mode, nlink, uid, gid, atime, mtime, ctime, size, file_type):
    print("Inserting into Files table {0}".format(file_id))
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO files
                                  (id, mode, nlink, uid, gid, atime, mtime, ctime, size, file_type) VALUES
                                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        insert_files_tuple = (file_id, mode, nlink, uid, gid, atime, mtime, ctime, size, file_type)
        result = cursor.execute(sql_insert_blob_query, insert_files_tuple)
        connection.commit()
        print("inserted successfully into Files table {0}".format(file_id))

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into files MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def get_highest_id():
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')
        cursor = connection.cursor()
        max_id = "select max(Id) from folder"
        cursor.execute(max_id)
        result = cursor.fetchall()
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed connecting to Database with error :{0}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return result


path = '/'

folders = []
files = []
root = []
all_objects = []

# print(listdir(path))
# r=root, d=directories, f = files
is_folder = 1
is_file = 1


# print(os.stat('/home'))
# print(os.stat('/home/sai'))


# function to initiate loading
def writing_db(path):
    for r, d, f in os.walk(path):
        root.append(r)
        # print("printing root")
        # print(r)
        # insert_folders(os.stat(r).st_ino, os.stat(r).st_ino, os.path.join(r, fol), fol,
        #                connection, cursor)
        # print(r)
        # print(os.stat(r))
        # os.path.getsize("/path/isa_005.mp3")

        # print("printing folders")
        # print(d)
        # insert_folders(os.stat(r).st_ino, os.stat(r).st_ino, r,"")
        # print("printing files")
        # print(f)
        folders.append(d)
        files.append(f)
        all_objects.append([root, folders, files])
        # if 'git-daemon' not in r and 'libc-bin' not in r  and 'libxml2' not in r and '48x48' not in r  and 'fdl'
        # not in r:
        if '8689' not in r and '8592' not in r and '/media' not in r:
            for fol in f:
                max_id = get_highest_id()[0][0] + 1
                os.chdir(os.path.join(r))
                try:
                    if not os.path.islink(fol):
                        insert_files(os.stat(str(os.path.join(r, fol))).st_ino, os.stat(os.path.join(r, fol)).st_mode,
                                     os.stat(os.path.join(r, fol)).st_nlink, os.stat(r).st_uid, os.stat(r).st_gid,
                                     os.stat(r).st_atime, os.stat(r).st_mtime, os.stat(r).st_ctime,
                                     os.stat(os.path.join(r, fol)).st_size,
                                     str(mime.guess_type(os.path.join(r, fol))))
                    else:
                        print("True for ", fol)
                        print("True for ", os.path.join(r))
                        insert_files(max_id, str(99999),
                                     str(1), os.stat(r).st_uid, os.stat(r).st_gid,
                                     str(int(time.time())),
                                     str(int(time.time())),
                                     str(int(time.time())), str(5), 'file')
                except OSError as e:
                    print(e.errno)
                #
                try:
                    if os.path.islink(fol):
                        print("True for ", fol)
                        print("True for ", os.path.join(r))
                        insert_folders(max_id, os.stat(r).st_ino, r, "", fol,
                                       os.stat(os.path.join(r, fol)).st_ino)
                    else:
                        insert_folders(os.stat(os.path.join(r, fol)).st_ino, os.stat(r).st_ino, r, "", fol, str(0))
                except OSError as e:
                    print(e.errno)
                try:
                    if os.path.islink(fol):
                        print("True for ", fol)
                        print("True for ", os.path.join(r))
                        if fol != 'swapfile' and fol != 'initctl':
                            insertBLOB(max_id, convertToBinaryData(os.path.join(r, fol)))
                    else:
                        if fol != 'swapfile' and fol != 'initctl':
                            insertBLOB(os.stat(os.path.join(r, fol)).st_ino, convertToBinaryData(os.path.join(r, fol)))
                # writing_db(os.path.join(r, fol))
                except OSError as e:
                    print(e.errno)

            for fol in d:
                # print(os.path)
                max_id = get_highest_id()[0][0] + 1
                os.chdir(os.path.join(r))
                if os.path.islink(fol):
                    print("True for ", fol)
                    print("True for ", os.path.join(r))
                try:
                    if os.path.islink(fol):
                        print("True for ", fol)
                        print("True for ", os.path.join(r))
                        insert_folders(max_id,stat(r).st_ino,os.path.join(r, fol), fol, "",
                                       os.stat(os.path.join(r, fol)).st_ino)
                    else:
                        insert_folders(os.stat(os.path.join(r, fol)).st_ino, os.stat(r).st_ino, os.path.join(r, fol),
                                       fol, "", str(0))
                except OSError as e:
                    print(e.errno)
                try:
                    if os.path.islink(fol):
                        print("True for ", fol)
                        print("True for ", os.path.join(r))
                        insert_files(os.stat(str(os.path.join(r, fol))).st_ino, os.stat(os.path.join(r, fol)).st_mode,
                                     os.stat(os.path.join(r, fol)).st_nlink, os.stat(r).st_uid, os.stat(r).st_gid,
                                     os.stat(r).st_atime, os.stat(r).st_mtime, os.stat(r).st_ctime,
                                     os.stat(os.path.join(r, fol)).st_size,
                                     str(mime.guess_type(os.path.join(r, fol))))
                    else:
                        insert_files(os.stat(os.path.join(r, fol)).st_ino, os.stat(os.path.join(r, fol)).st_mode,
                                     os.stat(os.path.join(r, fol)).st_nlink,
                                     os.stat(r).st_uid, os.stat(r).st_gid, os.stat(r).st_atime, os.stat(r).st_mtime,
                                     os.stat(r).st_ctime, os.stat(os.path.join(r, fol)).st_size, "folder")
                except OSError as e:
                    print(e.errno)


writing_db(path)
print("we are done")
