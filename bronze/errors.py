from sys import exit

# Base class
class Error():
  def __init__(self,description="...",error_no=1):
    self.name = self.__class__.__name__
    self.description = description
    # Displaying error 
    # May change
    print(f"{self.name} : {self.description}")
    # Ending the program
    exit(error_no)

# FileDoesntExistError
class FileDoesntExistError(Error):
  def __init__(self):
    super().__init__(description="That file doesnt seem to exist. Please enter a valid filename",error_no=1)

  