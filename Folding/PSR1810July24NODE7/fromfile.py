from __future__ import division, print_function

import numpy as np

shift40 = np.array([4,0], np.int8)
shift76543210 = np.array([7,6,5,4,3,2,1,0], np.int8)
msblsb_bits = np.array([-16, 15], np.int8)
twopiby256 = 2.*np.pi / 256.

NP_DTYPES = {'1bit': 'i1', '4bit': 'i1', 'nibble': 'i1'}


def fromfile(file, dtype, count, verbose=False):
    """Read recsize bytes, with type dtype which can be bits.

    Calls np.fromfile but handles some special dtype's:
    '1bit' : Unfold for 1-bit sampling (LSB first),
             returns 8*count np.int8 samples, with values of +1 or -1
    '4bit' : Unfold for 4-bit sampling (LSB first)
             returns 2*count np.int8 samples, with -8 < value < 7
    'nibble' : Unfold for Ue-Li's 8-bit complex numbers
             returns count np.complex64 samples, with amplitudes in 4 lsb,
             as sqrt(-2*log(1-((unsigned-4bit/16+0.5)/16.))
             and phase in msb, ((signed-4bit)+0.5) * 2 * pi
             **NOT FINISHED YET** **NEEDS SCALING**
    """

    np_dtype = NP_DTYPES.get(dtype, dtype)
    if verbose:
        print("Reading {} units of dtype={}".format(count, np_dtype))
    # go via direct read to ensure we can read from gzip'd files
    raw = np.fromstring(file.read(count * np.dtype(np_dtype).itemsize),
                        dtype=np_dtype, count=count)
    if raw.size != count:
        raise EOFError

    if np_dtype is dtype:
        return raw
    elif dtype == '1bit':
        # For a given int8 byte containing bits 76543210
        # left_shift(byte[:,np.newaxis], shift76543210):
        #    [0xxxxxxx, 10xxxxxx, 210xxxxx, 3210xxxx,
        #     43210xxx, 543210xx, 6543210x, 76543210]
        split = np.left_shift(raw[:,np.newaxis], shift76543210).flatten()
        # right_shift(..., 6):
        #    [0000000x, 11111110, 22222221, 33333332,
        #     44444443, 55555554, 66666665, 77777776]
        # so least significant bits go first.
        np.right_shift(split, 6, split)  # explicitly give output for speedup
        # | 1 -> value becomes +1 or -1
        split |= 1
        return split
    elif dtype == '4bit':
        # For a given int8 byte containing bits 76543210
        # left_shift(byte[:,np.newaxis], shift40):  [3210xxxx, 76543210]
        split = np.left_shift(raw[:,np.newaxis], shift40).flatten()
        # right_shift(..., 4):                      [33333210, 77777654]
        # so least significant bits go first.
        np.right_shift(split, 4, split)  # explicitly give output for speedup
        return split
    elif dtype == 'nibble':
        # For a given int8 byte containing bits 76543210
        split = np.bitwise_and(raw[:,np.newaxis], msblsb_bits)
        # now interpretation:
        # lsb=amplitude=0..15; msb=phase=16*(-8..7)=-128..112
        # calculate sqrt(-2*log(1-((idf/16+0.5)/16.)); inplace for speed
        iph = split[:,0]
        idf = split[:,1]
        # idf += 0.5
        # idf /= 16.
        # idf = np.subtract(1., idf, out=idf)
        # idf = np.log(idf, out=idf)
        # idf *= 2.
        # amp = np.sqrt(idf, out=idf)
        amp = (idf.astype(np.float32)+0.5) / 16.
        amp = np.sqrt(-2.*np.log(1.-amp))
        phase = (iph.astype(np.float32) + 8.) * twopiby256
        return amp * np.exp(1.j * np.pi * phase)
    else:
        # this should never happen, but just in case...
        raise TypeError('data type "{}" not understood (but in NP_DTYPES!)'
                        .format(dtype))
