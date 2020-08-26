import errors
from env import Env
from sys import argv
import time
from os import system

def start():
  startTime = time.time()
  try :
    environment = Env(argv[1])
    fname = argv[1].split('.brz')[0]
    system('g++ -o ./'+fname+".brz_out "+fname+'.cpp')
    if len(argv) == 3:
      if argv[2] == "run":
        system('chmod +x ./'+fname+'.brz_out')
        system('./'+fname+'.brz_out')
  except:
    raise
    errors.FileDoesntExistError()

  return time.time()-startTime

if __name__ == "__main__":
  print(f"\033[92m=> Compiled and exited in {start()} seconds")