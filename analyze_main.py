"""
Imports
"""
from analysis_utils import *
from matplotlib import pyplot as plt
import time_series_test as tst
import seaborn as sns
from datamatrix import SeriesColumn


"""
# Load data
"""
dm = get_merged_data()
dm, fdm = filter_dm(dm)

"""
x
"""
fdm.erg_amp = fdm.erg[:, ...]
m = fdm.erg_amp.mean
std = fdm.erg_amp.std
plt.plot(fdm.erg.plottable, alpha=.25); plt.show()

cdm = fdm.erg_amp > m - 3 * std
cdm = cdm.erg_amp < m + 3 * std
plt.plot(cdm.erg.plottable, alpha=.25); plt.show()


"""
# Pupil constriction

Plot pupil constriction after stimulus onset as a function of stimulus 
intensity for full-field flashes.
"""
tst.plot(fdm, dv='pupil', x0=0, sampling_freq=1000, hues='jet',
         hue_factor='intensity_cdm2',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
plt.ylabel('Pupil size (mm)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'pupil-by-intensity.svg')
plt.show()


"""
# Time-frequency plots
"""
Y_FREQS = np.array([0, 4, 9, 25])
plt.imshow(fdm.eog_tfr[...], aspect='auto')
plt.yticks(Y_FREQS, FREQS[Y_FREQS])
plt.xticks(np.arange(0, 30, 3), np.arange(0, .15, .015))
plt.xlabel('Time (ms)')
plt.ylabel('Frequency (Hz)')
    

"""
# Effects of intensity

Plot the ERG and EEG signals after stimulus onset as a function of stimulus
intensity for full-field flashes.
"""
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Full field ERG by intensity')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg', hue_factor='intensity_cdm2', x0=X0,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
clusters = [(94, 151, 588.644491911626, 1.0),
  (38, 64, 242.5394210652641, 0.998),
  (12, 36, 212.02132303969242, 0.997),
  (68, 88, 113.98986841669849, 0.975)]
annotate_clusters(clusters)
plt.xlim(0, .15)
plt.xticks([])
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) Full field EEG by intensity')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erp_occipital', hue_factor='intensity_cdm2',
         x0=X0, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
clusters = [(116, 151, 183.47360047954274, 0.999),
  (24, 64, 171.89639861702193, 0.999),
  (68, 88, 118.39609350450344, 0.995),
  (94, 100, 12.794898805235192, 0.653)]
annotate_clusters(clusters)
plt.hlines(y, xmin=.044, xmax=.084, color='gray')
plt.hlines(y, xmin=.087, xmax=.106, color='gray')
plt.xlim(0, .15)
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-intensity.svg')
plt.show()


"""
Split by upper and lower electrodes. 
"""
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Full field ERG by intensity (upper electrodes)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg_upper', hue_factor='intensity_cdm2', x0=X0,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
plt.xlim(0, .15)
plt.xticks([])
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) Full field ERG by intensity (lower electrodes)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg_lower', hue_factor='intensity_cdm2', x0=X0,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
plt.xlim(0, .15)
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-upper-lower-by-intensity.svg')
plt.show()



"""
# Effects of visual field

Plot the ERG and EEG signals after stimulus onset as a function of visual 
field, first for left vs right flashes.
"""
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Lateralized ERG by horizontal visual field')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(dm.field == {'left', 'right'}, dv='laterg',
         hue_factor='field', x0=X0, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Visual field'})
plt.xlim(0, .15)
plt.xticks([])
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) Lateralized EEG by horizontal visual field')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(dm.field == {'left', 'right'}, dv='laterp_occipital',
         hue_factor='field', x0=X0, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Visual field'})
plt.xlim(0, .15)
plt.axhline(0, color='black', linestyle='-')
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-horizontal-field.svg')
plt.show()


"""
And then for upper vs lower flashes.
"""
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) ERG by vertical visual field')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(dm.field == {'top', 'bottom'}, dv='erg',
         hue_factor='field', x0=X0, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Visual field'})
plt.xlim(0, .15)
plt.xticks([])
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) EEG by vertical visual field')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(dm.field == {'top', 'bottom'}, dv='erp_occipital',
         hue_factor='field', x0=X0, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Visual field'})
plt.xlim(0, .15)
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-vertical-field.svg')
plt.show()


"""
# Correlations with pupil size

Plot the ERG and EEG signals after stimulus onset as a function of pupil size
(five bins) for full-field flashes.
"""
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Full field ERG by pupil size (binned)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg', hue_factor='bin_pupil_mm', x0=X0,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil size'})
clusters = [(64, 151, 526.3421609758193, 1.0),
            (36, 56, 66.31554008492043, 0.967)]
annotate_clusters(clusters)
plt.xlim(0, .15)
plt.xticks([])
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) Full field EEG by pupil size (binned)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erp_occipital', hue_factor='bin_pupil_mm',
         x0=X0, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil size'})
plt.xlim(0, .15)
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-pupil-size-bin.svg')


"""
Separately for upper and lower electrodes
"""
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Full field ERG by pupil size (binned, upper electrodes)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg_upper', hue_factor='bin_pupil_mm', x0=X0,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil size'})
plt.xlim(0, .15)
plt.xticks([])
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'a) Full field ERG by pupil size (binned, lower electrodes)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg_lower', hue_factor='bin_pupil_mm', x0=X0,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil size'})
plt.xlim(0, .15)
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-upper-lower-by-pupil-size-bin.svg')


"""
# Effects of pupil-size change (dilating vs constricting)

Plot the ERG and EEG signals after stimulus onset as a function of pupil-size
change (dilating vs constricting) for full-field flashes.
"""
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Full field ERG by pupil-size change')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg', hue_factor='pupil_dilation', x0=X0,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil-size change'})
clusters = [(16, 151, 606.7320941314092, 1.0)]
annotate_clusters(clusters)
plt.xlim(0, .15)
plt.xticks([])
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) Full field EEG by pupil-size change')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erp_occipital', hue_factor='pupil_dilation',
         x0=X0, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil-size change'})
plt.xlim(0, .15)
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-pupil-size-change.svg')


"""
Separately for upper and lower electrodes
"""
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Full field ERG by pupil-size change (upper electrodes)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg_upper', hue_factor='pupil_dilation', x0=X0,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil-size change'})
plt.xlim(0, .15)
plt.xticks([])
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) Full field ERG by pupil-size change (lower electrodes)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg_lower', hue_factor='pupil_dilation', x0=X0,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil-size change'})
plt.xlim(0, .15)
plt.axhline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-upper-lower-by-pupil-size-change.svg')


"""
# The relationship between pupil-size change and pupil size
"""
tst.plot(dm, dv='pupil', hue_factor='pupil_dilation')
