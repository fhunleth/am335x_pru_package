# vim: ts=2:sw=2:tw=80:nowrap

from ptypes import *
from constants_simple import *

def get_default_INTC_config():
  return tpruss_intc_initdata(
    sysevts_enabled = (
      PRU_TRIGGER_R31_30,
      PRU_TRIGGER_R31_31,
      PRU_TRIGGER_HOST_INTR_0,
      PRU_TRIGGER_HOST_INTR_1,
      -1 ),
    sysevt_to_channel_map = (
      tsysevt_to_channel_map(PRU_TRIGGER_R31_30,      CHANNEL0),
      tsysevt_to_channel_map(PRU_TRIGGER_R31_31,      CHANNEL1),
      tsysevt_to_channel_map(PRU_TRIGGER_HOST_INTR_0, CHANNEL2),
      tsysevt_to_channel_map(PRU_TRIGGER_HOST_INTR_1, CHANNEL3),
      tsysevt_to_channel_map(-1,-1) ),
    channel_to_host_map = (
      tchannel_to_host_map(CHANNEL0,  PRU_INTERRUPT_R31_30),
      tchannel_to_host_map(CHANNEL1,  PRU_INTERRUPT_R31_31),
      tchannel_to_host_map(CHANNEL2,  PRU_HOST_INTR_0),
      tchannel_to_host_map(CHANNEL3,  PRU_HOST_INTR_1),
      tchannel_to_host_map(-1,-1) ),
    hosts_enabled = (
      PRU_INTERRUPT_R31_30,
      PRU_INTERRUPT_R31_31,
      PRU_HOST_INTR_0,
      PRU_HOST_INTR_1,
      -1 ),
  )
