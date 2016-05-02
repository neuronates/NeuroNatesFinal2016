#!usr/bin/python

from __future__ import print_function
#import scipy.signal
#from scipy import *
#from scipy import signal
#import scipy.signal
import scipy
import numpy
import sys

def _boolrelextrema(data, comparator,
                  axis=0, order=1, mode='clip'):
    """
    Calculate the relative extrema of `data`.

    Relative extrema are calculated by finding locations where
    comparator(data[n],data[n+1:n+order+1]) = True.

    Parameters
    ----------
    data: ndarray
    comparator: function
        function to use to compare two data points.
        Should take 2 numbers as arguments
    axis: int, optional
        axis over which to select from `data`
    order: int, optional
        How many points on each side to require
        a `comparator`(n,n+x) = True.
    mode: string, optional
        How the edges of the vector are treated.
        'wrap' (wrap around) or 'clip' (treat overflow
        as the same as the last (or first) element).
        Default 'clip'. See numpy.take

    Returns
    -------
    extrema: ndarray
        Indices of the extrema, as boolean array
        of same shape as data. True for an extrema,
        False else.

    See also
    --------
    argrelmax,argrelmin

    Examples
    --------
    >>> testdata = numpy.array([1,2,3,2,1])
    >>> argrelextrema(testdata, numpy.greater, axis=0)
    array([False, False,  True, False, False], dtype=bool)
    """

    if((int(order) != order) or (order < 1)):
        raise ValueError('Order must be an int >= 1')

    datalen = data.shape[axis]
    locs = numpy.arange(0, datalen)

    results = numpy.ones(data.shape, dtype=bool)
    main = data.take(locs, axis=axis, mode=mode)
    for shift in xrange(1, order + 1):
        plus = data.take(locs + shift, axis=axis, mode=mode)
        minus = data.take(locs - shift, axis=axis, mode=mode)
        results &= comparator(main, plus)
        results &= comparator(main, minus)
        if(~results.any()):
            return results
    return results

def argrelmax(data, axis=0, order=1, mode='clip'):
    """
    Calculate the relative maxima of `data`.

    See also
    --------
    argrelextrema,argrelmin
    """
    return argrelextrema(data, numpy.greater, axis, order, mode)


def argrelextrema(data, comparator,
                  axis=0, order=1, mode='clip'):
    """
    Calculate the relative extrema of `data`

    Returns
    -------
    extrema: ndarray
        Indices of the extrema, as an array
        of integers (same format as argmin, argmax

    See also
    --------
    argrelmin, argrelmax

    """
    results = _boolrelextrema(data, comparator,
                              axis, order, mode)
    if ~results.any():
        return (numpy.array([]),) * 2
    else:
        return numpy.where(results)



def readData(fileName):
    
    # skip the first row assuming it contains column names
    data = numpy.loadtxt(open(fileName,"rb"),delimiter=",",skiprows=0)
    
    return data



def score(vec):
   
    vec[numpy.where(vec >= 0.400)] = -10
    vec[numpy.where(vec >= 0.300)] = -9
    vec[numpy.where(vec >= 0.200)] = -8
    vec[numpy.where(vec >= 0.175)] = -7
    vec[numpy.where(vec >= 0.150)] = -6
    vec[numpy.where(vec >= 0.125)] = -5
    vec[numpy.where(vec >= 0.100)] = -4
    vec[numpy.where(vec >= 0.075)] = -3
    vec[numpy.where(vec >= 0.050)] = -2
    vec[numpy.where(vec >= 0.025)] = -1
    vec[numpy.where(vec >= 0)] = -0
    vec = vec + 5
    
    return vec


