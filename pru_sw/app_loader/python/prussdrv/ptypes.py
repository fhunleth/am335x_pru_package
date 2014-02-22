# vim: ts=2:sw=2:tw=80:nowrap

import ctypes
from ctypes import \
  c_int, c_uint, c_short, c_ushort, \
  c_uint8, c_uint16, c_uint32, c_uint64, \
  c_byte, c_ubyte, c_char, c_char_p, c_void_p, POINTER

from constants_simple import *


class tsysevt_to_channel_map(ctypes.Structure):
  _fields_ = [ ('sysevt', c_short), ('channel', c_short) ]
  def __str__(self):
    return '{} -> {}'.format(self.sysevt, self.channel)

class tchannel_to_host_map(ctypes.Structure):
  _fields_ = [ ('channel', c_short), ('host',    c_short) ]
  def __str__(self):
    return '{} -> {}'.format(self.channel, self.host)


class tpruss_intc_initdata(ctypes.Structure):
  _fields_ = [
    #Enabled SYSEVTs - Range:0..63
    #{-1} indicates end of list
    ('sysevts_enabled', c_byte * NUM_PRU_SYS_EVTS),
    #SysEvt to Channel map. SYSEVTs - Range:0..63 Channels -Range: 0..9
    #{-1, -1} indicates end of list
    ('sysevt_to_channel_map', tsysevt_to_channel_map * NUM_PRU_SYS_EVTS),
    #Channel to Host map.Channels -Range: 0..9  HOSTs - Range:0..9
    #{-1, -1} indicates end of list
    ('channel_to_host_map', tchannel_to_host_map * NUM_PRU_CHANNELS),
    #Enabled Host interrupt lines
    #Host0-Host9 {Host0/1:PRU0/1, Host2..9 : PRU_HOST_INTR_0..7}
    ('hosts_enabled', c_uint * NUM_PRU_HOSTS),
  ]

  def __repr__(self):
    return str(self)

  def __str__(self):
    events = list()
    for i in self.sysevts_enabled:
      if i == -1: break
      events.append( i )

    etc_map = list()
    for mp in self.sysevt_to_channel_map:
      if mp.sysevt == -1: break
      etc_map.append( '  ' + str(mp) )

    cth_map = list()
    for mp in self.channel_to_host_map:
      if mp.channel == -1: break
      cth_map.append( '  ' + str(mp) )

    hosts = list()
    for i in self.hosts_enabled:
      if i > NUM_PRU_HOSTS:
        break
      hosts.append( i )
    return 'INTC config: {{\n'             \
           '  events enabled: {}\n'       \
           '  events to channel map: {{\n' \
           '{}\n'                         \
           '  }}\n'                        \
           '  channel to host map: {{\n'   \
           '{}\n'                         \
           '  }}\n'                        \
           '  hosts enabled: {}\n'        \
           .format( events, '\n'.join(etc_map), '\n'.join(cth_map), hosts )


  @property
  def events(self):
    for h in self.sysevts_enabled:
      if h >= NUM_PRU_SYS_EVTS: break
      yield h

  @events.setter
  def events(self, new_list):
    self.sysevts_enabled[:] = new_list
    self.sysevts_enabled[len(new_list)] = -1

  @property
  def host_interrupts(self):
    for h in self.hosts_enabled:
      if h >= NUM_PRU_HOSTS: break
      yield h

  @property
  def exported_host_interrupts(self):
    """Different view of hosts: only those accessible by ARM code"""
    for h in self.hosts_enabled:
      if h in [ PRU_INTERRUPT_R31_30, PRU_INTERRUPT_R31_31 ]: continue
      if h >= NUM_PRU_HOSTS: break
      yield h

  @host_interrupts.setter
  def host_interrupts(self, new_list):
    self.hosts_enabled[:] = new_list
    self.hosts_enabled[len(new_list)] = -1
