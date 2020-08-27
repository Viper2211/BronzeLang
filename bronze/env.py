from lexer import lex
from parser import *
import re

tab = 0
inFunction = False
functions = ""

# the main part of our code. Env class is a transpiler that will take our bronze code and produce the equivalent code in main.cpp as C++ code.
class Env():
  def __init__(self,source):
    self.source = source+'.brz_in'
    cppFile = source+'.cpp'
    global functions
    open(cppFile,'w').write('int main(){\n')
    
    # Processing the file again
    raw_lines = open(self.source,'r').readlines()
    lines = []
    for i in raw_lines:
      if len(re.match(r'[ \n\t]*',i).group())!=len(i.split(';')[0]):
        lines.append(i)
        
    # Actual start to lexing and parsing
    for i in lines:
      # Lexing
      tokens = lex(i)
      # Parsing
      parsed = parse(tokens)
      # Getting the ast
      parsed = classes[parsed[0]](parsed[1])
      
      # Based on the differnt ast, they will be written differently
      if type(parsed) in (Declaration,Assignment,Expression,FunctionCall,CppCode) and not inFunction:
        open(cppFile,'a').write(parsed.eval()+";\n")
      elif not inFunction and type(parsed) in (If,WhileLoop,ForLoop,End):
        open(cppFile,'a').write(parsed.eval()+"\n")
      else:
        if type(parsed) in (Function,End) :
          functions += parsed.eval()+"\n"
        else:
          functions += parsed.eval()+";\n"
          
    # Writing to the file
    open(cppFile,'a').write('}')
    currentCode = open(cppFile,'r').read()
    open(cppFile,'w').write('#include <iostream>\n#include <string>\n#include <cstdlib>\n'+functions+"\n"+currentCode)

#Initial variable assignment
class Declaration():
  'declaration : [#$%] ID = expression'
  def __init__(self,stream):
    writeStr = ""
    varType = stream.pop(0)[0]
    # Now, we will examine the code and if the character is a recognizable symbol, we will convert it into a string abbreviation of its data type.
    if varType == "#":
      writeStr += "int "
    elif varType == "$":
      writeStr += "std::string "
    elif varType == "%":
      writeStr += "bool "
    else:
      #otherwise, just ignore.
      pass
    # now, we will add our data type into our main code in main.cpp
    writeStr += stream.pop(0)[0]
    stream.pop(0)
    self.value = Expression(stream)
    self.writeStr = writeStr
  def eval(self):
    return f'{self.writeStr} = {self.value.eval()}'


# This is the class for re-assigning a variable later on.
class Assignment():
  'assignment : ID = expression'
  def __init__(self,stream):
    writeStr = ""
    # adding the new expression to our main.cpp
    writeStr += stream.pop(0)[0]
    stream.pop(0)
    self.value = Expression(stream)
    self.writeStr = writeStr
  def eval(self):
    return f'{self.writeStr} = {self.value.eval()}'


# Expression class to assign expressions without result. Ex: 5+6. Would assign + operator to 5 and 6 without evaluating result to 11.
class Expression():
  'expression: ID [+,-,*,/] ID'
  def __init__(self,stream):
    writeStr =""
    for i in stream:
      #checking the expression for if there is an operator, like 3 . If so, add a + sign. Otherwise, if it is a string like "cat", leave it as is.
      if i[0] =="~":
        writeStr += "+"+""
      else:
        writeStr += i[0]+" "
    self.writeStr = writeStr
  def eval(self):
    return self.writeStr


# If Statements
class If():
  'if statement : ? expression'
  def __init__(self,stream):
    global tab
    tab += 1
    stream.pop(0)
    writeStr = Expression(stream)
    self.writeStr = writeStr
  def eval(self):
    return 'if ( '+self.writeStr.eval()+') {'
    
    
# Else Statements
class Else():
  'else - :'
  def __init__(self,stream):
    global tab
    tab += 1
  def eval(self):
    return '} else {'


# While Loop construct
class WhileLoop():
  'while loop : @@ expression'
  def __init__(self,stream):
    global tab
    tab += 1
    stream.pop(0)
    writeStr = Expression(stream)
    self.writeStr = writeStr
  def eval(self):
    return 'while ( '+self.writeStr.eval()+') {'
    
    
# For loop construct
class ForLoop():
  '''for loop : @ ID expression|expression
                @ ID expression|expression|expression '''
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


# Functions
class Function():
  'function : ^ [#$%] ( [#$%] ID , ... )'
  def __init__(self,stream):
    global tab, inFunction
    inFunction = True
    stream.pop(0)
    writeStr = ""
    for i in stream:
      # now we will check to relate symbols to their data types. if the data type is not found, we will try to evaluate whatever symbol is given.
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
    

#program runs and calls to function. Then, function does a task and returns back to main program.
class FunctionCall:
  'function call : ID ( expression , ...)'
  def __init__(self,stream):
    self.writeStr = ""
    for i in stream:
      self.writeStr += i[0]
  def eval(self):
    return self.writeStr
    
    
# Return Statement
class Return():
  'return : >> expression'
  def __init__(self,stream):
    stream.pop(0)
    self.writeStr = "return "
    self.expr = Expression(stream)
  def eval(self):
    return f'{self.writeStr}{self.expr.eval()}'
    
    
#Closing Bracket
class End():
  'end: }'
  def __init__(self,stream):
    global tab
    if tab > 0:
      tab -= 1
    self.writeStr = "}"
  def eval(self):
    global inFunction
    inFunction = False
    return self.writeStr


# class to compile code using C ++. Compiler is main.cpp
class CppCode():
  def __init__(self,stream):
    self.writeStr = ""
    #now, we will compile our code by copying every line of code from main.cpp except for the skeleton and like a transpiler.
    self.writeStr = stream[0][0][5:]
  def eval(self):
    return self.writeStr

# Dictionary holding all classes
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
  p_cpp:CppCode,
}