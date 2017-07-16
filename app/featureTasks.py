from __future__ import absolute_import
from celery import task

import os, sys, subprocess
from featuresPrediction import features
from Bio import SeqIO

featuresDic={'seqLength':'Length of sequence',
'molecularWeight':'Molecular Weight',
'averageResidueWeight':'Average Residue Weight',
'alanineCount':'Count of alanine',
'cysteineCount':'Count of cysteine',
'asparticAcidCount':'Count of aspartic acid',
'glutamicAcidCount':'Count of glutamic acid',
'phenylalanineCount':'Count of phenylalanine',
'glycineCount':'Count of glycine',
'histidineCount':'Count of histidine',
'isoleucineCount':'Count of isoleucine',
'lysineCount':'Count of lysine',
'leucineCount':'Count of leucine',
'methionineCount':'Count of methionine',
'asparagineCount':'Count of asparagine',
'prolineCount':'Count of proline',
'glutamineCount':'Count of glutamine',
'arginineCount':'Count of arginine',
'serineCount':'Count of serine',
'threonineCount':'Count of threonine',
'valineCount':'Count of valine',
'tryptophanCount':'Count of tryptophan',
'tyrosineCount':'Count of tyrosine',
'tinyMoleCount':'Count of tiny mole',
'smallMoleCount':'Count of small mole',
'alaninePercentage':'Percentage of alanine',
'cysteinePercentage':'Percentage of cysteine',
'asparticAcidPercentage':'Percentage of aspartic acid',
'glutamicAcidPercentage':'Percentage of glutamic acid',
'phenylalaninePercentage':'Percentage of phenylalanine',
'glycinePercentage':'Percentage of glycine',
'histidinePercentage':'Percentage of histidine',
'isoleucinePercentage':'Percentage of isoleucine',
'lysinePercentage':'Percentage of lysine',
'leucinePercentage':'Percentage of leucine',
'methioninePercentage':'Percentage of methionine',
'asparaginePercentage':'Percentage of asparagine',
'prolinePercentage':'Percentage of proline',
'glutaminePercentage':'Percentage of glutamine',
'argininePercentage':'Percentage of arginine',
'serinePercentage':'Percentage of serine',
'threoninePercentage':'Percentage of threonine',
'valinePercentage':'Percentage of valine',
'tryptophanPercentage':'Percentage of tryptophan',
'tyrosinePercentage':'Percentage of tyrosine',
'tinyMolePercentage':'Percentage of tiny mole',
'smallMolePercentage':'Percentage of small mole',
'alanineDayhoffStat':'Dayhoff statistic of alanine',
'cysteineDayhoffStat':'Dayhoff statistic of cysteine',
'asparticAcidDayhoffStat':'Dayhoff statistic of aspartic acid',
'glutamicAcidDayhoffStat':'Dayhoff statistic of glutamic acid',
'phenylalanineDayhoffStat':'Dayhoff statistic of phenylalanine',
'glycineDayhoffStat':'Dayhoff statistic of glycine',
'histidineDayhoffStat':'Dayhoff statistic of histidine',
'isoleucineDayhoffStat':'Dayhoff statistic of isoleucine',
'lysineDayhoffStat':'Dayhoff statistic of lysine',
'leucineDayhoffStat':'Dayhoff statistic of leucine',
'methionineDayhoffStat':'Dayhoff statistic of methionine',
'asparagineDayhoffStat':'Dayhoff statistic of asparagine',
'prolineDayhoffStat':'Dayhoff statistic of proline',
'glutamineDayhoffStat':'Dayhoff statistic of glutamine',
'arginineDayhoffStat':'Dayhoff statistic of arginine',
'serineDayhoffStat':'Dayhoff statistic of serine',
'threonineDayhoffStat':'Dayhoff statistic of threonine',
'valineDayhoffStat':'Dayhoff statistic of valine',
'tryptophanDayhoffStat':'Dayhoff statistic of tryptophan',
'tyrosineDayhoffStat':'Dayhoff statistic of tyrosine',
'carbonCount':'Count of carbon sparing',
'nitrogenCount':'Count of nitrogen sparing',
'sulphurCount':'Count of sulphur sparing',
'oxygenCount':'Count of oxygen sparing',
'hydrogenCount':'Count of hydrogen sparing',
'carbonSparingAverage':'Average carbon sparing',
'nitrogenSparingAverage':'Average nitrogen sparing',
'sulphurSparingAverage':'Average sulphur sparing',
'oxygenSparingAverage':'Average oxygen sparing',
'hydrogenSparingAverage':'Average hydrogen sparing',
'aromaticity':'Aromaticity',
'instabilityIndex':'Instability Index',
'isoelectricPoint':'Isoelectric Point',
'gravy':'Grand average of hydropathy (GRAVY)',
'charge':'Charge',
'molarExtinctionCoefficient':'Molar Extinction Coefficient A280',
'absobance':'Absobance A280',
'probabilityOfExpression':'Probability of Expression Inclusion Bodies',
'aliphaticMoleCount':'Count of aliphatic mole',
'aromaticMoleCount':'Count of aromatic mole',
'polarMoleCount':'Count of polar mole',
'nonPolarMoleCount':'Count of non polar mole',
'chargedMoleCount':'Count of charged mole',
'acidicMoleCount':'Count of acidic mole',
'basicMoleCount':'Count of basic mole',
'aliphaticMolePercentage':'Percentage of aliphatic mole',
'aromaticMolePercentage':'Percentage of aromatic mole',
'polarMolePercentage':'Percentage of polar mole',
'nonPolarMolePercentage':'Percentage of non polar mole',
'chargedMolePercentage':'Percentage of charged mole',
'acidicMolePercentage':'Percentage of acidic mole',
'basicMolePercentage':'Percentage of basic mole',
'helixFraction':'Secondary helix fraction',
'turnFraction':'Secondary turn fraction',
'sheetFraction':'Secondary sheet fraction',
'secondaryHelixCount':'Count of secondary helix',
'secondarySheetCount':'Count of secondary sheet',
'secondaryTurnsCount':'Count of secondary turns',
'secondaryCoilCount':'Count of secondary coil',
'secondaryHelixPercentage':'Percentage of secondary helix',
'secondarySheetPercentage':'Percentage of secondary sheet',
'secondaryTurnsPercentage':'Percentage of secondary turns',
'secondaryCoilPercentage':'Percentage of secondary coil',
'cMannosylation':'C-mannosylation sites',
'proteasomalCleavage':'Proteasomal cleavages (MHC ligands)',
'nLinkedGlycosylation':'N-linked glycosylation sites',
'genericPhosphorylationSerine':'Generic phosphorylation sites of serine',
'genericPhosphorylationThreonine':'Generic phosphorylation sites of threonine',
'genericPhosphorylationTyrosine':'Generic phosphorylation sites of tyrosine',
'arginineLysinePropeptideCleavage':'Arginine and lysine propeptide cleavage sites',
'bindingRegionsDisordered':'Binding Regions in Disordered Proteins',
'mTP':'Mitochondrial targeting peptide (mTP)',
'sP':'Secretory pathway signal peptide (SP)',
'otherLocation':'Other subcellular location',
'transmembraneHelices':'Count of transmembrane helices',
'signalPeptides':'Presence of signal peptides',
'linearBcellEpitopes':'Count of linear B-cell epitopes',
'classIimmunogenicity':'Class I Immunogenicity score'}



