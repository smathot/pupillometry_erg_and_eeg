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
dm, fdm = filter_dm(dm)


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
plt.figure(figsize=(6, 3))
plt.ylim(*YLIM)
plt.axhline(0, color='black', linestyle='-')
tst.plot(fdm, dv='erg', hue_factor='previous_intensity_cdm2', x0=-.1,
         sampling_freq=1000, hues='jet',
         legend_kwargs={'title': 'Intensity (cd/m2)'})
plt.xlim(0, .15)
plt.ylabel('Voltage (µv)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-by-previous-intensity.svg')
plt.show()


"""
Recode some variable for convenient statistics
"""
import logging; logging.basicConfig(level=logging.INFO, force=True)
fdm.erg100 = fdm.erg[:, EEG_OFFSET:]
fdm.erp100 = fdm.erp_occipital[:, EEG_OFFSET:]
fdm.z_int = ops.z(fdm.previous_intensity_cdm2)
fdm.z_pup = ops.z(fdm.mean_pupil_area)
fdm.z_slo = ops.z(fdm.pupil_slope)
results_erg = tst.lmer_permutation_test(fdm,
    'erg100 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2, suppress_convergence_warnings=True)
print(results_erg)
# Output
# {'Intercept': [(40, 86, 376.88145322108613, 0.999),
#   (24, 38, 97.34686067068087, 0.0),
#   (120, 151, 81.77602523460646, 0.0),
#   (20, 22, 15.627974097095374, 0.0)],
#  'z_int': [(126, 151, 56.26052640473505, 0.933)],
#  'z_pup': [(66, 151, 362.699924126399, 1.0),
#   (36, 54, 50.16729504932524, 0.963)],
#  'z_slo': [(110, 151, 129.94903032416144, 0.928),
#   (54, 70, 38.019609068113695, 0.711)]}
