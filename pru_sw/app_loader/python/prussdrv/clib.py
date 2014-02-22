# vim: ts=2:sw=2:tw=80:nowrap

import ctypes

from ptypes import *
from constants_simple import *
from errors import assert_success, PrussDrvError, PRUNOTOPENED


__all__ = []


try:
  #load the prussdrv library
  drv = ctypes.CDLL('libprussdrv.so')
except:
  class fakefunc:
    def __call__(self, *args, **kwargs):
      raise PrussDrvError(PRUNOTOPENED)


  class fakelib:
    def __getattr__(self, name):
      if not self.__dict__.has_key(name):
        self.__dict__[name] = fakefunc()

      return self.__dict__[name]
  drv = fakelib()


def prototype( funcname, argtypes=[], restype=assert_success,
               prefix='prussdrv_', G=globals() ):
  func = getattr(drv, prefix + funcname)
  func.argtypes = argtypes
  func.restype  = restype
  G[funcname]   = func
  __all__.append( funcname )


# ### set function prototypes ###
prototype( 'init' )
prototype( 'open',                     [c_uint]             )
prototype( 'version',                  [],        c_int     )
prototype( 'strversion',               [c_int],   c_char_p  )
prototype( 'pru_reset',                [c_uint]             )
prototype( 'pru_disable',              [c_uint]             )
prototype( 'pru_enable',               [c_uint]             )
prototype( 'pru_write_memory',         [pru_memory_t,   # pru_ram_id
                                        c_uint,         # wordoffset
                                        POINTER(c_uint),# memarea
                                        c_uint] )       # bytelength
prototype( 'pruintc_init',             [POINTER(tpruss_intc_initdata)] )
prototype( 'get_event_to_channel_map', [c_uint],  c_short   )
prototype( 'lookup_event_to_channel',  [POINTER(tpruss_intc_initdata), c_uint],
                                       c_short )
prototype( 'get_channel_to_host_map',  [c_uint],  c_short   )
prototype( 'lookup_channel_to_host',   [POINTER(tpruss_intc_initdata), c_uint],
                                       c_short )
prototype( 'get_event_to_host_map',    [c_uint],  c_short   )
prototype( 'lookup_event_to_host',     [POINTER(tpruss_intc_initdata), c_uint],
                                       c_short )
prototype( 'map_l3mem',                [POINTER(POINTER(c_ubyte))] )
prototype( 'map_extmem',               [POINTER(POINTER(c_ubyte))] )
prototype( 'extmem_size',              [],        c_uint    )
prototype( 'map_prumem',               [pru_memory_t,                 # pru_ram_id
                                        POINTER(POINTER(c_ubyte))] )  # pptr
prototype( 'map_peripheral_io',        [pru_peripheral_t,             # per_id
                                        POINTER(POINTER(c_ubyte))] )  # pptr
prototype( 'get_phys_addr',            [POINTER(c_ubyte)],  c_uint )
prototype( 'get_virt_addr',            [c_uint],  POINTER(c_ubyte) )
prototype( 'pru_wait_interrupt',       [c_uint],  c_uint    )
prototype( 'pru_wait_event',           [c_uint],  c_uint    )
prototype( 'pru_interrupt_fd',         [c_uint],  c_int     )
prototype( 'pru_send_event',           [c_uint]             )
prototype( 'pru_clear_event',          [c_uint]             )
prototype( 'pru_reset_interrupt',      [c_uint]             )
prototype( 'pru_reset_event',          [c_uint]             )
prototype( 'pru_send_wait_reset_event',[c_uint,   # send_eventnum
                                        c_uint] ) # ack_eventnum
prototype( 'exit' )
prototype( 'exec_program',             [c_int, c_char_p]    )
prototype( 'exec_code',                [c_int,              # pru id
                                        POINTER(c_uint32),  # pru code
                                        c_int] )            # length of pru code
# small redef, because we can easily measure lengths in python
_exec_code = exec_code
exec_code = lambda id, code: _exec_code(id, code, len(code))
