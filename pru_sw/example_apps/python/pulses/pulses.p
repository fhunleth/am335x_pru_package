// *
// * simple.p
// *

// *****************************************************************************/
// file:   simple.p
//
// brief:  _very_ simple example for signaling python code run on the ARM.
//
// *****************************************************************************/


.origin 0
.entrypoint START

#include <prucode.hp>

.struct Pulse
  .u32 count
  .u16 r30w0
  .u16 ignored
.ends

.struct Position
  .u32 value
.ends

START:

    // Enable OCP master port
    CONFIG_OCP

    // Config CONST_PRUSHAREDRAM
    CONFIG_PRU_RAM

    .enter PULSE_EXECUTION
      .assign Position, r5, r5, position
      .assign Pulse, r6, *, pulse

      LDI position, 0 // initialize position register to zero
      PULSE_LOOP:
        // load the next pulse from memory
        LBCO pulse, CONST_PRUDRAM, position, SIZE(pulse)
        QBEQ DONE, pulse.count, 0

        // Set the output pins
        MOV r30.w0, pulse.r30w0

        // Delay by counting down...
        COUNT:
          SUB pulse.count, pulse.count, 1
          QBLE COUNT, pulse.count, 1

        // Increment the pulse position for the next iteration
        ADD position, position, SIZE(pulse)
        QBA PULSE_LOOP

      DONE:

    .leave PULSE_EXECUTION

    // Send notification to Host for program completion
    TRIGGER_EVENT PRU_TRIGGER_HOST_INTR_0

    HALT
