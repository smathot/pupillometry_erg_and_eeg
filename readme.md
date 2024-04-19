# Effects of pupil size and stimulus intensity on early retinal responses

Experimental resources for the following manuscript:

- Mathôt, S., Weiden, D., Dimigen, O. (in preparation). Effects of pupil size and stimulus intensity on early retinal responses.

Analysis code is stored on GitHub:

- <https://github.com/smathot/pupillometry_erg_and_eeg>

Everything else (experiment file, data, checkpoints, and output) is stored on the OSF:

- <https://osf.io/g5utq/>

## Dependencies

The main dependencies are `eeg_eyetracking_parser` and `datamatrix` (>= 1.0) which can be installed as follows:

```
pip install eeg_eyetracking_parser datamatrix
```

See `environment.yaml` for a complete description of the Python environment used for the analysis.

The experiment file requires [OpenSesame](https://osdoc.cogsci.nl/) 4.0. The experiment requires the [`Pulse_EVT2` plug-in](https://github.com/markspan/EVT2), which needs to be installed separately.


## System requirements

Most of the analyses require 16GB of memory. To run the memoization script for multiple participants in parallel, 64 GB is recommended. To speed up the decoding analyses, a cuda-enabled graphics card is recommended.


## Running the analysis

### Explanation of files and folders on the OSF

The analysis scripts are hosted on GitHub. However, the data files, intermediate files, and output files are hosted on the OSF. You need both in order to reproduce the analyses.

- `data\` contains `.zip` archives with the raw data organized in BIDS format. There is one archive per participant, which needs to be extracted. Eye tracking data is in EyeLink `.edf` format. EEG data is in Brain Vision format (`.vhdr`, `.vmrk`, `.eeg`). For the calibration analysis, the `.edf` files need to be put together into a single subfolder called `eyetracking_data`.
- `checkpoints\` contains processed data. The main checkpoint used for the analyses described in the paper is `TODO.dm`.
- `output\` contains various output file:
  - TODO


### Analysis scripts

The analysis scripts are named by the type of analysis they perform. In addition, `analysis_utils.py` is a module with helper functions that are used by the other analysis scripts. This file is not intended to be executed directly.


## Data logbook

- In the `.vmrk` file for session 82, line 263 contained an extraneous trigger that was manually removed.
- In the `.vmrk` file for session 111, line 184 contained an extraneous trigger that was manually removed.
- Sessions 101, 102 were excluded due to excessive blinking and reduced data quality.


## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
