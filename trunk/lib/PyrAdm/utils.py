def yes(msg, yesDefault = False):
  """TODO"""

  if yesDefault:
    y = 'Y'
    n = 'n'
  else:
    y = 'y'
    n = 'N'
    
  answer = raw_input("%s (%c/%c): " % (msg, y, n))
  if len(answer) == 0:
    answer = yesDefault
  else:
    if answer.lower() == 'y':
      answer = True
    else:
      answer = False

  return answer

# vim:ts=2:sw=2:et
