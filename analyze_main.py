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
del dm.erp  # free memory
print(f'before blink removal: {len(dm)}')
dm = (dm.blink_latency < 0) | (dm.blink_latency > .5)
print(f'after blink removal: {len(dm)}')
fdm = dm.field == 'full'


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
# Effects of visual field

Plot the ERG and EEG signals after stimulus onset as a function of visual 
field, first for left vs right flashes.
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
And then for upper vs lower flashes.
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
# Correlations with pupil size

Plot the ERG and EEG signals after stimulus onset as a function of pupil size
(five bins) for full-field flashes.
"""
# First calculate pupil bins
fdm.bin_pupil = -1
fdm.bin_pupil_mm = 0
for i, bdm in enumerate(ops.bin_split(fdm.z_pupil, 2)):
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
# Effects of pupil-size change (dilating vs constricting)

Plot the ERG and EEG signals after stimulus onset as a function of pupil-size
change (dilating vs constricting) for full-field flashes.
"""
plt.figure(figsize=(8, 8))
plt.subplot(211)
plt.title(f'a) Full field ERG by pupil-size change')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(.04, color='black', linestyle=':')
plt.axvline(.06, color='black', linestyle=':')
plt.axvline(.08, color='black', linestyle=':')
plt.axvline(.1, color='black', linestyle=':')
tst.plot(fdm, dv='erg', hue_factor='pupil_dilation', x0=-.05,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil-size change'})
plt.xticks([])
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) Full field EEG by pupil-size change')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.axvline(.04, color='black', linestyle=':')
plt.axvline(.06, color='black', linestyle=':')
plt.axvline(.08, color='black', linestyle=':')
plt.axvline(.1, color='black', linestyle=':')
tst.plot(fdm, dv='erp_occipital', hue_factor='pupil_dilation',
         x0=-.05, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Pupil-size change'})
plt.axhline(0, color='black', linestyle=':')
plt.axvline(0, color='black', linestyle=':')
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-pupil-size-change.svg')


"""
# The relationship between pupil-size change and pupil size
"""
tst.plot(dm, dv='pupil', hue_factor='pupil_dilation')


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
Plot variability by pupil size
"""
vdm = DataMatrix(length=fdm.intensity.count * fdm.bin_pupil.count 
                 * fdm.subject_nr.count)
vdm.pupil_std = SeriesColumn(depth=fdm.erg.depth - 50)
for row, (intensity, bin_pupil, subject_nr, sdm) in zip(vdm,
      ops.split(fdm.intensity, fdm.bin_pupil, fdm.subject_nr)):
   row.intensity = intensity
   row.bin_pupil = bin_pupil
   row.subject_nr = subject_nr
   row.pupil_std = sdm.erg.std[50:]

for intensity, idm in ops.split(vdm.intensity):
   tst.plot(idm, dv='pupil_std', hue_factor='bin_pupil')
   plt.show()
tst.plot(vdm, dv='pupil_std', hue_factor='bin_pupil')

# vresult = tst.lmer_permutation_test(vdm,
#    'pupil_std ~ bin_pupil + intensity', groups='subject_nr',
#    suppress_convergence_warnings=True)
