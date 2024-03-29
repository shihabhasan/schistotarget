from __future__ import absolute_import
from celery import task

import os, sys, subprocess
import hashlib
from featuresMoreConservative import features
from duplicate_seq_remover import duplicate_seq_remover
from Bio import SeqIO
from StringIO import StringIO
from datetime import datetime
import json
import numpy as np
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.neighbors import NearestCentroid
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis  
from sklearn.linear_model import RidgeClassifier, SGDClassifier, Perceptron, PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neural_network import MLPClassifier

from app.models import ImmunoMoreConservative

featuresDic={
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
'alaninePercentage':'Percentage of tiny mole',
'cysteinePercentage':'Percentage of small mole',
'asparticAcidPercentage':'Percentage of alanine',
'glutamicAcidPercentage':'Percentage of cysteine',
'phenylalaninePercentage':'Percentage of aspartic acid',
'glycinePercentage':'Percentage of glutamic acid',
'histidinePercentage':'Percentage of phenylalanine',
'isoleucinePercentage':'Percentage of glycine',
'lysinePercentage':'Percentage of histidine',
'leucinePercentage':'Percentage of isoleucine',
'methioninePercentage':'Percentage of lysine',
'asparaginePercentage':'Percentage of leucine',
'prolinePercentage':'Percentage of methionine',
'glutaminePercentage':'Percentage of asparagine',
'argininePercentage':'Percentage of proline',
'serinePercentage':'Percentage of glutamine',
'threoninePercentage':'Percentage of arginine',
'valinePercentage':'Percentage of serine',
'tryptophanPercentage':'Percentage of threonine',
'tyrosinePercentage':'Percentage of valine',
'tinyMolePercentage':'Percentage of tryptophan',
'smallMolePercentage':'Percentage of tyrosine',
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
'classIimmunogenicity':'Class I Immunogenicity score'
}



#---------------------immuno MORE CONSERVATIVE-----------------

