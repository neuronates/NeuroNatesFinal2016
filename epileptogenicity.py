from __future__ import print_function
import scipy
import numpy
import csv
import sys



# high-beta or low-gamma waves
# power spectral density = X(w)X'(w)/2pi
# want PSD(beta,gamma)/PSD(theta,alpha)
# ER = (E_beta + E_gamma)/(E_theta + E_alpha)
# E(w) is estimated with a sliding window of duration D using the periodogram method
# cumulative sum of (ER[n] - avgER[0-n] - pos. bias)
# when this sum minus the local minimum exceeds a threshold, it detects a seizure_autocorrelation
# tells us both the alarm time (threshold exceeded index) and the change-point detection time (local min index)
# two params: threshold lambda and the positive bias term
# bias corresponds to magnitude of changes that should not raise an alarm
# higher lamdba means lower false alarm rate but leads to higher instances of non-detection
# duration used - 6s



def readData(fileName):
    
    # skip the first row assuming it contains column names
    data = numpy.loadtxt(open(fileName,"rb"),delimiter=",",skiprows=0)
    
    return data


def seizure(data, thresh = 0.3, bias = 0.1):
    
    # probably want to initialize by computing the ER for x number of windows, estimate a normal distribution
    # then compute threshold from whatever is statistically significant
    
    #Take some number of initial windows and set threshold to the minimum statistically significant value above the mean modeling the output as a normal distribution
    
    #print(numpy.shape(data))
    fs = 256                    # sampling frequency
    duration = 5                # time duration of the window
    advance = duration * fs     # the number of samples to shift the window forward by
    
    startIndex = 0
    endIndex = advance - 1
    
    thetaLow = 4
    thetaHigh = 7
    alphaLow = 8
    alphaHigh = 12
    
    betaLow = 13
    betaHigh = 24
    gammaLow = 25
    gammaHigh = 97
    
    ER = numpy.array([])
    
    while (endIndex < len(data)):
        
        energySpectrum = numpy.multiply(scipy.fft(data[startIndex:endIndex]), scipy.conj(scipy.fft(data[startIndex:endIndex])))
        energyRatio = sum(energySpectrum[betaLow:gammaHigh]) / sum(energySpectrum[thetaLow:alphaHigh])
        
        numpy.append(ER, energyRatio)
        
        endIndex = endIndex + advance
        startIndex = startIndex + advance
        
    
    U_n = numpy.array([])
    seizureIndex = numpy.array([])
    seizureStart = numpy.array([])
    
    
    
    for i in range(0, len(ER)-1):
        
        numpy.append(U_n, ER[i] - numpy.average(ER[0:i]) - bias)
        
        if(U_n[i] - min(U_n) > thresh):
            seizureIndex = numpy.append(seizureIndex, i)
            seizureStart = numpy.append(seizureStart, numpy.argmin(U_n))
        
    if(len(seizureIndex) == 0 and len(seizureStart) == 0):
        seizureIndex = numpy.array([-1])
        seizureStart = numpy.array([-1])
        
    return (seizureIndex, seizureStart)

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: Seizure Detection Autocorrelation Scoring <input file name> ", file=sys.stderr)
        exit(-1)
        
    data = readData(sys.argv[1])
    (seizureIndex, seizureStart) = seizure(data)
    
    print(seizureIndex)
    print(seizureStart)
    
