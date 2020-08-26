# Data types
STRING = 'STRING'
NUMBER = 'NUMBER'
ID = 'IDENTIFIER'
IF = 'IF'
FOR = 'FOR'
END = 'END'

# Other
OP = 'OP'

def expect(stream:list, token:str):
  try:
    if stream[0][1] == token:
      return stream.pop(0)
    raise SyntaxError('Invalid Token')
  except:
    return False
    
def accept(stream:list, token):
  try:
    first = stream[0][1]
    if type(token) == str:
      if first == token:
        return stream.pop(0)
    elif type(token) == tuple:
      for i in token:
        if first == i:
          return stream.pop(0)
  except:
    return False

def p_expr(stream:list)->bool:
  if accept(stream,(NUMBER,ID)) and len(stream)>1:
    if accept(stream,OP)[0] in ("+",'-','*','/','%'):
      return p_expr(stream)
    return True
  if accept(stream,(STRING,ID)) and len(stream)>1:
    if accept(stream,OP)[0] == '~':
      return p_expr(stream)
    return True
  if len(stream) == 0:
    return True
  return False

def p_declaration(stream:list)->bool:
  if accept(stream,OP)[0] in ("#",'$'):
    expect(stream,ID)
    accept(stream,OP)
    p_expr(stream)
    return True
  return False

def p_assignment(stream:list)->bool:
  if expect(stream,ID):
    if accept(stream,OP)[0] == "=":
      if p_expr(stream):
        return True
  return False

def p_if(stream:list)->bool:
  if expect(stream,IF):
    if p_expr(stream):
      return True
  return False

def p_for(stream:list)->bool:
  sep1 = 0
  for i in range(0,len(stream)):
    if stream[i][0] == "|":
      sep1 = i-2
  sep2 = False
  for i in range(0,len(stream)):
    if stream[i][0] == "|":
      sep1 = i-2
  if sep2:
    sep1 -= 2

  if expect(stream,FOR):
    if expect(stream,ID):
      if p_expr(stream[:sep1]):
        while not accept(stream,OP):
          stream.pop(0)
        if p_expr(stream[:sep2]):
          if sep2:
            while not accept(stream,OP):
              stream.pop(0)
            if p_expr(stream):
              return True
          return True
  return False

def p_end(stream:list)->bool:
  if expect(stream,END):
    return True
  return False

parsers = [p_for,p_if,p_end,p_declaration,p_assignment,p_expr]  

def parse(stream:list) :
  streamCopy = stream.copy()
  for parser in parsers:
    try:
      if parser(streamCopy):
        return parser, stream
    except:
      pass
  return False, stream