from lmfit.models import GaussianModel, ConstantModel, SkewedGaussianModel,\
                         PolynomialModel
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def fit(spectra, obj, sigma=2.0, ord=4, iter=4):
    
    poly = PolynomialModel(3)
    pars = poly.make_params()
    for p in range(4):
        label = 'c'+str(p)
        pars[label].set(value=1., vary=True)
    wkcopy = np.copy(spectra[1])
    truesp = [i for i in wkcopy if i > 5]
    truex = [spectra[0][i] for i in range(len(spectra[1])) if spectra[1][i] > 5]
    outcont = poly.fit(truesp, pars, x=truex)
    firstcont = outcont.eval(x=spectra[0])
    
    xn = np.copy(spectra[0])
    yn = np.copy(spectra[1])/firstcont
    
    #it plots the first step just to check out how it's being done
    pl1=plt.subplot((iter+1)*100+11)
    pl1.plot(xn, spectra[1], 'k-', linewidth=0.3)
    pl1.plot(xn, firstcont, 'r-', linewidth=0.6)
    pl1.set_ylim([0, np.mean(firstcont)*1.5])
    
    for i in range(iter):
        i_=np.copy(i)
        niter=str(i_+1)
        sigma = sigma-i*0.21*sigma
        
        md = np.median(yn)
        n = len([i for i in yn if i > 0.1])
        offset = (len(xn)-n)/2
        absor = md - min(yn[offset:n-offset])
        freq, bin = np.histogram(yn, bins=50, range=(md-absor, md+absor))
        rebin = [(bin[b+1]+bin[b])/2 for b in range(len(bin)-1)]
        
        
        gauss = SkewedGaussianModel()
        pars = gauss.make_params()
        pars['center'].set(value=md, vary=True)
        pars['amplitude'].set(vary=True)
        pars['sigma'].set(vary=True)
        pars['gamma'].set(vary=True)
        out = gauss.fit(freq, pars, x=rebin)
        
        var = sigma*out.best_values['sigma']
        xrbn = np.linspace(rebin[0], rebin[-1], num=100)
        yrbn = list(out.eval(x=xrbn))
        mode = xrbn[yrbn.index(max(yrbn))]
        
        ync = np.copy(spectra[1])
        xnc = np.copy(spectra[0])
        
        mask = []
        for j in range(len(yn)):
            if (yn[j] > mode+var/2) or (yn[j] < mode-var/2):
                mask.append(False)
            else:
                mask.append(True)
        mask = np.array(mask)
        ync = ync[mask]
        xnc = xnc[mask]
        
        poly2 = PolynomialModel(ord)
        pars2 = poly2.make_params()
        for p in range(ord+1):
            label = 'c'+str(p)
            pars2[label].set(value=1., vary=True)
        outcont2 = poly2.fit(ync, pars2, x=xnc)
        
        contf = outcont2.eval(x=xn)
        yn = spectra[1]/contf
        err = spectra[2]/contf
        
        #here it plots each step to see what's crackin'
        pln=plt.subplot(int((iter+1)*100+10+(i_+2)))
        pln.plot(xn, yn*(np.mean(contf)*0.8), 'k-', linewidth=0.3)
        pln.plot(xnc, ync, 'r-', linewidth=0.3)
        pln.plot(xn, contf, 'b-', linewidth=0.6)
        pln.set_ylim([0, np.mean(contf)*1.2])
        
    plt.savefig(obj[0]+'_fit.png', dpi=300)
    plt.clf()
        
    return np.array([xn, yn, err])
