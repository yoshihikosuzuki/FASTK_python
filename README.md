# FASTK_python

Python interface for [FASTK](https://github.com/thegenemyers/FASTK) (currently Histex and Profex). Python >= 3 is required.

## How to install

```bash
$ git clone https://github.com/yoshihikosuzuki/FASTK_python
$ cd FASTK_python
$ make
$ python setup.py install --user
```

## How to use

```python
import fastk

# Histex
hist = fastk.histex("/path/to/source[.hist]")

# Profex
prof = fastk.profex("/path/to/source[.prof]", read_id=1)
```

### `histex()`

```
Signature: fastk.histex(fastk_prefix: str, min_count: int = 1, max_count: int = 100) -> bits.util._counter.RelCounter
Docstring:
Run Histex and return a histogram of k-mer count frequencies.

positional arguments:
  @ fastk_prefix : Prefix of the output files of FastK.

optional arguments:
  @ [min|max]_count : Specify the range of the k-mer count.
```

### `profex()`

```
Signature: fastk.profex(fastk_prefix: str, read_id: int) -> List[int]
Docstring:
Run Profex and return the k-mer count profile of a single read.

positional arguments:
  @ fastk_prefix : Prefix of the output files of FastK.
  @ read_id      : Read ID (1, 2, ...)
```
