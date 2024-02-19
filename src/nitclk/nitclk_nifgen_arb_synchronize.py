"""Fgen Arb Synchronize (TClk).

This example demonstrates how to generate synchronized waveforms with any number of SMC-based PXI waveform generators in the same chassis,
or any number of SMC-based PCI waveform generators sharing a common RTSI bus.

The waveform generators continuously generate synchronized square waves.

Immediate trigger is used to start generation on all modules.
"""

import math

import nifgen
import nitclk


def create_waveform_data(number_of_samples):
    """Take the number of samples and return an array of waveform data."""
    waveform_data = []
    angle_per_sample = (2 * math.pi) / number_of_samples
    for i in range(number_of_samples):
        waveform_data.append(math.sin(i * angle_per_sample) * math.sin(i * angle_per_sample * 20))

    return waveform_data


with nifgen.Session(resource_name="PXI1Slot1", options={}) as session1, nifgen.Session(resource_name="PXI1Slot2", options={}) as session2:
    waveform_data = create_waveform_data(1000)
    session_list = [session1, session2]
    for session in session_list:
        session.output_mode = nifgen.OutputMode.ARB
        session.arb_sample_rate = 100e6
        session.create_waveform(waveform_data)

    nitclk.configure_for_homogeneous_triggers(session_list)
    nitclk.synchronize(session_list, min_tclk_period=0)
    nitclk.initiate(session_list)

    nitclk.is_done()

    session1.abort()
    session2.abort()
