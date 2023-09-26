import nidcpower

master_SMU = "PXI1Slot1"
master_chn = "0"

slave_SMU_names = ["PXI1Slot2", "PXI1Slot3"]
slave_SMU_chns = ["0", "0"]
slave_voltage_level = [3.0, 3.0]
slave_current_limit_range = [10e-3, 10e-3]
slave_current_limit = [10e-3, 10e-3]

slave_sessions = []

with nidcpower.Session(resource_name=master_SMU, channels=master_chn, reset=False, options={}) as master_session:
    master_session.source_mode = nidcpower.SourceMode.SINGLE_POINT
    master_session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
    master_session.voltage_level = 1.0
    master_session.current_limit_range = 10e-3
    master_session.current_limit = 10e-3
    master_session.source_delay = 50e-3
    master_session.measure_when = nidcpower.MeasureWhen.AUTOMATICALLY_AFTER_SOURCE_COMPLETE
    master_session.source_trigger_type = nidcpower.TriggerType.NONE
    source_trigger_terminal = f"/{master_SMU}/Engine{master_chn}/SourceTrigger"
    source_complete_terminal = f"/{master_SMU}/Engine{master_chn}/SourceCompleteEvent"
    master_session.commit()

    for slave in range(len(slave_SMU_names)):
        slave_sessions.append(nidcpower.Session(resource_name=slave_SMU_names[slave], channels=slave_SMU_chns[slave], reset=False, options={}))
        slave_sessions[slave].source_mode = nidcpower.SourceMode.SINGLE_POINT
        slave_sessions[slave].output_function = nidcpower.OutputFunction.DC_VOLTAGE
        slave_sessions[slave].voltage_level = slave_voltage_level[slave]
        slave_sessions[slave].current_limit_range = slave_current_limit_range[slave]
        slave_sessions[slave].current_limit = slave_current_limit[slave]
        slave_sessions[slave].source_delay = 3e-5
        slave_sessions[slave].measure_when = nidcpower.MeasureWhen.ON_MEASURE_TRIGGER
        slave_sessions[slave].source_trigger_type = nidcpower.TriggerType.DIGITAL_EDGE
        slave_sessions[slave].digital_edge_source_trigger_input_terminal = source_trigger_terminal
        slave_sessions[slave].measure_trigger_type = nidcpower.TriggerType.DIGITAL_EDGE
        slave_sessions[slave].digital_edge_measure_trigger_input_terminal = source_complete_terminal
        slave_sessions[slave].commit()
        slave_sessions[slave].initiate()
    
    master_session.initiate()

    master_meas = master_session.fetch_multiple(count=1, timeout=5)
    print(f"Master Measurements: \n- Voltage: {master_meas[0][0]}\n- Current: {master_meas[0][1]}\n- In Compliance: {master_meas[0][2]}")

    slave_measurements = []

    for slave in range(len(slave_SMU_names)):
        slave_measurements.append(slave_sessions[slave].fetch_multiple(count=1, timeout=5))
        print(f"{slave_SMU_names[slave]} Measurements: \n- Voltage: {slave_measurements[slave][0][0]}\n- Current: {slave_measurements[slave][0][1]}\n- In Compliance: {slave_measurements[slave][0][2]}")