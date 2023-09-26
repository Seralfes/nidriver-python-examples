import niswitch

with niswitch.Session(resource_name="PXI2564", topology="2564/16-SPST", simulate=False, reset_device=False) as session:
    session.scan_list = "ch0->com0;"
    session.trigger_input = niswitch.TriggerInput.SOFTWARE_TRIG
    session.continuous_scan = True
    session.initiate()
    session.send_software_trigger()