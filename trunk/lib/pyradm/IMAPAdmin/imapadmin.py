#!/usr/bin/python

from string import split, strip, find
from codecs import utf_7_decode, utf_7_encode
import re
from imaplib import IMAP4, IMAP4_SSL

class IMAPAdminError:
  """TODO"""

  def __init__(self, value):

     self.value = value

  def __str__(self):

    return repr(self.value)
     
def parseACL(acl):
  """TODO"""

  if (acl == "none"):
    pass
  elif acl == "read":
    acl = "lrs"
  elif acl == "write":
    acl = "lrswipd"
  elif acl == "all":
    acl = "lrswipdca"
  else:
    if acl[0] in ('+', '-'):
      mod = acl[0]
      acl = acl[1:0]
    else:
      mod = ""
    for a in acl:
      if not (a in "lrswipdca"): raise IMAPAdminError("Bad ACL - " + acl)
    acl = mod + acl
  return acl

def utf_7_imap_decode(str):
  """TODO"""

  shiftEnd = 0
  shiftStart = find(str, "&")
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
    shiftStart = find(str, "&", shiftEnd)

  return utf_7_decode(str)

listRE = re.compile("(\(.*\)) \"(.*)\" \"(.*)\"")
    
class IMAPAdmin:
  """TODO"""
  
  def __init__(self, config):
    """TODO"""

    self.__config = config
    
    if config["connection"]["ssl"]:
      self.__server = IMAP4_SSL(config["server"]["host"], config["server"]["port"])
    else:
      self.__server = IMAP4(config["server"]["host"], config["server"]["port"])

    self.login(config["credentials"]["user"], config["credentials"]["passwd"])

  def login(self, user, passwd):
    """
    Identify client using plaintext password.

    IMAPAdmin.login(user, password)

    Method returns nothing.
 
    NB: 'password' will be quoted.
    """
    
    result = self.__server.login(user, passwd)
    if result[0] == 'NO': raise IMAPAdminError(result[1][0])
    
  def create(self, mailbox):
    """
    Create new mailbox.

    IMAPAdmin.create(mailbox)
    """

    result = self.__server.create(mailbox)
    if result[0] == 'NO': raise IMAPAdminError(result[1][0])
    
  def delete(self, mailbox):
    """TODO"""

    result = self.__server.delete(mailbox)
    if result[0] == 'NO': raise IMAPAdminError(result[1][0])
    
  def getacl(self, mailbox):
    """TODO"""

    result = self.__server.getacl(mailbox)
    if result[0] == 'NO': raise IMAPAdminError("%s: %s" % (result[1][0], mailbox))

    if (result[1][0][0] == '"'):
      aclList = split(result[1][0][find(result[1][0], '" ') + 2:])
    else:
      aclList = split(result[1][0][find(result[1][0], ' ') + 1:])
    acl = []

    while len(aclList) > 0:
      acl.append((aclList[0], aclList[1]))
      aclList = aclList[2:]
      
    return acl

  def setacl(self, mailbox, acls):
    """TODO"""

    for acl in acls:
      self.__server.setacl(mailbox, acl[0], acl[1])

  def list(self, pattern):
    """TODO"""

    result = self.__server.list(pattern)
    if result[0] == 'NO': raise IMAPAdminError(result[1][0] + "!!!")

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
