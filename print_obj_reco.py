#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
# $Id$
import ROOT
import sys
import math
from optparse import OptionParser

ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputPath', default = '/afs/cern.ch/cms/Tutorials/TWIKI_DATA/MET/TTJets_AODSIM_524_numEvent100.root', action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():

    files = [inputPath]

    events = Events(files)

    handleMETs = Handle("std::vector<reco::PFMET>") 

    print "    run       lumi      event        mex        mey        met        phi"

    for event in events:

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

        print '%7d %10d %10d' % (run, lumi, eventId),
        event.getByLabel(("pfMet", '', 'RECO'), handleMETs)
        met = handleMETs.product().front()

        print '%10.3f' % met.px(),
        print '%10.3f' % met.py(),
        print '%10.3f' % met.pt(),
        print '%10.2f' % (met.phi()/math.pi*180.0),
        print

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
