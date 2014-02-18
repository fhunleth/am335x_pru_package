// *
// * PRU_PRU1toPRU0_Interrupt.p
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
// file:   PRU_PRU1toPRU0_Interrupt.p
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
.entrypoint PRU1_TO_PRU0_INTERRUPT

#include <prucode.hp>


// ***************************************
// *       Local Macro definitions       *
// ***************************************

#define EVT_FROM_PRU0     PRU_TRIGGER0_R31_30 // event from pru0
#define EVT_FROM_PRU0_BIT 30                  // r31:bit from pru0
#define EVT_TO_PRU0       PRU_TRIGGER0_R31_31 // event to pru0

PRU1_TO_PRU0_INTERRUPT:
POLL:
    // Poll for receipt of interrupt on host 0
    WBS       r31, EVT_FROM_PRU0_BIT

FUNC:
    // Clear the status of the interrupt
    CLEAR_EVENT EVT_FROM_PRU0

    // Config CONST_DDR pointer to 0x80000000
    CONFIG_DDR_RAM

    MOV       r0, 0x0A
    SBCO      r0, CONST_DDR, 0x00, 4

    //Generate EVT_TO_PRU0
    TRIGGER_EVENT EVT_TO_PRU0

DONE:
    // Send notification to Host for program completion
    TRIGGER_EVENT PRU_TRIGGER_HOST_INTR_1

    HALT
