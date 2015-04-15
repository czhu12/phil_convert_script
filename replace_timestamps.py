from random import randint
from path import path
import re
import glob
import os

# Set up, whatever directory this script is in, create another directory called input and another called output.
# Put all the files you want to modify in input, leave output empty
#--| replace_timestamps.py
#--| output/
#----|
#--| input/
#----| // put files here

daysPerYear = 365
secondsPerDay = 86400
millisPerSeconds = 1000
millisPerYear = daysPerYear * secondsPerDay * millisPerSeconds

EXT = "prf"
DIR = "./input/"
RAND = 15
MIN_RAND = 5
EXIT_DIR = "./output/"

def main():

  for f in os.listdir(DIR):
    if f.endswith(EXT):
      file_handle = os.path.abspath("{0}{1}".format( DIR, f))
      fix_file(file_handle, f)

def fix_file(handle, filename):
  with open(handle, 'rw') as phil_file:
    for line in phil_file:
      occurances = re.findall("\d{13}", line)
      
      new_line = line
      for occurance in occurances:
        if occurance in line:
          occurance_int = int(occurance)
          # Make a fuzzy factor so that the time will be randomized within RAND + MIN_RAND days before the actual timestamp
          # IE, if the timestamp is for april 25 2014, RAND is 3, MIN_RAND is 1, it will be between (april 21st to april 24th 2015)
          # That way, this script could be used for multiple people.
          occurance_int += millisPerYear - fuzzy_factor()
          new_occurance = str(occurance_int)
          new_line = re.sub(occurance, new_occurance, new_line)
          #a = line.index(occurance)
          #print a
        else:
          print("Something went wrong")

      save_file(new_line, filename)
        

def fuzzy_factor():
  millisPerDay = millisPerSeconds * secondsPerDay
  millisRandom = millisPerDay * RAND
  millisMin = millisPerDay * MIN_RAND
  return randint(0, millisRandom + millisMin)

def save_file(line, filename):
  save_path = "{0}{1}".format(EXIT_DIR, filename)
  with open(save_path, 'w') as save_file:
    save_file.write(line)

if __name__ == "__main__":
  main()
