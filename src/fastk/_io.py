from typing import List, Optional, Tuple

from bits.seq import FastaRecord, load_seq

from ._Histex import histex
from ._Profex import profex, profex_multi
from ._type import ProfiledRead


def load_pread(
    read_id: int, fastk_prefix: str, seq_fname: Optional[str] = None
) -> ProfiledRead:
    """Load a single count profile and optionally its sequence.
    Note that the profile is always zero-padded.

    positional arguments:
      @ read_id      : Read ID (1, 2, 3, ...).
      @ fastk_prefix : Prefix of .prof file.
      @ seq_fname    : Sequence file name. If not specified, 'N's are set.
    """
    counts, K = profex(fastk_prefix, read_id, zero_padding=False, return_k=True)
    L = len(counts) + K - 1
    if seq_fname is not None:
        read = load_seq(seq_fname, read_id)
        seq, name = read.seq, read.name if hasattr(read, "name") else None
        assert (
            read.length < K or read.length == L
        ), "Profile length + K - 1 != Read length"
    else:
        seq, name = "N" * L, None
    return ProfiledRead(_seq=seq, id=read_id, name=name, K=K, counts=counts)


def load_preads(
    read_id_range: Tuple[int, int],
    fastk_prefix: str,
    seq_fname: Optional[str] = None,
) -> List[ProfiledRead]:
    """Load multiple profiles."""
    b, e = read_id_range
    profs = list(profex_multi(fastk_prefix, list(range(b, e + 1)), return_k=True))
    if seq_fname is not None:
        reads = load_seq(seq_fname, read_id_range, verbose=True)
    else:
        reads = [FastaRecord(seq="N" * 1, name=None) for _ in range(b, e + 1)]
    return [
        ProfiledRead(
            _seq=read.seq,
            id=read_id,
            name=read.name,
            K=K,
            counts=counts,
        )
        for read_id, (counts, K), read in zip(range(b, e + 1), profs, reads)
    ]
