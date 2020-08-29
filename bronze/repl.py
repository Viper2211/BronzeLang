import errors
from env import Env
from sys import argv
import preprocessing
import time
from os import system

code = ""

while True:
  code = preprocessing.preprocess(input('>')+'\n')
  open('__repl.brz_in','w').write(code)
  Env('__repl')
  system('g++ -o __repl.brz_out __repl.cpp')
  system('chmod +x __repl.brz_out')
  system('./__repl.brz_out')
