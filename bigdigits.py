import sys
import numpy

#Defining digits

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
m=0
while m<7:
    line=""
    n=0
    while n<len(sys.argv[1]):
        g=int(sys.argv[1][n])
        d=digits[g]
        line=line+(d[m])+"  "
        n=n+1
    print line
    m=m+1
