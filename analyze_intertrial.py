"""
Imports
"""
from analysis_utils import *
from matplotlib import pyplot as plt
import time_series_test as tst
import seaborn as sns
from datamatrix import SeriesColumn, operations as ops


"""
# Load data
"""
dm = get_merged_data()
del dm.erp  # free memory
print(f'before blink removal: {len(dm)}')
dm = (dm.blink_latency < 0) | (dm.blink_latency > .5)
print(f'after blink removal: {len(dm)}')
fdm = dm.field == 'full'
add_bin_pupil(fdm)


"""
Add carry-over data
"""
idm = DataMatrix()
fdm.previous_intensity_cdm2 = 0
fdm.trial_diff = 0
for subject_nr, session_nr, sdm in ops.split(fdm.subject_nr, fdm.session_nr):
    print(len(sdm))
    sdm.previous_intensity_cdm2[1:] = sdm.intensity_cdm2[:-1]
    sdm.trial_diff[1:] = sdm.count_trial_sequence[1:] - sdm.count_trial_sequence[:-1]
    sdm = sdm.trial_diff == 1
    idm <<= sdm
fdm = idm

"""
# Effects of intensity of previous trial

Plot the ERG and EEG signals after stimulus onset as a function of stimulus
intensity for full-field flashes.
"""
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Full field ERG by intensity (previous trial)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg', hue_factor='previous_intensity_cdm2', x0=-.05,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
y = -5e-6
plt.xlim(0, .15)
plt.xticks([])
plt.ylabel('Voltage (µv)')
plt.subplot(212)
plt.title(f'b) Full field EEG by intensity (previous trial)')
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erp_occipital', hue_factor='previous_intensity_cdm2',
         x0=-.05, sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
y = -5e-6
plt.xlim(0, .15)
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-previous-intensity.svg')
plt.show()


"""
Recode some variable for convenient statistics
"""
fdm.erg50 = fdm.erg[:, 50:]
fdm.erp50 = fdm.erp_occipital[:, 50:]
fdm.z_int = ops.z(fdm.previous_intensity_cdm2)
fdm.z_pup = ops.z(fdm.mean_pupil_area)
fdm.z_slo = ops.z(fdm.pupil_slope)
results_erg = tst.lmer_permutation_test(fdm,
    'erg50 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2, suppress_convergence_warnings=True)
print(results_erg)
# {'Intercept': [(60, 104, 350.3198909529296, 0.999), (34, 56, 138.95756176490073, 0.0), (138, 151, 31.623055454478646, 0.0)], 'z_int': [(122, 151, 67.54670180383071, 0.938)], 'z_pup': [(86, 151, 231.92924534197934, 1.0), (54, 74, 55.766043050079006, 0.965)], 'z_slo': [(122, 151, 113.39599338452528, 0.921), (38, 52, 33.094110188028765, 0.637), (70, 74, 7.889665788849149, 0.373)]}
