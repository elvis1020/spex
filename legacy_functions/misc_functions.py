import numpy as np
from PyAstronomy import pyasl
from lmfit.models import GaussianModel, ConstantModel, SkewedGaussianModel,\
                         PolynomialModel
from scipy.interpolate import interp1d


# TODO: put descriptions in docstrings
# TODO: explain inputs and ouputs

#apparent continuum regions on giraffe spectra
cnt_regions = [(5672.5, 5674.8),
               (5763.9, 5765.8),
               (6069.5, 6075.8),
               (6184.3, 6184.9),
               (6328.0, 6329.5),
               (6371.9, 6372.5),
               (6422.4, 6423.6),
               (6426.6, 6427.8),
               (6577.8, 6578.4),
               (6615.1, 6616.4),
               (6626.4, 6627.1),
               (6691.15, 6691.95),
               (6718.1, 6719.15),
               (6778.1, 6779.3),
               (7496.5, 7497.0),
               (7519.9, 7520.3)]

#function to measure signal-to-noise ratio given a region
def measure_SNR(spec, region):
    
    idx1 = (np.abs(spec[0]-region[0])).argmin()
    idx2 = (np.abs(spec[0]-region[1])).argmin()
    reg = np.array(spec[1][idx1:idx2])
    if (len(reg) != 0) and (np.std(reg) > 1e-10):
        return np.mean(reg)/np.std(reg)
    else:
        return 0


#function to convert decimal to HMS coordinates
def deg2HMS(ra='', dec='', round=False):
    
    RA, DEC, rs, ds = '', '', '', ''
    if dec:
        if str(dec)[0] == '-':
            ds, dec = '-', abs(dec)
        deg = int(dec)
        decM = abs(int((dec-deg)*60))
        if round:
            decS = int((abs((dec-deg)*60)-decM)*60)
        else:
            decS = (abs((dec-deg)*60)-decM)*60
        DEC = '{0}{1}:{2}:{3}'.format(ds, deg, decM, decS)
    if ra:
        if str(ra)[0] == '-':
            rs, ra = '-', abs(ra)
        raH = int(ra/15)
        raM = int(((ra/15)-raH)*60)
        if round:
            raS = int(((((ra/15)-raH)*60)-raM)*60)
        else:
            raS = ((((ra/15)-raH)*60)-raM)*60
        RA = '{0}{1}:{2}:{3}'.format(rs, raH, raM, raS)
    if ra and dec:
        return (RA, DEC)
    else:
        return RA or DEC


#function to measure radial velocity by fourier cross-correlation
#given a template spectrum
def pyfxcor(inspec, template, vmin=-400., vmax=400., res=3, rej=200):
    
    rv, cc = pyasl.crosscorrRV(inspec[0], inspec[1], template[0], template[1],
                               vmin, vmax, res, skipedge=rej)
    
    cen_gs = np.argmax(cc)
    perfx, perfy = rv[cen_gs-5:cen_gs+6], cc[cen_gs-5:cen_gs+6]
    
    try:
        gauss = ConstantModel() + GaussianModel()
        pars = gauss.make_params()
        pars['center'].set(value=rv[np.argmax(cc)], vary=True)
        pars['amplitude'].set(value=max(cc), vary=True)
        pars['sigma'].set(vary=True)
        pars['c'].set(value=0, vary=True)
        out = gauss.fit(perfy, pars, x=perfx)
        ct = out.best_values['center']
        cterr = out.params['center'].stderr
    except:
        return 'error', ''
    
    return ct, cterr
    

#function to clean cosmic rays and bad pixels
def clean(spectra, sigfactor=2.6):
    
    md = np.median(spectra[1])
    n = int(len(spectra[0])*0.8)
    offset = (len(spectra[0])-n)/2
    absor = md - min(spectra[1][offset:n-offset])
    freq, bin = np.histogram(spectra[1], bins=50, range=(md-absor, md+absor))
    rebin = [(bin[b+1]+bin[b])/2 for b in range(len(bin)-1)]
    
    gauss = SkewedGaussianModel()
    pars = gauss.make_params()
    pars['center'].set(value=md, vary=True)
    pars['amplitude'].set(vary=True)
    pars['sigma'].set(vary=True)
    pars['gamma'].set(vary=True)
    out = gauss.fit(freq, pars, x=rebin)
    
    var = sigfactor*out.best_values['sigma']
    xrbn = np.linspace(rebin[0], rebin[-1], num=100)
    yrbn = list(out.eval(x=xrbn))
    mode = xrbn[yrbn.index(max(yrbn))]
    
    xn = np.copy(spectra[0])
    yn = np.copy(spectra[1])
    
    ist=0
    pts=[]
    errflg = False
    for i in range(len(xn)):
        if (yn[i] > mode+var) and (errflg == False):
            cnt = 0
            errflg = True
            ist = np.copy(i)
            cnt += 1
        if (yn[i] > mode+var) and (errflg == True):
            cnt += 1
        if (yn[i] < mode+var) and (errflg == True):
            pts = np.linspace(yn[ist-1], yn[i], cnt+2)[1:-1]
            for p in range(ist, i):
                yn[p] = pts[p-ist]
            errflg = False
            
    return np.array([xn, yn])

