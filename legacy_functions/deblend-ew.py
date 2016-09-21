# Measure EW function definition
# there's a lotta trash here, probably.

s2pi = sqrt(2 * pi)
s2 = sqrt(2.0)


def linear(x, slope, intercept):
    return slope * x + intercept


def const(x, c):
    return c


def voigt(x, amplitude, center, sigma, gamma):
    if gamma is None:
        gamma = sigma
    z = (x - center + 1j * gamma) / (sigma * s2)
    return amplitude * wofz(z).real / (sigma * s2pi)


def gaussian(x, amplitude, center, sigma):
    return (amplitude / (s2pi * sigma)) * exp(
        -(x - center) ** 2 / (2 * sigma ** 2))


def call_linear(x, y):
    linear = LinearModel(prefix='cont_')
    pars = cont.guess(y, x=x)
    return linear, pars


def call_constant(x, y, ylock):
    const = ConstantModel(prefix='constant_')
    pars = const.guess(np.array(y), x=np.array(x))
    pars['constant_c'].set(ylock, min=ylock - ylock * 0.001,
                           max=ylock + ylock * 0.001)
    return const, pars


def call_gauss(x, y, cen, count, pars):
    label = 'g' + str(count) + '_'
    gauss = GaussianModel(prefix=label)
    pars.update(gauss.make_params())
    pars[label + 'center'].set(cen, min=cen - 0.01, max=cen + 0.01)
    pars[label + 'amplitude'].set(0, min=-(max(y) - min(y)) * 1.5, max=0.0001)
    pars[label + 'sigma'].set(fw_set / 4, min=0.005, max=fw_set / 2.3548)
    return gauss


def call_voigt(x, y, cen, count, pars):
    label = 'v' + str(count) + '_'
    voigt = VoigtModel(prefix=label)
    pars.update(voigt.make_params())
    pars[label + 'center'].set(cen, min=cen - 0.01, max=cen + 0.01)
    pars[label + 'amplitude'].set(0, min=-(max(y) - min(y)) * 1.5, max=0.0001)
    pars[label + 'sigma'].set(fw_set / 4, min=0.005, max=fw_set / 2.3548)
    pars[label + 'gamma'].set(value=fw_set / 4, vary=True, expr='')
    return voigt


def build_voigt(number, fpars, x):
    label = 'v' + str(number) + '_'
    c = fpars['constant_c']
    lbd = fpars[label + 'center']
    amp = fpars[label + 'amplitude']
    sgm = fpars[label + 'sigma']
    gma = fpars[label + 'gamma']
    y = [const(i, c) + voigt(i, amp, lbd, sgm, gma) for i in x]
    return y


def build_gauss(number, fpars, x):
    label = 'g' + str(number) + '_'
    c = fpars['constant_c']
    lbd = fpars[label + 'center']
    amp = fpars[label + 'amplitude']
    sgm = fpars[label + 'sigma']
    y = [const(i, c) + gaussian(i, amp, lbd, sgm) for i in x]
    return y


def return_ew_voigt(number, fpars, a, b):
    label = 'v' + str(number) + '_'
    c = fpars['constant_c']
    lbd = fpars[label + 'center']
    amp = fpars[label + 'amplitude']
    sgm = fpars[label + 'sigma']
    gma = fpars[label + 'gamma']

    def integrand(x):
        return (1 - (((c) + (
        amp * wofz((x - lbd + 1j * gma) / (sgm * s2)).real / (sgm * s2pi))) / (
                     c)))

    return [integrate.quad(integrand, a, b)[0], lbd, 2.3548 * sgm]


def return_ew_gauss(number, fpars, a, b):
    label = 'g' + str(number) + '_'
    c = fpars['constant_c']
    lbd = fpars[label + 'center']
    amp = fpars[label + 'amplitude']
    sgm = fpars[label + 'sigma']

    def integrand(x):
        return 1 - (((c) + ((amp / (s2pi * sgm)) * exp(
            -(1.0 * x - lbd) ** 2 / (2 * sgm ** 2)))) / (c))

    return [integrate.quad(integrand, a, b)[0], lbd, 2.3548 * sgm,
            integrate.quad(integrand, a, b)[1]]


