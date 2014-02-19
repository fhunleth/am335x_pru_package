# vim: ts=2:sw=2:tw=80:nowrap
"""
Simple helper class to ensure strict typing on arguments to functions that take
enumerations.
"""
from inspect import currentframe

__all__ = ['Enum']

# The ctypes stuff here is taken from python recipe:
# http://code.activestate.com/recipes/576415/

from ctypes import c_uint
class EnumerationType(type(c_uint)):
  def __new__(metacls, name, bases, dict):
    if not "_members_" in dict:
      _members_ = {}
      for key,value in dict.items():
        if not key.startswith("_"):
          _members_[key] = value
      dict["_members_"] = _members_
    cls = type(c_uint).__new__(metacls, name, bases, dict)

    # use globals of parent.parent frame.
    f = currentframe()
    G = f.f_back.f_back.f_globals

    for key,value in cls._members_.items():
        G[key] = value
    return cls

  def __contains__(self, value):
    return value in self._members_.values()

  def __repr__(self):
    return "<Enumeration %s>" % self.__name__

class Enumeration(c_uint):
  __metaclass__ = EnumerationType
  _members_ = {}
  def __init__(self, value):
    try:
      self.name = self.reverse[value]
    except KeyError:
      raise ValueError("No enumeration member with value %r" % value)
    c_uint.__init__(self, value)


  @classmethod
  def from_param(cls, param):
    if isinstance(param, Enumeration):
      if param.__class__ != cls:
        raise ValueError("Cannot mix enumeration members")
      else:
        return param
    else:
      return cls(param)

  def __repr__(self):
    return "<member %s=%d of %r>" % (self.name, self.value, self.__class__)



# this was borrowed from another one of my projects
def Enum( *seq, **named):
  """
    Example: Enum( 'A0', 'B0',
                   ('A','Thing A'), ('B', 'B is cool'),
                   C=(10, 'C is dumb'),
                   D=(11, 'D is best') )
    optional keyword arguments:
      __name__ :  sets the name of the enum
      __start__:  sets the beginning of sequential items
  """
  enum_name = named.get('__name__', 'AnonymousEnum')

  def kv_to_iE(k,v):
    try:
      return (v[0], (k,v[1]))
    except TypeError:
      return (v, k)

  begin = named.pop('__start__', 0)
  enums = dict()
  doc = dict()
  for i, E in \
    zip( xrange(begin, begin+len(seq)), seq ) + \
    [ kv_to_iE(k,v) for k,v in named.items() ]:
    try:
      assert type(E) is not str
      Label = E[0]
      Doc = E[1]
    except:
      Label = Doc = E
    enums[ Label ] = i
    doc[i] = Doc

  forward = dict(enums)
  reverse = dict((v,k) for k,v in enums.iteritems())
  enums['doc'] = doc
  enums['forward'] = forward
  enums['reverse'] = reverse
  return type(enum_name, (Enumeration,), enums)
