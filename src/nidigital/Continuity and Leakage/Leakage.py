import nidigital
import os

test_voltages = [0, 3]
current_limit = 25e-6
currents = []
pass_fail = []

with nidigital.Session(resource_name="PXIe6570", reset_device=False, options={}) as session:
    dir = os.path.join(os.path.dirname(__file__))

    pin_map_filename = os.path.join(dir, 'PinMap.pinmap')
    session.load_pin_map(file_path=pin_map_filename)

    session.channels["All_Pins"].selected_function = nidigital.SelectedFunction.PPMU
    session.channels["All_Pins"].ppmu_aperture_time_units = nidigital.PPMUApertureTimeUnits.SECONDS
    session.channels["All_Pins"].ppmu_aperture_time = 20e-6

    session.channels["Power"].ppmu_output_function = nidigital.PPMUOutputFunction.VOLTAGE
    session.channels["Power"].ppmu_current_limit_range = 10e-3
    session.channels["Power"].ppmu_voltage_level = 3.3
    session.channels["Power"].ppmu_source()

    session.channels["DUTPins"].ppmu_current_limit_range = 10e-6
    session.channels["DUTPins"].ppmu_output_function = nidigital.PPMUOutputFunction.VOLTAGE

    pin_info = session.channels["DUTPins"].get_pin_results_pin_information()


    for i in range(len(test_voltages)):
        session.channels["DUTPins"].ppmu_voltage_level = test_voltages[i]
        session.channels["DUTPins"].ppmu_source()
        currents.append(session.channels["DUTPins"].ppmu_measure(measurement_type=nidigital.PPMUMeasurementType.CURRENT))
        for j in range(len(pin_info)):
            print(f'{pin_info[j][0]} on Site {pin_info[j][1]} @ {test_voltages[i]}V: {currents[i][j]:3e}A --> {"Pass" if currents[i][j] <= current_limit else "Fail"}')
    
    session.channels[""].selected_function = nidigital.SelectedFunction.DISCONNECT