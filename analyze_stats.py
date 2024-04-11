"""
Imports
"""
from analysis_utils import *
import time_series_test as tst
from statsmodels.formula.api import ols
from matplotlib import pyplot as plt
from statsmodels.formula.api import mixedlm


"""
# Load data
"""
dm = get_merged_data()
print(f'before blink removal: {len(dm)}')
dm = (dm.blink_latency < 0) | (dm.blink_latency > .5)
print(f'after blink removal: {len(dm)}')
fdm = dm.field == 'full'
add_bin_pupil(fdm)

"""
Recode some variable for convenient statistics
"""
fdm.erg50 = fdm.erg[:, 50:]
fdm.erp50 = fdm.erp_occipital[:, 50:]
fdm.z_int = ops.z(fdm.intensity_cdm2)
fdm.z_pup = ops.z(fdm.mean_pupil_area)
fdm.z_slo = ops.z(fdm.pupil_slope)



"""
Determine peak erg45 index separately for each participant
"""
fdm.erg45_index = 0
fdm.erg45_peak = 0
for subject_nr, intensity, sdm in ops.split(fdm.subject_nr, fdm.intensity):
   erg45_index = np.argmin(sdm.erg.mean[80:110]) + 80
   fdm.erg45_index[sdm] = erg45_index
   fdm.erg45_peak[sdm] = sdm.erg[:, erg45_index - 2:erg45_index + 3][:, ...]

   
"""
Individual correlations between pupil-size change and ERG45
"""
tdm = DataMatrix(length=fdm.subject_nr.count)
for row, (subject_nr, sdm) in zip(tdm, ops.split(fdm.subject_nr)):
   model = ols('erg45_peak ~ z_int + z_pup + z_slo', data=sdm).fit()
   row.z_int = model.tvalues['z_int']
   row.z_pup = model.tvalues['z_pup']
   row.z_slo = model.tvalues['z_slo']
plt.plot(sorted(tdm.z_int), 'o-', label='Intensity')
plt.plot(sorted(tdm.z_pup), 'o-', label='Pupil size')
plt.plot(sorted(tdm.z_slo), 'o-', label='Pupil-size change')
plt.axhline(0, linestyle=':', color='black')
plt.legend()


"""
# Statistics

Predict ERG45 peak based on intensity, pupil size, and stimulus intensity.
"""
model = mixedlm(formula='erg45_peak ~ z_int + z_pup + z_slo',
                data=fdm, groups='subject_nr').fit()
print(model.summary())


"""
Uses model comparison to test wether the ERG45 peak is predicted best by
the intensity or by the intensity plus an adjustment factor.
"""
model = mixedlm(formula='erg45_peak ~ intensity_cdm2',
                data=fdm, groups='subject_nr').fit(reml=False)
print(model.summary())
print(model.aic)
model = mixedlm(formula='erg45_peak ~ intensity_cdm2 + intensity_cdm2 % influx_adjustment',
                data=fdm, groups='subject_nr').fit(reml=False)
print(model.summary())
print(model.aic)


"""
Perform a sample-by-sample analysis for visualization.
"""
result = tst.lmer_series(fdm,
    'erg50 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2)
for row in result[1:]:
    plt.plot(row.z, label=row.effect)
plt.axhline(0, color='black', linestyle=':')
plt.axhline(1.96, color='black', linestyle=':')
plt.axhline(-1.96, color='black', linestyle=':')
plt.legend()
plt.show()
result = tst.lmer_series(fdm,
    'erp50 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2)
for row in result[1:]:
    plt.plot(row.z, label=row.effect)
plt.axhline(0, color='black', linestyle=':')
plt.axhline(1.96, color='black', linestyle=':')
plt.axhline(-1.96, color='black', linestyle=':')
plt.legend()
plt.show()


"""
Cluster-based permutation tests for the ERG and ERP signals

Results ERG

Intensity:
- 32 - 54 ms, p = .002
- 56 - 84 ms, p < .001
- 86 - 106 ms, p = .020
- 116 - 151 ms, p < .001
Pupil size:
- 56 - 76 ms, p = .021
- 84 - 151 ms, p < .001
Pupil dilation:
- 26 - 151 ms, p < .001

Results ERP
Intensity:
- 44 - 84 ms, p = .001
- 88 - 106, p = .002
"""
results_erg = tst.lmer_permutation_test(fdm,
    'erg50 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2, suppress_convergence_warnings=True)
print(results_erg)
# Output
# {'Intercept': [(60, 104, 339.7570481597462, 1.0), (32, 56, 178.52256096270145, 0.0), (136, 151, 37.66049548327012, 0.0)], 'z_int': [(116, 151, 281.3613825576001, 1.0), (56, 84, 278.00461891319617, 1.0), (32, 54, 189.5803611590004, 0.998), (86, 106, 105.79734833303719, 0.98)], 'z_pup': [(84, 151, 381.3753663568668, 1.0), (56, 76, 70.0786227727514, 0.979)], 'z_slo': [(26, 151, 580.414213713522, 1.0), (6, 16, 20.67233638060932, 0.481)]}
results_erp = tst.lmer_permutation_test(fdm,
    'erp50 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2, suppress_convergence_warnings=True)
print(results_erp)
# Output
# {'Intercept': [(104, 151, 241.8637994918009, 0.535), (66, 94, 103.64184434129604, 0.0), (42, 54, 28.354857410013334, 0.0)], 'z_int': [(44, 84, 181.2442494509215, 0.999), (88, 106, 106.66170507941264, 0.988), (138, 151, 51.25600127698418, 0.922), (114, 118, 8.256975799286591, 0.627)], 'z_pup': [(94, 102, 16.70387741684087, 0.845)], 'z_slo': []}


"""
Fixational drift
"""
import seaborn as sns
import analysis_utils
analysis_utils.N_PUPIL_BINS = 10
add_bin_pupil(fdm)
fdm.gaze_x = srs.smooth(fdm.gaze_x, winlen=11)
fdm.gaze_y = srs.smooth(fdm.gaze_y, winlen=11)
fdm.gaze_vel = ((fdm.gaze_x[1:, :150] - fdm.gaze_x[:-1, :150]) ** 2
                + (fdm.gaze_y[1:, :150] - fdm.gaze_y[:-1, :150]) ** 2) ** .5
fdm.mean_gaze_vel = fdm.gaze_vel[:, ...]
gdm = fdm.mean_gaze_vel != np.nan
gdm = gdm.mean_gaze_vel < 200
fdm = fdm.mean_gaze_vel != np.nan
fdm = fdm.mean_gaze_vel < 200
sns.distplot(list(gdm.mean_gaze_vel))
plt.show()
tst.plot(gdm, dv='gaze_vel', hue_factor='bin_pupil')
plt.show()
tst.plot(gdm, dv='gaze_vel', hue_factor='pupil_dilation')
plt.show()
sns.pointplot(data=gdm, y='mean_gaze_vel', x='bin_pupil')
plt.show()
sns.pointplot(data=gdm, y='mean_gaze_vel', x='pupil_dilation')
plt.show()
model = mixedlm(formula='mean_gaze_vel ~ z_pup',
                data=gdm, groups='subject_nr').fit()
print(model.summary())
