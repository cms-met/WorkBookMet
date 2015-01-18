import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:/data/shared/Short_Exercise_MET/TTJets_MINIAODSIM_PHYS14_numEvent5000.root',
options.outputFile = 'extMet.root'
options.maxEvents = -1
options.parseArguments()

##____________________________________________________________________________||
process = cms.Process('EXTMET')

##____________________________________________________________________________||
process.load('FWCore.MessageService.MessageLogger_cfi')

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

##____________________________________________________________________________||
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup', '')

##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
    )

##____________________________________________________________________________||
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
    outputCommands = cms.untracked.vstring(
        'drop *',
        "keep PileupSummaryInfos_addPileupInfo__HLT",
        "keep edmTriggerResults_TriggerResults__PAT",
        "keep recoVertexs_offlineSlimmedPrimaryVertices__PAT",
        "keep patMETs_slimmedMETs__PAT",
        "keep recoPFMETs_pfMVAMEt__*",
        "keep double_METSignificance_*_*",
        )
    )

##____________________________________________________________________________||
process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True)
    )
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

##____________________________________________________________________________||
process.load("RecoJets.JetProducers.ak4PFJets_cfi")
process.ak4PFJets.src = cms.InputTag("packedPFCandidates")
from JetMETCorrections.Configuration.DefaultJEC_cff import ak4PFJetsL1FastL2L3
process.load("RecoMET.METPUSubtraction.mvaPFMET_cff")
process.pfMVAMEt.srcPFCandidates = cms.InputTag("packedPFCandidates")
process.pfMVAMEt.srcVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.puJetIdForPFMVAMEt.jec =  cms.string('AK4PF')
process.puJetIdForPFMVAMEt.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
process.puJetIdForPFMVAMEt.rho = cms.InputTag("fixedGridRhoFastjetAll")

##____________________________________________________________________________||
process.load("RecoMET/METProducers.METSignificance_cfi")
process.load("RecoMET/METProducers.METSignificanceParams_cfi")

##____________________________________________________________________________||
process.e1 = cms.EndPath(process.out)

##____________________________________________________________________________||
