from __future__ import absolute_import
from celery import task

import os, sys, subprocess
import time
import sqlite3
import hashlib
sys.path.append('/home/shihab/protcat/scripts')
from features import features
from duplicate_seq_remover import duplicate_seq_remover
from Bio import SeqIO
from StringIO import StringIO
import numpy as np
from sklearn import svm, preprocessing
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
from datetime import datetime


idx="Sequence ID, Toal length of the proetin sequence, Percentage of alanine, Percentage of cysteine, Percentage of aspartic acid, \
     Percentage of glutamic acid, Percentage of phenylalanine, Percentage of glycine, Percentage of histidine, Percentage of isoleucine, \
     Percentage of lysine, Percentage of leucine, Percentage of methionine, Percentage of asparagine, Percentage of proline, \
     Percentage of glutamine, Percentage of arginine, Percentage of serine, Percentage of threonine, Percentage of valine, \
     Percentage of tryptophan, Percentage of tyrosine, Molecular Weight, Aromaticity, Instability Index, Isoelectric Point, \
     Grand average of hydropathy (GRAVY), Helix, Turn, Sheet, Average Residue Weight, Charge, Molar Extinction Coefficient A280, \
     Absobance A280, Probability of Expression Inclusion Bodies, DayhoffStat of alanine, DayhoffStat of cysteine, DayhoffStat of aspartic acid, \
     DayhoffStat of glutamic acid, DayhoffStat of phenylalanine, DayhoffStat of glycine, DayhoffStat of histidine, DayhoffStat of isoleucine, \
     DayhoffStat of lysine, DayhoffStat of leucine, DayhoffStat of methionine, DayhoffStat of asparagine, DayhoffStat of proline, DayhoffStat of glutamine, \
     DayhoffStat of arginine, DayhoffStat of serine, DayhoffStat of threonine, DayhoffStat of valine, DayhoffStat of tryptophan, DayhoffStat of tyrosine, \
     Percentage of tiny mole, Percentage of small mole, Percentage of aliphatic mole, Percentage of aromatic mole , Percentage of polar mole, \
     Percentage of non polar mole, Percentage of charged mole, Percentage of acidic mole, Percentage of basic mole, Percentage of secondary helix, \
     Percentage of secondary sheet, Percentage of secondary turns, Percentage of secondary coil, C-mannosylation sites, Proteasomal cleavages (MHC ligands), \
     N-linked glycosylation sites, Generic phosphorylation sites of serine, Generic phosphorylation sites of threonine, Generic phosphorylation sites of tyrosine, \
     Transmembrane helices in proteins, Arginine and lysine propeptide cleavage sites, Signal peptide cleavage sites"	



