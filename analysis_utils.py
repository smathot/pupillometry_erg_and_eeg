"""
# ERG, EEG, and pupil size

Imports, constants, and general functionality

LOGBOOK: 82, line 263 extraneous trigger
"""
import eeg_eyetracking_parser as eet
from eeg_eyetracking_parser import _eeg_preprocessing as eep
import mne; mne.set_log_level(False)
from mne.time_frequency import tfr_morlet
from datamatrix import DataMatrix, convert as cnv, operations as ops, \
    series as srs, functional as fnc
import numpy as np
from scipy.stats import linregress
from pathlib import Path

SUBJECTS = 31, 32, 41, 42, 51, 52, 61, 62, 71, 72, 81, 82, 91, 92
EEG_EPOCH = -0.05, 0.15
CHECKPOINT = '22022024'
PUPIL_EPOCH = 0, 1.5
ERG_PEAK1 = .047
ERG_PEAK2 = .076
MIN_BLINK_LATENCY = .1
YLIM = -6e-6, 9e-6
STIMULUS_TRIGGER = 1
FREQS = np.arange(4, 30, 1)
MORLET_MARGIN = .5

Z_THRESHOLD = 3
# Maps [-1, 1] intensity to cd/m2
INTENSITY_CDM2 = {
    -1: 0,
    -.51: 2.69,
    -.17: 9.84,
    .2: 24.24,
    .59: 48.45,
    1: 85
}
# Ordinally coded intensity
INTENSITY_ORD = {
    -1: 0,
    -.51: 1,
    -.17: 2,
    .2: 3,
    .59: 4,
    1: 5
}
mne.io.pick._PICK_TYPES_DATA_DICT['misc'] = True
FOLDER_SVG = Path('svg')
if not FOLDER_SVG.exists():
    FOLDER_SVG.mkdir()
FOLDER_TOPOMAPS = FOLDER_SVG / 'topomaps'
if not FOLDER_TOPOMAPS.exists():
    FOLDER_TOPOMAPS.mkdir()


# Monkeypatch the preprocessor to avoid EOGs from being subtracted and instead
# marking them as separate EOG channels
def custom_eog_channels(raw, *args, **kwargs):
    raw.set_channel_types(
        dict(VEOGB='eog', VEOGT='eog', HEOGL='eog', HEOGR='eog'))
eep.create_eog_channels = custom_eog_channels


def intensity_cdm2(i):
    return {
        -1: 0,
        -.51: 2.69,
        -.17: 9.84,
        .2: 24.24,
        .59: 48.45,
        1: 85
    }[i]


def area_to_mm(au):
    """Converts in arbitrary units to millimeters of diameter. This is specific
    to the recording set-up.
    
    Parameters
    ----------
    au: float
    
    Returns
    -------
    float
    """
    return -0.9904 + 0.1275 * au ** .5


def z_by_freq(col):
    """Performs z-scoring across trials, channels, and time points but 
    separately for each frequency.
    
    Parameters
    ----------
    col: MultiDimensionalColumn
    
    Returns
    -------
    MultiDimensionalColumn
    """
    zcol = col[:]
    for i in range(zcol.shape[2]):
        zcol._seq[:, :, i] = (
            (zcol._seq[:, :, i] - np.nanmean(zcol._seq[:, :, i]))
            / np.nanstd(zcol._seq[:, :, i])
        )
    return zcol


def read_subject(subject_nr):
    return eet.read_subject(
        subject_nr, eeg_preprocessing=[
            'drop_unused_channels',
            'rereference_channels',
            'annotate_emg',
            'create_eog_channels',
            'set_montage',
            'band_pass_filter',
            'autodetect_bad_channels',
            'interpolate_bads'])
    

