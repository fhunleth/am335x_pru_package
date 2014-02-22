/*
 * pruss_intc_mapping.h
 *
 * Example PRUSS INTC mapping for the application
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

#ifndef AM33XX
  #define AM33XX
#endif

/** List of system events, or at least the ones we care about for now (those
 * pru-related). */
//{
#ifdef AM33XX
  #define PRU_EVENT_0     16
  #define PRU_EVENT_1     17
  #define PRU_EVENT_2     18
  #define PRU_EVENT_3     19
  #define PRU_EVENT_4     20
  #define PRU_EVENT_5     21
  #define PRU_EVENT_6     22
  #define PRU_EVENT_7     23
  #define PRU_EVENT_8     24
  #define PRU_EVENT_9     25
  #define PRU_EVENT_10    26
  #define PRU_EVENT_11    27
  #define PRU_EVENT_12    28
  #define PRU_EVENT_13    29
  #define PRU_EVENT_14    30
  #define PRU_EVENT_15    31
#else
  #define PRU_EVENT_0     32
  #define PRU_EVENT_1     33
  #define PRU_EVENT_2     34
  #define PRU_EVENT_3     35
  #define PRU_EVENT_4     36
  #define PRU_EVENT_5     37
  //#define PRU_EVENT_6     38
  //#define PRU_EVENT_7     39
  //#define PRU_EVENT_8     40
  //#define PRU_EVENT_9     41
  //#define PRU_EVENT_10    42
  //#define PRU_EVENT_11    43
  //#define PRU_EVENT_12    44
  //#define PRU_EVENT_13    45
  //#define PRU_EVENT_14    46
  //#define PRU_EVENT_15    47
#endif
//}


/** List of INTC channels */
//{
#define CHANNEL0                0
#define CHANNEL1                1
#define CHANNEL2                2
#define CHANNEL3                3
#define CHANNEL4                4
#define CHANNEL5                5
#define CHANNEL6                6
#define CHANNEL7                7
#define CHANNEL8                8
#define CHANNEL9                9
//}


/** List of Host Interrupt lines */
//{
#define PRU_HOST_0              0
#define PRU_HOST_1              1
#define PRU_HOST_2              2
#define PRU_HOST_3              3
#define PRU_HOST_4              4
#define PRU_HOST_5              5
#define PRU_HOST_6              6
#define PRU_HOST_7              7
#define PRU_HOST_8              8
#define PRU_HOST_9              9
//}


/** Host interrupts mapped back for PRU[01] use */
//{
#define PRU_INTERRUPT_R31_30    PRU_HOST_0
#define PRU_INTERRUPT_R31_31    PRU_HOST_1
//}


/** Host interrupts exported to ARM
 * @see pr1_host_intr[7:0], page 17
 */
//{
#define PRU_HOST_INTR_0         PRU_HOST_2
#define PRU_HOST_INTR_1         PRU_HOST_3
#define PRU_HOST_INTR_2         PRU_HOST_4
#define PRU_HOST_INTR_3         PRU_HOST_5
#define PRU_HOST_INTR_4         PRU_HOST_6
#define PRU_HOST_INTR_5         PRU_HOST_7
#define PRU_HOST_INTR_6         PRU_HOST_8
#define PRU_HOST_INTR_7         PRU_HOST_9
//}


// Host-2 also exported to TSC_ADC (page 17)
#define PRU_TSC_ADC_INTR        PRU_HOST_2
// Host-8 also exported as DMA interrupt (page 17)
#define PRU_DMA_INTR_0          PRU_HOST_8
#define PRU_DMA_INTR_1          PRU_HOST_9



/** Useful defines for the default configuration of the interrupt controller.
 * @see PRUSS_INTC_INITDATA
 */
//{
#define PRU_TRIGGER0_R31_30     PRU_EVENT_0
#define PRU_TRIGGER1_R31_30     PRU_EVENT_1
#define PRU_TRIGGER0_R31_31     PRU_EVENT_2
#define PRU_TRIGGER1_R31_31     PRU_EVENT_3
#define PRU_TRIGGER_HOST_INTR_0 PRU_EVENT_4
#define PRU_TRIGGER_HOST_INTR_1 PRU_EVENT_5
//}



/** Default configuration of interrupt controller mappings.
 * This configuration enables four system events which are mapped over to four
 * distinct host interrupts.
 * Two of these are intended for setting the 30th or 31st bits in the r31
 * register of both PRU0 and PRU1.  The associated events can be triggered by
 * either PRU as well as from the ARM.
 * The other two mappings are intended to interrupt the ARM processor.  The
 * associated events can also be triggered from any of the PRU0/1 and ARM, but
 * are most useful when used by the PRU0/1 processors to distinctly interrupt
 * the ARM processor.
 */
#define PRUSS_INTC_INITDATA {                   \
  { /* enabled system events */                 \
    PRU_TRIGGER0_R31_30,                        \
    PRU_TRIGGER1_R31_30,                        \
    PRU_TRIGGER0_R31_31,                        \
    PRU_TRIGGER1_R31_31,                        \
    PRU_TRIGGER_HOST_INTR_0,                    \
    PRU_TRIGGER_HOST_INTR_1,                    \
    -1 },                                       \
  { /* event to channel mapping */              \
    {PRU_TRIGGER0_R31_30,     CHANNEL0},        \
    {PRU_TRIGGER1_R31_30,     CHANNEL0},        \
    {PRU_TRIGGER0_R31_31,     CHANNEL1},        \
    {PRU_TRIGGER1_R31_31,     CHANNEL1},        \
    {PRU_TRIGGER_HOST_INTR_0, CHANNEL2},        \
    {PRU_TRIGGER_HOST_INTR_1, CHANNEL3},        \
    {-1,-1}   },                                \
  { /* channel to host interrupt line mapping */\
    {CHANNEL0,  PRU_INTERRUPT_R31_30},          \
    {CHANNEL1,  PRU_INTERRUPT_R31_31},          \
    {CHANNEL2,  PRU_HOST_INTR_0},               \
    {CHANNEL3,  PRU_HOST_INTR_1},               \
    {-1,-1}   },                                \
  { /* enabled host interrupts */               \
    PRU_INTERRUPT_R31_30,                       \
    PRU_INTERRUPT_R31_31,                       \
    PRU_HOST_INTR_0,                            \
    PRU_HOST_INTR_1,                            \
    -1 }                                        \
} \

