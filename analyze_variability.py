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
del dm.erp  # free memory
print(f'before blink removal: {len(dm)}')
dm = (dm.blink_latency < 0) | (dm.blink_latency > .5)
print(f'after blink removal: {len(dm)}')
fdm = dm.field == 'full'
add_bin_pupil(fdm)


"""
# Calculate variability

For each combination of subject, intensity, and pupil size bin, the standard 
deviation of the ERG and ERP signals is stored as a new series column.
"""
vdm_bin_pupil = DataMatrix(length=fdm.intensity.count * fdm.bin_pupil.count 
                 * fdm.subject_nr.count)
vdm_bin_pupil.erg_std = SeriesColumn(depth=fdm.erg.depth - 50)
vdm_bin_pupil.erp_std = SeriesColumn(depth=fdm.erp_occipital.depth - 50)
# vdm_bin_pupil.gaze_std = SeriesColumn(depth=fdm.gaze_vel.depth)
for row, (intensity, bin_pupil, subject_nr, sdm) in zip(vdm_bin_pupil,
      ops.split(fdm.intensity, fdm.bin_pupil, fdm.subject_nr)):
   row.intensity = intensity
   row.bin_pupil = bin_pupil
   row.subject_nr = subject_nr
   row.erg_std = sdm.erg_nobaseline.std[50:]
   row.erp_std = sdm.erp_occipital_nobaseline.std[50:]
   
   
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
vdm_pupil_dilation.erg_std = SeriesColumn(depth=fdm.erg.depth - 50)
vdm_pupil_dilation.erp_std = SeriesColumn(depth=fdm.erp_occipital.depth - 50)
for row, (intensity, pupil_dilation, subject_nr, sdm) in zip(
      vdm_pupil_dilation,
      ops.split(fdm.intensity, fdm.pupil_dilation, fdm.subject_nr)):
   row.intensity = intensity
   row.pupil_dilation = pupil_dilation
   row.subject_nr = subject_nr
   row.erg_std = sdm.erg_nobaseline.std[50:]
   row.erp_std = sdm.erp_occipital_nobaseline.std[50:]
   
   
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
# For non-baseline-corrected signal:
# Output:
# {'Intercept': [(0, 151, 1439.7196152471026, 0.996)], 'bin_pupil': [(0, 151, 357.6170572914245, 0.993)], 'intensity': []}
#
# For baseline-corrected signal:
# Output:
# {'Intercept': [(0, 151, 1607.5309512623128, 1.0)], 'bin_pupil': [(63, 151, 319.09325830520874, 1.0), (0, 42, 118.6424451962442, 0.982), (51, 54, 5.968038848591654, 0.692)], 'intensity': []}
#
# Control analysis after excluding trials with mean gaze velocity > 200
# Output:
# {'Intercept': [(0, 151, 1595.4887193992306, 1.0)], 'bin_pupil': [(64, 151, 302.19229455147587, 0.998), (10, 57, 131.24767906586305, 0.978)], 'intensity': []}

result_erp_bin_pupil = tst.lmer_permutation_test(vdm_bin_pupil,
   'erp_std ~ bin_pupil + intensity', groups='subject_nr',
   suppress_convergence_warnings=True)
print(result_erp_bin_pupil)
# For non-baseline-corrected signal:
# Output:
# {'Intercept': [(0, 151, 1891.0498128198317, 0.124)], 'bin_pupil': [(5, 18, 28.036962698852413, 0.845)], 'intensity': []}
#
# For baseline-corrected signal:
# Output:
# {'Intercept': [(0, 151, 1665.8808516710758, 0.318)], 'bin_pupil': [(69, 77, 17.27321748502119, 0.669)], 'intensity': []}

result_erg_pupil_dilation = tst.lmer_permutation_test(vdm_pupil_dilation,
   'erg_std ~ pupil_dilation + intensity', groups='subject_nr',
   suppress_convergence_warnings=True)
print(result_erg_pupil_dilation)
# For non-baseline-corrected signal:
# Output:
# {'Intercept': [(0, 151, 1236.4045841665286, 0.965)], 'pupil_dilation[T.Dilating]': [(124, 130, 11.846359311752675, 0.926)], 'intensity': []}
#
# For baseline-corrected signal:
# Output:
# {'Intercept': [(0, 151, 1511.7901320515743, 0.0)], 'pupil_dilation[T.Dilating]': [], 'intensity': []}

result_erp_pupil_dilation = tst.lmer_permutation_test(vdm_pupil_dilation,
   'erp_std ~ pupil_dilation + intensity', groups='subject_nr',
   suppress_convergence_warnings=True)
print(result_erp_pupil_dilation)
# For non-baseline-corrected signal:
# Output:
# {'Intercept': [(0, 151, 1883.0479001258147, 0.0)], 'pupil_dilation[T.Dilating]': [], 'intensity': []}
#
# For baseline-corrected signal:
# Output:
# {'Intercept': [(0, 151, 1666.789422073107, 0.066)], 'pupil_dilation[T.Dilating]': [(0, 41, 124.18694026929987, 0.999)], 'intensity': [(101, 108, 14.94440696902355, 0.624)]}
