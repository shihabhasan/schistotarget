from Bio import SeqIO
from Bio.SeqUtils import ProtParam

import sys, os, subprocess
import re
import time, hashlib

from pepstat import pepstat
from garnier import garnier
from netcglyc import netcglyc
from netchop import netchop
from netnglyc import netnglyc
from netphos import netphos
from prop import prop
from anchor import anchor
from targetp import targetp
from bepipred import bepipred
from immuno import immuno
from countBiMers import countBiMers

def features(seqID, sequence):
    parameters=""
         
    seq=sequence.upper().replace("X","").replace("*","").replace("U","C").replace("B","D")

    X = ProtParam.ProteinAnalysis(seq)
    
    count=X.count_amino_acids()
    parameters=parameters+str(len(sequence))+","
    
    percent=X.get_amino_acids_percent()
    parameters=parameters+str(round(percent["A"], 4))+","+str(round(percent["C"], 4))+","+str(round(percent["D"], 4))+","+str(round(percent["E"], 4))+","+str(round(percent["F"], 4))\
                   +","+str(round(percent["G"], 4))+","+str(round(percent["H"], 4))+","+str(round(percent["I"], 4))+","+str(round(percent["K"], 4))+","+str(round(percent["L"], 4))+","+str(round(percent["M"], 4))\
                   +","+str(round(percent["N"], 4))+","+str(round(percent["P"], 4))+","+str(round(percent["Q"], 4))+","+str(round(percent["R"], 4))+","+str(round(percent["S"], 4))+","+str(round(percent["T"], 4))\
                   +","+str(round(percent["V"], 4))+","+str(round(percent["W"], 4))+","+str(round(percent["Y"], 4))+","

    

    parameters=parameters+str(X.molecular_weight())+","
    parameters=parameters+str(round(X.aromaticity(), 4))+","
    parameters=parameters+str(round(X.instability_index(), 4))+","
    parameters=parameters+str(round(X.isoelectric_point(), 4))+","
    parameters=parameters+str(round(X.gravy(), 4))+","
    parameters=parameters+str(round(X.secondary_structure_fraction()[0], 4))+","+str(round(X.secondary_structure_fraction()[1], 4))+","+str(round(X.secondary_structure_fraction()[2], 4))+","
    parameters=parameters+str(round(X.molecular_weight()/len(seq), 4))+","

    #-----------------------PEPSTATS-------------------------------
    
    inFileName=seqID.replace("|","_").replace(":","_")+"_"+hashlib.md5(time.asctime()).hexdigest()
    inFasta=open(inFileName, "w")
    inFasta.write(">"+seqID.replace("|","_")+"\n"+seq+"\n")
    inFasta.close()

    parameters=parameters+pepstat(inFileName)+","
                   

    tiny = count["A"]+count["C"]+count["G"]+count["S"]+count["T"]
    tiny_per = round(((float(tiny)/len(seq))*100),3)
    parameters=parameters+str(tiny_per)+","

    small = count["A"]+count["C"]+count["D"]+count["G"]+count["N"]+count["P"]+count["S"]+count["T"]+count["V"]
    small_per = round(((float(small)/len(seq))*100),3)
    parameters=parameters+str(small_per)+","

    aliphatic = count["I"]+count["L"]+count["V"]
    aliphatic_per = round(((float(aliphatic)/len(seq))*100),3)
    parameters=parameters+str(aliphatic_per)+","

    aromatic = count["F"]+count["H"]+count["W"]+count["Y"]
    aromatic_per = round(((float(aromatic)/len(seq))*100),3)
    parameters=parameters+str(aromatic_per)+","

    polar = count["D"]+count["E"]+count["H"]+count["K"]+count["N"]+count["Q"]+count["R"]+count["S"]+count["T"]
    polar_per = round(((float(polar)/len(seq))*100),3)
    parameters=parameters+str(polar_per)+","

    nonPolar = count["A"]+count["C"]+count["F"]+count["G"]+count["I"]+count["L"]+count["M"]+count["P"]+count["V"]+count["W"]+count["Y"]
    nonPolar_per = round(((float(nonPolar)/len(seq))*100),3)
    parameters=parameters+str(nonPolar_per)+","

    charged = count["D"]+count["E"]+count["H"]+count["K"]+count["R"]
    charged_per = round(((float(charged)/len(seq))*100),3)
    parameters=parameters+str(charged_per)+","
    
    acidic = count["D"]+count["E"]
    acidic_per = round(((float(acidic)/len(seq))*100),3)
    parameters=parameters+str(acidic_per)+","
    
    basic = count["H"]+count["K"]+count["R"]
    basic_per = round(((float(basic)/len(seq))*100),3)
    parameters=parameters+str(basic_per)+","
    


    #------------------------GARNIER--------------------------------

    parameters=parameters+garnier(inFileName)+","


    #--------------------------NetCGlyc--------------------------------

    parameters=parameters+netcglyc(inFileName)+","

    #--------------------------NetChop--------------------------------

    parameters=parameters+netchop(inFileName)+","
    

    #--------------------------NetNGlyc--------------------------------

    parameters=parameters+netnglyc(inFileName)+","
    

    #--------------------------NetPhos--------------------------------

    parameters=parameters+netphos(inFileName)+","


    #--------------------------ProP----------------------------------

    parameters=parameters+prop(inFileName)+","


    #--------------------------ANCHOR----------------------------------

    parameters=parameters+anchor(inFileName)+","

    #--------------------------TargetP----------------------------------

    parameters=parameters+targetp(inFileName)+","


    #--------------------------BepiPred----------------------------------

    parameters=parameters+bepipred(inFileName)+","

    #--------------------------Immunogenicity----------------------------------

    parameters=parameters+immuno(inFileName)

    #--------------------------countBiMers----------------------------------

    parameters=parameters+countBiMers(seq)

    #--------------------------#####################---------------------


    os.remove(inFileName)
    
    return parameters

    
