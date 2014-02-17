// *
// * PRU_PRU0toPRU1_Interrupt.p
// *
// * Copyright (C) 2012 Texas Instruments Incorporated - http://www.ti.com/
// *
// *
// *  Redistribution and use in source and binary forms, with or without
// *  modification, are permitted provided that the following conditions
// *  are met:
// *
// *    Redistributions of source code must retain the above copyright
// *    notice, this list of conditions and the following disclaimer.
// *
// *    Redistributions in binary form must reproduce the above copyright
// *    notice, this list of conditions and the following disclaimer in the
// *    documentation and/or other materials provided with the
// *    distribution.
// *
// *    Neither the name of Texas Instruments Incorporated nor the names of
// *    its contributors may be used to endorse or promote products derived
// *    from this software without specific prior written permission.
// *
// *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// *  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// *  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// *  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// *  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
// *
// *

// *
// * ============================================================================
// * Copyright (c) Texas Instruments Inc 2010-12
// *
// * Use of this software is controlled by the terms and conditions found in the
// * license agreement under which this software has been supplied or provided.
// * ============================================================================
// *

// *****************************************************************************/
// file:   PRU_PRU0toPRU1_Interrupt.p
//
// brief:  PRU example to show PRU to PRU interrupts.
//
//
//  (C) Copyright 2012, Texas Instruments, Inc
//
//  author     M. Watkins
//
//  version    0.1     Created
// *****************************************************************************/


.origin 0
.entrypoint PRU0_TO_PRU1_INTERRUPT

#include <prucode.hp>


// ***************************************
// *       Local Macro definitions       *
// ***************************************

#define SYS_EVT           PRU_TRIGGER_R31_30
#define SYS_EVT_PRU1      PRU_TRIGGER_R31_31
#define SYS_EVT_PRU1_BIT  31


PRU0_TO_PRU1_INTERRUPT:

    // Enable OCP master port
    CONFIG_OCP

    //Generate SYS_EVT
    TRIGGER_EVENT SYS_EVT

    // Poll for receipt of interrupt on host 1
POLL:
    WBS       r31, SYS_EVT_PRU1_BIT

DONE:
    // Config CONST_DDR pointer to 0x80000000
    CONFIG_DDR_RAM

    MOV       r0, 0x0B
    SBCO      r0, CONST_DDR, 0x04, 4

    // Clear the status of the interrupt
    CLEAR_EVENT SYS_EVT_PRU1

    // Send notification to Host for program completion
    TRIGGER_EVENT PRU_TRIGGER_HOST_INTR_0

    HALT
