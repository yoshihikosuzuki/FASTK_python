from ctypes import CDLL, POINTER, Structure, c_char_p, c_int, c_longlong, c_ushort, cast
from os.path import dirname, isfile, join

from bits.seq import load_seq

from ._profile import Pread


class Profile(Structure):
    _fields_ = [("profile", POINTER(c_ushort)), ("length", c_int), ("K", c_int)]


lib = CDLL(join(dirname(__file__), "Profex.so"))
lib.load_profile.restype = POINTER(Profile)


def profex(
    fastk_prefix: str,
    read_ids: int | tuple[int, int],
    seq_fname: str | None = None,
    zero_padding: bool = False,
) -> Pread | list[Pread]:
    """Run Profex and return the k-mer count profile of a single read.

    positional arguments:
      @ fastk_prefix : Prefix of the output files of FastK.
      @ read_ids     : Read ID (1, 2, ...) or tuple of (start, end) read IDs (1, 2, ...)

    optional arguments:
      @ seq_fname    : Sequence file name. If not specified, 'N's are set.
      @ zero_padding : If True, add (K - 1) zero counts to the prefix.
    """
    assert isfile(f"{fastk_prefix}.prof"), "No .prof file"

    is_single_read = isinstance(read_ids, int)
    if is_single_read:
        read_ids = (read_ids, read_ids)

    if seq_fname is not None:
        reads = load_seq(seq_fname, read_ids, verbose=True)

    lib.open_profile(c_char_p(fastk_prefix.encode("utf-8")))

    preads = []
    b, e = read_ids
    for read_id in list(range(b, e + 1)):
        ret = lib.load_profile(c_longlong(read_id))
        x = cast(ret.contents.profile, POINTER(c_ushort * ret.contents.length))[0]
        counts = [x[i] for i in range(len(x))]
        K = ret.contents.K
        if zero_padding:
            counts = [0] * (K - 1) + counts
        if seq_fname is None:
            pread = Pread(id=read_id, counts=counts, K=K)
        else:
            read = reads[read_id - b]
            seq, name = read.seq, read.name if hasattr(read, "name") else None
            assert (
                read.length < K or read.length == len(counts) + K - 1
            ), "Profile length + K - 1 != Read length"
            pread = Pread(id=read_id, counts=counts, K=K, _seq=seq, name=name)
        preads.append(pread)

    lib.free_profile(ret)

    return preads if not is_single_read else preads[0]
