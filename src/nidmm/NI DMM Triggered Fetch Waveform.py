###### This example demonstrates how to take a waveform voltage measurement on two DMMs #######
###### The DMMs are synced via PXI_TRIG0 sent out by an SMU, since the DMMs are incapable of sourcing a trigger ######

import nidmm
import nidcpower

# Create DMM and SMU sessions. Make sure to change the resource names to the ones you specify in NI MAX:
options = {'simulate': False}

SMU_session = nidcpower.Session("PXIe4135", channels=None, reset=False, options=options, independent_channels=True)
DMM1_session = nidmm.Session("PXISlot4", False, False, options)
DMM2_session = nidmm.Session("PXISlot5", False, False, options)

dmm_sessions = [DMM1_session, DMM2_session]

def configure_smu(session):
    session.source_mode = nidcpower.SourceMode.SEQUENCE             # This also works for Single Point sourcing
    session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
    session.voltage_level_autorange = True
    session.current_level_autorange = True
    session.current_limit = 0.01
    session.set_sequence(values=[2.0], source_delays=[0.0])         # If Single Point is used, replace this with session.voltage_level = float
    session.measure_record_length = 100                             # Remove this is Single Point is used
    session.aperture_time = 0.1
    
def configure_dmm(sessions):
    for session in sessions:
        session.configure_waveform_acquisition(measurement_function=nidmm.Function.WAVEFORM_VOLTAGE, range=10, rate=1e6, waveform_points=50)
    configure_triggers(sessions)

def configure_triggers(sessions):
    SMU_session.source_trigger_type = nidcpower.TriggerType.NONE    
    SMU_session.source_complete_event_output_terminal = "PXI_TRIG0"                                     # Specify PXI Trigger line 0 where the source complete event will be routed
    sessions[0].configure_trigger(trigger_source=nidmm.TriggerSource.PXI_TRIG0, trigger_delay=0.0)      # Configure trigger for DMM1 to wait for a signal on PXI Trigger line 0
    sessions[1].configure_trigger(trigger_source=nidmm.TriggerSource.PXI_TRIG0, trigger_delay=0.0)      # Configure trigger for DMM2 to wait for a signal on PXI Trigger line 0
    initiate_instruments(sessions)

def initiate_instruments(sessions):
    for session in sessions:
        session.initiate()
    SMU_session.initiate()

def close_instruments(sessions):
    for session in sessions:
        session.abort()
        session.close()
    SMU_session.abort()
    SMU_session.close()

def measurement(sessions):
    configure_smu(SMU_session)
    configure_dmm(sessions)
    backlog, acquisition_state = sessions[0].read_status()              # read_status() returns the "number of measurements available to be read" (backlog) and the current acquisition state
    backlog2, acquisition_state2 = sessions[1].read_status()
    DMM1_measurements = DMM1_session.fetch_waveform(backlog)            # Use the backlog variable to specify the number of measurements to fetch
    DMM2_measurements = DMM2_session.fetch_waveform(backlog2)
    print("DMM1: ", DMM1_measurements,
          "\n\nDMM2: ", DMM2_measurements)
    close_instruments(sessions)
    
measurement(dmm_sessions)
