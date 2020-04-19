import os
import subprocess
from os import listdir
from os import stat
import time
import mysql.connector
from mysql.connector import Error
from subprocess import call
from termcolor import colored


def get_parent_id(path=None, parent_id=None):
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')

        cursor = connection.cursor()
        sql_insert_blob_query = """ select id from folder where folder_name != '' and path = %s"""
        cursor.execute(sql_insert_blob_query, (path,))
        result = cursor.fetchall()
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")
            if len(result) == 1:
                return result[0][0]
            else:
                print("you are in root folder")
                return parent_id


def ls_function(parentid):
    files_list = []
    folders_list = []
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')

        cursor = connection.cursor()
        folder_names_sql = """ select folder_name as name from folder where parent_id = %s and folder_name != ''"""
        file_names_sql = """ select file_name as name from folder where parent_id = %s and file_name != ''"""
        cursor.execute(folder_names_sql, (parent_id,))
        result = cursor.fetchall()
        connection.commit()
        for r in result:
            folders_list.append(r[0])

        cursor.execute(file_names_sql, (parent_id,))
        result = cursor.fetchall()
        connection.commit()
        for r in result:
            files_list.append(r[0])

        for fol in folders_list:
            print(colored(fol, 'blue'), end = '    ')
        # print("")
        for fil in files_list:
            print(fil, end = '    ')
        print("")

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def result_to_print(r=None):
    print_list = []
    permission = ''
    binary = bin(r[0])
    if binary[2] == '0':
        permission += '-'
    else:
        permission += 'd'
    for i in range(-9, -1):
        if i in [-9, -6, -3]:
            # print(binary[i])
            # print(type(binary[i]))
            if binary[i] == '1':
                permission += 'r'
            else:
                permission += '-'
        if i in [-8, -5, -2]:
            if binary[i] == '1':
                permission += 'w'
            else:
                permission += '-'
        if i in [-7, -4, -1]:
            if binary[i] == '1':
                permission += 'x'
            else:
                permission += '-'

    print_list.append(permission)
    # permission += ' ' + str(r[1])
    print_list.append(str(r[1]))
    # permission += ' ' + user[str(r[2])]
    print_list.append(user[str(r[2])])
    # permission += ' ' + group[str(r[3])]
    print_list.append(group[str(r[3])])
    # permission += ' ' + str(r[4])
    print_list.append(str(r[4]))
    # permission += ' ' + str(time.ctime(r[5]))
    print_list.append(str(time.ctime(r[5])))
    # permission += ' ' + str(r[6])
    print_list.append(str(r[6]))
    # folders_list.append(permission)
    return print_list


def lsl_function(parent_id, user, group):
    # files_list = []
    # folders_list = []
    folders_list_print = []
    files_list_print = []
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')

        cursor = connection.cursor()
        folder_names_sql = """select mode,nlink,uid,gid,size,mtime,folder_name from folder  join files on  files.id = folder.id 
        where parent_id = %s and folder_name != ''"""
        file_names_sql = """ select mode,nlink,uid,gid,size,mtime,file_name from folder  join files on  files.id = folder.id 
        where parent_id = %s and file_name != ''"""
        cursor.execute(folder_names_sql, (parent_id,))
        result = cursor.fetchall()
        connection.commit()
        for r in result:
            folders_list_print.append(result_to_print(r))

        cursor.execute(file_names_sql, (parent_id,))
        result = cursor.fetchall()
        connection.commit()
        for r in result:
            files_list_print.append(result_to_print(r))

        # for fol in folders_list:
        #     print(colored(fol, 'blue'))
        for fol in folders_list_print:
            for l in fol:
                print(colored(l.rjust(8), 'blue'), end = '  ')
            print("")
        # for fil in files_list:
        #     print(fil)
        for fol in files_list_print:
            for l in fol:
                print(l.rjust(8), end = '  ')
            print("")
        # print("")

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def pwd_function(pwd):
    """
    function to print the current working directory
    :param pwd: current directory path
    :return: None
    """
    print(colored(pwd, 'white'))


