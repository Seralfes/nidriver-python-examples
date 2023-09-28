#!/usr/bin/python

import argparse
from ctypes import pythonapi
import niscope
import nitclk
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4, width=80)


def example(resource_name1, resource_name2, options, channels, max_input_freq, vertical_range, min_sample_rate, min_record_length, trigger_source, trigger_level):
    with niscope.Session(resource_name=resource_name1) as session1, niscope.Session(resource_name=resource_name2) as session2:
        session_list = [session1, session2]
        for session in session_list:
            session.configure_chan_characteristics(input_impedance=1e6, max_input_frequency=max_input_freq) # 1 M ohm and -1 to achieve full bandwidth
            session.configure_vertical(range=vertical_range, coupling=niscope.VerticalCoupling.DC, offset=0, probe_attenuation=1, enabled=True)
            session.configure_horizontal_timing(min_sample_rate=min_sample_rate, min_num_pts=min_record_length, ref_position=50, num_records=1, enforce_realtime=True)
            if session == session_list[0]:
                session.configure_trigger_edge(trigger_source=trigger_source, level=trigger_level, trigger_coupling=niscope.TriggerCoupling.DC, 
                                            slope=niscope.TriggerSlope.POSITIVE, holdoff=0, delay=0)
                
        nitclk.configure_for_homogeneous_triggers(session_list)
        nitclk.synchronize(session_list, min_tclk_period=0)
        nitclk.initiate(session_list)

        for session in session_list:
            print(session.channels[0].fetch_array_measurement(array_meas_function=niscope.ArrayMeasurement.MULTI_ACQ_AVERAGE, meas_num_samples=-1))


def _main(argsv):
    parser = argparse.ArgumentParser(description='Demonstrates synchronizing multiple scopes.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n1', '--resource-name1', default='PXI1Slot9', help='Resource name of an NI digitizer.')
    parser.add_argument('-n2', '--resource-name2', default='PXI1Slot10', help='Resource name of an NI digitizer.')
    parser.add_argument('-c', '--channels', default='0', help='Channel(s) to use')
    parser.add_argument('-f', '--max-freq', default=-1.00, type=float, help='Max input frequency (Hz)')
    parser.add_argument('-vr', '--vertical-range', default=5.00, type=float, help='Vertical range (V)')
    parser.add_argument('-sr', '--min-sample-rate', default=100e6, type=float, help='Min sample rate (S/s)')
    parser.add_argument('-l', '--min-length', default=1000, type=int, help='Measure record length')
    parser.add_argument('-ts', '--trigger-source', default='0', type=str, help='Trigger source')
    parser.add_argument('-tl', '--trigger-level', default=0.00, type=float, help='Trigger level (V)')
    parser.add_argument('-op', '--option-string', default='', type=str, help='Option string')
    args = parser.parse_args(argsv)
    example(args.resource_name1, args.resource_name2, args.channels, args.option_string, args.max_freq, args.vertical_range,
            args.min_sample_rate, args.min_length, args.trigger_source, args.trigger_level)


def main():
    _main(sys.argv[1:])


def test_example():
    options = {'simulate': False, 'driver_setup': {'Model': '5122', 'BoardType': 'PXIe', }, }
    example('PXI1Slot9', 'PXI1Slot10', '0', options, -1.00, 5.00, 100e6, 1000, '0', 0.00)


def test_main():
    cmd_line = ['--option-string', 'Simulate=0, DriverSetup=Model:5122; BoardType:PXIe', ]
    _main(cmd_line)


if __name__ == '__main__':
    main()