@fnc.memoize(persistent=True, key=f'../checkpoints/{CHECKPOINT}.dm')
def get_merged_data():
    dm = DataMatrix()
    for subject_nr in SUBJECTS:
        raw, events, metadata = read_subject(subject_nr)
        sdm = cnv.from_pandas(metadata)
        sdm.blink_latency = -1
        trial_nr = -1
        stim_onset = None
        for a in raw.annotations:
            if a['description'] == '1':
                trial_nr += 1
                stim_onset = a['onset']
            if stim_onset is None:
                continue
            if a['description'] == 'BLINK':
                blink_latency = a['onset'] - stim_onset
                sdm.blink_latency[trial_nr] = blink_latency
                stim_onset = None
        sdm.pupil = cnv.from_mne_epochs(
            eet.PupilEpochs(raw, eet.epoch_trigger(events, STIMULUS_TRIGGER),
                            tmin=PUPIL_EPOCH[0], tmax=PUPIL_EPOCH[1],
                            metadata=metadata, baseline=None),
            ch_avg=True)
        sdm.eog = cnv.from_mne_epochs(
            mne.Epochs(raw, eet.epoch_trigger(events, STIMULUS_TRIGGER),
                       tmin=EEG_EPOCH[0], tmax=EEG_EPOCH[1],
                       picks='eog', metadata=metadata))
        sdm.erp = cnv.from_mne_epochs(
            mne.Epochs(raw, eet.epoch_trigger(events, STIMULUS_TRIGGER),
                       tmin=EEG_EPOCH[0], tmax=EEG_EPOCH[1],
                       picks='eeg', metadata=metadata))
        # Get time-frequency analyses
        epochs = mne.Epochs(raw, eet.epoch_trigger(events, STIMULUS_TRIGGER),
                       tmin=EEG_EPOCH[0] - MORLET_MARGIN,
                       tmax=EEG_EPOCH[0] + MORLET_MARGIN, picks='eog',
                       metadata=metadata)
        morlet = tfr_morlet(
            epochs, freqs=FREQS, n_cycles=2, n_jobs=-1,
            return_itc=False, use_fft=True, average=False,
            decim=5, picks=np.arange(len(epochs.info['ch_names'])))
        morlet.crop(0, EEG_EPOCH[1])
        sdm.eog_tfr = cnv.from_mne_tfr(morlet)
        sdm.eog_tfr = z_by_freq(sdm.eog_tfr)[:, ...]
        # The subject number is the first digit, the session number the second
        sdm.session_nr = sdm.subject_nr % 10
        sdm.subject_nr = sdm.subject_nr // 10
        sdm.erg = sdm.eog[:, ...]
        sdm.erg_upper = sdm.eog[:, ('VEOGB', 'VEOGT')][:, ...]
        sdm.erg_lower = sdm.eog[:, ('HEOGL', 'HEOGR')][:, ...]
        sdm.laterg = sdm.eog[:, ('VEOGB', 'HEOGL')][:, ...] - \
            sdm.eog[:, ('VEOGT', 'HEOGR')][:, ...]
        sdm.erp_occipital = sdm.erp[:, ('O1', 'Oz', 'O2')][:, ...]
        sdm.laterp_occipital = sdm.erp[:, 'O1'] - sdm.erp[:, 'O2']
        # We first convert pupil size to millimeters, and then take the mean
        # over the first 150 ms (below the response latency), The slope is also
        # calculated over this initial 150 ms.
        sdm.pupil = sdm.pupil @ area_to_mm
        sdm.mean_pupil = sdm.pupil[:, 0:150][:, ...]
        x = np.arange(150)
        for row in sdm:
            result = linregress(x, row.pupil[:150])
            row.pupil_slope = result.slope
        # We recode pupil size as surface area (as opposed to diamter),
        # baseline size, and z-scored values. We also make a binary split
        # on the slope indicating whether the pupil was constricting or
        # dilating.
        sdm.mean_pupil_area = sdm.mean_pupil ** 2
        sdm.bl_pupil = srs.baseline(sdm.pupil, sdm.pupil, 0, 50)
        sdm.z_pupil = ops.z(sdm.mean_pupil)
        sdm.z_pupil_slope = ops.z(sdm.pupil_slope)
        sdm.pupil_dilation = 'Constricting'
        sdm.pupil_dilation[sdm.pupil_slope > 0] = 'Dilating'
        sdm.z_erg = ops.z(sdm.erg[:, 90:110][:, ...])
        dm <<= sdm
    dm = dm.z_erg != np.nan
    dm = dm.mean_pupil != np.nan
    dm = dm.z_erg < Z_THRESHOLD
    dm = dm.z_erg > -Z_THRESHOLD
    dm = dm.z_pupil < Z_THRESHOLD
    dm = dm.z_pupil > -Z_THRESHOLD
    dm = dm.z_pupil_slope < Z_THRESHOLD
    dm = dm.z_pupil_slope > -Z_THRESHOLD
    dm = dm.target == 0
    dm.intensity_cdm2 = dm.intensity @ (lambda i: INTENSITY_CDM2[i])
    dm.intensity_ord = dm.intensity @ (lambda i: INTENSITY_ORD[i])
    dm.influx_cdm2 = dm.intensity_cdm2 * dm.mean_pupil ** 2
    dm.has_blink = 0
    dm.has_blink[dm.blink_latency >= 0] = 1
    return dm
