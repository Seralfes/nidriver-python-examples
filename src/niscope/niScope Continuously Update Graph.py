import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import niscope

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig, ax = plt.subplots()

num_samples = 250
x_increment = 2e-8

def animate(i):
    waveforms = session.channels["1"]._read(num_samples=num_samples)
    line.set_ydata(waveforms[0])
    return line,

with niscope.Session(resource_name='PXI1Slot1', options={}) as session:
    session.configure_vertical(range=5.0, coupling=niscope.VerticalCoupling.AC)
    session.configure_horizontal_timing(min_sample_rate=50000000, min_num_pts=num_samples, ref_position=50.0, num_records=1, enforce_realtime=True)
    waveforms = session.channels["1"]._read(num_samples=num_samples)
    x_time = [x_increment * x for x in range(num_samples)]

    line, = ax.plot(x_time, waveforms[0])

    ax.xaxis.set_major_formatter(ticker.EngFormatter(unit="s"))
    ax.yaxis.set_major_formatter(ticker.EngFormatter(unit="V"))
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    ax.grid()

    ani = animation.FuncAnimation(fig, animate, interval=100, blit=True, save_count=50)

    plt.title(label="Waveform Graph")
    plt.show()