def removeNoisyData(locs, data):
    
    flag = -1
    
    while (flag != 0):
        flag = 0
        
        for i in range(0, len(locs)-2):
            
            if (data[locs[i]].all() < 0):
                flag = -1
                locs[i] = numpy.array([])
                break
            
            if (len(numpy.where(data[locs[i]:locs[i+1]] < 0)[0])):
                flag = 1
                
                if (data[locs[i]] < data[locs[i+1]]):
                    locs[i] = numpy.array([])
                else:
                    locs[i+1] = numpy.array([])
                break
            
            if(not numpy.array_equal(locs[i], numpy.array([1])) and not numpy.array_equal(locs[i], numpy.array([len(data)-1]))):
                if(sum(data[locs[i]-1:locs[i]+1]).all() < 0):
                    locs[i] = numpy.array([])
                    flag = 1
                    break
    
    return locs


def seizure(data):
    
    # assume all traces lie in columns 
    fs = 256
    seiz = 0
    # compute autocorrelation of data
    adata = scipy.ifft(numpy.multiply(scipy.fft(data), scipy.conj(scipy.fft(data))))
    finalScore = numpy.zeros(len(adata))
    
    for i in range(0, len(adata)-1):
        
        maxIndices = argrelmax(data[0:i])
        length = numpy.shape(maxIndices)[1]
        
        maxIndices = numpy.append([1], maxIndices)   # pads with the first and last indices
        maxIndices = numpy.append(maxIndices, [256*6])
        corrSum = numpy.zeros(length)
        
        maxIndices = removeNoisyData(maxIndices, adata)
        
        
        # only one peak, the signal is not periodic
        if (length < 2):
            seiz = 0
            return seiz
        
        
        for k in range(1, length-2):
            
            # the following lines should have a find < 0 instead of > 0, however,
            # there are 0 values that fit that are found when that is the case...
            #timeOne = maxIndices[k] + 1 - numpy.where(numpy.flipud(adata[maxIndices[k-1]:maxIndices[k]]) > 0)[0][0]       #       find(flipud(adata(locs(k-1):locs(k)))<0,1);
            #timeTwo = maxIndices[k] - 1 + numpy.where(adata[maxIndices[k]:maxIndices[k+1]] > 0)[0][0]

            #tempSum = numpy.cumsum(1/fs*adata[timeTwo:timeOne])  
            #corrSum[k] = 1/fs*(timeTwo - 1 + (tempSum > tempSum[-1]/2))[0];
            
            
            d1 = numpy.where(numpy.flipud(adata[maxIndices[k-1]:maxIndices[k]]) < 0)
            d2 = numpy.where(adata[maxIndices[k]:maxIndices[k+1]] < 0)
            
            if(len(d1) == 0):
                d1 = numpy.array([0])
                
            if(len(d2) == 0):
                d2 = numpy.array([0])
            
            timeOne = maxIndices[k] + 1 -d1
            timeTwo = maxIndices[k] - 1 + d2
            
            tempSum = numpy.cumsum(1/fs*adata[timeOne,timeTwo])  
            
            # added this in to avoid index out of bounds exception when finding the peak
            if(len(tempSum) == 0):
                corrSum[k] = 0
                break
            
            peak = numpy.where(tempSum > tempSum[-1]/2)
            
            if(len(numpy.where(tempSum > peak[0]))):
                corrSum[k] = 0
                break
            
            corrSum[k] = 1/fs*(timeTwo - 1 + peak[0]);
            
            # What is the purpose of this break?
            if k > 4:
                break
        
        
        corrSum[numpy.where(corrSum == 0)] = numpy.array([])
        
        if(filter(lambda x: x == 0, corrSum)):
            return seiz
        
        
        corrSum = corrSum[1:-1]/corrSum[0];
        corrSum = numpy.abs(numpy.round(corrSum) - corrSum)
        results = score(corrSum) 
        finalScore[i] = numpy.sum(results) 
    
    seiz = sum(finalScore >= 12) > 0;
    return seiz


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: Seizure Detection Autocorrelation Scoring <input file name>", file=sys.stderr)
        exit(-1)
        
    data = readData(sys.argv[1])
    
    finalScore = seizure(data)
    print(finalScore)
    
