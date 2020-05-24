import unittest
import sys
import pandas
from Userclass import User

class prog_test(unittest.TestCase):
    '''
    This class is used to test all the functionalities of the program
    '''
    def regitest(self):
        '''
        Used to test the register fuctionality of the program
        '''
        datalog = pandas.DataFrame(columns=['username'])
        datalog['username'] = ['test1']
        datalog['password'] = ['1234']
        datalog['isAdmin'] = 1
        datatest = User()
        datatest.is_login = True
        datatest.delete1('test1', 1234)
        datatest.createdusers = datalog
        expect = ['\nRegistered user successfully.']
        gathresult = []
        test1 = [
            ['test1', '1234', 'Admin']
        ]

        for test in test1:
            gathresult.append(datatest.register(test[0], test[1], test[2]))

        print(datatest.delete1('test1', 1234))

        self.assertListEqual(gathresult, expect)

    def logintest(self):
        '''
        This function is used to test the login feature of the program
        '''
        datalog = pandas.DataFrame(columns=['username'])
        datalog['username'] = ['test']
        datalog['password'] = ['123']
        datalog['isAdmin'] = 1
        datatest = User()
        datatest.createdusers = datalog
        datatest.login('test', 123)
        print(datatest.delete1('test', 123))
        datatest.register('test', '123', 'admin')
        expect = ['\nWrong password!']
        gathresult = []
        test1 = [
            ['test', '1234'],
        ]

        for test in test1:
            gathresult.append(datatest.login(test[0], test[1]))
        datatest.is_login = True
        print(datatest.delete1('test', 123))
        datatest.quit()

        self.assertListEqual(gathresult, expect)    


    def commandtest(self):
        '''
        This fuction tests wheather the commands are displaying correctly
        or not.
        '''
        datatest = User()
        exptoutput = datatest.commands

        datatest.quit()

        lotest = pandas.DataFrame(columns=['username', 'password', 'isAdmin'])
        lotest.to_csv('ServerAccessSession/Users.csv', index=False)

        self.assertTrue(exptoutput)


    def quittest(self):
        '''
        This fuction is used to test weather the session is quiting or not.
        '''
        expresult = ["\nSigned out"]
        obtresult = []

        datatest = User()

        obtresult.append(datatest.quit())

        login_rst = pandas.DataFrame(columns=['username', 'password', 'isAdmin'])
        login_rst.to_csv('ServerAccessSession/Users.csv', index=False)

        self.assertListEqual(obtresult, expresult)


def completest(usetest):
    '''
    This fuction tests all the functionalities of the program.
    '''
    load = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(load.loadTestsFromTestCase(usetest))
    runtest = unittest.TextTestRunner(verbosity=2)
    result = runtest.run(suite)

    if result.skipped:
        return False

    return result.wasSuccessful()

def testing():
    '''
    This function tests the all completed fuctions steps.
    '''
    print('*'*60 + "\nTesting:\n")
    return completest(prog_test)

if __name__ == "__main__":
    if testing() is not True:
        print("\n\tThe test failed,")
        sys.exit(1)

    sys.exit(0)
