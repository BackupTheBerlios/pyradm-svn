from string import split, strip, find, replace
from codecs import utf_7_decode, utf_7_encode
import re
import imaplib

class IMAPError:
  """TODO"""

  def __init__(self, value):

     self.value = value

  def __str__(self):

    return repr(self.value)

def parseRights(rights):
  """TODO"""

  if (len(rights) > 0) and (rights[0] in ('+', '-')):
    mod = rights[0]
    rights = rights[1:]
  else:
    mod = None
    
  if (rights == "none"):
    mod = None
  elif rights == "read":
    rights = "lrs"
  elif rights == "write":
    if mod == '-':
      rights = "wipdca"
    else:
      rights = "lrswipd"
  elif rights == "all":
    if mod == '-':
      mod = None
      rights = "none"
    else:
      rights = "lrswipdca"
  else:
    for r in rights:
      if not (r in "lrswipdca"): raise IMAPError("Bad rights: %s (%s)" % (rights, r))
 
  return (mod, rights)

def utf_7_imap_decode(str):
  """TODO"""

  shiftEnd = 0
  shiftStart = find(str, "&")
  
  if shiftStart == -1:
    plusPos = find(str, "+", shiftEnd, shiftStart)
    while plusPos != -1:
      str = str[:plusPos + 1] + "-" + str[plusPos + 1:]
      plusPos = find(str, "+", plusPos + 2, shiftStart)
      
  while shiftStart != -1:
  
    plusPos = find(str, "+", shiftEnd, shiftStart)
    while plusPos != -1:
      str = str[:plusPos + 1] + "-" + str[plusPos + 1:]
      plusPos = find(str, "+", plusPos + 2, shiftStart)

    shiftEnd = find(str, "-", shiftStart)
    if shiftEnd != -1:
      if (shiftEnd - shiftStart) == 1:
        str = str[:shiftStart + 1] + str[shiftStart + 2:]
      else:
        str = str[:shiftStart] + "+" + str[shiftStart + 1:]

    commaPos = find(str, ",", shiftStart, shiftEnd)
    while commaPos != -1:
      str = str[:commaPos] + "/" + str[commaPos + 1:]
      commaPos = find(str, "+", commaPos + 2, shiftEnd)

    shiftStart = find(str, "&", shiftEnd)

  return utf_7_decode(str)

listRE = re.compile("(\(.*\)) \"(.*)\" \"(.*)\"")
