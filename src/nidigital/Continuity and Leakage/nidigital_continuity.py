"""NI-Digital Continuity test.

This example demonstrates how to perform a Continuity test with a PXIe-6570/1 Digital Pattern Driver.

The example is intended to work with any DUT, provided the same PinMap structure and groups are used.

Should the PinMap be changed, make sure to update the code appropriately.
"""

# Module imports
import nidigital
import os

force_current = 100e-6
high_limit = 0.8  # diode forward voltage high limit
low_limit = 0.0   # diode forward voltage low limit
voltages = []     # list that stores voltage measurements
pass_fail = ""

with nidigital.Session(resource_name="PXIe6570", reset_device=False, options={}) as session:
    # Store directory path
    dir = os.path.join(os.path.dirname(__file__))

    pin_map_filename = os.path.join(dir, 'PinMap.pinmap')
    session.load_pin_map(file_path=pin_map_filename)

    # Set all pins to PPMU mode
    session.channels["All_Pins"].selected_function = nidigital.SelectedFunction.PPMU
    session.channels["All_Pins"].ppmu_aperture_time_units = nidigital.PPMUApertureTimeUnits.SECONDS
    session.channels["All_Pins"].ppmu_aperture_time = 20e-6

    # Configure Power pins to 0V to simulate a short from the pin to ground
    session.channels["Power"].ppmu_output_function = nidigital.PPMUOutputFunction.VOLTAGE
    session.channels["Power"].ppmu_current_limit_range = 10e-3
    session.channels["Power"].ppmu_voltage_level = 0
    session.channels["Power"].ppmu_source()

    # Configure PPMU pins to the DUT for current sourcing
    session.channels["DUTPins"].ppmu_current_level_range = 128e-6
    session.channels["DUTPins"].ppmu_voltage_limit_low = -1.5
    session.channels["DUTPins"].ppmu_voltage_limit_high = 1.5
    session.channels["DUTPins"].ppmu_output_function = nidigital.PPMUOutputFunction.CURRENT
    session.channels["DUTPins"].ppmu_current_level = force_current
    pin_info = session.channels["DUTPins"].get_pin_results_pin_information()

    # Loop twice to test the positive and negative clamping diodes
    for i in range(2):
        session.channels["DUTPins"].ppmu_source()
        voltages.append(session.channels["DUTPins"].ppmu_measure(measurement_type=nidigital.PPMUMeasurementType.VOLTAGE))

        # Loop through each pin data and display the measurement results
        for j in range(len(pin_info)):

            # Compare measurement result to limits and determine pass or failure with possible cause
            if abs(voltages[i][j]) >= abs(low_limit) and abs(voltages[i][j]) <= abs(high_limit):
                pass_fail = "Pass"
            else:
                pass_fail = "Fail"

            print(f'{pin_info[j][0]} on Site {pin_info[j][1]} '
                  f'@ {session.channels["DUTPins"].ppmu_current_level:.3e} A: '
                  f'{voltages[i][j]:.3f} V --> {pass_fail}')

        # Negate all values to test negative clamping diode
        session.channels["DUTPins"].ppmu_current_level = force_current * -1     
    
    session.channels[""].selected_function = nidigital.SelectedFunction.DISCONNECT
