# Imports
import errors
from env import Env
from sys import argv
import preprocessing
import time
from os import system

# File name
fileName = ""

def start():
  # Getting the start time
  startTime = time.time()
  try :
    # Executing and compiling everything
    newCode = preprocessing.preprocess(open(argv[1],'r').read())
    fname = argv[1].split('.brz')[0]
    open(fname+'.brz_in','w').write(newCode)
    Env(fname)
    system('g++ -o '+fname+".brz_out "+fname+'.cpp')
    system('chmod +x '+fname+'.brz_out')
  except:
    raise
    errors.FileDoesntExistError()

  return time.time()-startTime,fname

if __name__ == "__main__":
  speed,filename = start()
  print(f"\033[92m=> Compiled in {speed} seconds\033[0m")
  # Deleting unnecessary files
  system('rm '+filename+'.brz_in')
  system('rm '+filename+'.cpp')