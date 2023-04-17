import unittest 
from unittest.mock import patch 
from io import StringIO 
import sys 
 
def method(): 
 
  input_num = float(input('Type a number.')) 
  remainder = input_num % 2 
  if remainder == 0: 
    print('Number is even.') 
  else: 
    print('Number is odd.') 
class myTests(unittest.TestCase): 
    # get_input will return 'yes' during this test 
    @patch('builtins.input',return_value='5') 
    def testOdd(self, input): 
        capturedOutput = StringIO()          # Create StringIO object 
        sys.stdout = capturedOutput                   #  and redirect stdout. 
        method()                                  # Call unchanged function. 
        sys.stdout = sys.__stdout__                   # Reset redirect. 
        outputArray = capturedOutput.getvalue().split('\n') 
        if (len(outputArray)>1): 
            outputArray.pop() 
        self.assertEqual(outputArray, 
           ['Number is odd.'],) 
 
    @patch('builtins.input',return_value='4') 
    def testEven(self, input): 
        capturedOutput = StringIO()          # Create StringIO object 
        sys.stdout = capturedOutput                   #  and redirect stdout. 
        method()                                  # Call unchanged function. 
        sys.stdout = sys.__stdout__                   # Reset redirect. 
        outputArray = capturedOutput.getvalue().split('\n') 
        if (len(outputArray)>1): 
            outputArray.pop() 
        self.assertEqual(outputArray, 
           ['Number is even.'],) 
 
tests = [myTests().testOdd(),myTests().testEven()] 
_test_result = tests[0] 
for test in tests: 
    if test is not None: 
        _test_result = test 
print(test[0])
