

def preprocess(code:str):
  lines = code.split('\n')
  for i in range(0,len(lines)):
    line = lines[i]
    if line[:3] == "-->":
      fileName = line[4:]
      fileContent = open(fileName,'r').read() 
      lines[i] = fileContent
  return "\n".join(lines)

