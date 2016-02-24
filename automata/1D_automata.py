#!/usr/bin/env python2
#coding: utf8
#A general 1D automata that takes any rule accordung to the wolfram code with S=2 and D=1
#https://en.wikipedia.org/wiki/Wolfram_code
import random
import sys
import argparse

def dead_life2(l,rules,rule_range):
    roll      = lambda l,n: l[n:]+l[:n] #shift a list circular by n
    add       = lambda x,y: str(x)+str(y) #add two inputs into a string
    dead_life = lambda x: 1 if(x in rules) else 0 #decide state of cell for next step
    l_=roll(l,-rule_range) #temporary list containing the neighbourhood of each cell
    for i in range(-rule_range,rule_range):
        l_=map(add,l_,roll(l,i+1)) #creates a temporary list f 
    l=map(dead_life,l_) #compute next state
    return l    

def main():
    parser = argparse.ArgumentParser(description='1D cellular automata', epilog='By default the options used are:\n -rule 110 -length 80 -values 1 -steps 20')
    parser.add_argument('-rule', '-r',default=110, metavar='N', type=int,
                    help='Give the set of rules by its decimal identity. Rule can be choosen almost arbitrary big.')
    parser.add_argument('-length', '-l', metavar='LEN', default='80', type=int, help='An integer that gives the number of cells.')
    parser.add_argument('-values', '-v', default='1', type=int, help='An integer that defines the start condition of the cells.')
    parser.add_argument('-steps', '-s', default=20, type=int, help='Number of iteration steps.')
    parser.add_argument('-rand','-random', action='store_true', help='Set this flag for random starting conditions.')
    parser.add_argument('-file','-f', type=argparse.FileType('w', 0), help='Specify the file you want to save to.')
    args = parser.parse_args() #parse the command line options into args
    if (args.rand == True): l=[random.randrange(0,2) for x in range(args.length)] #fill l with random values
    else: #fill l depending on user choice
        l=[]
        for i in  str(args.values): l.append(max(min(int(i),1),0))
        if (args.length-1>len(l)): l=[0]*(((args.length-len(l))//2)+(args.length-len(l))%2)+l+[0]*((args.length-len(l))//2)    
    rule_range=1 #number of neighbours in each direction
    while 2**(2**(1+2*rule_range))<=args.rule: rule_range+=1 #update number of neighbours depending of user rule
    b=(2**((1+2*rule_range))-(len(bin(args.rule)[2:])))*'0'+str(bin(args.rule)[2:]) #translate user rule into a binary string (example: rule 90 --> 01011010)
    rules=[(len(bin(len(b)-1))-len(bin(n)))*'0'+bin(n)[2:] for n in range(len(b)) if b[(len(b))-n-1]=='1'][::-1] #creates a list of all conditions resulting to 1
    signs={0:" ",1:u"\u2588"} #Specifies the characters used for drawing
    if (args.file==None): print("".join([signs[i] for i in l]))
    else: args.file.write(("".join([signs[i] for i in l])+"\n").encode('utf8')) #out to screen/file
    for i in range(0,args.steps-1):
        l=dead_life2(l,rules,rule_range) #calculate next step
        if (args.file==None): print("".join([signs[i] for i in l]))
        else: args.file.write(("".join([signs[i] for i in l])+"\n").encode('utf8')) #out to screen/file
    if (args.file!=None): args.file.close()

if __name__ == '__main__':
    main()
