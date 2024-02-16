"""
Imports
"""
from analysis_utils import *
import time_series_test as tst


"""
# Load data
"""
dm = get_merged_data()
print(f'before blink removal: {len(dm)}')
dm = (dm.blink_latency < 0) | (dm.blink_latency > .5)
print(f'after blink removal: {len(dm)}')
fdm = dm.field == 'full'



"""
# Statistics

Predict ERGs and ERPs based on intensity and pupil size.
"""
fdm.erg50 = fdm.erg[:, 50:]
fdm.erg45 = fdm.erg[:, 90:100]
fdm.erp50 = fdm.erp_occipital[:, 50:]
fdm.z_int = ops.z(fdm.intensity_cdm2)
fdm.z_pup = ops.z(fdm.mean_pupil_area)
fdm.z_slo = ops.z(fdm.pupil_slope)


cv_erg45 = tst.lmer_crossvalidation_test(fdm,
    'erg45 ~ z_int + z_pup + z_slo',
    groups='subject_nr')


stats_erg = tst.lmer_permutation_test(
    fdm, 'erg50 ~ z_int + z_pup + z_slo',
    groups='subject_nr')
# stats_erp = tst.lmer_permutation_test(
#     fdm, 'erp50 ~ z_int + z_pup + z_slo',
#     groups='subject_nr')

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
