__help__ = {}

class Help:
  """TODO"""

  def __setitem__(self, topic, message):
    """TODO"""

    __help__[topic] = message

  def __getitem__(self, topic):
    """TODO"""

    return __help__[topic]

# vim:ts=2:sw=2:et
