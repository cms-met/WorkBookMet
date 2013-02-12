# $Id: obj_pat_cfg.py,v 1.2 2013/02/08 21:36:16 sakuma Exp $

##____________________________________________________________________________||
import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
process = cms.Process("FILT")

##____________________________________________________________________________||
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.Geometry.GeometryIdeal_cff")

process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

##____________________________________________________________________________||
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string("FT_R_53_V21::All")

##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        'file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/MET/MET_Run2012C_AOD_532_numEvent100.root'
        )
    )

##____________________________________________________________________________||
process.load("RecoMET.METFilters.metFilters_cff")

process.p = cms.Path(
    process.metFilters
)

##____________________________________________________________________________||
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('filtered.root'),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p'))
    )

process.outpath = cms.EndPath(process.out)

##____________________________________________________________________________||
