import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:/eos/uscms/store/user/cmsdas/2014/MET/TTJets_AODSIM_532_numEvent100.root',
options.outputFile = 'corrMet.root'
options.maxEvents = -1
options.parseArguments()

##____________________________________________________________________________||
process = cms.Process("CORR")

##____________________________________________________________________________||
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.load("Configuration.Geometry.GeometryIdeal_cff")
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
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep recoGenMETs_*_*_*',
        'keep recoCaloMETs_*_*_*',
        'keep recoPFMETs_*_*_*',
        'keep *_*_*_CORR'
        )
    )

##____________________________________________________________________________||
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.correctionTermsCaloMet_cff")

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff")

process.corrPfMetType1.jetCorrLabel = cms.string("ak5PFL1FastL2L3")
# process.corrPfMetType1.jetCorrLabel = cms.string("ak5PFL1FastL2L3Residual")

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0PFCandidate_cff")

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0RecoTrack_cff")

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetShiftXY_cff")

process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_mc
# process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_data

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.correctedMet_cff")

##____________________________________________________________________________||
process.p = cms.Path(
    process.correctionTermsPfMetType1Type2 +
    process.correctionTermsPfMetType0RecoTrack +
    process.correctionTermsPfMetType0PFCandidate +
    process.correctionTermsPfMetShiftXY +
    process.correctionTermsCaloMet +
    process.caloMetT1 + 
    process.caloMetT1T2 + 
    process.pfMetT0rt +
    process.pfMetT0rtT1 +
    process.pfMetT0pc +
    process.pfMetT0pcT1 +
    process.pfMetT0rtTxy +
    process.pfMetT0rtT1Txy +
    process.pfMetT0pcTxy +
    process.pfMetT0pcT1Txy +
    process.pfMetT1 +
    process.pfMetT1Txy
)

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
