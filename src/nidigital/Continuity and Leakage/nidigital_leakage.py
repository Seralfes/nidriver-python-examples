"""NI-Digital Leakage test.

This example demonstrates how to perform a Leakage test with a PXIe-6570/1 Digital Pattern Driver.

The example is intended to work with any DUT, provided the same PinMap structure and groups are used.

Should the PinMap be changed, make sure to update the code appropriately.
"""

# Module imports
import nidigital
import os

test_voltages = [0, 3]
current_limit = 25e-6
currents = []  # list that stores current measurements
pass_fail = [] # list that stores Pass/Fail results

with nidigital.Session(resource_name="PXIe6570", reset_device=False, options={}) as session:
    # Store directory path
    dir = os.path.join(os.path.dirname(__file__))

    pin_map_filepath = os.path.join(dir, 'PinMap.pinmap')
    session.load_pin_map(file_path=pin_map_filepath)

    # Set all pins to PPMU mode
    session.channels["All_Pins"].selected_function = nidigital.SelectedFunction.PPMU
    session.channels["All_Pins"].ppmu_aperture_time_units = nidigital.PPMUApertureTimeUnits.SECONDS
    session.channels["All_Pins"].ppmu_aperture_time = 20e-6

    # Configure Power pins for supplying power to the DUT
    session.channels["Power"].ppmu_output_function = nidigital.PPMUOutputFunction.VOLTAGE
    session.channels["Power"].ppmu_current_limit_range = 10e-3
    session.channels["Power"].ppmu_voltage_level = 3.3
    session.channels["Power"].ppmu_source()

    # Configure PPMU pins to the DUT for voltage sourcing
    session.channels["DUTPins"].ppmu_current_limit_range = 10e-6
    session.channels["DUTPins"].ppmu_output_function = nidigital.PPMUOutputFunction.VOLTAGE

    pin_info = session.channels["DUTPins"].get_pin_results_pin_information()

    # Loop through specified test voltages
    for i in range(len(test_voltages)):
        session.channels["DUTPins"].ppmu_voltage_level = test_voltages[i]
        session.channels["DUTPins"].ppmu_source()
        currents.append(session.channels["DUTPins"].ppmu_measure(measurement_type=nidigital.PPMUMeasurementType.CURRENT))

        # Loop through each pin data and display the measurement results
        for j in range(len(pin_info)):
            print(f'{pin_info[j][0]} on Site {pin_info[j][1]} @ {test_voltages[i]}V: {currents[i][j]:3e}A --> {"Pass" if currents[i][j] <= current_limit else "Fail"}')
    
    session.channels[""].selected_function = nidigital.SelectedFunction.DISCONNECT
