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
parser.add_option('-i', '--inputPath', default = 'extMet.root', action = 'store', type = 'string')
parser.add_option("-n", "--nevents", action = "store", default = -1, type = 'long', help = "maximum number of events to process")
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():

    printHeader()
    if getNEvents(inputPath):
        count(inputPath)

##____________________________________________________________________________||
def printHeader():
    print '%6s'  % 'run',
    print '%10s' % 'lumi',
    print '%9s'  % 'event',
    print '%5s'  % 'nPU',
    print '%5s'  % 'nVtx',
    print '%10s' % 'S',
    print '%10s' % 'pfMetT1',
    print '%10s' % 'genMet',
    print

##____________________________________________________________________________||
def count(inputPath):

    signal.signal(signal.SIGINT, handler)

    files = [inputPath]
    events = Events(files, maxEvents = options.nevents)

    handlePatMETs = Handle("std::vector<pat::MET>")
    handleVertices = Handle("std::vector<reco::Vertex>")
    handlePUSummaries = Handle("std::vector<PileupSummaryInfo>")

    handlePFMETs = Handle("std::vector<reco::PFMET>")

    handleDouble = Handle("double")

    for event in events:

        if GLOBAL_LAST: break

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

        # obtain the number of the mixed in-time pile-up interactions (MC only)
        # (https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchool2014PileupReweighting)
        event.getByLabel(("addPileupInfo", "", "HLT"), handlePUSummaries)
        puSummaries = handlePUSummaries.product()
        nInTimePileUp = puSummaries[[s.getBunchCrossing() for s in puSummaries].index(0)].getPU_NumInteractions()

        # obtain the number of the reconstructed primary vertices
        event.getByLabel(("offlineSlimmedPrimaryVertices", "", "PAT"), handleVertices)
        vertices = handleVertices.product()
        nVertices = vertices.size()

        # get "slimmedMETs"
        event.getByLabel(("slimmedMETs", "", "PAT"), handlePatMETs)
        slimmedMET = handlePatMETs.product().front()
        genMET = slimmedMET.genMET()

        # get "METSignificance"
        event.getByLabel(("METSignificance", "METSignificance", "EXTMET"), handleDouble)
        metSig = handleDouble.product()[0]

        print '%6d %10d %9d %5d %5d' % (run, lumi, eventId, nInTimePileUp, nVertices),
        print '%10.3f' % metSig,
        print '%10.3f' % slimmedMET.pt(),
        print '%10.3f' % genMET.pt(),
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
