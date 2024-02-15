"""
# Load data
"""
from analysis_utils import *

dm = get_merged_data()
print(f'before blink removal: {len(dm)}')
dm = (dm.blink_latency < 0) | (dm.blink_latency > .5)
print(f'after blink removal: {len(dm)}')
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
plt.savefig(FOLDER_SVG / 'eog-channels.svg')
plt.show()


"""
Plot EOGs separately for uppper and lower, split by blink presences.
"""
import time_series_test as tst
import seaborn as sns

plt.figure(figsize=(8, 8))
plt.subplot(211)
plt.title('a) Upper-eyelid electrodes')
tst.plot(fdm, dv='erg_upper', hue_factor='has_blink', x0=-.05,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Blink presence'})
plt.xlabel('Time since flash onset (s)')
plt.ylabel('Voltage (µv)')
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(.04, color='black', linestyle=':')
plt.axvline(.06, color='black', linestyle=':')
plt.axvline(.08, color='black', linestyle=':')
plt.axvline(.1, color='black', linestyle=':')
plt.xticks([])
plt.ylim(-9e-6, 9e-6)
plt.subplot(212)
plt.title('b) Lower-eyelid electrodes')
tst.plot(fdm, dv='erg_lower', hue_factor='has_blink', x0=-.05,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Blink presence'})
plt.xlabel('Time since flash onset (s)')
plt.ylabel('Voltage (µv)')
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(.04, color='black', linestyle=':')
plt.axvline(.06, color='black', linestyle=':')
plt.axvline(.08, color='black', linestyle=':')
plt.axvline(.1, color='black', linestyle=':')
plt.ylim(-9e-6, 9e-6)
plt.savefig(FOLDER_SVG / 'eog-channels-by-blink.svg')
plt.show()


"""
Plot histogram of blink latencies
"""
plt.figure(figsize=(8, 4))
bdm = fdm.blink_latency > 0
sns.histplot(list(bdm.blink_latency), bins=20, binrange=(0, 1))
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'blink-histogram.svg')
plt.show()


"""
# Pupil constriction
"""
tst.plot(fdm, dv='pupil', x0=0, sampling_freq=1000, hues='jet',
         hue_factor='intensity_cdm2',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
plt.ylabel('Pupil size (mm)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'pupil-by-intensity.svg')
plt.show()


"""
# Effects of intensity and for full visual field
"""
plt.figure(figsize=(8, 8))
plt.subplot(211)
plt.title(f'a) Full field ERG by intensity')
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
plt.title(f'b) Full field EEG by intensity')
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
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-intensity.svg')
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
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-horizontal-field.svg')
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
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-vertical-field.svg')
plt.show()


"""
# Effects of pupil size

Plot ERG and EEG over time by pupil size bin.
"""
# First calculate pupil bins
fdm.bin_pupil = -1
fdm.bin_pupil_mm = 0
for i, bdm in enumerate(ops.bin_split(fdm.z_pupil, 5)):
    fdm.bin_pupil[bdm] = i
    fdm.bin_pupil_mm[bdm] = bdm.mean_pupil.mean
# Then plot
plt.figure(figsize=(8, 8))
plt.subplot(211)
plt.title(f'a) Full field ERG by pupil size (binned)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(.04, color='black', linestyle=':')
plt.axvline(.06, color='black', linestyle=':')
plt.axvline(.08, color='black', linestyle=':')
plt.axvline(.1, color='black', linestyle=':')
tst.plot(fdm, dv='erg', hue_factor='bin_pupil_mm', x0=-.05,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil size'})
plt.xticks([])
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) Full field EEG by pupil size (binned)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(.04, color='black', linestyle=':')
plt.axvline(.06, color='black', linestyle=':')
plt.axvline(.08, color='black', linestyle=':')
plt.axvline(.1, color='black', linestyle=':')
tst.plot(fdm, dv='erp_occipital', hue_factor='bin_pupil_mm',
         x0=-.05, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil size'})
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-pupil-size-bin.svg')


"""
# Effects of pupil-size change

Plot ERG over time as a function of whether the pupil is dilating or 
constricting.
"""
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
tst.plot(fdm, dv='erg', hue_factor='pupil_dilation', x0=-.05,
         sampling_freq=1000,
         legend_kwargs={'title': 'Pupil-size change'})
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-by-pupil-dilation.svg')
plt.show()


"""
# The relationship between pupil-size change and pupil size
"""
tst.plot(dm, dv='pupil', hue_factor='pupil_dilation')
sns.pointplot(y='mean_pupil', x='pupil_dilation', data=fdm)
plt.plot(fdm.mean_pupil, fdm.pupil_slope, '.')
sns.histplot(list(fdm.mean_pupil))

"""
Plot voltage by pupil size and intensity for specific time points
"""
fdm.erg45 = fdm.erg[:, 90:110][:, ...]
fdm.erg75 = fdm.erg[:, 110:130][:, ...]
fdm.erg100 = fdm.erg[:, 150:200][:, ...]
plt.figure(figsize=(12, 4))
plt.subplots_adjust(wspace=0)
plt.subplot(131)
plt.title('a) 40 - 60 ms')
sns.pointplot(x='intensity_cdm2', hue='bin_pupil_mm', y='erg45', data=fdm,
              palette='flare')
plt.legend(title='Pupil size (bin)')
plt.xlabel('Intensity (cd/m2)')
plt.ylabel('Voltage (µv)')
plt.ylim(*YLIM)
plt.subplot(132)
plt.title('b) 60 - 80 ms')
sns.pointplot(x='intensity_cdm2', hue='bin_pupil_mm', y='erg75', data=fdm,
              palette='flare')
plt.ylim(*YLIM)
plt.legend(title='Pupil size (bin)')
plt.xlabel('Intensity (cd/m2)')
plt.yticks([])
plt.subplot(133)
plt.title('b) 100 - 150 ms')
sns.pointplot(x='intensity_cdm2', hue='bin_pupil_mm', y='erg100', data=fdm,
              palette='flare')
plt.ylim(*YLIM)
plt.legend(title='Pupil size (bin)')
plt.xlabel('Intensity (cd/m2)')
plt.yticks([])
plt.savefig(FOLDER_SVG / 'erg-by-pupil-size-bin-and-intensity.svg')
plt.show()


"""
# Topomap

For each 20 ms time window, create a topographical map
"""
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
                         axes=ax, show=False)
    plt.savefig(FOLDER_TOPOMAPS / f'topomap-{t}.svg')
    plt.show()


"""
# Granger causality
"""
from statsmodels.tsa.stattools import grangercausalitytests

minlag = 10
maxlag = 30
erg_first = []
erp_first = []
for subject_nr, sdm in ops.split(fdm.subject_nr):
    print(subject_nr)
    x1 = np.diff(sdm.erp_occipital.mean)
    x2 = np.diff(sdm.erg.mean)
    data = np.array([x1, x2]).T
    f = []
    for lag in range(minlag, maxlag):
        results = grangercausalitytests(data, maxlag=[lag], verbose=False)
        fvalue = results[lag][0]['params_ftest'][0]
        f.append(fvalue)
    # results = grangercausalitytests(data, maxlag=np.arange(minlag, maxlag, 1),
    #                                 verbose=False)
    # for lag, result in results.items():
    #     fvalue = result[0]['params_ftest'][0]
    #     f.append(fvalue)
    plt.plot(f, color='green')
    erg_first.append(f)
    data = np.array([x2, x1]).T
    f = []
    for lag in range(minlag, maxlag):
        results = grangercausalitytests(data, maxlag=[lag], verbose=False)
        fvalue = results[lag][0]['params_ftest'][0]
        f.append(fvalue)    
    # results = grangercausalitytests(data, maxlag=np.arange(minlag, maxlag, 1),
    #                                 verbose=False)
    # f = []
    # for lag, result in results.items():
    #     fvalue = result[0]['params_ftest'][0]
    #     f.append(fvalue)
    plt.plot(f, color='red')
    erp_first.append(f)
plt.xticks(np.arange(0, maxlag - minlag, 5), np.arange(minlag, maxlag, 5))
plt.ylabel('Granger causality')
plt.xlabel('Lag (ms)')
plt.savefig(FOLDER_SVG / 'granger-causality.svg')


"""
# Statistics

Predict ERGs and ERPs based on intensity and pupil size.
"""
fdm.erg50 = fdm.erg[:, 50:]
fdm.erp50 = fdm.erp_occipital[:, 50:]
fdm.z_int = ops.z(fdm.intensity_cdm2)
fdm.z_pup = ops.z(fdm.mean_pupil_area)
fdm.z_slo = ops.z(fdm.pupil_slope)
stats_erg = tst.lmer_permutation_test(
    fdm, 'erg50 ~ z_int + z_pup + z_slo',
    groups='subject_nr')
stats_erg = tst.lmer_permutation_test(
    fdm, 'erp50 ~ z_int + z_pup + z_slo',
    groups='subject_nr')

# result = tst.lmer_series(fdm,
#     'erg50 ~ z_int + z_pup + z_slo',
#     groups='subject_nr', winlen=2)
# for row in result[1:]:
#     plt.plot(row.z, label=row.effect)
# plt.axhline(0, color='black', linestyle=':')
# plt.axhline(1.96, color='black', linestyle=':')
# plt.axhline(-1.96, color='black', linestyle=':')
# plt.legend()
# plt.show()
