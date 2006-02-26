class Help:
  """TODO"""

  __help__ = {}

  def __setitem__(self, topic, message):
    """TODO"""

    Help.__help__[topic] = message

  def __getitem__(self, topic):
    """TODO"""

    return Help.__help__[topic]

# vim:ts=2:sw=2:et
