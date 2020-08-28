import re
import parser

# Tokens
tokens = {
  r"cpp\_\_ [\s\S]*":parser.CPP,
  r'\?':parser.IF,
  r'\@\@':parser.WHILE,
  r'\@':parser.FOR,
  r'\:':parser.ELSE,
  r'\^':parser.FUNC,
#  r'\^\^':parser.CLASS,
  r'\.':parser.END,
  r"\d+":parser.NUMBER,
  r'\>\>':parser.RETURN,
  r'true|false':parser.BOOL,
  r'"[^"]*"':parser.STRING,
  r'Args\.\.\.':parser.ID,
  r'\&[a-zA-Z][a-zA-Z0-9_]*':parser.ID,
  r'\*[a-zA-Z][a-zA-Z0-9_]*':parser.ID,
  r'[a-zA-Z][a-zA-Z0-9_]*':parser.ID,
  r'\>\=':parser.OP,
  r'\<\=':parser.OP,
  r'\=\=':parser.OP,
  r'\!\=':parser.OP,
  r'\|\|':parser.OP,
  r'\&\&':parser.OP,
  r'\S':parser.OP,
}

# Lex function
def lex(code):
  # Stream : the list we are going to be returning
  stream = []
  # Setting up the code for lexing
  code = code.replace('\n','')
  code = code.replace('\t',' ')
  if "\\cpp\\" not in code:
    code = code.split(';')[0]

  # While the code still exists, match the code with the tokens
  while code and len(code) > 0:
    try:
      # Ignoring whitespace
      while code[0] in (' '):
        code = code[1:]
    except:
      pass
    
    # If there is a match, add that token to the stream
    matched = False
    for token in tokens:
      match = re.match(token, code)
      if match:
        code = code[len(match.group(0)):] 
        matched = True
        stream.append((match.group(0), tokens[token]))
    # Else, return -1
    if not matched:
      stream.append((code,-1))
      return stream

  # Return the stream
  return stream