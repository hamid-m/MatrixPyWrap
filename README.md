# MatrixPyWrap

Wrapping Matrix C-Code from UAV Lab in Python.  

* Useful Tutorial on ctypes [here](http://python.net/crew/theller/ctypes/tutorial.html)

## Basic Usage of Ctypes

1. Compile to get `.so` file
```
gcc -lm -shared -Wl,-soname,matrix -o matrix.so -fPIC matrix.c
```

2. Load into python using ctypes and define input and output arguments for each function.  An example would be the `mat_creat` function:
```python
mat_creat = matrix.mat_creat
mat_creat.argtypes = [ctypes.c_int]*3
mat_creat.restype = cPPDOUBLE
```


Where `cPPDOUBLE` is simply an alias for the *pointer-to-pointer-of-doubles* needed to specify the c-matrix type.

## MatCol, MatRow
There are two methods (A and B) to gain access to MatCol and MatRow.

* **Method A:** Defining python method to do casting.
    - (+) no need to modify C library
    - (-) slower (laptop: 2.2 microsec per loop)

* **Method B:** Modifying C to give wrappable MatCol, MatRow function.
    - (+) faster (laptop: 3: 693 nanasec per loop)
    - (-) requires modifying C library

Current implementation uses Method A, so that the original C-Library can be used.

### Method A: Defining python method to do casting.
    #define Mathead(a)  ((MATHEAD *)((MATHEAD *)(a) - 1))
    #define MatRow(a)   (Mathead(a)->row)
    #define MatCol(a)   (Mathead(a)->col)

This enables determining the size of the C-matrix.

### Method B: Modifying C to give wrappable MatCol, MatRow function.

    1) Comment out the 3 '#define' lines in matrix.h
    2) Add the following function definitions in matrix.c
        /* Wrapper Functions
        * Hamid, March 12, 2014
        */
        int MatRow(MATRIX a){
         return(Mathead(a)->row);
        }

        int MatCol(MATRIX a){
        return(Mathead(a)->col);
        }
    3) Add the following Python definitions:

        MatCol = matrix.MatCol
        MatCol.argtypes = [ctypes.POINTER( ctypes.POINTER( ctypes.c_double ))]
        MatCol.restype  = ctypes.c_int

        MatRow = matrix.MatRow
        MatRow.argtypes = [ctypes.POINTER( ctypes.POINTER( ctypes.c_double ))]
        MatRow.restype  = ctypes.c_int



## Other Bits and Pieces

*Past History*

1. March 14, 2014: access to MatRow and MatCol implemented.
2. March 11, 2014: This seems to be working.  However, we need a way to access the Mathead(), MatRow, and MatCol functions.  Otherwise, we have no way to know the size of our matrix!
3. June 3, 2014: pushed onto UMN Github for further development

*Notes:*

1. There is little/no error checking in matrix.c  For example, passing a
  non-square matrix to mat_deg causes dramatic crashing.