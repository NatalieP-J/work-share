#!/usr/bin/python
#File exploring capabilities of __init__

class Colour:
    def __init__(self,colour,age):
        self.colour=colour
        self.age=age
    def colourScheme(self):
        print 'The colour of the TARDIS is', self.colour
        print 'The doctor is', self.age, 'years old'

p=Colour(raw_input('What is your favourite colour?'),raw_input('How old is the world?'))
p.colourScheme()
