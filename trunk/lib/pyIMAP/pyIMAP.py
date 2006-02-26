#!/usr/bin/python

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
    
class IMAP:
  """TODO"""
  
  def __init__(self, host = None, port = None, ssl = False, cacert = None, cert = None, key = None):
    """TODO"""

    if host and port:
      if ssl:
        self.__server = imaplib.IMAP4_SSL(host, port)
      else:
        self.__server = imaplib.IMAP4(host, port)

  def login(self, user, passwd):
    """
    Identify client using plaintext password.

    IMAPAdmin.login(user, password)

    Method returns nothing.
 
    NB: 'password' will be quoted.
    """
    
    result = self.__server.login(user, passwd)
    if result[0] == 'NO': raise IMAPError(result[1][0])
    
  def create(self, mailbox):
    """
    Create new mailbox.

    IMAPAdmin.create(mailbox)
    """

    result = self.__server.create(mailbox)
    if result[0] == 'NO': raise IMAPError(result[1][0])
    
  def delete(self, mailbox):
    """TODO"""

    result = self.__server.delete(mailbox)
    if result[0] == 'NO': raise IMAPError(result[1][0])
    
  def getacl(self, mailbox):
    """TODO"""

    result = self.__server.getacl(mailbox)
    if result[0] == 'NO': raise IMAPError("%s: %s" % (result[1][0], mailbox))

    if (result[1][0][0] == '"'):
      aclList = split(result[1][0][find(result[1][0], '" ') + 2:])
    else:
      aclList = split(result[1][0][find(result[1][0], ' ') + 1:])
    acl = []

    while len(aclList) > 0:
      acl.append((aclList[0], aclList[1]))
      aclList = aclList[2:]
      
    return acl

  def setacl(self, mailbox, acl):
    """TODO"""

    effectiveACL = self.getacl(mailbox)
    for a in acl:
      user = a[0]
      (mod, rights) = parseRights(a[1])
      newRights = rights
      if mod:
        for effectiveRights in effectiveACL:
          if effectiveRights[0] == user:
            newRights = effectiveRights[1]
            if mod == '-':
              for r in rights:
                if r in newRights:
                  newRights = replace(newRights, r, '')
            else:
              for r in rights:
                if not (r in newRights):
                  newRights += r
        if newRights == "":
          newRights = "none"
      else:
        newRights = rights
      self.__server.setacl(mailbox, user, newRights)

  def list(self, pattern):
    """TODO"""

    result = self.__server.list(pattern)
    if result[0] == 'NO': raise IMAPError(result[1][0] + "!!!")

    mailboxes = []
    if result[1][0]:
      for r in result[1]:
        mailBoxStat = listRE.match(r)
        mailbox = mailBoxStat.group(3)
        namespace = mailBoxStat.group(2)
        hasChildren = mailBoxStat.group(1) == "(\HasChildren)"
        
        mailboxes.append((mailbox, namespace, hasChildren))

    return mailboxes

  def logout(self):
    """TODO"""

    self.__server.shutdown()
