"""

Script for random region generation RM1 Mappability on human genome hg38.
To be improved and generalized for use on any genome. All the variable parameters have to be parsed
through the terminal so that the script doesn't have to be change and so that nothing is hard coded.

"""
# sizes of the human chromosomes
dimension_dict={'chr13': 114364328, 'chr12': 133275309, 'chr11': 135086622, 'chr10': 133797422,\
 'chr17': 83257441, 'chr16': 90338345, 'chr15': 101991189, 'chr14': 107043718, 'chr19': 58617616,\
 'chr18': 80373285, 'chrY': 57227415, 'chr22': 50818468, 'chrX': 156040895, 'chr20': 64444167,\
 'chr21': 46709983, 'chr7': 159345973, 'chr6': 170805979, 'chr5': 181538259, 'chr4': 190214555, \
 'chr3': 198295559, 'chr2': 242193529, 'chr1': 248956422, 'chr9': 138394717, 'chr8': 145138636}

# weights based on percentage mappable regions. In sum give 1. See section 2.2.3 in the BA Thesis
# for explanation
kmer100={'chr1':0.079149,'chr2':0.085056,'chr3':0.071048,'chr4':0.067183,'chr5':0.063207,\
'chr6':0.058915,'chr7':0.053848,'chr8':0.050605,'chr9':0.039585,'chr10':0.046928,'chr11':0.046556,\
'chr12':0.047077,'chr13':0.034862,'chr14':0.030896,'chr15':0.026539,'chr16':0.026195,\
'chr17':0.025596,'chr18':0.026942,'chr19':0.019023,'chr20':0.022081,'chr21':0.011808,\
'chr22':0.011606,'chrX':0.050983,'chrY':0.004312}

import numpy as np
def getMappableIR(inputf,chr_name,kmer,mapname,N,outputf):
    """Generate N*kmer[chr_name] positions on a respective chromosome using the map of choice"""
    with open(inputf,"r"):
        chr_arr = np.genfromtxt(inputf,dtype=None)
    counter = 1
    while counter<=round(N*kmer[chr_name]):
        rand_num = np.random.randint(1,dimension_dict[chr_name])
        matched_index = np.searchsorted(chr_arr["f0"],rand_num)-1
        if chr_arr["f1"][matched_index] == True:
            #append to the file that has been previously created with headers
            with open(outputf, 'a') as f:
                print (chr_name,"\t",rand_num,"\t",rand_num+1,"\t",\
                 "unmatched","\t",mapname,"\t", "hg38", file=f)
                counter+=1
        else:
            continue
    print("generated ", round(N*kmer100[chr_name]), " IS on ", chr_name)

#first write a new file with tables header (example kmer=100):
with open('results/map100_IS100000.txt', 'w') as f:
    print("Chromosome\tStart\tEnd\tMatch\tRnd Model\tAssembly", file=f)

listofchr = ["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11",\
"chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22",\
"chrX","chrY"]

#for each chromosome compute the corresponding number of IR and append to the file
for chrom in listofchr:
    getMappableIR('results/{0}_100_mappable.txt'.format(chrom), chrom, kmer100, "map_100", 100000,\
     'results/map100_IS100000.txt')
