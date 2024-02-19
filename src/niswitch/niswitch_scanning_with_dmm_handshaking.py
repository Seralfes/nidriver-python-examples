"""Switch - Scanning with a DMM - Handshaking (NI-SWITCH).

This example demonstrates how to scan a series of channels on a switch module and take measurements with an NI digital multimeter using handshaking.
"""
import nidmm
import niswitch


samples_to_fetch = 5

with niswitch.Session(resource_name="PXI2564", topology="2564/16-SPST", simulate=False, reset_device=True) as switch_session:
    switch_session.trigger_input = niswitch.TriggerInput.TTL0
    switch_session.scan_advanced_output = niswitch.ScanAdvancedOutput.TTL1
    switch_session.continuous_scan = True
    switch_session.scan_list = "ch0->com0;"
    switch_session.commit()

    with nidmm.Session(resource_name="DMM", id_query=False, reset_device=False, options={}) as dmm_session:
        dmm_session.configure_measurement_absolute(measurement_function=nidmm.Function.DC_VOLTS, range=10.0, resolution_absolute=1e-3)
        dmm_session.configure_trigger(trigger_source=nidmm.TriggerSource.PXI_TRIG1)
        dmm_session._set_attribute_vi_int32(attribute_id=1250334, attribute_value=0)    # Trigger slope set to Falling
        dmm_session.configure_multi_point(trigger_count=1, sample_count=0, sample_trigger=nidmm.SampleTrigger.IMMEDIATE)
        dmm_session._set_attribute_vi_int32(attribute_id=1150010, attribute_value=0)
        dmm_session.meas_complete_dest = nidmm.MeasurementCompleteDest.PXI_TRIG0
        dmm_session._set_attribute_vi_int32(attribute_id=1150002, attribute_value=0)
        dmm_session.initiate()

        switch_session.initiate()

        dmm_status = dmm_session.read_status()
        print(dmm_status)
        measurement = dmm_session.fetch_multi_point(array_size=max(dmm_status[0], samples_to_fetch), maximum_time=5000)
        print(measurement)
