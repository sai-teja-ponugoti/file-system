import os
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
        if i in [-7, -4, -3]:
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
            # # folders_list.append(stat.S_ISDIR(r[0]))
            # # folders_list.append(oct(r[0]) & 0o0400)
            # permission = ''
            # print_list = []
            # binary = bin(r[0])
            # if binary[2] == '0':
            #     permission += '-'
            # else:
            #     permission += 'd'
            # for i in range(-9, -1):
            #     if i in [-9, -6, -3]:
            #         # print(binary[i])
            #         print(type(binary[i]))
            #         if binary[i] == '1':
            #             permission += 'r'
            #         else:
            #             permission += '-'
            #     if i in [-8, -5, -2]:
            #         if binary[i] == '1':
            #             permission += 'w'
            #         else:
            #             permission += '-'
            #     if i in [-7, -4, -3]:
            #         if binary[i] == '1':
            #             permission += 'x'
            #         else:
            #             permission += '-'
            # print_list.append(permission)
            # # permission += ' ' + str(r[1])
            # print_list.append(str(r[1]))
            # # permission += ' ' + user[str(r[2])]
            # print_list.append(user[str(r[2])])
            # # permission += ' ' + group[str(r[3])]
            # print_list.append(group[str(r[3])])
            # # permission += ' ' + str(r[4])
            # print_list.append(str(r[4]))
            # # permission += ' ' + str(time.ctime(r[5]))
            # print_list.append(str(time.ctime(r[5])))
            # # permission += ' ' + str(r[6])
            # print_list.append(str(r[6]))
            # # folders_list.append(permission)
            # files_list_print.append(print_list)
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


# finished this function
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
            if './' in c[1] :
                path = pwd + '/' + c[1][2:]
            elif '/' not in c[1]:
                path = pwd + '/' + c[1]
            elif '/' in c[1] and c[1][0] != '/':
                path = pwd + '/' + c[1]

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


# def get_find_results(search_path, name, type):
#     try:
#         connection = mysql.connector.connect(host='localhost',
#                                              database='filesys',
#                                              user='filesys',
#                                              password='asdfgh123')
#         find_query = """"""
#         result_list_print = []
#         cursor = connection.cursor()
#         if type == 'nl':
#             find_query_file = """select concat(path,"/",file_name) as file from folder where file_name like %s """
#             find_query_folder = """select path as file from folder where folder_name like %s """
#             name = '%' + name
#             name += '%'
#             cursor.execute(find_query_file, (name,))
#             result = cursor.fetchall()
#             connection.commit()
#             for r in result:
#                 if search_path in r:
#                     print(r[0])
#             cursor.execute(find_query_folder, (name,))
#             result = cursor.fetchall()
#             connection.commit()
#             for r in result:
#                 if search_path in r:
#                     print(r[0])
#
#         elif type == '-l':
#             find_query_file = """select mode,nlink,uid,gid,size,mtime,concat(path,"/",file_name) as file from folder
#             join files on files.id = folder.id where file_name like %s """
#             find_query_folder = """select mode,nlink,uid,gid,size,mtime,path as file from
#             folder join files on files.id = folder.id where folder_name like %s """
#             name = '%' + name
#             name += '%'
#             cursor.execute(find_query_file, (name,))
#             result = cursor.fetchall()
#             connection.commit()
#             for r in result:
#                 result_list_print.append(result_to_print(r))
#             cursor.execute(find_query_folder, (name,))
#             result = cursor.fetchall()
#             connection.commit()
#             for r in result:
#                 result_list_print.append(result_to_print(r))
#             for res in result_list_print:
#                 for re in res:
#                     if search_path in re:
#                         print(re.rjust(8), end=' ')
#                 print("")
#
#     except mysql.connector.Error as error:
#         print("Failed inserting BLOB data into MySQL table {}".format(error))
#
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()


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
                print(data)
                print(data[0])
                print(data[0][0].splitlines())
                for l in range(0, len(data[0][0].splitlines())):
                    if search_pattern in data[0][0].splitlines()[l]:
                        print("line {0} : {1} in file : {2}".rjust(8).format(l, data[0][0].splitlines()[l], re[1]))

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


user = {"0": "root", "1": "daemon", "2": "bin", "3": "sys", "4": "sync", "5": "games", "6": "man", "7": "lp",
        "8": "mail", "9": "news", "10": "uucp", "13": "proxy", "33": "www-data", "34": "backup", "38": "list",
        "39": "irc", "41": "gnats", "65534": "nobody", "100": "systemd-network", "101": "systemd-resolve",
        "102": "syslog", "103": "messagebus", "104": "_apt", "105": "uuidd", "106": "avahi-autoipd", "107": "usbmux",
        "108": "dnsmasq", "109": "rtkit", "110": "cups-pk-helper", "111": "speech-dispatcher", "112": "whoopsie",
        "113": "kernoops", "114": "saned", "115": "pulse", "116": "avahi", "117": "colord", "118": "hplip",
        "119": "geoclue", "120": "gnome-initial-setup", "121": "gdm", "1000": "sai", "122": "mysql", "999": "mssql",
        "123": "gitlog", "124": "gitdaemon"}
group = {"0": "root", "1": "daemon", "2": "bin", "3": "sys", "65534": "sync", "60": "games", "12": "man", "7": "lp",
         "8": "mail", "9": "news", "10": "uucp", "13": "proxy", "33": "www-data", "34": "backup", "38": "list",
         "39": "irc", "41": "gnats", "65534": "nobody", "102": "systemd-network", "103": "systemd-resolve",
         "106": "syslog", "107": "messagebus", "65534": "_apt", "111": "uuidd", "112": "avahi-autoipd", "46": "usbmux",
         "65534": "dnsmasq", "114": "rtkit", "116": "cups-pk-helper", "29": "speech-dispatcher", "117": "whoopsie",
         "65534": "kernoops", "119": "saned", "120": "pulse", "122": "avahi", "123": "colord", "7": "hplip",
         "124": "geoclue", "65534": "gnome-initial-setup", "125": "gdm", "1000": "sai", "127": "mysql", "999": "mssql",
         "65534": "gitlog", "65534": "gitdaemon"}

pwd = '/home/sai'
parent_id = 2260994
parent_id = get_parent_id(pwd, parent_id)

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
    else:
        print(command, ": command not found.You can use commands pwd, cd, ls, find and grep")
