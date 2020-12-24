from ctypes import CDLL, POINTER, Structure, cast, c_int, c_ushort, c_char_p, c_longlong
from typing import List
from os.path import dirname, join


class Profile(Structure):
    _fields_ = [("profile", POINTER(c_ushort)),
                ("length", c_int)]


lib = CDLL(join(dirname(__file__), "Profex.so"))
lib.load_profile.restype = POINTER(Profile)


def profex(fastk_prefix: str,
           read_id: int) -> List[int]:
    """Run Profex and return the k-mer count profile of a single read.

    positional arguments:
      @ fastk_prefix : Prefix of the output files of FastK.
      @ read_id      : Read ID (1, 2, ...)
    """
    ret = lib.load_profile(c_char_p(fastk_prefix.encode('utf-8')),
                           c_longlong(read_id))
    x = cast(ret.contents.profile,
             POINTER(c_ushort * ret.contents.length))[0]
    counts = [x[i] for i in range(len(x))]
    lib.free_profile(ret)
    return counts
