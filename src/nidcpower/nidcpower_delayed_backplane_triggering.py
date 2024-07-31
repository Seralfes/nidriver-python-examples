"""NI-DCPower SMU Delayed Backplane Triggering.

This example demonstrates how to setup a delayed trigger for one SMU,
using another SMU as the trigger source.

This example uses Single Point source mode, but should be easily adaptable to use Advanced Sequence mode.
"""

import nidcpower


# Change SMU resources names accordingly
SMU1_resource_name = "PXI4139"
SMU2_resource_name = "PXIe4135"

# Delays the generation of the Source Complete Event (but not the sourcing or measuring) of SMU1
# to use as the trigger for SMU2
# this is the parameter you are interested in modifying
SMU1_source_delay = 50e-6               # the unit for this parameter is seconds

with nidcpower.Session(SMU1_resource_name) as smu1, nidcpower.Session(SMU2_resource_name) as smu2:
    # SMU1 Settings
    smu1.source_mode = nidcpower.SourceMode.SINGLE_POINT
    smu1.output_function = nidcpower.OutputFunction.DC_VOLTAGE
    smu1.voltage_level = 1
    smu1.measure_when = nidcpower.MeasureWhen.AUTOMATICALLY_AFTER_SOURCE_COMPLETE

    # Source without waiting for a trigger. When the channel starts sourcing, it will export the Source Complete Event.
    smu1.source_trigger_type = nidcpower.TriggerType.NONE

    smu1.source_delay = SMU1_source_delay

    # SMU2 Settings
    smu2.source_mode = nidcpower.SourceMode.SINGLE_POINT
    smu2.output_function = nidcpower.OutputFunction.DC_VOLTAGE
    smu2.voltage_level = 1
    smu2.measure_when = nidcpower.MeasureWhen.AUTOMATICALLY_AFTER_SOURCE_COMPLETE
    smu2.source_trigger_type = nidcpower.TriggerType.DIGITAL_EDGE

    # Pulls the Source Complete Event from the SMU1,
    # and automatically routes the signal through the PXI backplane
    smu2.digital_edge_source_trigger_input_terminal = f"/{smu1.io_resource_descriptor}/Engine0/SourceCompleteEvent"

    smu1.commit()
    smu2.commit()

    smu2.initiate()
    smu1.initiate()

    smu2.wait_for_event(event_id=nidcpower.Event.SOURCE_COMPLETE, timeout=6)

    smu1_measurements = smu1.fetch_multiple(count=1)
    smu2_measurements = smu2.fetch_multiple(count=1)

    volts_smu1 = smu1_measurements[0]
    volts_smu2 = smu2_measurements[0]

    print(volts_smu1)
    print(volts_smu2)
