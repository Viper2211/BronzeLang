import re
import parser

tokens = {
  r'\?':parser.IF,
  r'\@\@':parser.WHILE,
  r'\@':parser.FOR,
  r'\:':parser.ELSE,
  r'\.':parser.END,
  r"\d+":parser.NUMBER,
  r'true|false':parser.BOOL,
  r'"[^"]*"':parser.STRING,
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

def lex(code):
  stream = []
  code = code.replace('\n','')
  code = code.split(';')[0]
  while code and len(code) > 0:
    try:
      while code[0] in (' ','\t'):
        code = code[1:]
    except:
      pass
    for token in tokens:
      match = re.match(token, code)
      if match:
        code = code[len(match.group(0)):] 
        stream.append((match.group(0), tokens[token]))
  return stream