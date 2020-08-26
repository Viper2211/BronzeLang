import re
import parser

tokens = {
  r'\?':parser.IF,
  r'\@':parser.FOR,
  r'\.':parser.END,
  r"\d+":parser.NUMBER,
  r'"[^"]*"':parser.STRING,
  r'[a-zA-Z][a-zA-Z0-9_]*':parser.ID,
  r'\S':parser.OP,
}

def lex(code):
  stream = []
  code = code.replace('\n','')
  code = code.split(';')[0]
  while code:
    while code[0] in (' ','\t'):
      code = code[1:]
    for token in tokens:
      match = re.match(token, code)
      if match:
        code = code[len(match.group(0)):] 
        stream.append((match.group(0), tokens[token]))
  return stream