#---------------------PROTCAT BACKGROUND TASK------------------
@task
def run_predict(cat1_filename, cat2_filename, test_filename, email):
    train_para_1=""
    train_para_2=""
    test_para=""
    test_features=""

    cat1_records=SeqIO.parse(cat1_filename, "fasta")
    for cat1_record in cat1_records:
        train_para_1=train_para_1+features(cat1_record.id, str(cat1_record.seq))+"\n"

    cat2_records=SeqIO.parse(cat2_filename, "fasta")
    for cat2_record in cat2_records:
        train_para_2=train_para_2+features(cat2_record.id, str(cat2_record.seq))+"\n"

    test_records=SeqIO.parse(test_filename, "fasta")
    
    seqID_list=[]
    for test_record in test_records:
        run_para=features(test_record.id, str(test_record.seq))
        test_para=test_para+run_para+"\n"
        test_features=test_features+test_record.id+","+run_para+"\n"
        seqID_list.append(test_record.id)

    cat1_records.close()
    cat2_records.close()
    test_records.close()

    result_file=open(test_filename+"_result.txt", 'w')
    
   
    
   #---------------------WORKING WITH SCIKIT-LEARN------------

    train_positive=np.genfromtxt(StringIO(train_para_1), delimiter=",")
    train_negative=np.genfromtxt(StringIO(train_para_2), delimiter=",")
    test_data=np.genfromtxt(StringIO(test_para), delimiter=",")
    
    train_data=np.concatenate((train_positive,train_negative))
    train_label=np.concatenate((np.ones(len(train_positive)), np.zeros(len(train_negative))))

    
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    
    train_data_scaled = min_max_scaler.fit(train_data).transform(train_data)

    test_data_scaled = min_max_scaler.fit(train_data).transform(test_data)
    

    #-------------------------------------------------------------
    C_range = 2. ** np.arange(-5, 5)
    gamma_range = 2. ** np.arange(-5, 5)
    
    param_grid = dict(gamma=gamma_range, C=C_range)

    k=int(round(np.sqrt(len(train_data)/2.0)))

    clf = GridSearchCV(SVC(probability=True), param_grid=param_grid, cv=StratifiedKFold(train_label, k))

    clf.fit(train_data_scaled, train_label)

    test_predicted = clf.predict(test_data_scaled)

    train_predicted=clf.predict(train_data_scaled)
    
    decisions = clf.decision_function(test_data_scaled)

    probabilities = clf.predict_proba(test_data_scaled)

    result_file.write("ProtCat Prediction for: "+test_filename+"\n")
    result_file.write("SVM Kernel: "+clf.best_estimator_.kernel+", C: "+str(clf.best_estimator_.C)+", Gamma: "+str(clf.best_estimator_.gamma)+"\n")
    result_file.write("Number of sequences in training dataset (Type-1+Type-2 proteins), n: "+str(len(train_positive))+" + "+str(len(train_negative))+" = "+str(len(train_data))+"\n")
    result_file.write("Number of Cross validation folds, K = square root(n/2): "+str(k)+"\n")
    result_file.write("Number of sequences in test data set: "+str(len(test_data))+"\n")
    
    result_file.write("Accuracy Score: "+str(accuracy_score(train_label, train_predicted))+"\n")
    result_file.write("Precision Score: "+str(precision_score(train_label, train_predicted))+"\n")
    result_file.write("Recall Score: "+str(recall_score(train_label, train_predicted))+"\n\n\n")
    
    result_file.write("Sequence_ID\tPrediction\tScore\tProbability\n")

        
    #-----------------
    i=0
    for pred in test_predicted:
        decision=str(decisions[i]).replace("[","").replace("]","")
        probability=probabilities[:,1][i]
        if pred==1.0:
            pred='Type-1 Protein'
        if pred==0.0:
            pred='Type-2 Protein'

        if probability>0.5:
            result_file.write(seqID_list[i]+"\t"+pred+"\t"+decision+"\t"+str(probability)+"\n")
        else:
            result_file.write(seqID_list[i]+"\t"+pred+"\t"+decision+"\t"+str(1-probability)+"\n")
        i=i+1
    result_file.close()


    #--------------------PLOT--------------------------------------
    train_positive_scaled=min_max_scaler.fit(train_data).transform(train_positive)
    train_negative_scaled=min_max_scaler.fit(train_data).transform(train_negative)
    x1=np.mean(train_positive_scaled, axis=0).tolist()
    x2=np.mean(train_negative_scaled, axis=0).tolist()
    x3={}
    j=0
    records=SeqIO.parse(test_filename, "fasta")
    if test_data_scaled.ndim==1:
        for record in records:
            x3[record.id]=test_data_scaled.tolist()
    else:
        j=0
        for record in records:
            x3[record.id]=test_data_scaled[j].tolist()
            j=j+1
    records.close()


    #--------------------EMAIL SENDING--------------------------------------
    f1=open(test_filename+"_features.csv",'w')
    f1.write(idx+"\n"+test_features)
    f1.close()
    if email!="":
        command = "echo 'Your ProtCat Prediction Result is attached for job ID: "+test_filename+"\n\n\nKind regards,\n\nLutz Krause & Shihab Hasan\nComputational Medical Genomics Group, The University of Queensland Diamantina Institute' | mutt -a "+test_filename+"'_result.txt' -a "+test_filename+"'_features.csv' -s 'ProtCat Prediction Result' -- "+email
        subprocess.call(command, shell=(sys.platform!="Linux"))

    f = open(test_filename+"_result.txt",'r')
    stat_lines = f.readlines()[:10]
    f.close()

    f = open(test_filename+"_result.txt",'r')
    lines = f.readlines()[11:]
    f.close()
    
    f2 = open(test_filename+"_features.csv",'r')
    allLines=f2.readlines()
    fh, fd = allLines[:1], allLines[1:] 
    f2.close()
    f1.close()
    os.remove(cat1_filename)
    os.remove(cat2_filename)
    os.remove(test_filename)
    os.remove(test_filename+"_result.txt")
    os.remove(test_filename+"_features.csv")
    
    return (stat_lines, lines, x1, x2, x3, fh, fd)






