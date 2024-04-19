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
gdm = fdm[:]
gdm = gdm.mean_gaze_vel != np.nan
gdm = gdm.mean_gaze_vel < 200
plt.figure(figsize=(6, 10))
plt.subplots_adjust(hspace=.4)
plt.subplot(311)
plt.title('a) Histogram of per-trial mean gaze velocity')
sns.distplot(list(gdm.mean_gaze_vel), kde=False)
plt.xlabel('Gaze velocity (arbitrary units)')
plt.subplot(312)
plt.title('b) Gaze velocity as a function of pupil size (all data)')
sns.pointplot(data=fdm, y='mean_gaze_vel', x='bin_pupil')
plt.ylabel('Gaze velocity (arbitrary units)')
plt.xlabel('Pupil size (bin)')
plt.ylim(25, 100)
plt.subplot(313)
plt.title('c) Gaze velocity as a function of pupil size (gaze velocity < 200)')
sns.pointplot(data=gdm, y='mean_gaze_vel', x='bin_pupil')
plt.ylabel('Gaze velocity (arbitrary units)')
plt.xlabel('Pupil size (bin)')
plt.ylim(25, 100)
plt.savefig(FOLDER_SVG / 'gaze-velocity.svg')
plt.show()
