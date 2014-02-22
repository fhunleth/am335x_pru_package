# vim: ts=2:sw=2:tw=80:nowrap

import select

from ctypes import \
  Union, \
  c_uint8,   c_uint16,  \
  c_uint32,  c_uint64,  \
  c_ubyte, POINTER, byref

import clib
from constants import \
  get_default_INTC_config, \
  PRUSS0_SHARED_DATARAM, PRUSS0_PRU0_DATARAM

__all__ = ['MemoryModel', 'ExecModel']

class MemoryModel(Union):
  _pack_ = 1
  _fields_ = [
    ('raw',    POINTER( c_ubyte  )),
    ('uint8',  POINTER( c_uint8  )),
    ('uint16', POINTER( c_uint16 )),
    ('uint32', POINTER( c_uint32 )),
    ('uint64', POINTER( c_uint64 )),
  ]

  def __init__(self, size, *args, **kwargs):
    Union.__init__(self,*args,**kwargs)
    self.size = size


class ExecModel(object):
  MemoryModel = MemoryModel
  _responses_ = list()

  def make_intc_config(self):
    return get_default_INTC_config()

  def __init__( self, program_path, pruId = 0, disable_on_exit=False ):
    self.program_path = program_path
    self.pruId = pruId
    self.disable_on_exit = disable_on_exit

    # initialize memory objects before mapping
    self.shared = self.MemoryModel(12 * 1<<10)
    self.data   = self.MemoryModel( 8 * 1<<10)
    self.other  = self.MemoryModel( 8 * 1<<10)

    self.intc_data = self.make_intc_config()

    self.__responses = {
      h:list()  for h in self.intc_data.exported_host_interrupts
    }

    for h, fn in self._responses_:
      self.add_response( h, eval(fn) )

    try:
      # Initialize the PRU
      clib.init()

      # Open PRU Interrupt(s)
      for host_interrupt in self.intc_data.exported_host_interrupts:
        clib.open(host_interrupt)

      # Get the interrupt initialized
      clib.pruintc_init( byref(self.intc_data) )

      # initialize maps to PRU memory
      clib.map_prumem(PRUSS0_SHARED_DATARAM, byref(self.shared.raw))
      clib.map_prumem(PRUSS0_PRU0_DATARAM+pruId, byref(self.data.raw))
      clib.map_prumem((PRUSS0_PRU0_DATARAM+pruId+1)%2, byref(self.other.raw))
    except:
      try: self.__del__()
      except: pass
      raise

  def __del__(self):
    if ( self.disable_on_exit ):
      # Disable PRU and close memory mapping
      try:
        clib.pru_disable(self.pruId)
      except: pass
    clib.exit()

  def add_response(self, host_interrupt, function):
    if host_interrupt not in self.__responses:
      raise RuntimeError('Invalid/Unmapped host-interrupt')
    self.__responses[host_interrupt].append( function )

  def respond( self, timeout=None ):
    poll = select.poll()
    fd_to_h = dict()
    for h, flist in self.__responses.items():
      if not flist: continue
      fd = clib.pru_interrupt_fd(h)
      fd_to_h[fd] = h
      poll.register( fd, select.POLLIN|select.POLLPRI )

    while True:
      polled = poll.poll(timeout)

      if not polled:
        return # timed out / giving up

      for fd, ev_mask in polled:
        h = fd_to_h[fd]
        count = clib.pru_wait_interrupt(h) # should return immediately
        remove = list()
        for f in self.__responses[ h ]:
          if f(h, count) == False:
            remove.append( f )
        for f in remove:
          self.__responses[h].remove( f )


        if len(self.__responses[h]) == 0:
          poll.unregister( fd )
          fd_to_h.pop(fd)

      if len(fd_to_h) == 0:
        return

  def run(self, timeout=None):
    clib.exec_program(self.pruId, self.program_path)
    self.respond(timeout)
