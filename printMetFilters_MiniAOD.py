#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
import sys
import math
import signal
from optparse import OptionParser

ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
GLOBAL_LAST = False

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputPath', default = '/afs/cern.ch/cms/Tutorials/TWIKI_DATA/MET/TTJets_AODSIM_532_numEvent100.root', action = 'store', type = 'string')
parser.add_option("-n", "--nevents", action = "store", default = -1, type = 'long', help = "maximum number of events to process")
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():

    printHeader()
    if getNEvents(inputPath):
        counts = count(inputPath)
        printCounts(counts)

##____________________________________________________________________________||
def count(inputPath):

    signal.signal(signal.SIGINT, handler)

    files = [inputPath]
    events = Events(files, maxEvents = options.nevents)

    handleTriggerResults = Handle("edm::TriggerResults")

    counts = { }
    for event in events:

        if GLOBAL_LAST: break

        event.getByLabel(('TriggerResults', '', 'PAT'), handleTriggerResults)
        triggerResults = handleTriggerResults.product()
        triggerNames = event._event.triggerNames(triggerResults)
        for triggerName in triggerNames.triggerNames():
            if not triggerResults.accept(triggerNames.triggerIndex(triggerName)): continue
            key = (triggerName, )
            if key not in counts: counts[key] = 0
            counts[key] += 1

    return counts

##____________________________________________________________________________||
def printHeader():
    print '%40s' % 'filter',
    print '%5s' % 'n',
    print

##____________________________________________________________________________||
def printCounts(counts):
    keys = counts.keys()
    keys.sort()
    # colSize = max([len(k[0]) for k in keys])
    for k in keys:
        print '%40s' % k[0],
        print '%5d'  % counts[k],
        print

##____________________________________________________________________________||
def getNEvents(inputPath):
    file = ROOT.TFile.Open(inputPath)
    events = file.Get('Events')
    return events.GetEntries()

##____________________________________________________________________________||
def handler( signum, frame ):
    global GLOBAL_LAST
    GLOBAL_LAST = True

##____________________________________________________________________________||
def loadLibraries():
    argv_org = list(sys.argv)
    sys.argv = [e for e in sys.argv if e != '-h']
    ROOT.gSystem.Load("libFWCoreFWLite")
    ROOT.AutoLibraryLoader.enable()
    ROOT.gSystem.Load("libDataFormatsFWLite")
    ROOT.gSystem.Load("libDataFormatsPatCandidates")
    sys.argv = argv_org

##____________________________________________________________________________||
loadLibraries()
from DataFormats.FWLite import Events, Handle

##____________________________________________________________________________||
if __name__ == '__main__':
    main()
