#!/usr/bin/env python
# vim: ts=2:sw=2:tw=80:nowrap

import sys
sys.path.insert(0,'../../../app_loader/python')#prepend this to get this version

from ctypes import Structure, POINTER, c_uint16, c_uint32
from random import randint

from prussdrv import MemoryModel, ExecModel, PRU_HOST_INTR_0



class Pulse(Structure):
  _pack_ = 1
  _fields_ = [
    ('count', c_uint32),
    ('r30',   c_uint16),
    ('ignored',c_uint16),
  ]

class PulseMemory(MemoryModel):
  _pack_ = 1
  _fields_ = [ ('pulses', POINTER( Pulse )) ]


class ExecExample(ExecModel):
  MemoryModel = PulseMemory

  def __init__(self):
    ExecModel.__init__(self,program_path='pusles.bin')
    self.add_response(PRU_HOST_INTR_0, self.exit_after_pru0)

    for i in xrange(100):
      # just pick some random pulse data
      self.data.pulses[i] = Pulse(count=randint(1,100), r30=randint(0,2**16-1))
    # create end marker
    self.data.pulses[100] = Pulse(count=0)

  def exit_after_pru0(self, host_interrupt, count):
    print 'finished'

ExecExample().run()
