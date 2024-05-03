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
dm, fdm = filter_dm(dm)


"""
Recode some variable for convenient statistics
"""
fdm.erg100 = fdm.erg[:, EEG_OFFSET:]
fdm.erp100 = fdm.erp_occipital[:, EEG_OFFSET:]
fdm.z_int = ops.z(fdm.intensity_cdm2)
fdm.z_pup = ops.z(fdm.mean_pupil_area)
fdm.z_slo = ops.z(fdm.pupil_slope)



"""
Determine peak erg45 index separately for each participant and intensity level
"""
fdm.erg25_index = 0
fdm.erg25_peak = 0
for subject_nr, intensity, sdm in ops.split(fdm.subject_nr, fdm.intensity):
   erg25_index = np.argmin(sdm.erg.mean[ERG_PEAK_RANGE[0]:ERG_PEAK_RANGE[1]]) + ERG_PEAK_RANGE[0]
   fdm.erg25_index[sdm] = erg25_index
   fdm.erg25_peak[sdm] = sdm.erg[:, erg25_index - 2:erg25_index + 3][:, ...]

   
"""
Individual correlations between pupil-size change and ERG45
"""
tdm = DataMatrix(length=fdm.subject_nr.count)
for row, (subject_nr, sdm) in zip(tdm, ops.split(fdm.subject_nr)):
   model = ols('erg25_peak ~ z_int + z_pup + z_slo', data=sdm).fit()
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
model = mixedlm(formula='erg25_peak ~ z_int + z_pup + z_slo',
                data=fdm, groups='subject_nr').fit()
print(model.summary())


"""
Uses model comparison to test wether the ERG45 peak is predicted best by
the intensity or by the intensity plus an adjustment factor.
"""
model = mixedlm(formula='erg25_peak ~ intensity_cdm2',
                data=fdm, groups='subject_nr').fit(reml=False)
print(model.summary())
print(model.aic)
model = mixedlm(formula='erg25_peak ~ intensity_cdm2 + intensity_cdm2 % influx_adjustment',
                data=fdm, groups='subject_nr').fit(reml=False)
print(model.summary())
print(model.aic)


