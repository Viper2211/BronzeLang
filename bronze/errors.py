from sys import exit

class Error():
  def __init__(self,description="...",error_no=1):
    self.name = self.__class__.__name__
    self.description = description 
    print(f"{self.name} : {self.description}")
    exit(error_no)

class FileDoesntExistError(Error):
  def __init__(self):
    super().__init__(description="That file doesnt seem to exist. Please enter a valid filename",error_no=23)

  