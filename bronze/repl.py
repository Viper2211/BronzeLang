import errors
from env import Env
from sys import argv
import preprocessing
import time
from os import system

while True:
    newCode = preprocessing.preprocess(input('>'))
    fname = '__repl__'
    open(fname+'.brz_in','w').write(newCode)
    Env(fname)
    system('g++ -o '+fname+".brz_out "+fname+'.cpp')
    system('chmod +x '+fname+'.brz_out')
    system(fname+'.brz_out')