def cd_function(pwd=None, command=None, parent_id=None):
    """

    :param command: cd command entered by the user
    :param pwd: present working directory
    :param parent_id: parent_id of the pwd

    """
    c = command.split(' ', 1)
    if c[1] == '..' and len(c) == 2 and pwd != '/home/sai':
        # pwd = pwd.rsplit('/', 1)[0]
        # parent_id = get_parent_id(pwd.rsplit('/', 1)[0])
        return pwd.rsplit('/', 1)[0], get_parent_id(pwd.rsplit('/', 1)[0])
    elif c[1] == '..' and len(c) == 2 and pwd == '/home/sai':
        print("you are in root folder")
        return pwd, parent_id
    elif c[1] == '.' and len(c) == 2:
        return pwd, parent_id
    elif './' in c[1] or '/' not in c[1] or '/' in c[1]:
        try:
            connection = mysql.connector.connect(host = 'localhost',
                                                 database = 'filesys',
                                                 user = 'filesys',
                                                 password = 'asdfgh123')
            if './' in c[1]:
                path = pwd + '/' + c[1][2:]
            elif '/' not in c[1]:
                if pwd != '/':
                    path = pwd + '/' + c[1]
                elif pwd == '/':
                    path = pwd + c[1]
            elif '/' in c[1] and c[1][0] != '/':
                if pwd != '/':
                    path = pwd + '/' + c[1]
                elif pwd == '/':
                    path = pwd + c[1]

            cursor = connection.cursor()
            sql_insert_blob_query = """ select id from folder where folder_name != '' and path = %s"""

            cursor.execute(sql_insert_blob_query, (path,))
            result = cursor.fetchall()
            connection.commit()

        except mysql.connector.Error as error:
            print("Failed Connecting to Mysql Server due to {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                # print("MySQL connection is closed")
                if len(result) == 1:
                    for r in result:
                        return path, r[0]
                else:
                    print("bash: cd: ", c[1], ": No such file or directory")
                    return pwd, parent_id
    else:
        try:
            connection = mysql.connector.connect(host = 'localhost',
                                                 database = 'filesys',
                                                 user = 'filesys',
                                                 password = 'asdfgh123')

            cursor = connection.cursor()
            sql_insert_blob_query = """ select id from folder where folder_name != '' and path = %s"""

            cursor.execute(sql_insert_blob_query, (c[1],))
            result = cursor.fetchall()
            connection.commit()
            # print("Image and file inserted successfully as a BLOB into python_employee table", result[0][0])
            # print(len(result))
            # if len(result) == 1:
            # for r in result:
            # print("printing result  = {0}".format(r[0]))

        except mysql.connector.Error as error:
            print("Failed Connecting to Mysql Server due to {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                # print("MySQL connection is closed")
                if len(result) == 1:
                    for r in result:
                        return c[1], r[0]
                else:
                    print("bash: cd: ", c[1], ": No such file or directory")
                    return pwd, parent_id


def find_function(command=None):
    name = command.rsplit(' ', 1)[1]
    search_path = command.rsplit(' ', 1)[0].split(' ', 1)[1]

    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')
        find_query = """"""
        result_list_print = []
        cursor = connection.cursor()
        find_query_file = """select mode,nlink,uid,gid,size,mtime,concat(path,"/",file_name) as file from folder 
            join files on files.id = folder.id where file_name like %s """
        find_query_folder = """select mode,nlink,uid,gid,size,mtime,path as file from 
            folder join files on files.id = folder.id where folder_name like %s """
        name = '%' + name
        name += '%'
        cursor.execute(find_query_file, (name,))
        result = cursor.fetchall()
        connection.commit()
        for r in result:
            re = result_to_print(r)
            if search_path in re[-1]:
                result_list_print.append(re)
        cursor.execute(find_query_folder, (name,))
        result = cursor.fetchall()
        connection.commit()
        for r in result:
            re = result_to_print(r)
            if search_path in re[-1]:
                result_list_print.append(re)
        for res in result_list_print:
            for re in res:
                print(re.rjust(8), end = ' ')
            print("")

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def grep_function(pwd, command):
    print("reached grep function ")
    name = command.rsplit(' ', 1)[1]
    search_pattern = command.rsplit(' ', 1)[0].split(' ', 1)[1]
    search_pattern = search_pattern.replace('\"', '')
    print(name, search_pattern)

    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')
        find_query = """"""
        result_list_print = []
        cursor = connection.cursor()
        all_path_file_ids = "select id,file_name from folder  where path =  \"" + pwd + "\" and file_name like %s"
        name = '%' + name
        name += '%'
        cursor.execute(all_path_file_ids, (name,))
        result = cursor.fetchall()
        connection.commit()
        for r in result:
            like_search_pattern = '%' + search_pattern + '%'
            find_file_id = "select folder.id,file_name from folder join data_blocks on folder.id = data_blocks.id " \
                           "where folder.id = " \
                           " \"" + str(r[0]) + "\" and data like %s "
            cursor.execute(find_file_id, (like_search_pattern,))
            result_file_id = cursor.fetchall()
            connection.commit()
            for re in result_file_id:
                data_query = "select data from data_blocks where id = %s"
                cursor.execute(data_query, (str(re[0]),))
                data = cursor.fetchall()
                print("printing type of data ", type(data))
                # print(data)
                # print(data[0])
                # print(data[0][0].splitlines())
                for l in range(0, len(data[0][0].splitlines())):
                    if search_pattern in data[0][0].splitlines()[l]:
                        print("line {0} : {1} in file : {2}".rjust(8).format(l, data[0][0].splitlines()[l], re[1]))

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# function to create a new directory using mkdir command just like in Linux systems
def new_directory(pwd=None, parent_id=None, dir_name=None):
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')
        # result_list_print = []
        cursor = connection.cursor()
        max_id = "select max(Id) from folder"
        cursor.execute(max_id)
        result = cursor.fetchall()
        connection.commit()
        new_dir_folder_table = """INSERT INTO folder
                                  (id,parent_id,path,folder_name,file_name,is_folder, is_file) VALUES 
                                  (%s,%s,%s,%s,%s,%s,%s)"""
        new_dir_file_table = """ INSERT INTO files
                                  (id, mode, nlink, uid, gid, atime, mtime, ctime, size, file_type) VALUES
                                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        folder_name_check = """select folder_name from folder where folder_name != '' and parent_id = %s """
        check_tuple = parent_id
        cursor.execute(folder_name_check, (check_tuple,))
        check = cursor.fetchall()
        check_result = False
        for c in check:
            if c[0] == dir_name:
                check_result = True
        if not check_result:
            # print(type(str(int(max_id) + 1)))
            insert_folder_tuple = (
                str(result[0][0] + 1), str(parent_id), str(pwd + dir_name), str(dir_name), '', str(1), str(0))
            res = cursor.execute(new_dir_folder_table, insert_folder_tuple)
            connection.commit()
            insert_files_tuple = (
                str(result[0][0] + 1), str(16877), str(1), str(1000), str(1000), str(int(time.time())),
                str(int(time.time())), str(int(time.time())), str(4096), 'fodler')
            res = cursor.execute(new_dir_file_table, insert_files_tuple)
            connection.commit()
            print("Successfully created a new directory :", dir_name)
        else:
            print("mkdir: cannot create directory ‘" + dir_name + "’: File exists")
    except mysql.connector.Error as error:
        print("Failed connecting to Database with error :{0}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# function to create a new text file using touch command just like in Linux systems
def create_touch_file(pwd, parent_id, command):
    # 33188
    cmd = command.split(' ', 1)
    file_name = cmd[1]
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123')
        cursor = connection.cursor()
        # check if a file exists with the same name
        check_file_query = "select id,file_name from folder where parent_id = %s and file_name != ''"
        cursor.execute(check_file_query, (parent_id,))
        result = cursor.fetchall()
        connection.commit()
        check = False
        for r in result:
            if file_name == r[1]:
                check = True
        # if file does not exists process to create a new empty file
        if not check:
            cursor = connection.cursor()
            max_id = "select max(Id) from folder"
            cursor.execute(max_id)
            result = cursor.fetchall()
            connection.commit()
            new_dir_folder_table = """INSERT INTO folder
                                      (id,parent_id,path,folder_name,file_name,is_folder, is_file) VALUES 
                                      (%s,%s,%s,%s,%s,%s,%s)"""
            new_dir_file_table = """ INSERT INTO files
                                      (id, mode, nlink, uid, gid, atime, mtime, ctime, size, file_type) VALUES
                                      (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            insert_folder_tuple = (
                str(result[0][0] + 1), str(parent_id), str(pwd), '', str(file_name), str(0), str(1))
            res = cursor.execute(new_dir_folder_table, insert_folder_tuple)
            connection.commit()
            insert_files_tuple = (
                str(result[0][0] + 1), str(33204), str(1), str(1000), str(1000), str(int(time.time())),
                str(int(time.time())),
                str(int(time.time())), str(0), 'file')
            res = cursor.execute(new_dir_file_table, insert_files_tuple)
            connection.commit()
            print("Successfully created a new file:", file_name)
        else:
            print("touch : cannot create file :‘" + file_name + "’: File exists")

    except mysql.connector.Error as error:
        print("Failed connecting to Database with error :{0}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# function to delete a file or delete whole directory recursively using rm command just like in Linux systems
def delete_directory(pwd=None, parent_id=None, command=None):
    cmd = command.split()
    if len(cmd) == 2:
        file_name = cmd[1]
        try:
            connection = mysql.connector.connect(host = 'localhost',
                                                 database = 'filesys',
                                                 user = 'filesys',
                                                 password = 'asdfgh123')
            # result_list_print = []
            cursor = connection.cursor()
            check_file_query = "select id,file_name from folder where parent_id = %s and file_name != ''"
            cursor.execute(check_file_query, (parent_id,))
            result = cursor.fetchall()
            connection.commit()
            check = False
            for r in result:
                if file_name == r[1]:
                    id = r[0]
                    check = True
            if check:
                # delete file from folders table
                delete_file_query_Q1 = """delete from folder where id = %s"""
                cursor = connection.cursor()
                cursor.execute(delete_file_query_Q1, (id,))
                connection.commit()
                # delete file from files table
                cursor = connection.cursor()
                delete_file_query_Q2 = """delete from files where id = %s"""
                cursor.execute(delete_file_query_Q2, (id,))
                connection.commit()
                cursor = connection.cursor()
                delete_file_query_Q3 = """delete from data_blocks where id = %s"""
                cursor.execute(delete_file_query_Q3, (id,))
                connection.commit()
            else:
                print("no such file to be deleted :", file_name)

        except mysql.connector.Error as error:
            print("Failed connecting to Database with error :{0}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    elif len(cmd) > 2:
        if cmd[1] == '-r':
            folder_name = cmd[2]
            try:
                connection = mysql.connector.connect(host = 'localhost',
                                                     database = 'filesys',
                                                     user = 'filesys',
                                                     password = 'asdfgh123')
                # result_list_print = []
                cursor = connection.cursor()
                check_file_query = "select id,folder_name from folder where parent_id = %s and folder_name != ''"
                cursor.execute(check_file_query, (parent_id,))
                result = cursor.fetchall()
                connection.commit()
                check = False
                for r in result:
                    if folder_name == r[1]:
                        id = r[0]
                        check = True
                if check:
                    # selecting all the files and folder in the folder to delete them recursively
                    select_file_ids = """select id from folder where parent_id = %s"""
                    # delete folder from folders tables
                    delete_folder_Q1 = """delete from folder where id = %s """
                    # delete folder from files tables
                    delete_folder_Q2 = """delete from files where id = %s """
                    # delete folder files from folders tables
                    delete_folder_Q3 = """delete from folder where parent_id = %s"""
                    # delete folder files from files table
                    delete_folder_Q4 = """delete from files where id not in (select id from folder)"""
                    # delete files from data_blocks table
                    delete_folder_Q5 = """delete from data_blocks where id = %s """

                    cursor = connection.cursor()
                    cursor.execute(select_file_ids, (id,))
                    file_ids_result = cursor.fetchall()
                    connection.commit()
                    cursor = connection.cursor()
                    cursor.execute(delete_folder_Q1, (id,))
                    connection.commit()
                    cursor = connection.cursor()
                    cursor.execute(delete_folder_Q2, (id,))
                    connection.commit()
                    cursor = connection.cursor()
                    cursor.execute(delete_folder_Q3, (id,))
                    connection.commit()
                    cursor = connection.cursor()
                    cursor.execute(delete_folder_Q4)
                    connection.commit()
                    for f in file_ids_result:
                        cursor = connection.cursor()
                        print(type(f[0]))
                        print(f)
                        cursor.execute(delete_folder_Q5, (int(f[0]),))
                        connection.commit()

                else:
                    print("no such directory to be deleted :", folder_name)

            except mysql.connector.Error as error:
                print("Failed connecting to Database with error :{0}".format(error))

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()


# function to execute any executables available in current directory
def execute_executable(pwd, parent_id, command):
    cmd = command.split(' ', 1)
    try:
        connection = mysql.connector.connect(host = 'localhost',
                                             database = 'filesys',
                                             user = 'filesys',
                                             password = 'asdfgh123',
                                             use_pure = True)
        cursor = connection.cursor()
        # check if a file exists with the same name
        check_file_query = "select id,file_name from folder where parent_id = %s and file_name != ''"
        cursor.execute(check_file_query, (parent_id,))
        result = cursor.fetchall()
        connection.commit()
        check = False
        for r in result:
            if cmd[1] == r[1]:
                id = r[0]
                file_name = cmd[1]
                check = True
        if check:
            data_query = "select data from data_blocks where id = %s"
            cursor.execute(data_query, (str(id),))
            data = cursor.fetchall()
            # print("printing type of data ", type(data))
            # print(data[0][0])
            # print(type(data[0][0]))
            f = open(file_name + '.exe', "wb+")
            f.write(data[0][0])
            f.close()
            # os.chmod(file_name, 0o777)
            cwd = os.getcwd()
            p = subprocess.Popen('./' + file_name + '.exe')
            p.wait()

            # os.system(r"/home/sai/Desktop/final/hell.exe")
            print("We are done again")

    except mysql.connector.Error as error:
        print("Failed connecting to Database with error :{0}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


user = {"0": "root", "1": "daemon", "2": "bin", "3": "sys", "4": "sync", "5": "games", "6": "man", "7": "lp",
        "8": "mail", "9": "news", "10": "uucp", "13": "proxy", "30": "dip", "33": "www-data", "34": "backup",
        "38": "list",
        "39": "irc", "41": "gnats", "65534": "nobody", "100": "systemd-network", "101": "systemd-resolve",
        "102": "syslog", "103": "messagebus", "104": "_apt", "105": "uuidd", "106": "avahi-autoipd", "107": "usbmux",
        "108": "dnsmasq", "109": "rtkit", "110": "cups-pk-helper", "111": "speech-dispatcher", "112": "whoopsie",
        "113": "kernoops", "114": "saned", "115": "pulse", "116": "avahi", "117": "colord", "118": "hplip",
        "119": "geoclue", "120": "gnome-initial-setup", "121": "gdm", "1000": "sai", "122": "mysql", "999": "mssql",
        "123": "gitlog", "124": "gitdaemon"}
group = {"0": "root", "1": "daemon", "2": "bin", "3": "sys", "65534": "sync", "60": "games", "12": "man", "7": "lp",
         "8": "mail", "9": "news", "10": "uucp", "13": "proxy", "30": "dip", "33": "www-data", "34": "backup",
         "38": "list",
         "39": "irc", "41": "gnats", "65534": "nobody", "102": "systemd-network", "103": "systemd-resolve",
         "106": "syslog", "107": "messagebus", "65534": "_apt", "111": "uuidd", "112": "avahi-autoipd", "46": "usbmux",
         "65534": "dnsmasq", "114": "rtkit", "116": "cups-pk-helper", "29": "speech-dispatcher", "117": "whoopsie",
         "65534": "kernoops", "119": "saned", "120": "pulse", "122": "avahi", "123": "colord", "7": "hplip",
         "124": "geoclue", "65534": "gnome-initial-setup", "125": "gdm", "1000": "sai", "127": "mysql", "999": "mssql",
         "65534": "gitlog", "65534": "gitdaemon"}
pwd = '/'
parent_id = 2
# parent_id = get_parent_id(pwd, parent_id)


print("You are going to enter Bash - hold your seats")
print("Entered Bash , you can use commands pwd, cd, ls, find and grep")
while True:
    print(colored("localhost:-" + pwd + " :~$ ", 'yellow'), end = '')
    command = input()
    cmd = command.split(' ')
    if cmd[0].strip() == 'ls' and len(cmd) == 1:
        ls_function(parent_id)
    elif cmd[0].strip() == 'ls' and len(cmd) == 2:
        lsl_function(parent_id, user, group)
    elif cmd[0].strip() == 'pwd':
        pwd_function(pwd)
    elif cmd[0].strip() == 'cd':
        pwd, parent_id = cd_function(pwd, command, parent_id)
        # print(pwd, " and ", parent_id)
    elif cmd[0].strip() == 'find':
        find_function(command)
    elif cmd[0].strip() == 'grep':
        grep_function(pwd, command)
    elif cmd[0] == 'mkdir':
        new_directory(pwd, parent_id, cmd[1])
    elif cmd[0] == 'rm':
        delete_directory(pwd, parent_id, command)
    elif cmd[0] == 'touch':
        create_touch_file(pwd, parent_id, command)
    elif cmd[0] == 'exec':
        execute_executable(pwd, parent_id, command)
    else:
        print(command, ": command not found.You can use commands pwd, cd, ls, find and grep")
