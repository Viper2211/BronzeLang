from lexer import lex
from parser import *

tab = 1
inFunction = False
functions = ""

class Env():
  def __init__(self,source):
    self.source = source
    global functions
    open('main.cpp','w').write('int main(){\n')
    for i in open(self.source,'r').readlines():
      tokens = lex(i)
      parsed = parse(tokens)
      parsed = classes[parsed[0]](parsed[1])
      if type(parsed) in (Declaration,Assignment,Expression,FunctionCall) and not inFunction:
        open('main.cpp','a').write('\t'*tab +parsed.eval()+";\n")
      elif not inFunction and type(parsed) in (If,WhileLoop,ForLoop,End):
        open('main.cpp','a').write('\t'*tab +parsed.eval()+"\n")
      else:
        if type(parsed) == Function or type(parsed) == End:
          functions += parsed.eval()+"\n"
        else:
          functions += parsed.eval()+";\n"
    open('main.cpp','a').write('}')
    currentCode = open('main.cpp','r').read()
    open('main.cpp','w').write('#include <iostream>\n#include <string>\n'+functions+"\n"+currentCode)

class Declaration():
  def __init__(self,stream):
    writeStr = ""
    varType = stream.pop(0)[0]
    if varType == "#":
      writeStr += "int "
    elif varType == "$":
      writeStr += "std::string "
    elif varType == "%":
      writeStr += "bool "
    else:
      pass
    writeStr += stream.pop(0)[0]
    stream.pop(0)
    self.value = Expression(stream)
    self.writeStr = writeStr
  def eval(self):
    return f'{self.writeStr} = {self.value.eval()}'

class Assignment():
  def __init__(self,stream):
    writeStr = ""
    writeStr += stream.pop(0)[0]
    stream.pop(0)
    self.value = Expression(stream)
    self.writeStr = writeStr
  def eval(self):
    return f'{self.writeStr} = {self.value.eval()}'

class Expression():
  def __init__(self,stream):
    writeStr =""
    for i in stream:
      if i[0] =="~":
        writeStr += "+"+""
      else:
        writeStr += i[0]+" "
    self.writeStr = writeStr
  def eval(self):
    return self.writeStr
    
class If():
  def __init__(self,stream):
    global tab
    tab += 1
    stream.pop(0)
    writeStr = Expression(stream)
    self.writeStr = writeStr
  def eval(self):
    return 'if ( '+self.writeStr.eval()+') {'

class Else():
  def __init__(self,stream):
    global tab
    tab += 1
  def eval(self):
    return '} else {'

class WhileLoop():
  def __init__(self,stream):
    global tab
    tab += 1
    stream.pop(0)
    writeStr = Expression(stream)
    self.writeStr = writeStr
  def eval(self):
    return 'while ( '+self.writeStr.eval()+') {'

class ForLoop():
  def __init__(self,stream):
    global tab
    tab += 1
    writeStr = ""
    stream.pop(0)
    self.varName = stream.pop(0)[0]
    self.sep1 = 0
    for i in range(0,len(stream)):
      if stream[i][0] == "|":
        self.sep1 = i
        break
    self.sep2 = False
    for i in range(0,len(stream)):
      if stream[i][0] == "|" and i > self.sep1:
        self.sep2 = i
        break
    self.start = Expression(stream[:self.sep1])
    if self.sep2:
      self.end = Expression(stream[self.sep1+1:self.sep2])
      self.increment = Expression(stream[self.sep2+1:]).eval()
    else:
      self.end = Expression(stream[self.sep1+1:])

    self.start,self.end= self.start.eval(),self.end.eval()

  def eval(self):
    if not self.sep2:
      return f'for (int {self.varName}={self.start};{self.varName}<{self.end};{self.varName}++) '+'{'
    return f'for (int {self.varName}={self.start};{self.varName}<{self.end};{self.varName}+={self.increment}) '+'{'

class Function():
  def __init__(self,stream):
    global tab, inFunction
    inFunction = True
    stream.pop(0)
    writeStr = ""
    for i in stream:
      if i[0] == "#":
        writeStr += "int"
      elif i[0] == "$":
        writeStr += "std::string"
      elif i[0] == "%":
        writeStr += "bool"
      else:
        writeStr += " "+i[0]+" "
    self.writeStr = writeStr
  def eval(self):
    return self.writeStr+'{'

class FunctionCall:
  def __init__(self,stream):
    self.writeStr = ""
    for i in stream:
      self.writeStr += i[0]
  def eval(self):
    return self.writeStr

class Return():
  def __init__(self,stream):
    stream.pop(0)
    self.writeStr = "return "
    self.expr = Expression(stream)
  def eval(self):
    return f'{self.writeStr}{self.expr.eval()}'

class End():
  def __init__(self,stream):
    global tab
    if tab > 0:
      tab -= 1
    self.writeStr = "}"
  def eval(self):
    global inFunction
    inFunction = False
    return self.writeStr

classes = {
  p_end:End,
  p_if:If,
  p_declaration:Declaration,
  p_expr:Expression,
  p_assignment:Assignment,
  p_for:ForLoop,
  p_while:WhileLoop,
  p_else:Else,
  p_function:Function,
  p_return:Return,
  p_function_call:FunctionCall,
}