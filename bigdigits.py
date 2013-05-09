import sys
import numpy

#creating big  digits

Zero = [" 00000 ","0     0","0     0","0     0","0     0","0     0"," 00000 "]
One = ["    1   ","  1 1   ","    1   ","    1   ","    1   ","    1   ","11111111",]
Two = ["   22   "," 2    2 ","2      2","     2  ","   2    "," 2      ","22222222"]
Three = ["  333   ","3     3 ","     3  ","   3    ","     3  ","3     3 ","  333   "]
Four = ["      4  ","    4 4  ","   4  4  ","  4   4  "," 44444444","      4  ","      4  "]
Five = ["55555555","5       ","555555  ","      5 ","       5","      5 ","555555  "]
Six = ["     6","   6   "," 6     ","6 6666 ","66    6","66    6","  6666 "]
Seven = ["77777777","      7 ","     7  ","    7   ","   7    ","  7     "," 7      "]
Eight = ["  88888 ","8     8"," 8   8 ","  888  "," 8   8 ","8     8"," 88888 "]
Nine = ["  99999   "," 9     9  "," 9     9  ","  99999   ","     9    ","    9     ","   9      "]
digits=[Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine]

m=0 #m represents the row within each number
while m<7: #each number in digits is seven characters high, therefore m can be at most six.
    n=0 #n represents the column within the user input
    while n<len(sys.argv[1]): #the maximum number of columns is one less than the number of characters in the number entered by the user
        g=int(sys.argv[1][n]) #define g as the integer value of the nth column of the number entered by the user
        d=digits[g] #d is the entry in the list digits that has index g. Since the digits list is the names of the integers in numerical order, digits[g] is the name of whatever integer g happens to be. This index g in digits was defined as a list above.
        print (d[m])+"  ", #print the mth row of the list d as well as a small amount of white space to act as a buffer between the numbers
        n=n+1 #n, being the column number, takes on integer values.
    print '' #once the mth row has been printed for all n up to one less than the length of the user input, move to the next row
    m=m+1 #m, being the row number, takes on integer values

