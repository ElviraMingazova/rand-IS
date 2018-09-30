"""

Example script for random region generation RM2 restriction enzyme matched positions on human
genome hg38. This script will generate 100000 random IS on hg38 mappable regiones matched to
MseI restriction sites if you have followed all the steps of the HowTo instruction.

"""

# weights based on percentage mappable regions. In sum give 1. See section 2.2.3 in the BA Thesis
# for explanation
kmer100={'chr1':0.079149,'chr2':0.085056,'chr3':0.071048,'chr4':0.067183,'chr5':0.063207,\
'chr6':0.058915,'chr7':0.053848,'chr8':0.050605,'chr9':0.039585,'chr10':0.046928,'chr11':0.046556,\
'chr12':0.047077,'chr13':0.034862,'chr14':0.030896,'chr15':0.026539,'chr16':0.026195,\
'chr17':0.025596,'chr18':0.026942,'chr19':0.019023,'chr20':0.022081,'chr21':0.011808,\
'chr22':0.011606,'chrX':0.050983,'chrY':0.004312}

import numpy as np
def getEnzMatchedIR(inputenzf,inputmappf,chr_name,kmer,N,mapname,enzname,outputf):
    enz = np.sort(np.genfromtxt(inputenzf, dtype=int))
    chr_arr = np.genfromtxt(inputmappf,dtype=None)
    counter = 1
    while counter<=round(N*kmer[chr_name]):
        rand_num = np.random.choice(enz)
        matched_index = np.searchsorted(chr_arr["f0"],rand_num)-1
        if chr_arr["f1"][matched_index] == True:
            with open(outputf, 'a') as f:
                print (chr_name,"\t",rand_num,"\t",rand_num+1,"\t", enzname,"\t",mapname,"\t", \
                "hg38", file=f)
                counter+=1
        else:
            continue
    print("generated ", round(N*kmer100[chr_name]), " IS on ", chr_name)


#create the file with the headers
with open('results/MseI_map100_IS100000.txt', 'w') as f:
    print("Chromosome\tStart\tEnd\tMatch\tRnd Model\tAssembly", file=f)

listofchr = ["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11",\
"chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22",\
"chrX","chrY"]

#for each chromosome compute the corresponding number of IR and append to the file
for chrom in listofchr:
    getEnzMatchedIR('results\MseI_{0}_pos.txt'.format(chrom),'results/{0}_100_mappable.txt'.format(chrom),\
    chrom, kmer100,100000,'map_100','MseI','results/MseI_map100_IS100000.txt')
