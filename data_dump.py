import os
from os import listdir
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
        with open(filename, 'rb') as file:
            binaryData = file.read()
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
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_folders(folder_id, parent_id, path, folder_name, file_name, is_folder, is_file):
    print("Inserting into Folders table {0} {1} {2}".format(path, folder_name, file_name))
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO folder
                                  (id,parent_id,path,folder_name,file_name,is_folder, is_file) VALUES 
                                  (%s,%s,%s,%s,%s,%s,%s)"""

        insert_folder_tuple = (folder_id, parent_id, path, folder_name, file_name, is_folder, is_file)
        result = cursor.execute(sql_insert_blob_query, insert_folder_tuple)
        connection.commit()
        print("inserted successfully into Folders table {0} {1} {2}".format(path, folder_name, file_name))

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

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
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


path = '/proc'
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
        if '8689' not in r and '8592' not in r and '/media' not in r and '/home' not in r:
            for fol in f:
                # print(os.path.getsize(os.path.join(r, fol)))
                # print("printing file name {0}".format(fol))
                # print("printing join path name {0}".format(os.path.join(r, fol)))
                # print("printing inode number {0}".format(os.stat(os.path.join(r, fol)).st_ino))
                # print(os.path.join(r, fol))
                # print(os.stat(os.path.join(r, fol)))
                try:
                    insert_files(os.stat(str(os.path.join(r, fol))).st_ino, os.stat(os.path.join(r, fol)).st_mode,
                                 os.stat(os.path.join(r, fol)).st_nlink, os.stat(r).st_uid, os.stat(r).st_gid,
                                 os.stat(r).st_atime, os.stat(r).st_mtime, os.stat(r).st_ctime,
                                 os.stat(os.path.join(r, fol)).st_size,
                                 str(mime.guess_type(os.path.join(r, fol))))
                except OSError as e:
                    print(e.errno)
                #
                try:
                    insert_folders(os.stat(os.path.join(r, fol)).st_ino, os.stat(r).st_ino, r, "", fol, 0, 1)
                except OSError as e:
                    print(e.errno)
                try:
                    if fol != 'swapfile' and fol != 'initctl':
                        insertBLOB(os.stat(os.path.join(r, fol)).st_ino, convertToBinaryData(os.path.join(r, fol)))
                # writing_db(os.path.join(r, fol))
                except OSError as e:
                    print(e.errno)

            for fol in d:
                print(os.path.join(r, fol))
                # print(os.stat(os.path.join(r, fol)))
                try:
                    insert_folders(os.stat(os.path.join(r, fol)).st_ino, os.stat(r).st_ino, os.path.join(r, fol), fol,
                                   "", 1, 0)
                except OSError as e:
                    print(e.errno)
                try:
                    insert_files(os.stat(os.path.join(r, fol)).st_ino, os.stat(os.path.join(r, fol)).st_mode,
                                 os.stat(os.path.join(r, fol)).st_nlink,
                                 os.stat(r).st_uid, os.stat(r).st_gid, os.stat(r).st_atime, os.stat(r).st_mtime,
                                 os.stat(r).st_ctime, os.stat(os.path.join(r, fol)).st_size, "folder")
                except OSError as e:
                    print(e.errno)
            # writing_db(os.path.join(r, fol))


# print("printing folders")
# for f in folders:
#     print(f)
#
# print("printing files")
# for f in files:
#     print(f)
#
# print("printing roots")
# for f in root:
#     print(f)
#
# print("printing all objects")
# for f in all_objects:
#     print(f)
#
# print(len(folders))
# print(len(files))
# print(len(root))
# print(len(all_objects))

writing_db(path)
print("we are done")
#
# for obj in all_objects:
#     # for n in range(len(obj[1])):
#     # insert_folders(os.stat(all_objects[n+1][0]).st_ino, os.stat(obj[0]).st_ino, all_objects[n+1][0], obj[1][n])
#     # folder_id, parent_id, folder_path, folder_name
#     path = obj[0]
#     for l in obj:
#         # print(type(l))
#         if len(l) != 0 and type(l) != str:
#             for file in l:
#                 # print(os.path.join(path, file))
#                 # print('File         :', file)
#                 # print('Access time  :',
#                 #       datetime.datetime.strptime(time.ctime(os.path.getatime(os.path.join(path, file))),
#                 #                                  "%a %b %d %H:%M:%S %Y"))
#                 # print('Modified time:',
#                 #       datetime.datetime.strptime(time.ctime(os.path.getmtime(os.path.join(path, file))),
#                 #                                  "%a %b %d %H:%M:%S %Y"))
#                 # print('Change time  :',
#                 #       datetime.datetime.strptime(time.ctime(os.path.getctime(os.path.join(path, file))),
#                 #                                  "%a %b %d %H:%M:%S %Y"))
#                 # print('Size         :', os.path.getsize(os.path.join(path, file)))
#                 print(os.stat(os.path.join(path, file)))
#                 print(mime.guess_type(os.path.join(path, file)))
#         else:
#             if len(l) != 0:
#                 # print('File         :', l)
#                 # print('Access time  :', time.ctime(os.path.getatime(l)))
#                 # print('Modified time:', time.ctime(os.path.getmtime(l)))
#                 # print('Change time  :', time.ctime(os.path.getctime(l)))
#                 # print('Size         :', os.path.getsize(l))
#                 # print('created time  :', time.ctime(os.stat(l)[8]))
#                 print(os.stat(l))
#                 print(mime.guess_type(l))
