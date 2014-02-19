#!/usr/bin/env python
# vim: ts=2:sw=2:tw=80:nowrap

import sys
sys.path.insert(0,'../../../app_loader/python')#prepend this to get this version

import prussdrv

pruss_intc_config = prussdrv.get_default_INTC_config()

# Initialize the PRU
prussdrv.init()

# Open PRU Interrupt
prussdrv.open(PRU_HOST_INTR_0)

# Get the interrupt initialized
prussdrv.pruintc_init( byref(pruss_intc_config) )

# Execute program on PRU0; it will wait for interrupt
prussdrv.exec_program(0, 'simple.bin')

# wait for PRU_TRIGGER_HOST_INTR_0 event
prussdrv.pru_wait_interrupt(PRU_HOST_INTR_0)

# clear event and reset interrupt line (see docs in prussdrv.h)
prussdrv.pru_reset_event(PRU_TRIGGER_HOST_INTR_0)
