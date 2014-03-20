import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')

# add a list of strings for events to process
options.register ('eventsToProcess',
				  '',
				  VarParsing.multiplicity.list,
				  VarParsing.varType.string,
				  "Events to process")
options.register ('maxSize',
				  0,
				  VarParsing.multiplicity.singleton,
				  VarParsing.varType.int,
				  "Maximum (suggested) file size (in Kb)")

options.register ('certFile',
                               '',
                               VarParsing.multiplicity.singleton,
                               VarParsing.varType.string,
                               "json file")

options.register ('triggerConditions',
                  '',
                  VarParsing.multiplicity.list,
                  VarParsing.varType.string,
                  "Trigger Condition")


options.parseArguments()

process = cms.Process("PickEvent")
process.source = cms.Source ("PoolSource",
	  fileNames = cms.untracked.vstring (options.inputFiles),
)

if options.eventsToProcess:
    process.source.eventsToProcess = \
           cms.untracked.VEventRange (options.eventsToProcess)


if options.certFile:
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = options.certFile).getVLuminosityBlockRange()

process.maxEvents = cms.untracked.PSet(
	    input = cms.untracked.int32 (options.maxEvents)
)


process.Out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string (options.outputFile)
)

if options.maxSize:
    process.Out.maxSize = cms.untracked.int32 (options.maxSize)

if options.triggerConditions:
    process.load('HLTrigger.HLTfilters.triggerResultsFilter_cfi')
    process.triggerResultsFilter.l1tResults = cms.InputTag('')
    process.triggerResultsFilter.hltResults = cms.InputTag('TriggerResults::HLT')
    process.triggerResultsFilter.triggerConditions = (options.triggerConditions)
    process.p = cms.Path(process.triggerResultsFilter)
    process.Out.SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p'))
    process.load("FWCore.MessageLogger.MessageLogger_cfi")
    process.MessageLogger.cerr.FwkReport.reportEvery = 100
    process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

process.end = cms.EndPath(process.Out)