"""
Perform a sample-by-sample analysis for visualization.
"""
result = tst.lmer_series(fdm,
    'erg100 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2)
for row in result[1:]:
    plt.plot(row.z, label=row.effect)
plt.axhline(0, color='black', linestyle=':')
plt.axhline(1.96, color='black', linestyle=':')
plt.axhline(-1.96, color='black', linestyle=':')
plt.legend()
plt.show()
result = tst.lmer_series(fdm,
    'erp100 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2)
for row in result[1:]:
    plt.plot(row.z, label=row.effect)
plt.axhline(0, color='black', linestyle=':')
plt.axhline(1.96, color='black', linestyle=':')
plt.axhline(-1.96, color='black', linestyle=':')
plt.legend()
plt.show()


"""
Cluster-based permutation tests for the ERG and ERP signals. Although there was
initially a hint of variability being affected by pupil size, this effect
disappeared after a slightly different preprocessing (due to compensating for
the photodiode). This may have been spurious or is very weak, and as such we
leave it for now.
"""
import logging; logging.basicConfig(level=logging.INFO, force=True)
results_erg = tst.lmer_permutation_test(fdm,
    'erg100 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2, suppress_convergence_warnings=True)
print(results_erg)
# Output
# {'Intercept': [(40, 84, 344.018221404389, 1.0),
#   (16, 38, 181.3876541097527, 0.0),
#   (118, 151, 95.27266208637255, 0.0)],
#  'z_int': [(94, 151, 588.644491911626, 1.0),
#   (38, 64, 242.5394210652641, 0.998),
#   (12, 36, 212.02132303969242, 0.997),
#   (68, 88, 113.98986841669849, 0.975)],
#  'z_pup': [(64, 151, 526.3421609758193, 1.0),
#   (36, 56, 66.31554008492043, 0.967)],
#  'z_slo': [(16, 151, 606.7320941314092, 1.0)]}

results_erp = tst.lmer_permutation_test(fdm,
    'erp100 ~ z_int + z_pup + z_slo',
    groups='subject_nr', winlen=2, suppress_convergence_warnings=True)
print(results_erp)
# Output
# {'Intercept': [(86, 151, 303.28993020140734, 0.374),
#   (46, 76, 105.92162470683012, 0.0),
#   (18, 36, 41.50473054632326, 0.0)],
#  'z_int': [(116, 151, 183.47360047954274, 0.999),
#   (24, 64, 171.89639861702193, 0.999),
#   (68, 88, 118.39609350450344, 0.995),
#   (94, 100, 12.794898805235192, 0.653)],
#  'z_pup': [(132, 146, 30.562503478100183, 0.906),
#   (76, 90, 28.62322826418741, 0.9)],
#  'z_slo': []}

"""
Statistical analyses with interaction terms
"""
results_erg = tst.lmer_permutation_test(fdm,
    'erg100 ~ z_int * z_pup * z_slo',
    groups='subject_nr', winlen=2, suppress_convergence_warnings=True)
print(results_erg)
# Output
# {'Intercept': [(40, 84, 343.2766228810468, 0.996),
#   (16, 38, 181.49700317429685, 0.0),
#   (118, 151, 95.10729491306738, 0.0)],
#  'z_int': [(94, 151, 580.1808887707748, 1.0),
#   (38, 64, 244.67405421088569, 0.999),
#   (12, 36, 209.24801813853804, 0.996),
#   (68, 88, 110.43147590359217, 0.973)],
#  'z_pup': [(64, 151, 519.9292187555513, 1.0),
#   (36, 56, 67.29018085622731, 0.966)],
#  'z_int:z_pup': [(44, 70, 80.78833597009395, 0.989),
#   (130, 148, 47.380979809094, 0.96),
#   (14, 20, 12.615279427974727, 0.82)],
#  'z_slo': [(16, 151, 599.8106694003424, 1.0)],
#  'z_int:z_slo': [(104, 122, 42.1026230884066, 0.826),
#   (90, 100, 21.261422997971188, 0.675),
#   (36, 46, 21.082034251404938, 0.671),
#   (0, 2, 3.9664122892792624, 0.575)],
#  'z_pup:z_slo': [(70, 106, 88.47418794714277, 0.972)],
#  'z_int:z_pup:z_slo': [(150, 151, 2.1256313702740393, 0.712)]}

results_erp = tst.lmer_permutation_test(fdm,
    'erp100 ~ z_int * z_pup * z_slo',
    groups='subject_nr', winlen=2, suppress_convergence_warnings=True)
print(results_erp)
# Output
# {'Intercept': [(86, 151, 303.4408530726622, 0.436),
#   (46, 76, 107.67998346113265, 0.0),
#   (20, 36, 36.59282902539055, 0.0)],
#  'z_int': [(116, 151, 173.53457025784408, 1.0),
#   (26, 64, 171.27259671111142, 1.0),
#   (68, 88, 117.67999465131382, 0.998),
#   (94, 102, 17.682482919225603, 0.711)],
#  'z_pup': [(132, 148, 34.9193462948077, 0.916),
#   (76, 92, 33.81194973667516, 0.91)],
#  'z_int:z_pup': [(40, 68, 84.5655241173102, 0.985),
#   (128, 151, 76.46321319906427, 0.975),
#   (78, 92, 47.36793157430726, 0.929),
#   (98, 110, 31.869626161348783, 0.872)],
#  'z_slo': [],
#  'z_int:z_slo': [(102, 118, 39.46734167180677, 0.827),
#   (78, 92, 33.939941242832525, 0.781)],
#  'z_pup:z_slo': [],
#  'z_int:z_pup:z_slo': [(128, 150, 60.60719182129, 0.947)]}
