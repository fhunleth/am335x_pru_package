/*
 * prussdrv.h
 *
 * Describes PRUSS userspace driver for Industrial Communications
 *
 * Copyright (C) 2010 Texas Instruments Incorporated - http://www.ti.com/
 *
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *    Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 *    Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the
 *    distribution.
 *
 *    Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 *  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 *  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 *  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 *  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
*/

/*
 * ============================================================================
 * Copyright (c) Texas Instruments Inc 2010-11
 *
 * Use of this software is controlled by the terms and conditions found in the
 * license agreement under which this software has been supplied or provided.
 * ============================================================================
*/

#ifndef _PRUSSDRV_H
#define _PRUSSDRV_H

#include <sys/types.h>

#if defined (__cplusplus)
extern "C" {
#endif

#define NUM_PRU_HOSTIRQS        8
#define NUM_PRU_HOSTS          10
#define NUM_PRU_CHANNELS       10
#define NUM_PRU_SYS_EVTS       64

#define PRUSS_V1                1 // AM18XX
#define PRUSS_V2                2 // AM33XX

    /** Types of memory on PRU0/1. */
    typedef enum {
        PRUSS0_PRU0_DATARAM,
        PRUSS0_PRU1_DATARAM,
        PRUSS0_PRU0_IRAM,
        PRUSS0_PRU1_IRAM,
        PRUSS0_SHARED_DATARAM     // AM33XX only
    } pru_memory_t;

    /** Peripheral devices available in AM33xx series. */
    typedef enum {
       	PRUSS0_CFG,
       	PRUSS0_UART,
       	PRUSS0_IEP,
       	PRUSS0_ECAP,
       	PRUSS0_MII_RT,
       	PRUSS0_MDIO
    } pru_peripheral_t;


    typedef struct __sysevt_to_channel_map {
        short sysevt;
        short channel;
    } tsysevt_to_channel_map;
    typedef struct __channel_to_host_map {
        short channel;
        short host;
    } tchannel_to_host_map;
    typedef struct __pruss_intc_initdata {
        //Enabled SYSEVTs - Range:0..63
        //{-1} indicates end of list
        char sysevts_enabled[NUM_PRU_SYS_EVTS];
        //SysEvt to Channel map. SYSEVTs - Range:0..63 Channels -Range: 0..9
        //{-1, -1} indicates end of list
        tsysevt_to_channel_map sysevt_to_channel_map[NUM_PRU_SYS_EVTS];
        //Channel to Host map.Channels -Range: 0..9  HOSTs - Range:0..9
        //{-1, -1} indicates end of list
        tchannel_to_host_map channel_to_host_map[NUM_PRU_CHANNELS];
        //Enabled Host interrupt lines
        //Host0-Host9 {Host0/1:PRU0/1, Host2..9 : PRU_HOST_INTR_0..7}
        unsigned int hosts_enabled[NUM_PRU_HOSTS];
    } tpruss_intc_initdata;

    int prussdrv_init(void);

    int prussdrv_open(unsigned int host_interrupt);

    /** Return version of PRU.  This must be called after prussdrv_open. */
    int prussdrv_version();

    /** Return string description of PRU version. */
    const char* prussdrv_strversion(int version);

    int prussdrv_pru_reset(unsigned int prunum);

    int prussdrv_pru_disable(unsigned int prunum);

    int prussdrv_pru_enable(unsigned int prunum);

    int prussdrv_pru_write_memory(pru_memory_t pru_ram_id,
                                  unsigned int wordoffset,
                                  const unsigned int *memarea,
                                  unsigned int bytelength);

    int prussdrv_pruintc_init(const tpruss_intc_initdata *prussintc_init_data);

    /** Find and return the channel a specified event is mapped to.
     * Note that this only searches for the first channel mapped and will not
     * detect error cases where an event is mapped erroneously to multiple
     * channels.
     * @return channel-number to which a system event is mapped.
     * @return -1 for no mapping found
     */
    short prussdrv_get_event_to_channel_map( unsigned int eventnum );

    /** Lookup, from the specified interrupt controller configuration, which
     * channel a given event should be mapped to.
     */
    short prussdrv_lookup_event_to_channel( const tpruss_intc_initdata *intc_data,
                                            unsigned int eventnum );

    /** Find and return the host interrupt line a specified channel is mapped
     * to.  Note that this only searches for the first host interrupt line
     * mapped and will not detect error cases where a channel is mapped
     * erroneously to multiple host interrupt lines.
     * @return host-interrupt-line to which a channel is mapped.
     * @return -1 for no mapping found
     */
    short prussdrv_get_channel_to_host_map( unsigned int channel );

    /** Lookup, from the specified interrupt controller configuration, which
     * host interrupt line a given channel should be mapped to.
     */
    short prussdrv_lookup_channel_to_host( const tpruss_intc_initdata *intc_data,
                                           unsigned int channel );

    /** Find and return the host interrupt line a specified event is mapped
     * to.  This first finds the intermediate channel and then the host.
     * @return host-interrupt-line to which a system event is mapped.
     * @return -1 for no mapping found
     */
    short prussdrv_get_event_to_host_map( unsigned int eventnum );

    /** Lookup, from the specified interrupt controller configuration, which
     * host interrupt line a given event should be mapped to.
     */
    short prussdrv_lookup_event_to_host( const tpruss_intc_initdata *intc_data,
                                         unsigned int eventnum );

    int prussdrv_map_l3mem(void **address);

    int prussdrv_map_extmem(void **address);

    unsigned int prussdrv_extmem_size(void);

    int prussdrv_map_prumem(pru_memory_t pru_ram_id, void **address);

    int prussdrv_map_peripheral_io(pru_peripheral_t per_id, void **address);

    unsigned int prussdrv_get_phys_addr(const void *address);

    void *prussdrv_get_virt_addr(unsigned int phyaddr);

    /** Wait for the specified host interrupt.
     * @return the number of times the event has happened. */
    unsigned int prussdrv_pru_wait_interrupt(unsigned int host_interrupt);

    /** Wait for the host interrupt to which the specified system event is
     * mapped.
     * @return the number of times the event has happened. */
    unsigned int prussdrv_pru_wait_event(unsigned int sysevent);

    int prussdrv_pru_interrupt_fd(unsigned int host_interrupt);

    int prussdrv_pru_send_event(unsigned int eventnum);

    /** Test whether the Enabled Status is pending for a particular system
     * event.
     * According the page 154 of the PRU-ICSS reference guide:
     *   The pending status reflects whether the system interrupt occurred since
     *   the last time the status register bit was cleared.
     */
    int prussdrv_pru_event_status(unsigned int sysevent);

    /** Clear the specified event.
     * Does not reset the host interrupt.
     * @see pruss_pru_reset_event
     * @see pruss_pru_reset_interrupt
     */
    int prussdrv_pru_clear_event(unsigned int sysevent);

    /** Reset the host interrupt.
     * Does not clear the system event that caused the interrupt.
     *
     * Generally, this should be done _after_ the system event that caused the
     * interrupt has been cleared (i.e. via prussdrv_pru_clear_event).
     *
     * If the interupt is still set, perhaps because of another event that has
     * not yet been cleared, this function will immediately re-trigger the
     * interrupt line.  See Section 6.4.9 of Reference manual about HIEISR
     * register.
     *
     * @see pruss_pru_clear_event
     * @see pruss_pru_reset_event
     */
    int prussdrv_pru_reset_interrupt(unsigned int host_interrupt);

    /** Clear the specified event and reset the associated interrupt.
     * Simplified event/interrupt clear/reset routine that does:
     *    1. pruss_pru_clear_event(sysevent)
     *    2. pruss_pru_reset_interrupt( get_interrupt(sysevent) )
     * @see pruss_pru_clear_event
     * @see pruss_pru_reset_interrupt
     */
    int prussdrv_pru_reset_event(unsigned int sysevent);

    int prussdrv_pru_send_wait_reset_event(unsigned int send_eventnum,
                                           unsigned int ack_eventnum);

    int prussdrv_exit(void);

    int prussdrv_exec_program(int prunum, const char *filename);

    int prussdrv_exec_code(int prunum, const unsigned int *code, int codelen);

#if defined (__cplusplus)
}
#endif
#endif
