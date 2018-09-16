
# How to generate a random IS dataset

## Steps (short)  
*RM1*
1. Choose and download the genome of choice in the fasta format
- conversion step, database link
2. Using GEM-library compute the mappability of that genome
- parameters description, steps (gem-indexer, gem-mappability, ), convertion gem-2-wig --> wig2bed. Resulting file is in the BED format
3. In case of the full genome / several chromosomes identify the mappability percentage for each chr - this will be used as weights by the IS generation.
4. Run the program that generates N integration sites on the respective genome (unmatched)
- the program should actually include step 3 and compute the weights for each chromosome automatically.


*RM2*
4. Choose the restriction enzyme and extract the starting positions of the restriction sites writing it into a separate file.
4. Run the program that generates N integration sites on the respective genome (matched)  
- the program should actually include step 3 and compute the weights for each chromosome automatically.


## Dependencies
- GEM library tools
- twoBitToFa
- wig2bed from the Bedops package  
*RM2*
- scan_for_matches

Plan:

1. Use the genome of choice in fasta format. As first approximation it has to be in a specific folder (i.e. ./Genomes/).
2. Install GEM libraries in order to compute the mappability (add the html link and the manuscript references).
3. Compute the the mappability of the genome (.gem -> .wig -> .bed) using a specific /k-mer/ (length of the aligned read). We recommend to use 3 different k-mers: 40, 100, 200 (about 7-8 hours each).
4. Compute the mappability fraction for each chromosome to correct the number of generated IS (write an example). l

Then the tool diverge depending on the type of random IS selected (RM0: pure random without mappability (not described); RM1: with mappability (a); RM:2 with mappability and restriction sites(b)).

5a. From the mappability file (BED format) extract $n$ integrations from regions that have mappability $m>threshold$ (by default $threshold = 1$).
5b. From the mappability file (BED format) extract $n$ integrations from the restriction map (scan_for_matches) that have mappability $m>threshold$ (by default $threshold = 1$).
6. The format of the final table has 6 columns:
a) Chr
b) Start
c) End
d) Match: unmatched (RM1) / enzyme_name (i.e. MseI, ...)
e) RM: map_k-mer (i.e. map_40)
f) Assembly: genome assembly (hg38)

# Workflow

2.03
18:00 - 20:30 (2,5 h)
I downloaded the full human genome here http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/


### Virtualenv
Usage under https://virtualenv.pypa.io/en/stable/userguide/#usage

- Go to the repository rand-IS and type in `source bin/activate`
- To deactivate type in `deactivate`


8.03
16:30 - 18:30 (2,0 h)

Downloaded GEM - library, unpacked, added to PATH:
export PATH=$PATH:~/rand-IS/bin/GEM/bin

- Saved the script getRegionW2_weighted.py from the Github to scripts/ directory in rand-IS.
- Run pip install future
- Refactored the file with `futurize getRegionW2_weighted.py` to make it compatible with python3
- Tested the file - works



9.03
14:30 - 19:00 (4,5 h)

- Edited the getRegionW2_weighted.py script, made it more beautiful according to PEP8,
added main() function, integration sites are now being saved in a pandas DataFrame which is also saved in
the outputfile. Now the script needs an additional command line argument -o with the location of the output IS table.

- Made commits to GitHub, had a problem that my commit was not recognized as mine due to the wrong default email stored on my working laptop which was <elvira@akariel.tp2.gnwkservices.com>, took some time to make that commit appear in my history on git.

To do:
- write a HowTo for the RM0 basic random IS generator
- start working on RM1

12.03
15:00 - 17:00

Writing a HowTo for RM0

2.04 - 19:35 - 21:15

Continued on HowTo, described where to find and how to download the chromosome dimensions for a given organism


To do: make the assembly appear correct
Finish the HowTo for RM0
Update GitHub