def run_immuno_more_conservative(filename, input_email, feature_mode, task_id):
    parameter=""
    test_features=""
    test_para=""
    seqID_list=[]
    result_dict={}
    result_file=open(filename+"_result.csv", 'w')
    result_file.write("Sequence_ID,Gaussian Naive Bayes Prediction,Gaussian Naive Bayes Probability,\
    BernoulliNB Prediction,BernoulliNB Probability\n")

    featureList = [
        'glutamicAcidDayhoffStat',
        'isoelectricPoint',
        'glutamicAcidPercentage',
        'sheetFraction',
        'secondaryTurnsPercentage',
        'acidicMolePercentage',
        'cysteineDayhoffStat',
        'cysteinePercentage',
        'secondaryHelixPercentage',
        'otherLocation',
        'secondarySheetPercentage',
        'alanineDayhoffStat',
        'alaninePercentage',
        'isoleucinePercentage',
        'isoleucineDayhoffStat',
        'probabilityOfExpression',
        'transmembraneHelices',
        'phenylalaninePercentage',
        'phenylalanineDayhoffStat',
        'asparagineDayhoffStat',
        'asparaginePercentage',
        'aromaticMolePercentage'
    ]

    bimerList = [
        'EA',
        'QW',
        'GE',
        'IF',
        'CI',
        'FI',
        'ML',
        'EV',
        'VC',
        'DA',
        'LN',
        'SI',
        'CN',
        'ES',
        'TM',
        'LD',
        'PV',
        'RP',
        'AR',
        'CK',
        'YN',
        'NA',
        'IP',
        'AE',
        'LE',
        'DT',
        'NN',
        'VY',
        'CV',
        'HD',
        'TL',
        'MH',
        'TF',
        'HM',
        'RE',
        'DN',
        'WT',
        'GD',
        'EE',
        'KQ',
        'KH',
        'VE',
        'EG',
        'IY',
        'FD'
    ]

    bimerIDs = ','.join(map(str, bimerList))


    records=SeqIO.parse(filename, "fasta")
    for record in records:
        hash_sequence=hashlib.md5(str(record.seq)).hexdigest()
        data=ImmunoMoreConservative.objects.filter(sequence=hash_sequence)
        if len(data)==0:
            run_para=features(record.id, str(record.seq), featureList, bimerList)
            parameter=parameter+run_para+"\n"
            seqID_list.append(record.id)
            test_features=test_features+run_para+"\n"
            test_para=test_para+record.id+","+run_para+"\n"
        else:
            for p in data:
                p.access=p.access+1
                p.time=datetime.now()
                p.save()
                test_features=test_features+p.features+"\n"
                test_para=test_para+record.id+","+p.features+"\n"
                result_dict[str(record.id)]=p.prediction
    records.close()
    
   #---------------------WORKING WITH SCIKIT-LEARN------------
    if parameter!="":
        parameters=StringIO(parameter)
        train_positive_file="immuno_positive_more_conservative.csv"
        train_negative_file="immuno_negative_more_conservative.csv"
        train_positive=np.genfromtxt(train_positive_file, delimiter=",")[1:,1:]
        train_negative=np.genfromtxt(train_negative_file, delimiter=",")[1:,1:]
        
        train_data=np.concatenate((train_positive,train_negative))
        train_label=np.concatenate((np.ones(len(train_positive)), np.zeros(len(train_negative))))
        test_data=np.genfromtxt(parameters, delimiter=",")
        
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
        
        train_data_scaled = min_max_scaler.fit(train_data).transform(train_data)

        test_data_scaled = min_max_scaler.fit(train_data).transform(test_data)
        
        #-------------------------------------------------------------
        duplicate_seq_remover(filename)
        fasta_rec=SeqIO.index(filename+"_nodups", "fasta")
        param=parameter.split("\n")
        #-------------------------------------------------------------
        
        gaussianNB={}
        bernoulliNB={}

        names = [gaussianNB, bernoulliNB]

        k=int(round(np.sqrt(len(train_data)/2.0)))

        classifiers = [
            GaussianNB(),
            BernoulliNB()]

        
        #-------------------------------------------------------------
        for name, clf in zip(names, classifiers):
            clf.fit(train_data_scaled, train_label)
            test_predicted = clf.predict(test_data_scaled)
            if hasattr(clf, "decision_function"):
                decisions = clf.decision_function(test_data_scaled)
                
            if hasattr(clf, "predict_proba"):
                probabilities = clf.predict_proba(test_data_scaled)


        #-----------------
            i=0
            for pred in test_predicted:
                if hasattr(clf, "decision_function"):
                    decision = str(decisions[i]).replace("[", "").replace("]", "")
                else:
                    decision = 'NA'
                if hasattr(clf, "predict_proba"):
                    probability = probabilities[:, 1][i]
                else:
                    probability = 'NA'
                if pred == 1.0:
                    pred = 'Immunoreactive Protein'
                if pred == 0.0:
                    pred = 'Non-Immunoreactive Protein'

                if probability == 'NA':
                    if decision == 'NA':
                        name[seqID_list[i]] = pred + "," + probability
                    else:
                        name[seqID_list[i]] = pred + "," + str(round(float(decision), 4)) + "," + probability
                else:
                    if decision == 'NA':
                        if probability > 0.5:
                            name[seqID_list[i]] = pred + "," + str(round(probability, 4))
                        else:
                            name[seqID_list[i]] = pred + "," + str(round(1 - probability, 4))
                    else:
                        if probability > 0.5:
                            name[seqID_list[i]] = pred + "," + str(round(float(decision), 4)) + "," + str(
                                round(probability, 4))
                        else:
                            name[seqID_list[i]] = pred + "," + str(round(float(decision), 4)) + "," + str(
                                round(1 - probability, 4))

                i = i + 1
        #-----------------
        j=0
        for seqID in seqID_list:
            result_dict[seqID]=gaussianNB[seqID]+"\t"+bernoulliNB[seqID]
            p=ImmunoMoreConservative(sequence=hashlib.md5(str(fasta_rec[seqID].seq)).hexdigest(), prediction=result_dict[seqID], features=str(param[j]), access=0, time=datetime.now())
            p.save()
            j=j+1

        fasta_rec.close()
        os.remove(filename+"_nodups")


    #--------------------PLOT--------------------------------------

    train_positive_file="immuno_positive_more_conservative.csv"
    train_negative_file="immuno_negative_more_conservative.csv"
    train_positive=np.genfromtxt(train_positive_file, delimiter=",")[1:,1:]
    train_negative=np.genfromtxt(train_negative_file, delimiter=",")[1:,1:]
    test_feat=StringIO(test_features)
    test_parameters=np.genfromtxt(test_feat, delimiter=",")
    train_data=np.concatenate((train_positive,train_negative))
    
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    
    train_positive_scaled = min_max_scaler.fit(train_data).transform(train_positive)
    train_negative_scaled = min_max_scaler.fit(train_data).transform(train_negative)
    test_parameters_scaled = min_max_scaler.fit(train_data).transform(test_parameters)

    x1=np.mean(train_positive_scaled, axis=0).tolist()
    x2=np.mean(train_negative_scaled, axis=0).tolist()
    x3={}
    duplicate_seq_remover(filename)
    records=SeqIO.parse(filename + "_nodups", "fasta")
    if test_parameters_scaled.ndim==1:
        for record in records:
            x3[record.id]=test_parameters_scaled.tolist()
            result_file.write(record.id+","+result_dict[record.id].replace("\t",",")+"\n")
    else:
        j=0
        for record in records:
            x3[record.id]=test_parameters_scaled[j].tolist()
            result_file.write(record.id+","+result_dict[record.id].replace("\t",",")+"\n")
            j=j+1
    result_file.close()
    records.close()


    #--------------------EMAIL SENDING--------------------------------------
    prediction_file=open(filename+"_prediction.csv", 'w')
    prediction_file.write("Sequence_ID,Prediction,Score \n")
    f = open(filename+"_result.csv",'r')
    all_lines=f.readlines()
    header, lines = all_lines[:1], all_lines[1:]
    duplicate_seq_remover(filename)
    fasta_record = SeqIO.index(filename + "_nodups", "fasta")
    for line in lines:
        prediction_count=line.count('Non-Immunoreactive Protein')
        l=line.split(",")
        if prediction_count>0:
            if len(str(fasta_record[l[0]].seq))<20:
                predicted = l[0] + ',Too short sequence,Unable to predict'
            else:
                predicted=l[0]+',Non-Immunoreactive Protein,'+str(2-prediction_count)+" / 2"
        else:
            if len(str(fasta_record[l[0]].seq))<20:
                predicted = l[0] + ',Too short sequence,Unable to predict'
            else:
                predicted=l[0]+',Immunoreactive Protein,'+str(2-prediction_count)+" / 2"
        prediction_file.write(predicted+"\n")
    f.close()
    fasta_record.close()
    os.remove(filename + "_nodups")
    prediction_file.close()
    f1=open(filename+"_features.csv",'w')
    f1.write('Sequence ID')
    ids=[]
    for feature in featureList:
        f1.write("," + featuresDic[feature])
        ids.append(featuresDic[feature])
    json_ids = json.dumps(ids)
    feature_cutoff = len(ids)
    f1.write("," + bimerIDs)
    f1.write("\n"+test_para)
    f1.close()


    if input_email!="":
        command = "echo 'Your SchistoTarget immunoreactive protein prediction result is ready for job ID: "+task_id+"\n\n"+\
                "You can view the interactive tables and plots by the link: http://schistotarget.bioapps.org/immuno_results/"+task_id+"\n\n\n"+\
                "Kind regards,\n\nLutz Krause & Shihab Hasan\nComputational Medical Genomics Group, The University of Queensland Diamantina Institute' | mutt -a "+filename+"'_prediction.csv' -a "+filename+"'_result.csv' -a "+filename+"'_features.csv' -s 'SchistoTarget Immunoreactivity Protein Prediction Result for job ID '"+task_id+" -- "+input_email
        subprocess.call(command, shell=(sys.platform!="Linux"))


    f2 = open(filename+"_features.csv",'r')
    allLines=f2.readlines()
    fh, fd = allLines[:1], allLines[1:] 
    f2.close()
    f1.close()
    
    f3=open(filename+"_prediction.csv", 'r')
    prediction_lines=f3.readlines()[1:] 
    f3.close()
    os.remove(filename)
    os.remove(filename+"_prediction.csv")
    os.remove(filename+"_result.csv")
    os.remove(filename+"_features.csv")
    feature_mode = "More Conservative"
    return (prediction_lines, header, lines, x1, x2, x3, fh, fd, feature_mode, json_ids, feature_cutoff)