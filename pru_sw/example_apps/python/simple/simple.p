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


START:

    // Enable OCP master port
    CONFIG_OCP

    // Send notification to Host for program completion
    TRIGGER_EVENT PRU_TRIGGER_HOST_INTR_0

    HALT
