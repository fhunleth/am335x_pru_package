# vim: ts=2:sw=2:tw=80:nowrap

from enum import Enum

# FROM prussdrv.h
NUM_PRU_HOSTIRQS       =  8
NUM_PRU_HOSTS          = 10
NUM_PRU_CHANNELS       = 10
NUM_PRU_SYS_EVTS       = 64

PRUSS_V1               =  1 # AM18XX
PRUSS_V2               =  2 # AM33XX

pru_memory_t = Enum(
  'PRUSS0_PRU0_DATARAM',
  'PRUSS0_PRU1_DATARAM',
  'PRUSS0_PRU0_IRAM',
  'PRUSS0_PRU1_IRAM',
  'PRUSS0_SHARED_DATARAM',    # AM33XX only
  __start__ = 0,
  __name__ = 'pru_memory_t',
)

pru_peripheral_t = Enum(
  #Available in AM33xx series - begin
  'PRUSS0_CFG',
  'PRUSS0_UART',
  'PRUSS0_IEP',
  'PRUSS0_ECAP',
  'PRUSS0_MII_RT',
  'PRUSS0_MDIO',
  #Available in AM33xx series - end
  __start__ = 0,
  __name__ = 'pru_peripheral_t',
)




# From pruss_intc_mapping.h:

# List of system events, or at least the ones we care about for now (those
# pru-related).
AM33XX = True
if AM33XX:
  # pru events 16:31 of the 64 total events
  pru_event_t = Enum(
    'PRU_EVENT_0',
    'PRU_EVENT_1',
    'PRU_EVENT_2',
    'PRU_EVENT_3',
    'PRU_EVENT_4',
    'PRU_EVENT_5',
    'PRU_EVENT_6',
    'PRU_EVENT_7',
    'PRU_EVENT_8',
    'PRU_EVENT_9',
    'PRU_EVENT_10',
    'PRU_EVENT_11',
    'PRU_EVENT_12',
    'PRU_EVENT_13',
    'PRU_EVENT_14',
    'PRU_EVENT_15',
    __start__ = 16,
    __name__ = 'pru_event_t',
  )
else:
  pru_event_t = Enum(
    'PRU_EVENT_0',
    'PRU_EVENT_1',
    'PRU_EVENT_2',
    'PRU_EVENT_3',
    'PRU_EVENT_4',
    'PRU_EVENT_5',
    __start__ = 32,
    __name__ = 'pru_event_t',
  )


# List of INTC channels
channel_t = Enum(
  'CHANNEL0',
  'CHANNEL1',
  'CHANNEL2',
  'CHANNEL3',
  'CHANNEL4',
  'CHANNEL5',
  'CHANNEL6',
  'CHANNEL7',
  'CHANNEL8',
  'CHANNEL9',
  __start__ = 0,
  __name__ = 'pru_channel_t',
)


# List of host interrupt lines
host_interrupt_t = Enum(
  'PRU_HOST_0',
  'PRU_HOST_1',
  'PRU_HOST_2',
  'PRU_HOST_3',
  'PRU_HOST_4',
  'PRU_HOST_5',
  'PRU_HOST_6',
  'PRU_HOST_7',
  'PRU_HOST_8',
  'PRU_HOST_9',
  __start__ = 0,
  __name__ = 'host_interrupt_t',
)

# Host interrupts mapped back for PRU[01] use
PRU_INTERRUPT_R31_30    = PRU_HOST_0
PRU_INTERRUPT_R31_31    = PRU_HOST_1


# Host interrupts exported to ARM
#@see pr1_host_intr[7:0], page 17
PRU_HOST_INTR_0         = PRU_HOST_2
PRU_HOST_INTR_1         = PRU_HOST_3
PRU_HOST_INTR_2         = PRU_HOST_4
PRU_HOST_INTR_3         = PRU_HOST_5
PRU_HOST_INTR_4         = PRU_HOST_6
PRU_HOST_INTR_5         = PRU_HOST_7
PRU_HOST_INTR_6         = PRU_HOST_8
PRU_HOST_INTR_7         = PRU_HOST_9



# Host-2 also exported to TSC_ADC (page 17)
PRU_TSC_ADC_INTR        = PRU_HOST_2
# Host-8 also exported as DMA interrupt (page 17)
PRU_DMA_INTR_0          = PRU_HOST_8
PRU_DMA_INTR_1          = PRU_HOST_9


# Useful defines for the default configuration of the interrupt controller.
# @see PRUSS_INTC_INITDATA
PRU_TRIGGER0_R31_30     = PRU_EVENT_0
PRU_TRIGGER1_R31_30     = PRU_EVENT_1
PRU_TRIGGER0_R31_31     = PRU_EVENT_2
PRU_TRIGGER1_R31_31     = PRU_EVENT_3
PRU_TRIGGER_HOST_INTR_0 = PRU_EVENT_4
PRU_TRIGGER_HOST_INTR_1 = PRU_EVENT_5
