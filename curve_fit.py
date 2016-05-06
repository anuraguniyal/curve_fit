import sys
import csv
from scipy.optimize import curve_fit
import scipy

def fn(x, *args):
    v = 0
    print args
    for i, k in enumerate(args):
        if i >= len(x):
            v += k
        else:
            v += k*x[i]
    return v

def test():
    def myfunc(x1, x2, x3):
        return 3*x1+4*x2+5*x3

    x_ar = [[], [], []]
    y_ar = []
    for x1 in range(3):
        for x2 in range(3):
            for x3 in range(3):
                y = myfunc(x1, x2, x3)
                x_ar[0].append(x1)
                x_ar[1].append(x2)
                x_ar[2].append(x3)
                y_ar.append(y)
                print "%s, %s, %s, %s"%(x1, x2, x3, y)

    p0 = scipy.array([2, 1, 1, 1, 2])
    popt, pcov = curve_fit(fn, scipy.array(x_ar), scipy.array(y_ar), p0)
    print popt

def curve_fit_csv(csv_file, indices):
    x_ar = None
    y_ar = []
    names = []
    for row in csv.reader(open(csv_file)):
        if len(row) == 0 or row[0][0] == '#':
            continue
        if indices is None:
            y_ar.append(float(row[-1]))
            x_values = row[:-1]
        else:
            names.append(row[0])
            y_ar.append(float(row[indices[-1]]))
            x_values = []
            for i in indices[:-1]:
                x_values.append(row[i])
        if x_ar is None:#
            x_ar = []
            for _ in x_values:
                x_ar.append([])
        for i, x in enumerate(x_values):
            x_ar[i].append(float(x))

    p0 = [1]*(len(x_ar)+1)
    popt, pcov = curve_fit(fn, scipy.array(x_ar), scipy.array(y_ar), scipy.array(p0))
    print "equation parameters"
    print popt
    print "covariance"
    print pcov
    if indices is None:
        return
    # if indices given lets print each row calculation
    for i, name in enumerate(names):
        calculated = popt[-1] # constant part
        for xi, p in enumerate(popt[:-1]):
            calculated += x_ar[xi][i]*p
        diff = (y_ar[i]-calculated)*100/y_ar[i]
        print "%s actual = %.1f calculated = %.1f  diff = %.1f%%"%(name, y_ar[i], calculated, diff)

if __name__ == "__main__":
    #exit(test())
    try:
        indices = [int(i) for i in sys.argv[2].split(",")]
    except IndexError,e:
        indices = None
    curve_fit_csv(sys.argv[1], indices)
