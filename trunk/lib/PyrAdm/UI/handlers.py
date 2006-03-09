#!/usr/bin/python

from string import split, strip
from pyIMAP import utf_7_imap_decode

class Logout:

  pass

def logout(imap, cl):
  """TODO"""

  imap.logout()
  raise Logout

def createShared(imap, mbName):
  """TODO"""

  if len(mbName) == 0:
    print "USAGE: createshared mailbox"
  elif mbName[:5] == "user.":
    print "INFO: Use 'createuser' command to create user's initial mailbox"
  else:
    imap.createSharedMB(mbName)
    print "Shared mailbox '" + mbName + "' created successfully" 


def deleteShared(imap, mailbox):
  """TODO"""

  if len(mailbox) == 0:
    print "USAGE: deleteshared mailbox"
  elif mailbox[:5] == "user.":
    print "INFO: Use 'deleteuser' command to delete user's mailbox"
  else:
    mailboxes = imap.list(mailbox)
    for mb in mailboxes:
      print "Delete mailbox %s ..." % (mb[0]),
      imap.delete(mb[0])
      print "OK"
    print "Shared mailbox '" + mailbox + "' deleted successfully" 

def setACL(imap, cl):
  """TODO"""

  args = split(cl)
  if args[0] == "-r":
    recursive = True
    args = args[1:]
  else:
    recursive = False
  
  mailbox = args[0]
  args = args[1:]
  
  acl = []
  while len(args) > 0:
    acl.append((args[0], args[1]))
    args = args[2:]
  
  imap.setacl(mailbox, acl)

def getACL(imap, cl):
  """TODO"""

  if len(cl) == 0:
    print "USAGE: getacl [-r] mailbox"
  else:
    args = split(cl)
    if args[0] == "-r":
      recursive = True
      args = args[1:]
    else:
      recursive = False
    
    for mailbox in args:
      if recursive:
        mailboxes = map(lambda m: m[0], imap.list(mailbox))
      else:
        mailboxes = [mailbox]
      for mb in mailboxes:
        acls = imap.getacl(mb)

        print "%s:" % utf_7_imap_decode(mb)[0]
        for acl in acls:
          print "  %s %s" % (acl[0], acl[1])

def getPerm(imap, cl):
  """TODO"""

  if len(cl) == 0:
    print "USAGE: getperm user pattern"
  else:
    args = cl.split(" ", 2)
    user = args[0]
    if len(args) > 1:
      pattern = strip(args[1])
    else:
      pattern = "*"

    print "%s:" % (user)
    mailboxes = imap.list(pattern)
    for mailbox in mailboxes:
      acl = imap.getacl(mailbox[0])
      for a in acl:
        if a[0] == user:
          print "  %s %s" % (utf_7_imap_decode(mailbox[0])[0], a[1])

def setPerm(imap, cl):
  """TODO"""

  args = cl.split(" ", 2)
  if len(args) < 2:
    print "USAGE: setperm user rights pattern"
  else:
    user = args[0]
    rights = args[1]
    if len(args) > 2:
      pattern = strip(args[2])
    else:
      pattern = "*"

    mailboxes = imap.list(pattern)
    for mailbox in mailboxes:
      acl = imap.getacl(mailbox[0])
      for a in acl:
        if a[0] == user:
          print "  %s ..." % (mailbox[0]),
          imap.setacl(mailbox[0], ((user, rights),))
          print " OK"
