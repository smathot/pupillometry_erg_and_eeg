%load_ext autoreload

"""
# Load data
"""
%autoreload
from analysis_utils import *

dm = get_merged_data()
fdm = dm.field == 'full'


"""
# General EOG and blink properties

Plot EOGs separately by channel.
"""
from matplotlib import pyplot as plt

plt.plot(fdm.eog[..., 'VEOGB'][0], label='VEOGB (upper left)')
plt.plot(fdm.eog[..., 'VEOGT'][0], label='VEOGT (upper right)')
plt.plot(fdm.eog[..., 'HEOGL'][0], label='HEOGL (lower left)')
plt.plot(fdm.eog[..., 'HEOGR'][0], label='HEOGR (lower right)')
plt.axhline(0, color='black', linestyle=':')
plt.axvline(50, color='black', linestyle=':')
plt.xticks(np.arange(0, 201, 50), np.arange(-50, 151, 50))
plt.xlabel('Time since flash onset (ms)')
plt.ylabel('Voltage')
plt.legend()
plt.savefig('svg/eog-channels.svg')
plt.show()


"""
Plot EOGs separately for uppper and lower, split by blink presences.
"""
import time_series_test as tst
import seaborn as sns

plt.figure(figsize=(8, 8))
plt.subplot(211)
tst.plot(fdm, dv='erg_upper', hue_factor='has_blink', x0=-.05,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Blink presence'})
plt.xlabel('Time since flash onset (s)')
plt.ylabel('Voltage (µv)')
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.xticks([])
plt.ylim(-9e-6, 9e-6)
plt.subplot(212)
tst.plot(fdm, dv='erg_lower', hue_factor='has_blink', x0=-.05,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Blink presence'})
plt.xlabel('Time since flash onset (s)')
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylim(-9e-6, 9e-6)
plt.savefig('svg/eog-channels-by-blink.svg')
plt.show()


"""
Plot histogram of blink latencies
"""
plt.figure(figsize=(8, 4))
bdm = fdm.blink_latency > 0
sns.histplot(list(bdm.blink_latency), bins=20, binrange=(0, 1))
plt.xlabel('Time since flash onset (s)')
plt.savefig('svg/blink-histogram.svg')
plt.show()


"""
# Pupil constriction
"""
tst.plot(fdm, dv='pupil', x0=0, sampling_freq=1000, hues='jet',
         hue_factor='intensity_cdm2',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
plt.ylabel('Pupil size (mm)')
plt.xlabel('Time since flash onset (s)')
plt.savefig('svg/pupil-by-intensity.svg')
plt.show()


"""
# Effects of intensity and visual field
"""
plt.figure(figsize=(8, 8))
plt.subplot(211)
plt.title(f'Full field ERG by intensity')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(ERG_PEAK1, color='green', linestyle=':')
plt.axvline(ERG_PEAK2, color='green', linestyle=':')
tst.plot(fdm, dv='erg', hue_factor='intensity_cdm2', x0=-.05,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
plt.xticks([])
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'Full field EEG by intensity')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(ERG_PEAK1, color='green', linestyle=':')
plt.axvline(ERG_PEAK2, color='green', linestyle=':')
tst.plot(fdm, dv='erp_occipital', hue_factor='intensity_cdm2',
         x0=-.05, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig('svg/erg-and-eeg-by-intensity.svg')
plt.show()


"""
# Effects of visual field on ERG and EEG

Left vs right
"""
plt.figure(figsize=(8, 8))
plt.subplot(211)
plt.title(f'Lateralized ERG by horizontal visual field')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(ERG_PEAK1, color='green', linestyle=':')
plt.axvline(ERG_PEAK2, color='green', linestyle=':')
tst.plot(dm.field == {'left', 'right'}, dv='laterg',
         hue_factor='field', x0=-.05, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Visual field'})
plt.xticks([])
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'Lateralized EEG by horizontal visual field')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(ERG_PEAK1, color='green', linestyle=':')
plt.axvline(ERG_PEAK2, color='green', linestyle=':')
tst.plot(dm.field == {'left', 'right'}, dv='laterp_occipital',
         hue_factor='field', x0=-.05, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Visual field'})
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig('svg/erg-and-eeg-by-horizontal-field.svg')
plt.show()


"""
Upper vs lower
"""
plt.figure(figsize=(8, 8))
plt.subplot(211)
plt.title(f'ERG by vertical visual field')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(ERG_PEAK1, color='green', linestyle=':')
plt.axvline(ERG_PEAK2, color='green', linestyle=':')
tst.plot(dm.field == {'top', 'bottom'}, dv='erg',
         hue_factor='field', x0=-.05, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Visual field'})
plt.xticks([])
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'EEG by vertical visual field')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(ERG_PEAK1, color='green', linestyle=':')
plt.axvline(ERG_PEAK2, color='green', linestyle=':')
tst.plot(dm.field == {'top', 'bottom'}, dv='erp_occipital',
         hue_factor='field', x0=-.05, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Visual field'})
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig('svg/erg-and-eeg-by-vertical-field.svg')
plt.show()


"""
# Effects of pupil size

Plot ERG and EEG over time by pupil size bin.
"""
# First calculate pupil bins
fdm.bin_pupil = -1
for i, bdm in enumerate(ops.bin_split(fdm.z_pupil, 5)):
    fdm.bin_pupil[bdm] = i
# Then plot
plt.figure(figsize=(8, 8))
plt.subplot(211)
plt.title(f'Full field ERG by pupil size (binned)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(ERG_PEAK1, color='green', linestyle=':')
plt.axvline(ERG_PEAK2, color='green', linestyle=':')
tst.plot(fdm, dv='erg', hue_factor='bin_pupil', x0=-.05,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil size (bin)'})
plt.xticks([])
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'Full field EEG by pupil size (binned)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(ERG_PEAK1, color='green', linestyle=':')
plt.axvline(ERG_PEAK2, color='green', linestyle=':')
tst.plot(fdm, dv='erp_occipital', hue_factor='bin_pupil',
         x0=-.05, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil size (bin)'})
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig('svg/erg-and-eeg-by-pupil-size-bin.svg')
plt.show()


"""
Plot voltage by pupil size and intensity for specific time points
"""
fdm.erg45 = fdm.erg[:, 90:110][:, ...]
fdm.erg75 = fdm.erg[:, 110:130][:, ...]
fdm.erg100 = fdm.erg[:, 150:200][:, ...]
plt.figure(figsize=(12, 4))
plt.subplots_adjust(wspace=0)
plt.subplot(131)
sns.pointplot(x='intensity_cdm2', hue='bin_pupil', y='erg45', data=fdm,
              palette='flare')
plt.legend(title='Pupil size (bin)')
plt.xlabel('Intensity (cd/m2)')
plt.ylabel('Voltage (µv)')
plt.ylim(*YLIM)
plt.subplot(132)
sns.pointplot(x='intensity_cdm2', hue='bin_pupil', y='erg75', data=fdm,
              palette='flare')
plt.ylim(*YLIM)
plt.legend(title='Pupil size (bin)')
plt.xlabel('Intensity (cd/m2)')
plt.yticks([])
plt.subplot(133)
sns.pointplot(x='intensity_cdm2', hue='bin_pupil', y='erg100', data=fdm,
              palette='flare')
plt.ylim(*YLIM)
plt.legend(title='Pupil size (bin)')
plt.xlabel('Intensity (cd/m2)')
plt.yticks([])
plt.savefig('svg/erg-by-pupil-size-bin-and-intensity.svg')
plt.show()


"""
# Topomap

For each 20 ms time window, create a topographical map
"""
%autoreload
from mne.channels import layout

raw, events, metadata = read_subject(SUBJECTS[0])
erp_pos = layout._find_topomap_coords(raw.info, 'eeg')
eog_pos = np.array([
    [-.05, .105],
    [-.05, .11],
    [.05, .105],
    [.05, .11]])
pos = np.concatenate([erp_pos, eog_pos])
dt = 20
times = np.arange(0, 121, dt)
data = np.zeros([len(times), fdm.erp.shape[1] + fdm.eog.shape[1]])
for i, t in enumerate(times):
    erp = np.concatenate([
        fdm.erp[:,:,50 + t:50 + t + dt][..., :, ...],
        fdm.eog[:,:,50 + t:50 + t + dt][..., :, ...]])
    data[i] = erp
for i, t in enumerate(times):
    ax = plt.gca()
    plt.title(f'Time {t} - {t + dt} ms')
    mne.viz.plot_topomap(data[i], pos, size=4, vlim=(data.min(), data.max()),
                         axes=ax)
    plt.show()


"""
# Granger causality
"""
from statsmodels.tsa.stattools import grangercausalitytests

minlag = 10
maxlag = 50
erg_first = []
erp_first = []
for subject_nr, sdm in ops.split(fdm.subject_nr):
    print(subject_nr)
    x1 = np.diff(sdm.erp_occipital.mean)
    x2 = np.diff(sdm.erg.mean)
    data = np.array([x1, x2]).T
    results = grangercausalitytests(data, maxlag=np.arange(minlag, maxlag, 1),
                                    verbose=False)
    f = []
    for lag, result in results.items():
        fvalue = result[0]['params_ftest'][0]
        f.append(fvalue)
    plt.plot(f, color='green')
    erg_first.append(f)
    data = np.array([x2, x1]).T
    results = grangercausalitytests(data, maxlag=np.arange(minlag, maxlag, 1),
                                    verbose=False)
    f = []
    for lag, result in results.items():
        fvalue = result[0]['params_ftest'][0]
        f.append(fvalue)
    plt.plot(f, color='red')
    erp_first.append(f)
plt.xticks(np.arange(0, maxlag - minlag, 5), np.arange(minlag, maxlag, 5))
plt.ylabel('Granger causality')
plt.xlabel('Lag (ms)')
plt.savefig('svg/granger-causality.svg')


"""
# Statistics

Predict ERGs and ERPs based on intensity and pupil size.
"""
stats_erg = tst.lmer_permutation_test(
    dm.field == 'full', 'erg ~ intensity_cdm2 + mean_pupil_area',
    groups='subject_nr')

stats_erp = tst.lmer_permutation_test(
    dm.field == 'full', 'erp_occipital ~ intensity_cdm2 + mean_pupil_area',
    groups='subject_nr')
