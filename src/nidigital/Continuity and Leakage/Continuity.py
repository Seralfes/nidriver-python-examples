import nidigital
import os

force_current = 100e-6
high_limit = 0.8
low_limit = 0.0
voltages = []
pass_fail = ""

with nidigital.Session(resource_name="PXIe6570", reset_device=False, options={}) as session:
    dir = os.path.join(os.path.dirname(__file__))

    pin_map_filename = os.path.join(dir, 'PinMap.pinmap')
    session.load_pin_map(file_path=pin_map_filename)

    session.channels["All_Pins"].selected_function = nidigital.SelectedFunction.PPMU
    session.channels["All_Pins"].ppmu_aperture_time_units = nidigital.PPMUApertureTimeUnits.SECONDS
    session.channels["All_Pins"].ppmu_aperture_time = 20e-6

    session.channels["Power"].ppmu_output_function = nidigital.PPMUOutputFunction.VOLTAGE
    session.channels["Power"].ppmu_current_limit_range = 10e-3
    session.channels["Power"].ppmu_voltage_level = 0
    session.channels["Power"].ppmu_source()

    session.channels["DUTPins"].ppmu_current_level_range = 128e-6
    session.channels["DUTPins"].ppmu_voltage_limit_low = -1.5
    session.channels["DUTPins"].ppmu_voltage_limit_high = 1.5
    session.channels["DUTPins"].ppmu_output_function = nidigital.PPMUOutputFunction.CURRENT
    session.channels["DUTPins"].ppmu_current_level = force_current
    pin_info = session.channels["DUTPins"].get_pin_results_pin_information()


    for i in range(2):
        session.channels["DUTPins"].ppmu_source()
        voltages.append(session.channels["DUTPins"].ppmu_measure(measurement_type=nidigital.PPMUMeasurementType.VOLTAGE))
        for j in range(len(pin_info)):
            if abs(voltages[i][j]) >= abs(low_limit) and abs(voltages[i][j]) <= abs(high_limit):
                pass_fail = "Pass"
            else:
                pass_fail = "Fail"
            print(f'{pin_info[j][0]} on Site {pin_info[j][1]} @ {session.channels["DUTPins"].ppmu_current_level:.3e}A: {voltages[i][j]:.3f} V --> {pass_fail}')     
        session.channels["DUTPins"].ppmu_current_level = force_current * -1     
    
    session.channels[""].selected_function = nidigital.SelectedFunction.DISCONNECT