def getclick(event):
    xval = event.xdata
    global yset
    global limits
    global limflag
    if limflag:
        limits.append(xval)
    if len(limits) == 1:
        yset = event.ydata
        print 'click on the right limit for fitting'
    if (len(limits) == 2):
        print 'type the fwhm limit'
        yset = (yset + event.ydata) / 2
        limflag = False
        plt.gcf().canvas.mpl_disconnect(clcm)


def getkey(event):
    keyp = event.key
    xval = event.xdata
    global lambdas
    global linefitype
    global returnk
    if keyp == 'enter':
        returnk = True
    else:
        print '%8.2f%3s%1s' % (xval, ' : ', keyp)
        lambdas.append(xval)
        linefitype.append(keyp)


# multiplot body:
# elif opc == 'ew':
if opc == 'ew':
    limits = []
    fw_set = ''
    yset = 0
    lambdas = []
    linefitype = []
    limflag = True
    print 'click on the left limit for fitting'
    clcm = plt.gcf().canvas.mpl_connect('button_press_event', getclick)
    while not is_number(fw_set):
        fw_set = raw_input()
    fw_set = float(fw_set)
    print '%7s%8.2f%3s%8.2f' % ('range: ', limits[0], ' - ', limits[1])
    print 'now mark the bottom of the lines for the fit.\n\'g\' for gaussian profile, \'v\' for voigt profile\npress enter when finished'
    kprm = plt.gcf().canvas.mpl_connect('key_press_event', getkey)
    whatever = raw_input()
    plt.gcf().canvas.mpl_disconnect(kprm)
    if linefitype.count('g') + linefitype.count('v') != len(linefitype):
        print 'you typed an unsupported profile. exiting ew module'
        break
    x_trim = xo[bissec(xo, limits[0]):bissec(xo, limits[1])]
    y_trim = yo[bissec(xo, limits[0]):bissec(xo, limits[1])]
    modf, pars = call_constant(x_trim, y_trim, yset)
    for i in range(len(lambdas)):
        if linefitype[i] == 'v':
            modf = modf + call_voigt(x_trim, y_trim, lambdas[i], i + 1, pars)
        if linefitype[i] == 'g':
            modf = modf + call_gauss(x_trim, y_trim, lambdas[i], i + 1, pars)
    out = modf.fit(y_trim, pars, x=x_trim)
    bvals = out.best_values
    alim, blim = x_trim[0], x_trim[-1]
    for i in range(len(lambdas)):
        if linefitype[i] == 'v':
            linpars_v = return_ew_voigt(i + 1, out.best_values, alim, blim)
            print '%5s%2d%5s%6.4f%11s%8.2f%9s%5.3f' % (
            'line ', i + 1, ': EW = ', linpars_v[0], ', center = ',
            linpars_v[1], ', fwhm = ', linpars_v[2])
        if linefitype[i] == 'g':
            linpars_g = return_ew_gauss(i + 1, out.best_values, alim, blim)
            print '%5s%2d%5s%6.4f%11s%8.2f%9s%5.3f' % (
            'line ', i + 1, ': EW = ', linpars_g[0], ', center = ',
            linpars_g[1], ', fwhm = ', linpars_g[2])
    plt.plot(x_trim, [yset for i in range(len(x_trim))], 'k-')
    plt.plot(x_trim, out.best_fit, 'b-')
    if len(lambdas) > 1:
        colors = plt.get_cmap('cool')(np.linspace(0.1, 0.9, len(lambdas)))
        for e in range(len(lambdas)):
            if linefitype[e] == 'v':
                plt.plot(x_trim, build_voigt(e + 1, bvals, x_trim),
                         linestyle='--', color=colors[e])
            if linefitype[e] == 'g':
                plt.plot(x_trim, build_gauss(e + 1, bvals, x_trim),
                         linestyle='--', color=colors[e])
    plt.draw()
    whatever = raw_input('press enter to continue')
