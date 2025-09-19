Python bindings for libcdr in Termux
==========

[![DOI](https://zenodo.org/badge/468935999.svg)](https://doi.org/10.5281/zenodo.7692820)

## Intro

Simple Python bindings for the [libcdr](https://wiki.documentfoundation.org/DLP/Libraries/libcdr) written by [Dr. Andrey Sobolev](mailto:as@tilde.pro).


## Installation

First, the `libcdr` newer than `v0.1.8` must be compiled.

```
apt install automake cmake libtool boost boost-headers librevenge cppunit libcdr
cp -r $HOME/../usr/include/librevenge-0.0/* $HOME/../usr/include
cp -r $HOME/../usr/include/libcdr-0.1/* $HOME/../usr/include
```

Then: `pip install git+https://github.com/0x64656164/pylibcdr`


## Usage

```
import sys
from pylibcdr import CDRParser
parser = CDRParser(sys.argv[1])
print(parser.dict)
```


## License

Inherited from the `libcdr` (MPL 2.0).
