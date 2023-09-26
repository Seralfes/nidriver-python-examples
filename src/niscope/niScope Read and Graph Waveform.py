import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import niscope

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig, ax = plt.subplots(nrows=1)

num_samples = 250
x_increment = 2e-8

with niscope.Session(resource_name='PXI1Slot1', options={}) as session:
    session.configure_vertical(range=5.0, coupling=niscope.VerticalCoupling.AC)
    session.configure_horizontal_timing(min_sample_rate=50000000, min_num_pts=num_samples, ref_position=50.0, num_records=1, enforce_realtime=True)
    waveforms = session.channels["1"]._read(num_samples=num_samples)
    print(waveforms[1])

    x_time = [x_increment * x for x in range(num_samples)]

    ax.xaxis.set_major_formatter(ticker.EngFormatter(unit="s"))
    ax.yaxis.set_major_formatter(ticker.EngFormatter(unit="V"))
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    ax.grid()
    ax.plot(x_time, waveforms[0])

    plt.title("Waveform Graph")
    plt.show()

    session.abort()