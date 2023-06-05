class Extendable(object):

  def _set_attrs_to_values(self, data={}):
    if isinstance(data, dict):
      for key in data.keys():
        if not hasattr(self, key) or not callable(getattr(self, key)):
          setattr(self, key, data[key])


class Observable(object):

  def __init__(self):
    self._events = dict()

  def connect(self, event_name, callback_fn):
    if isinstance(event_name, str):
      event_name = [event_name]
    for e in event_name:
      self._events[e] = callback_fn

  def disconnect(self, event_name):
    self._events.pop(event_name, None)

  def emit(self, event_name, *callback_args):
    if event_name in self._events:
      self._events[event_name](*callback_args, class_name = self.__class__.__name__, event_name = event_name)
