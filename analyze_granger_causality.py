"""
Imports
"""
from analysis_utils import *
from statsmodels.tsa.stattools import grangercausalitytests
from matplotlib import pyplot as plt
from scipy.stats import ttest_rel


"""
# Load data
"""
dm = get_merged_data()
dm, fdm = filter_dm(dm)


"""
# Granger causality

First perform the analysis
"""
minlag = 10
maxlag = 30
erg_first = []
erp_first = []
for subject_nr, sdm in ops.split(fdm.subject_nr):
    print(subject_nr)
    x1 = np.diff(sdm.erp_occipital.mean)
    x2 = np.diff(sdm.erg.mean)
    data = np.array([x1, x2]).T
    f = []
    results = grangercausalitytests(data, maxlag=np.arange(minlag, maxlag, 1),
                                    verbose=False)
    for lag, result in results.items():
        fvalue = result[0]['params_ftest'][0]
        f.append(fvalue)
    erg_first.append(f)
    data = np.array([x2, x1]).T
    f = []
    results = grangercausalitytests(data, maxlag=np.arange(minlag, maxlag, 1),
                                    verbose=False)
    f = []
    for lag, result in results.items():
        fvalue = result[0]['params_ftest'][0]
        f.append(fvalue)
    erp_first.append(f)
erg_first = np.array(erg_first)
erp_first = np.array(erp_first)
   

"""
Then plot and statistically analyze the results
"""
plt.figure(figsize=(6, 3))
plt.plot(erg_first.T, ':', color='green')
plt.plot(erg_first.mean(axis=0), color='green', label='ERG to occipital ERP')
plt.plot(erp_first.T, ':', color='red')
plt.plot(erp_first.mean(axis=0), color='red', label='Occipital ERP to ERG')
plt.xticks(np.arange(0, maxlag - minlag, 5), np.arange(minlag, maxlag, 5))
plt.ylabel('Granger causality')
plt.xlabel('Lag (ms)')
plt.legend(title='Direction')
plt.savefig(FOLDER_SVG / 'granger-causality.svg')
plt.show()
ttest = ttest_rel(erg_first, erp_first)
print(ttest.pvalue)
