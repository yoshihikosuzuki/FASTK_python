from ctypes import CDLL, POINTER, c_char_p, c_int, c_longlong, cast
from os.path import dirname, isfile, join

from ._hist import Hist

lib = CDLL(join(dirname(__file__), "Histex.so"))
lib.load_hist.restype = POINTER(c_longlong)


def histex(
    fastk_prefix: str, min_count: int = 1, max_count: int = 100, unique: bool = False
) -> Hist:
    """Run Histex and return a histogram of k-mer count frequencies.

    positional arguments:
      @ fastk_prefix : Prefix of the output files of FastK.

    optional arguments:
      @ [min|max]_count : Specify the range of the k-mer count.
      @ unique          : If True, return counts of *distinct* k-mers. That is,
                          each unique k-mer is counted once regardless of its
                          frequency in the reads. If False, all k-mer *instances*
                          int the dataset are counted.
    """
    assert isfile(f"{fastk_prefix}.hist"), "No .hist file"
    cgram = lib.load_hist(
        c_char_p(fastk_prefix.encode("utf-8")),
        c_int(min_count),
        c_int(max_count),
        c_int(1 if unique else 0),
    )
    x = cast(cgram, POINTER(c_longlong * (max_count - min_count + 1)))[0]
    hist = [(j, x[i]) for i, j in enumerate(range(min_count, max_count + 1))]
    lib.free_hist(cgram)
    return Hist(hist, min_count, max_count, unique)
