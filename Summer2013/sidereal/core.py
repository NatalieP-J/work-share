import warnings
import sofa_sidereal
import numpy as np

def time2gmst(t):
    try:
        return sofa_sidereal.iauGmst82(t.ut1.jd1, t.ut1.jd2)
    except:
        warnings.warn("UT1 not set in time; using UTC instead.")
        return sofa_sidereal.gmst82(t.utc.jd1, t.utc.jd2)

def time2gast(t):
    """Calculate Greenwich apparent sidereal time, from mean sidereal time
    using equation of equinoxes"""
    gmst = time2gmst(t)
    return gmst + sofa_sidereal.eqeq94(t.tt.jd1, t.tt.jd2)

def time2lmst(t):
    return time2gmst(t) + t.lon/180.*np.pi

def time2last(t):
    return time2gast(t) + t.lon/180.*np.pi