#---------------------FEATURES PREDICTION BACKGROUND TASK------------------
@task
def run_features(filename, feature_email, features_list, task_id):
    records=SeqIO.parse(filename, "fasta")
    featuresOutFile=open(filename+"_features.csv", "w")
    featuresOutFile.write('Sequence ID,')
    for feature in features_list[:-1]:
        featuresOutFile.write(featuresDic[str(feature)]+",")
    featuresOutFile.write(featuresDic[str(features_list[-1])])
    featuresOutFile.write('\n')
        
    for record in records:
        featuresOutFile.write(record.id+","+features(record.id, str(record.seq), features_list)+"\n")

    featuresOutFile.close()
    records.close()


    #--------------------EMAIL SENDING--------------------------------------

    if feature_email!="":
        command = "echo 'Your SchistoTarget Features Prediction Result is ready.\n\n"+\
                  "Kind regards,\n\nLutz Krause & Shihab Hasan\nComputational Medical Genomics Group, The University of Queensland Diamantina Institute' | mutt -a "+filename+"'_features.csv' -s 'SchistoTarget Features Prediction Result' -- "+feature_email

        subprocess.call(command, shell=(sys.platform != "Linux"))

    featureFile = open(filename+"_features.csv",'r')
    allLines=featureFile.readlines()
    fh, fd = allLines[:1], allLines[1:] 
    featureFile.close()
    os.remove(filename)
    os.remove(filename+"_features.csv")
    
    return (fh, fd)
