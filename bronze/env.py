from lexer import lex
from parser import *
import re

tab = 0
inFunction = False
functions = ""
starter = '#include <iostream>\n#include <string>\n#include <cstdlib>\n#include <cmath>\n#include <ctime>\n'

# the main part of our code. Env class is a transpiler that will take our bronze code and produce the equivalent code in main.cpp as C++ code.
class Env():
  def __init__(self,source):
    self.source = source+'.brz_in'
    cppFile = source+'.cpp'
    global functions

    # setting up the file
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
      try:
        parsed = classes[parsed[0]](parsed[1])
      except: raise
      # Based on the different ast, they will be written differently
      if type(parsed) in (Declaration,Assignment,Expression,FunctionCall,CppCode) and not inFunction:
        open(cppFile,'a').write(parsed.eval()+";\n")
      elif not inFunction and type(parsed) in (If,WhileLoop,ForLoop,End):
        open(cppFile,'a').write(parsed.eval()+"\n")
      else:
        if type(parsed) in (Function,Class) :
          functions += parsed.eval()+"\n"
        else:
          functions += parsed.eval()+";\n"
          
    # Writing to the file
    open(cppFile,'a').write('}')
    currentCode = open(cppFile,'r').read()
    open(cppFile,'w').write(starter+functions+"\n"+currentCode)

#Initial variable assignment
class Declaration():
  'declaration : [#$%] ID = expression'
  def __init__(self,stream):
    writeStr = ""
    # Now, we will examine the code and if the character is a recognizable symbol, we will convert it into a string abbreviation of its data type.
    while stream[1][0] != "=":
      if stream[0][0] == "#":
        writeStr += "int "
        stream.pop(0)
      elif stream[1][0] == "|":
        writeStr += "list "
        stream.pop(0)
      elif stream[0][0] == "##":
        writeStr += "float "
        stream.pop(0)
      elif stream[0][0] == "$":
        writeStr += "std::string "
        stream.pop(0)
      elif stream[0][0] == "%":
        writeStr += "bool "
        stream.pop(0)
      elif stream[0][0] == "_":
        writeStr += "public : "
        stream.pop(0)
      elif stream[0][0] == "__":
        writeStr += "protected : "
        stream.pop(0)
      elif stream[0][0] == "___":
        writeStr += "private : "
        stream.pop(0)
      else:
        writeStr += stream[0][0]+" "
        stream.pop(0)
    # now, we will add our data type into our main code in main.cpp
    writeStr += stream.pop(0)[0]

    self.value = Expression(stream)
    self.writeStr = writeStr
  def eval(self):
    return f'{self.writeStr} {self.value.eval()}'


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
        writeStr += i[0]
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
    # Getting the identifiers name
    self.varName = stream.pop(0)[0]
    # Checking for the first seperator and finding the index
    self.sep1 = 0
    for i in range(0,len(stream)):
      if stream[i][0] == "|":
        self.sep1 = i
        break
    # Check for the second seperator. If it does not exist, sep2 will remain False
    self.sep2 = False
    for i in range(0,len(stream)):
      if stream[i][0] == "|" and i > self.sep1:
        self.sep2 = i
        break

    # The start of the range
    self.start = Expression(stream[:self.sep1])
    # If a second "|" exists, then proceed to get the increment 
    if self.sep2:
      self.end = Expression(stream[self.sep1+1:self.sep2])
      self.increment = Expression(stream[self.sep2+1:]).eval()
    else:
      # Otherwise, just get the end value of the range
      self.end = Expression(stream[self.sep1+1:])

    self.start,self.end= self.start.eval(),self.end.eval()

  def eval(self):
    # If there no increment return something with an increment of 1
    if not self.sep2:
      return f'for (int {self.varName}={self.start};{self.varName}<{self.end};{self.varName}++) '+'{'
    # Otherwise increment the variable with this
    return f'for (int {self.varName}={self.start};{self.varName}<{self.end};{self.varName}+={self.increment}) '+'{'


# Functions
class Function():
  'function : ^ [#$%] ( [#$%] ID , ... )'
  def __init__(self,stream):
    global tab, inFunction
    inFunction = True
    tab += 1
    stream.pop(0)
    writeStr = ""
    for i in stream:
      # now we will check to relate symbols to their data types. if the data type is not found, we will try to evaluate whatever symbol is given.
      if i[0] == "#":
        writeStr += "int"
      elif i[0] == "##":
        writeStr += "float "
      elif i[0] == "$":
        writeStr += "std::string"
      elif i[0] == "%":
        writeStr += "bool"
      elif i[0] == "_":
        writeStr += "public :"
      elif i[0] == "__":
        writeStr += "protected :"
      elif i[0] == "___":
        writeStr += "private :"
      else:
        writeStr += " "+i[0]+" "
    self.writeStr = writeStr
  def eval(self):
    return self.writeStr+'{'
    
class Class():
  'class : ^^ ID'
  def __init__(self,stream):
    global tab, inFunction
    inFunction = True
    tab += 1
    stream.pop(0)
    self.writeStr = "class "+stream[0][0]
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
    if stream.pop(0)[0] != ">>":
      raise Exception
    self.writeStr = "return "
    # Just get an expr
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
    self.tab = tab
    self.writeStr = "}"
  def eval(self):
    global inFunction
    if self.tab == 0: inFunction = False
    return self.writeStr


# class to write cpp code in bronze
class CppCode():
  'c++ : cpp:: expression'
  def __init__(self,stream):
    self.writeStr = ""
    #now, we will add the code to the writestr, popping off the "cpp::"
    self.writeStr = stream[0][0][5:]
  def eval(self):
    return self.writeStr

# Dictionary holding all classes
classes = {
  p_class:Class,
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