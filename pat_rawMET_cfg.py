
##____________________________________________________________________________||
from PhysicsTools.PatAlgos.patTemplate_cfg import *

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/MET/TTJets_AODSIM_532_numEvent100.root', 
options.outputFile = 'pat_rawMET.root'
options.maxEvents = -1
options.parseArguments()

##____________________________________________________________________________||
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))
process.MessageLogger.cerr.FwkReport.reportEvery = 10

##____________________________________________________________________________||
process.options.allowUnscheduled = cms.untracked.bool(True)

##____________________________________________________________________________||
process.load("PhysicsTools.PatAlgos.producersLayer1.metProducer_cff")
process.patMETs.metSource  = cms.InputTag("pfMet")

##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
    )

##____________________________________________________________________________||
process.out.fileName = cms.untracked.string(options.outputFile)
process.out.outputCommands = cms.untracked.vstring(
    'drop *',
    'keep patMETs_patMETs__PAT',
    ) 

##____________________________________________________________________________||
