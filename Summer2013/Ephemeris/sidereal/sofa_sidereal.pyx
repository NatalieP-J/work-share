import warnings

import numpy as np
cimport numpy as np
import cython

DOUBLE = np.double
ctypedef np.double_t DOUBLE_T

cdef extern from "sofa.h":
    # Sidereal
    double iauGmst82(double dj1, double dj2)
    double iauEqeq94(double date1, double date2)
    void iauPnm00a(double date1, double date2, double rbpn[3][3])
    void iauTrxp(double r[3][3], double p[3], double trp[3])

DUBIOUS = 'dubious year for UTC (before 1960.0 or 5 years ' \
          'beyond last known leap second)'

def check_return(ret, func_name, warns={}, errors={}):
    """Check the return value from an iau routine"""
    if ret in warns:
        warnings.warn('{0}: {1}'.format(func_name, warns[ret]))
    elif ret in errors:
        raise ValueError('{0}: {1}'.format(func_name, errors[ret]))
    elif ret != 0:
        raise ValueError('Unexpected return code {0} from {1}'
                         .format(repr(ret), func_name))

@cython.wraparound(False)
@cython.boundscheck(False)
def gmst82(
    np.ndarray[double, ndim=1] dj1,
    np.ndarray[double, ndim=1] dj2):
    """
    **  Given:
    **     dj1,dj2    double    UT1 Julian Date (see note)
    **
    **  Returned (function value):
    **                double    Greenwich mean sidereal time (radians)
    **
    **  Notes:
    **
    **  1) The UT1 date dj1+dj2 is a Julian Date, apportioned in any
    **     convenient way between the arguments dj1 and dj2.  For example,
    **     JD(UT1)=2450123.7 could be expressed in any of these ways,
    **     among others:
    **
    **             dj1            dj2
    **
    **         2450123.7D0        0D0        (JD method)
    **          2451545D0      -1421.3D0     (J2000 method)
    **         2400000.5D0     50123.2D0     (MJD method)
    **         2450123.5D0       0.2D0       (date & time method)
    **
    **     The JD method is the most natural and convenient to use in
    **     cases where the loss of several decimal digits of resolution
    **     is acceptable.  The J2000 and MJD methods are good compromises
    **     between resolution and convenience.  The date & time method is
    **     best matched to the algorithm used:  maximum accuracy (or, at
    **     least, minimum noise) is delivered when the dj1 argument is for
    **     0hrs UT1 on the day in question and the dj2 argument lies in the
    **     range 0 to 1, or vice versa.
    **
    **  2) The algorithm is based on the IAU 1982 expression.  This is
    **     always described as giving the GMST at 0 hours UT1.  In fact, it
    **     gives the difference between the GMST and the UT, the steady
    **     4-minutes-per-day drawing-ahead of ST with respect to UT.  When
    **     whole days are ignored, the expression happens to equal the GMST
    **     at 0 hours UT1 each day.
    **
    **  3) In this function, the entire UT1 (the sum of the two arguments
    **     dj1 and dj2) is used directly as the argument for the standard
    **     formula, the constant term of which is adjusted by 12 hours to
    **     take account of the noon phasing of Julian Date.  The UT1 is then
    **     added, but omitting whole days to conserve accuracy.
    """
    cdef unsigned int i
    cdef unsigned n = dj1.shape[0]
    assert dj1.shape[0] == dj2.shape[0]
    cdef np.ndarray[double, ndim=1] out = np.empty(n, dtype=np.double)

    for i in range(n):
        out[i] = iauGmst82( dj1[i], dj2[i])
    return out


@cython.wraparound(False)
@cython.boundscheck(False)
def eqeq94(
    np.ndarray[double, ndim=1] date1,
    np.ndarray[double, ndim=1] date2):
    """**  Equation of the equinoxes, IAU 1994 model.
    **
    **  Given:
    **     date1,date2   double     TDB date (Note 1)
    **
    **  Returned (function value):
    **                   double     equation of the equinoxes (Note 2)
    **
    **  Notes:
    **
    **  1) The date date1+date2 is a Julian Date, apportioned in any
    **     convenient way between the two arguments.  For example,
    **     JD(TT)=2450123.7 could be expressed in any of these ways,
    **     among others:
    **
    **            date1          date2
    **
    **         2450123.7           0.0       (JD method)
    **         2451545.0       -1421.3       (J2000 method)
    **         2400000.5       50123.2       (MJD method)
    **         2450123.5           0.2       (date & time method)
    **
    **     The JD method is the most natural and convenient to use in
    **     cases where the loss of several decimal digits of resolution
    **     is acceptable.  The J2000 method is best matched to the way
    **     the argument is handled internally and will deliver the
    **     optimum resolution.  The MJD method and the date & time methods
    **     are both good compromises between resolution and convenience.
    **
    **  2) The result, which is in radians, operates in the following sense:
    **
    **        Greenwich apparent ST = GMST + equation of the equinoxes
    """
    cdef unsigned int i
    cdef unsigned n = date1.shape[0]
    assert date1.shape[0] == date2.shape[0]
    cdef np.ndarray[double, ndim=1] out = np.empty(n, dtype=np.double)

    for i in range(n):
        out[i] = iauEqeq94( date1[i], date2[i])
    return out

def pnm00a(
    np.ndarray[double, ndim=1] date1,
    np.ndarray[double, ndim=1] date2):
    """
    **  Given:
    **     date1,date2  double     TT as a 2-part Julian Date (Note 1)
    **
    **  Returned:
    **     rbpn         double[3][3]    classical NPB matrix (Note 2)
    **
    **  Notes:
    **
    **  1) The TT date date1+date2 is a Julian Date, apportioned in any
    **     convenient way between the two arguments.  For example,
    **     JD(TT)=2450123.7 could be expressed in any of these ways,
    **     among others:
    **
    **            date1          date2
    **
    **         2450123.7           0.0       (JD method)
    **         2451545.0       -1421.3       (J2000 method)
    **         2400000.5       50123.2       (MJD method)
    **         2450123.5           0.2       (date & time method)
    **
    **     The JD method is the most natural and convenient to use in
    **     cases where the loss of several decimal digits of resolution
    **     is acceptable.  The J2000 method is best matched to the way
    **     the argument is handled internally and will deliver the
    **     optimum resolution.  The MJD method and the date & time methods
    **     are both good compromises between resolution and convenience.
    **
    **  2) The matrix operates in the sense V(date) = rbpn * V(GCRS), where
    **     the p-vector V(date) is with respect to the true equatorial triad
    **     of date date1+date2 and the p-vector V(GCRS) is with respect to
    **     the Geocentric Celestial Reference System (IAU, 2000).
    """
    cdef unsigned int i
    cdef unsigned n = date1.shape[0]
    assert date1.shape[0] == date2.shape[0]
    cdef np.ndarray[double, ndim=2] mat = np.empty((3,3), dtype=np.double)
    #cdef np.ndarray[double, ndim=3] out = np.empty((n,3,3), dtype=np.double)

    for i in range(n):
        iauPnm00a( date1[i], date2[i], &mat[0,0])
    return 
