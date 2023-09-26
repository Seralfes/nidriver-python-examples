import nifgen

waveforms = {"sine": nifgen.Waveform.SINE,
             "square": nifgen.Waveform.SQUARE,
             "triangle": nifgen.Waveform.TRIANGLE,
             "dc": nifgen.Waveform.DC,
             "ramp_up": nifgen.Waveform.RAMP_UP,
             "ramp_down": nifgen.Waveform.RAMP_DOWN,
             "noise": nifgen.Waveform.NOISE}

with nifgen.Session(resource_name="PXI1Slot1", options={}) as session:
    session.output_mode = nifgen.OutputMode.FUNC
    session.configure_standard_waveform(waveform=waveforms["sine"], amplitude=2.0, frequency=1e6)
    session.output_enabled = True
    session.initiate()
    try:
        print("Waveform generation started. Press Ctrl + c to end the program")
        while True:
            pass
    except KeyboardInterrupt:
        session.output_enabled = False
        session.abort()
        print("Program ended")