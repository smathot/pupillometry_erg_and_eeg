"""
Imports
"""
from analysis_utils import *
from mne.channels import layout
from matplotlib import pyplot as plt


"""
# Load data
"""
dm = get_merged_data()
dm, fdm = filter_dm(dm, del_erp=False)


"""
# Topomaps

For each 20 ms time window, create a topographical map
"""
raw, events, metadata = read_subject(SUBJECTS[0])
erp_pos = layout._find_topomap_coords(raw.info, 'eeg')
eog_pos = np.array([
    [-.05, .105],  # VEOGT top
    [-.05, .11],   # HEOGL bottom
    [.05, .105],   # VEOGB top
    [.05, .11],    # HEOGR bottom
])
pos = np.concatenate([erp_pos, eog_pos])
dt = 10
times = np.arange(0, 121, dt)
data = np.zeros([len(times), fdm.erp.shape[1] + fdm.eog.shape[1]])
for i, t in enumerate(times):
    erp = np.concatenate([
        fdm.erp[:,:,EEG_OFFSET + t:EEG_OFFSET + t + dt][..., :, ...],
        fdm.eog[:,:,EEG_OFFSET + t:EEG_OFFSET + t + dt][..., :, ...]])
    data[i] = erp
for i, t in enumerate(times):
    ax = plt.gca()
    plt.title(f'Time {t} - {t + dt} ms')
    mne.viz.plot_topomap(data[i], pos, size=4, vlim=(data.min(), data.max()),
                         axes=ax, show=False)
    plt.savefig(FOLDER_TOPOMAPS / f'topomap-{t}.svg')
    plt.show()
