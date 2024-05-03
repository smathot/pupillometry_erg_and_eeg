"""
Imports
"""
from analysis_utils import *
from matplotlib import pyplot as plt
import time_series_test as tst
import seaborn as sns
from datamatrix import SeriesColumn, DataMatrix


"""
# Load data
"""
dm = get_merged_data()
dm, fdm = filter_dm(dm)


"""
# Calculate variability

For each combination of subject, intensity, and pupil size bin, the standard 
deviation of the ERG and ERP signals is stored as a new series column.
"""
vdm_bin_pupil = DataMatrix(length=fdm.intensity.count * fdm.bin_pupil.count 
                 * fdm.subject_nr.count)
vdm_bin_pupil.erg_std = SeriesColumn(depth=fdm.erg.depth - EEG_OFFSET)
vdm_bin_pupil.erp_std = SeriesColumn(depth=fdm.erp_occipital.depth - EEG_OFFSET)
# vdm_bin_pupil.gaze_std = SeriesColumn(depth=fdm.gaze_vel.depth)
for row, (intensity, bin_pupil, subject_nr, sdm) in zip(vdm_bin_pupil,
      ops.split(fdm.intensity, fdm.bin_pupil, fdm.subject_nr)):
   row.intensity = intensity
   row.bin_pupil = bin_pupil
   row.subject_nr = subject_nr
   row.erg_std = sdm.erg_nobaseline.std[EEG_OFFSET:]
   row.erp_std = sdm.erp_occipital_nobaseline.std[EEG_OFFSET:]
   
   
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Full field ERG')
tst.plot(vdm_bin_pupil, dv='erg_std', hue_factor='bin_pupil',
         sampling_freq=1000, hues='jet')
y = .35e-5
# plt.hlines(y, xmin=0, xmax=.42, color='gray', linewidth=1)
# plt.hlines(y, xmin=.063, xmax=.151, color='gray', linewidth=5)
plt.xlim(0, .15)
plt.ylim(1e-5, 2e-5)
plt.xticks([])
plt.ylabel('Variability (µv sd)')
plt.subplot(212)
plt.title(f'b) Full field EEG')
tst.plot(vdm_bin_pupil, dv='erp_std', hue_factor='bin_pupil',
         sampling_freq=1000, hues='jet')
plt.xlim(0, .15)
plt.ylabel('Variability (µv sd)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-variability-by-pupil-bin.svg')
plt.show()


"""
As above, but then separate for pupil dilation and constriction
"""
vdm_pupil_dilation = DataMatrix(length=fdm.intensity.count 
                                * fdm.pupil_dilation.count
                                * fdm.subject_nr.count)
vdm_pupil_dilation.erg_std = SeriesColumn(depth=fdm.erg.depth - EEG_OFFSET)
vdm_pupil_dilation.erp_std = SeriesColumn(depth=fdm.erp_occipital.depth - EEG_OFFSET)
for row, (intensity, pupil_dilation, subject_nr, sdm) in zip(
      vdm_pupil_dilation,
      ops.split(fdm.intensity, fdm.pupil_dilation, fdm.subject_nr)):
   row.intensity = intensity
   row.pupil_dilation = pupil_dilation
   row.subject_nr = subject_nr
   row.erg_std = sdm.erg_nobaseline.std[EEG_OFFSET:]
   row.erp_std = sdm.erp_occipital_nobaseline.std[EEG_OFFSET:]
   
   
plt.figure(figsize=FIGSIZE)
plt.subplot(211)
plt.title(f'a) Full field ERG')
tst.plot(vdm_pupil_dilation, dv='erg_std', hue_factor='pupil_dilation',
         sampling_freq=1000, hues='jet')
plt.xlim(0, .15)
plt.ylim(1e-5, 2e-5)
plt.xticks([])
plt.ylabel('Variability (µv sd)')
plt.subplot(212)
plt.title(f'b) Full field EEG')
tst.plot(vdm_pupil_dilation, dv='erp_std', hue_factor='pupil_dilation',
         sampling_freq=1000, hues='jet')
plt.xlim(0, .15)
plt.ylabel('Variability (µv sd)')
plt.xlabel('Time since flash onset (s)')
plt.savefig(FOLDER_SVG / 'erg-and-eeg-variability-by-pupil-dilation.svg')
plt.show()


"""
# Statistics

Use cluster-based permutation test to analyze the effect of binned pupil size
and stimulus intensity on the variability of the ERG and ERP signals.
"""
result_erg_bin_pupil = tst.lmer_permutation_test(vdm_bin_pupil,
   'erg_std ~ bin_pupil + intensity', groups='subject_nr',
   suppress_convergence_warnings=True)
print(result_erg_bin_pupil)
# Output
# {'Intercept': [(0, 151, 1415.4855411207257, 0.0)],
#  'bin_pupil': [],
#  'intensity': []}

result_erp_bin_pupil = tst.lmer_permutation_test(vdm_bin_pupil,
   'erp_std ~ bin_pupil + intensity', groups='subject_nr',
   suppress_convergence_warnings=True)
print(result_erp_bin_pupil)
# Output
# {'Intercept': [(0, 151, 1931.1045173217194, 0.147)],
#  'bin_pupil': [(0, 1, 1.9674423369775385, 0.702)],
#  'intensity': []}

result_erg_pupil_dilation = tst.lmer_permutation_test(vdm_pupil_dilation,
   'erg_std ~ pupil_dilation + intensity', groups='subject_nr',
   suppress_convergence_warnings=True)
print(result_erg_pupil_dilation)
# Output
# {'Intercept': [(0, 151, 1468.0597455728664, 0.0)],
#  'pupil_dilation[T.Dilating]': [],
#  'intensity': []}

result_erp_pupil_dilation = tst.lmer_permutation_test(vdm_pupil_dilation,
   'erp_std ~ pupil_dilation + intensity', groups='subject_nr',
   suppress_convergence_warnings=True)
print(result_erp_pupil_dilation)
# Output
# {'Intercept': [(0, 151, 1917.8152932990054, 0.0)],
#  'pupil_dilation[T.Dilating]': [],
#  'intensity': []}
