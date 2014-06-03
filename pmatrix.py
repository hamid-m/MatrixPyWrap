"""
This module is designed to expose the c-matrix library in Python.  Tools and
methods to support this process should be included here.
"""   
import ctypes
import os

# Constants from matrix.h
UNDEFINED    = -1
ZERO_MATRIX	 = 0
UNIT_MATRIX  = 1
ONES_MATRIX  = 2

cPPDOUBLE = ctypes.POINTER( ctypes.POINTER( ctypes.c_double ) )

# This structure is used to do appropriate casting and get size of matrix
class MATHEAD(ctypes.Structure):
    _fields_ = [("row", ctypes.c_int),
                ("col", ctypes.c_int)]

# Not sure if this is needed.
class MATBODY(ctypes.Structure):
    _fields_ = [("head", MATHEAD),
                ("matrix", ctypes.POINTER(ctypes.c_double))]
      
def MatRow(a):
    return ctypes.cast(a, ctypes.POINTER(MATHEAD))[-1].row
    
def MatCol(a):
    return ctypes.cast(a, ctypes.POINTER(MATHEAD))[-1].col



# Tutorial: http://python.net/crew/theller/ctypes/tutorial.html
# Compile:
# >> gcc -lm -shared -Wl,-soname,matrix -o matrix.so -fPIC matrix.c
matrix = ctypes.CDLL(os.path.abspath("matrix.so"))

# MAT_CREAT
mat_creat = matrix.mat_creat
mat_creat.argtypes = [ctypes.c_int]*3
mat_creat.restype = cPPDOUBLE

# MAT_FILL
mat_fill = matrix.mat_fill
mat_fill.argtypes = [cPPDOUBLE, ctypes.c_int]
mat_fill.restype = cPPDOUBLE

# MAT_FREE
mat_free = matrix.mat_free
mat_free.argtypes = [cPPDOUBLE]
mat_free.restype  = ctypes.c_int

# MAT_COPY
mat_copy = matrix.mat_copy
mat_copy.argtypes = [cPPDOUBLE, cPPDOUBLE]
mat_copy.restype = cPPDOUBLE

# MAT_DET
mat_det = matrix.mat_det
mat_det.argtypes = [cPPDOUBLE]
mat_det.restype = ctypes.c_double

# MAT_DUMP
mat_dump = matrix.mat_dump
mat_dump.argtypes = [cPPDOUBLE]
mat_dump.restype = cPPDOUBLE

# MAT_COPY
mat_copy = matrix.mat_copy
mat_copy.argtypes = [cPPDOUBLE, cPPDOUBLE]
mat_copy.restype = cPPDOUBLE

# MAT_COPY1
mat_copy1 = matrix.mat_copy1
mat_copy1.argtypes = [cPPDOUBLE, cPPDOUBLE]
mat_copy1.restype = cPPDOUBLE

# MAT_COLCOPY1
mat_colcopy1 = matrix.mat_colcopy1
mat_colcopy1.argtypes = [cPPDOUBLE, cPPDOUBLE, ctypes.c_int, ctypes.c_int]
mat_colcopy1.restype  = cPPDOUBLE

# FGETMAT
# TODO: fgetmat
# int fgetmat		(MATRIX, FILE *fp);



# # # # # # # #
# Python Tools #
# # # # # # # #
import numpy as np

def cmat2list(A):
    """
    Converts C-Matrix to nested list.
    """
    rows, cols = MatRow(A), MatCol(A)
    Alist = []
    for r in xrange(rows):
        row = []
        for c in xrange(cols):
            row.append(A[r][c])
        Alist.append(row)
    return Alist

def cmat2numpy(A, output='matrix'):
    """
    Convert C-Matrix to Numpy matrix (or array).  If numpy array is returned,
    the result will be 'squeezed' to remove extra dimensions.
    
    Parameters
    ----------
    A:     C-Matrix, formed using mat_creat()
    output:  variable type to return ['matrix' or 'array']
    
    Returns
    -------
    Anp: numpy (matrix or array) representation of C-Matrix A
    
    
    See Also
    --------
    cmat2list : returns a nested-list representation of C-Matrix.
    """
    Alist = cmat2list(A)
    if output == 'matrix':
        Anp = np.matrix(Alist, dtype=float)
    elif output == 'array':
        Anp = np.squeeze(np.array(Alist, dtype=float))
    else:
        print("Requested output type unrecognized.  Must be 'matrix' or 'array'.")
        print("Returning NaN")
        return np.NaN        
        
    return Anp
    

def list2cmat(Alist):
    """
    Convert nested list to C-Matrix
    """
    # Check input type
    if type(Alist) is not list:
        print("list2cmat(): Input type must be nested-list.")
        print("\tReturning NaN")
        return np.NaN
    # TODO: handle (error?) when variable dimension in list
    rows, cols = len(Alist), len(Alist[0])
    
    A = mat_creat(rows, cols, ZERO_MATRIX)
    for r in xrange(rows):
        for c in xrange(cols):
            A[r][c] = Alist[r][c]
            
    return A
    
    
def numpy2cmat(Anp):
    """
    Convert numpy array or matrix to C-Matrix
    
    See Also
    --------
    list2cmat() :  converts nested-list into C-Matrix
    """
    # Check input shape and reshape if smaller than 2-D
    shp = Anp.shape
    if len(shp) < 2:
        # For example, np.array(1.0) or np.array([1.0])
        Anp = Anp.reshape((1,1))
    elif len(shp) > 2:
        # For example, np.zeros((3,3,3))
        print("numpy2cmat(): input must be 2-D (or less).")
        print("\tReturning NaN")
        return np.NaN
    
    return list2cmat(Anp.tolist())

        


if __name__ == "__main__":
    row, col = 5, 8
    print("Example Usage: A(%i,%i)" % (row,col))
    A = mat_creat(row, col, UNIT_MATRIX)
    
    # Print A in Python
    print("\nPrinting using Python:")
    for r in range(MatRow(A)):
        for c in range(MatCol(A)):
            print(A[r][c]),
        print('')
        
    # Print using matrix.c Dump
    print("\nPrint using 'mat_dump':")
    mat_dump(A)



