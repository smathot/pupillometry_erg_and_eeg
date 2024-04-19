"""
Imports
"""
from analysis_utils import *
from matplotlib import pyplot as plt
import time_series_test as tst
import seaborn as sns
from datamatrix import operations as ops



"""
# Load data
"""
dm = get_merged_data()
fdm = dm.field == 'full'


"""
# General EOG and blink properties

Plot EOGs separately by channel.
"""
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
def plot_eog_by_blink(fdm, path, ylim=(-9e6, 9e6)):
   plt.figure(figsize=FIGSIZE)
   plt.subplot(211)
   plt.title('a) Upper-eyelid electrodes')
   tst.plot(fdm, dv='erg_upper', hue_factor='has_blink', x0=-.05,
            sampling_freq=1000, hues='jet',
            legend_kwargs={'title': 'Blink presence'})
   # plt.xlabel('Time since flash onset (s)')
   plt.ylabel('Voltage (µv)')
   plt.axhline(0, color='black', linestyle=':')
   plt.axvline(0, color='black', linestyle=':')
   plt.xticks([])
   if ylim:
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
   if ylim:
      plt.ylim(-9e-6, 9e-6)
   plt.savefig(path)
   plt.show()
   
   
plot_eog_by_blink(fdm, FOLDER_SVG / 'eog-channels-by-blink.svg')


"""
As above, but separately for each participant
"""
path = FOLDER_SVG / 'eog-channels-by-blink'
if not path.exists():
   path.mkdir()
for subject_nr, sdm in ops.split(fdm.subject_nr):
   print(f'Subject {subject_nr}')
   plot_eog_by_blink(sdm, path / f'subject-{subject_nr}.svg', ylim=None)
   
   

"""
Plot individual overall ERGs
"""
tst.plot(fdm, dv='erg', hue_factor='subject_nr')
plt.savefig(FOLDER_SVG / 'overall-erg-by-subject.svg')
plt.show()


"""
Plot histogram of blink latencies and blinks per subject
"""
plt.figure(figsize=FIGSIZE)
plt.subplots_adjust(hspace=.3)
plt.subplot(211)
bdm = fdm.blink_latency > 0
sns.histplot(list(bdm.blink_latency), bins=20, binrange=(0, 1))
plt.xlabel('Time since flash onset (s)')
plt.subplot(211)
plt.subplot(212)
sns.barplot(y='has_blink', x='subject_nr', data=fdm)
plt.xticks([])
plt.xlabel('Subject')
plt.ylabel('Blink proportion')
plt.savefig(FOLDER_SVG / 'blinks.svg')
plt.show()
