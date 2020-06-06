'''
The following set consists class with functions 
for passing commands to the server
'''
import pathlib
import time
import pandas
from shutil import rmtree
import csv
import os

class User():
        '''
    This class consists of the functions which are used to execute commands
    ****
    create_folder:
    Function for creating directory and folder
    ****
    register:
    Function to regeister a user
    ****
    login:
    Function for login of a registered user
    ****
    quit:
    Function for signout of a user
    ****
    delete1:
    Function for deleting a registered user
    ****
    change_folder:
    Function for changing directory
    ****
    commands:
    Function that displays all the commands that can be executed
    ****
    list:
    gives a list of all the working directories in the server- client exchange
    ****
    read_file:
    Function to read the given file in a given directory
    ****
    write_file:
    Function to write the given file in a given directory
    ****
    '''
    def __init__(self):
        '''
        The function consists of different parameters that return diffrent 
        values of boolean, characters, strings or integers
        '''
        self.usr_id = None
        self.directory = None
        self.indx = {}
        self.nochar = 100
        self.log_check = False
        self.checked_users = None
        self.users_loged = None
        
    
    def create_folder(self, folder_path):
        '''
        This fuction creates a creates a new directory and creates a folder
        in it.
        '''
        self.session()
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if not self.log_check:
            return"\nLogin to access"
        pas = int(logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if pas == 1:
            currentdir = "Root/Admin/"
        else:
            curr_dir = "Root/NotAdmin/"
        rmpath = os.path.join(currentdir, str(self.usr_id), self.directory)
        dirmax = []
        for sub in os.listdir(rmpath):
            pathos = os.path.join(rmpath, sub)
            if os.path.isdir(pathos):
                dirmax.append(sub)
        if folder_path in dirmax:
            return "\nThis path is already created"
        os.mkdir(os.path.join(rmpath, folder_path))
        return"\nSuccess"

    def register(self, usr_id, passw, prior):
        '''
        This fuction creates the users when rigister command is entered
        once the user has created a username and password he can be as admin 
        or normal account.
        -----------
        If username already exists its displayes a message that the usename already 
        exists
        '''
        self.session()
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        var1 = 100
        if usr_id in logdata['username'].tolist():
            return "\nUsername not available"
        if usr_id == "" or passw == "" or prior == "":
            return "\nYou cannot register empty user"
        store = pandas.DataFrame(columns=['username', 'password', 'isAdmin'])
        store['username'] = [usr_id]
        store['password'] = passw
        if prior.lower() == 'admin':
            store['isAdmin'] = 1
            var1 = 1
        else:
            store['isAdmin'] = 0
            var1 = 0
        logdata = logdata.append(store)
        logdata.to_csv("ServerAccessSession/Users.csv", index=False)
        dirname = str(usr_id)
        if var1 == 1:
            filloc = "Root/Admin/"
        else:
            filloc = "Root/NotAdmin/"

        os.mkdir(os.path.join(filloc, dirname))
        return "\nRegistration successfull."


    def login(self, usr_id, passw):
        '''
        This function deals with login of a user provided the user has been registered
        *********
        If the user is already logged in "Already logged in" is displayed 
        *********
        If the user is not registered "Username not registered is displayed
        *********
        If the password is entered wrong "Wrong password" is diplayed
        ********* 
        '''
        dict1 = {}
        lst1 = []
        lst2 = []
        passw = int(passw)
        loginuser = pandas.read_csv('ServerAccessSession/logged_in_Users.csv')
        self.session()
        dict1 = self.checked_users.to_dict('split')
        lendata = len(dict1['data'])
        for i in range(0, lendata):
            lst1.append(dict1['data'][i][0])
            lst2.append(int(dict1['data'][i][1]))
            print(lst2)
        if self.log_check:
            return "\nAlready logged in"
        if usr_id not in lst1:
            return "\nUsername not registered"
        if passw not in lst2:
            return "\nWrong password!"
        if usr_id in loginuser['username'].tolist():
            return "\nLogged in from different address"
        self.log_check = True
        self.usr_id = usr_id
        self.directory = ""
        tstore = pandas.DataFrame(columns=['username'])
        tstore['username'] = [usr_id]
        loginuser = loginuser.append(tstore)
        loginuser.to_csv('ServerAccessSession/logged_in_Users.csv', index=False)
        return "\nLogin Done."


    def quit(self):
        '''
        This function deals with signing out from the session of a given user
        ********
        After the command is entered the message "Signed out" is displayed
        and the session is signed out
        '''
        loginuser = pandas.read_csv('ServerAccessSession/logged_in_Users.csv')
        try:
            if self.usr_id in loginuser['username'].tolist():
                logindata = pandas.DataFrame(columns=['username'])
                logindata.to_csv('ServerAccessSession/logged_in_Users.csv', index=False)
            self.usr_id = None
            self.directory = ""
            self.log_check = False
            self.indx = {}
            return "\nSigned out"
        except KeyError:
            return "\nSigned out"

    def delete1(self, usr_id, pasw):
        '''
        This function is used to delete the given user
        ********
        The user must have Admin privilege to use this command 
        ********
        The admin can delete any user by entering the username 
        '''
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if self.log_check != True:
            return "\nlogin to proceed"
        if (logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values) != 1:
            return "\n need to be admin."
        if usr_id not in logdata['username'].tolist():
            return "\nNo user with username "+ usr_id + "found"
        if pasw != int(logdata.loc[logdata['username'] == usr_id]['password']):
            return "\nEnter the right password"
        count = int(logdata.loc[logdata['username'] == usr_id]['isAdmin'].values)
        lst1 = list()
        with open('ServerAccessSession/Users.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lst1.append(row)
                for field in row:
                    if field == usr_id:
                        lst1.remove(row)

        with open('ServerAccessSession/Users.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lst1)
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')

        if self.usr_id == usr_id:
            self.quit()

        if count == 1:
            filepath = "Root/Admin/"
        else:
            filepath = "Root/NotAdmin/"
        path = os.path.join(filepath, str(usr_id))
        rmtree(path)
        return"\nDeleting" + usr_id +"is success"


    def change_folder(self, directory):
        '''
        This function is used to change the directory of the user
        ********
        Admin can change the directory to any desired location
        ********
        '''
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        self.session()

        if not self.log_check:
            return "\nLogin to access"
        count1 = int(logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if count1 == 1:
            fileloc = "Root/Admin/"
        else:
            fileloc = "Root/NotAdmin/"
        path = os.path.join(fileloc, str(self.usr_id))

        dir4 = []
        for direc in os.walk(os.path.join(path)):
            dir4.append(os.path.normpath(os.path.realpath(direc)))
        patcha = os.path.join(path, self.directory, directory)
        patcha = os.path.normpath(os.path.realpath(patcha))
        print(self.directory)
        print(dir4)
        print(patcha)
        if patcha in dir4:
            self.directory = os.path.join(self.directory, directory)
            return "\n changed path to "+directory+"is success"
        else:
            return"\nenter correct path name"

    def commands(self):
        '''
        This function shows the commands that can be used in serverr client program
        ********
        The command and functions of the command
        are displayed in this fuction
        ********
        '''
        user_commands = ["register :","For registering the new user ,command:register <username> <password> <privilage>\n",
                 'login : ','To login, command:login <username> <password>,Note:password should be in integer\n',
                 'quit : ','To logout, command:quit\n',
                 'delete1 : ','To delete the user, command:delete1 <username> <password>\n',
                 'change_folder : ','To change the path, command:change_folder <name>\n',
                 'list : ','list of all files in the path, command:list\n',
                 'read_file : ','To read content from the file, command:read_file <name>\n',
                 'write_file : ','To write content into the file, command:write_file <name>\n',
                 'create_folder : ','To create new folder, command:create_folder <name>\n'
                ]

        msg = ''
        for i in range(0, len(user_commands), 2):
            msgline = ''.join([user_commands[i], user_commands[i+1]])
            msg += msgline + '*******\n'
            if i == len(user_commands):
                break
        return msg

    def list(self):
        
        self.session()
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if not self.log_check:
            return "\nLogin to access"
        count = (logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if count == 1:
            loc = os.path.join("Root/Admin/", str(self.usr_id), self.directory)
        else:
            loc = os.path.join("Root/NotAdmin/", str(self.usr_id), self.directory)
        dir4 = []
        for file_name in os.listdir(loc):
            mat = os.stat(os.path.join(loc, file_name))
            dir4.append([file_name, str(mat.st_size), str(time.ctime(mat.st_ctime))])
        det = "\nFile|Size|Modified Date"
        for data in dir4:
            data1 = " | ".join([data[0], data[1], data[2]]) + "\n"
            det += "-------\n" + data1
        return det


    def read_file(self, path):
        
        self.session()

        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if not self.log_check:
            return "\nLogin to access"
        pas = int(logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if pas == 1:
            path_d = os.path.join("Root/Admin/", str(self.usr_id), self.directory)
            path2 = "Root/Admin"
        else:
            path_d = os.path.join("Root/NotAdmin/", str(self.usr_id), self.directory)
            path2 = "Root/NotAdmin"

        files = []
        for file in os.listdir(os.path.join(path2, self.usr_id, self.directory)):
            if os.path.isfile(os.path.join(path2, self.usr_id, self.directory, file)):
                files.append(file)

        if path not in files:
            return "\ngiven file not found"
        t_path = os.path.join(path_d, path)
        if t_path not in list(self.indx.keys()):
            self.indx[t_path] = 0
        with open(t_path, "r") as fi:
            cont = fi.read()
        old_inx = str(self.indx[t_path]*self.nochar)
        indx = self.indx[t_path]
        data = cont[indx*self.nochar:(indx+1)*self.nochar]
        self.indx[t_path] += 1
        self.indx[t_path] %= len(cont)//self.nochar+1
        return "\n" + "Read file from " + old_inx + " to " + str(int(old_inx)+self.nochar) + "are\n" + data


    def write_file(self, path, data):
       
        self.session()
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if not self.log_check:
            return "\nLogin to access!!"
        pas = int(logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if pas == 1:
            rmpath = os.path.join("Root/Admin/", str(self.usr_id), self.directory, path)
            path2 = "Root/Admin/"
        else:
            rmpath = os.path.join("Root/NotAdmin/", str(self.usr_id), self.directory, path)
            path2 = "Root/NotAdmin/"
        t_file = []

        for file in os.listdir(os.path.join(path2, self.usr_id, self.directory)):
            if os.path.isfile(os.path.join(path2, self.usr_id, self.directory, file)):
                t_file.append(file)

        dat1 = ""
        for i in data:
            dat1 += i
        if path in t_file:
            with open(rmpath, "a+") as file:
                file.write(dat1)
            file.close()
            return"\nSuccess"
        with open(rmpath, "w+") as file:
            file.write(dat1)
        file.close()
        return"\nSuccessfully written"


    
    def rm_tree(self, rmpath):
        
        for child in pathlib.Path(rmpath).iterdir():
            if child.is_file():
                child.unlink()
            else:
                self.rm_tree(child)
        rmpath.rmdir()
    def session(self):
        
        self.checked_users = pandas.read_csv("ServerAccessSession/Users.csv")
        self.users_loged = pandas.read_csv("ServerAccessSession/logged_in_Users.csv")
    
    
