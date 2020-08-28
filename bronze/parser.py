# Data types
STRING = 'STRING'
NUMBER = 'NUMBER'
BOOL = 'BOOLEAN'
ID = 'IDENTIFIER'
# Keywords
IF = 'IF'
ELSE = 'ELSE'
FOR = 'FOR'
WHILE = 'WHILE'
FUNC = 'FUNCTION'
END = 'END'
RETURN = 'RETURN'
# Other
OP = 'OP'
CPP = 'C++ CODE'

# Expect function
# Checks if there is a match. Else, raises errror
def expect(stream:list, token:str):
  try:
    if stream[0][1] == token:
      return stream.pop(0)
    raise SyntaxError('Invalid Token')
  except:
    return False
    
# Accept function
# Checks if there is a match. Else, returns false
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

# Recursive checking for expressions 
def p_expr(stream:list)->bool:
  # If there is a number
  if accept(stream,(NUMBER,ID)) and len(stream)>1:
    # If there is an op, continue!
    if accept(stream,OP)[0] in ("+",'-','*','/','%'):
      return p_expr(stream)
    return True
  # If there is a string
  if accept(stream,(STRING,ID)) and len(stream)>1:
    # If there is a string concatenation op, continue
    if accept(stream,OP)[0] == '~':
      return p_expr(stream)
    return True
  # If there is a bool
  if accept(stream,(BOOL,ID)) and len(stream)>1:
    # If a boolean op follows, continue
    if accept(stream,OP)[0] in ('==','>','<','<=','>=','!=','&&','||'):
      return p_expr(stream)
    return True

  # If the stream is empty, return True
  if len(stream) == 0:
    return True

  # If there were no matches, this is not an expression
  return False

# Variable declaration
def p_declaration(stream:list)->bool:
  'declaration : [#$%] ID = expression'
  if accept(stream,OP)[0] in ("#",'$','%'):
    expect(stream,ID)
    if accept(stream,OP)[0] == "=":
      p_expr(stream)
      return True
  return False

# Assignment
def p_assignment(stream:list)->bool:
  'assignment : ID = expression'
  if expect(stream,ID):
    if accept(stream,OP)[0] == "=":
      if p_expr(stream):
        return True
  return False

# If statements
def p_if(stream:list)->bool:
  'if statement : ? expression'
  if expect(stream,IF):
    if p_expr(stream):
      return True
  return False
# For loop
def p_for(stream:list)->bool:
  '''for loop : @ ID expression|expression
                @ ID expression|expression|expression '''
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

def p_cpp(stream:list):
  'c++ : cpp__ {c++ code here}'
  if accept(stream,CPP):
    return True
  return False

# Functions
def p_function(stream:list)->bool:
  'function : ^ [#$%] ( [#$%] ID , ... )'
  if expect(stream,FUNC):
    return True
  return False

# Function call
def p_function_call(stream:list)->bool:
  'function call : ID ( expression , ...)'
  if expect(stream,ID):
    if expect(stream,OP)[0] == '(':
      return True
  return False

# While Loop
def p_while(stream:list)->bool:
  'while loop : @@ expression'
  if expect(stream,WHILE):
    if p_expr(stream):
      return True
  return False

# Else
def p_else(stream:list)->bool:
  'else - :'
  if expect(stream,ELSE):
    return True
  return False

# Return statement
def p_return(stream:list)->bool:
  'return : >> expression'
  if expect(stream,RETURN):
    return True
  return False

# End of loops or function defs
def p_end(stream:list)->bool:
  'end : .'
  if expect(stream,END):
    return True
  return False

# All the different possibilities
parsers = [p_function,p_function_call,p_for,p_while,p_if,p_return,p_else,p_end,p_declaration,p_assignment,p_expr,p_cpp]  

# Parse function
# Goes through all the parsers, and chooses the right one for that stream
# It then returns it
def parse(stream:list):
  streamCopy = stream.copy()
  for parser in parsers:
    try:
      if parser(streamCopy):
        return parser, stream
    except:
      pass
  return False, stream