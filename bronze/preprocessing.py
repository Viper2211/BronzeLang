import errors

# Preprocess
def preprocess(code:str)->str:
  "preproccesing code. returns string"
  lines = code.split('\n')
  
  for i in range(0,len(lines)):
    line = lines[i]
    # checking for imports
    if line[:3] == "-->":
      fileName = line[4:]
      fileName = fileName.replace(' ','')
      fileName = fileName.replace('\n','')
      fileName = fileName.replace('\t','')
      try:
        fileContent = open(fileName,'r').read() 
      except: 
        print(fileName)
        errors.FileDoesntExistError()
      lines[i] = fileContent
  
  return "\n".join(lines)