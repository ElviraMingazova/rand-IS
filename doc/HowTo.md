# Random dataset generation instruction
## RM 0

1. Open the Terminal, change into the working directory of choice using  
`cd <path to directory>`  
2. Clone the git repository rand-IS using the following command:  
`git clone https://github.com/ElviraMingazova/rand-IS.git`
and change into the working directory  
`cd rand-IS/`
4. Type in `source bin/activate` to activate the virtual environment in that directory.  
3. Create a generalized genome dimension file in the directory rand-IS/data/textfiles/ a textfile that contains two tab (or space) separated columns.
In the first column the names of the chromosomes in the format chr\__ (instead of __ is the number or X/Y in case of the human genome for example). You will find a couple of examples in the folder rand-IS/data/textfiles/.
        ___
        chr1	248956422  
        chr2	242193529  
        chr4	190214555  
        ...  
        chrY  57227415
        ___
The chromosome sizes can be downloaded from the database of the University of California, Santa Cruz (UCSC).
    - To do it manually tap this link http://hgdownload.cse.ucsc.edu/downloads.html, find the needed organism and search for the file chrom.sizes or chromInfo in one of the databases. You can also use directly the following link:  http://genome.ucsc.edu/cgi-bin/hgTracks?db=dm3&chromInfoPage=
    Just swap the db=xx for another genome.
    - Alternatively, you can use the tool fetchChromSizes, that is already in the rand-IS/bin repository.  
    Usage: `fetchChromSizes <db> > <db>.chrom.sizes`  
    This tool is used to fetch chrom.sizes information from UCSC for the given <db>.
    <db> - name of UCSC database, e.g.: hg38, hg18, mm9, etc ...  
    Example: `fetchChromSizes mm10 > ../data/textfiles/mm10.chrom.sizes.txt`  
    This data is available at the URL:
    `http://hgdownload.cse.ucsc.edu/goldenPath/<db>/bigZips/<db>.chrom.sizes`.  
    Don't forget to edit the downloaded file that there is only information described above and move it to the rand-IS/data/textfiles/ directory

4. To generate a random dataset of the IS type in the terminal:  
`python3 scripts/getRegionW2_weighted.py -n_ -r_ -d_ -i "data/textfiles/_.txt" -o "results/_.txt"`  
Instead of "_" you have to type in the correct value for the parameters.  
Explanation of the parameters:
  * n - Number of IS you want to generate
  * r - Range-value: defines an interval where the IS is located
  * d - Delta-value: expands the range with the value provided by user
  * i - Input-file .txt with names of chromosomes and their lengths in bp organized into two columns and separated by \t (tab or space)
  * o - Output-file where the random integration sites will be saved

## RM 1

**Dependencies**
- GEM library tools (https://sourceforge.net/projects/gemlibrary/files/)
- Bedops package  (https://bedops.readthedocs.io/en/latest/content/installation.html)


1. Choose and download the genome of choice in the fasta format into the rand-IS/data/genomes directory. Sometimes genomes are only available in twoBit format, then convert it to fasta using `twoBitToFa` tool. The genomes are available for download from here: http://hgdownload.cse.ucsc.edu/downloads.html.  
For example we will do it with the chrY sequence.  
`cd rand-IS/genomes`  
`wget http://hgdownload.cse.ucsc.edu/goldenPath/hg38/chromosomes/chrY.fa.gz`  
`gunzip chrY.fa.gz`
2. Compute the mappability of the genome (example commands for hg38.fa and kmer length 100)
  - Add GEM library to PATH  
  `PATH=$PATH:/home/elvira/rand-IS/bin/GEM/bin/`
  - create an indexed genome using  
  `gem-indexer -i data/genomes/hg38.fa -o results/hg38_index`
  - compute mappability file
  `gem-mappability -I results/hg38_index.gem -o results/hg38_100 -l 100`
  - convert results to wig format
  `gem-2-wig -I results/hg38_index.gem -i results/hg38_100.mappability -o results/hg38_100`

3. Next step is to compute percentage of the uniquely mappable regions on each chromosome (section 2.2.2 in my Bachelor thesis). This information will be important for random IS generation in the next step to assign weights.
  - Add BEDOPS package to PATH:  
  `PATH=$PATH:/home/elvira/rand-IS/bin/BEDOPS/`
  - Convert wig formatted file to BED format  
  `wig2bed < results/hg38_100.wig > results/hg38_100.bed`  

          |  chr name | start | end   | id   |  mappability value |
          |-----------|-------|-------|------|--------------------|
          | chr1      | 0     | 10000 | id-1 | 0.000000           |
          | chr1      | 10000 | 10001 | id-2 | 0.006463           |
          | chr2      | 10001 | 10005 | id-3 | 0.005249           |

    This is how the output then looks
  - Extract a textfile with two columns where the first column is a chromosome name and the second is the length of uniquely mappable parts (mappability value = 1). For that it was iterated over a list of chromosome names and bedextract-command from BEDOPS tools was used.
    - use the following bash code
    ```
    declare -a arr=("chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10" "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19" "chr20" "chr21" "chr22" "chrX" "chrY")
    kmer = 100
    for i in ${arr[@]}; do bedextract "$i" hg38_$kmer.bed | awk -v thr=1 -v chr=$i 'BEGIN {len = 0} {if ($5>=thr) len = len + ($3-$2)} END {print chr,len}'; done >> unique_regions_$kmer.txt
    ```

4. Generation of the random dataset on the mappable regions
  - Starting from a precomputed mappability file in bed-format create a textfile containing two columns: positions on a specific chromosome and True/False statement. If the region is uniquely mappable (mappability = 1) then "True" should be written opposite to it's starting position and if the mappability value is less than 1 - "False".
  ```
  declare -a arr=("chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10" "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19" "chr20" "chr21" "chr22" "chrX" "chrY")
  kmer = 100
  for i in ${arr[@]}; do bedextract "$i" hg38_$kmer.bed | awk '{if ($5==1) print $2, "true"; else print $2, "false"}' | awk -v prev=0 '{if ($2 != prev) print $0; prev = $2}' > $i_$kmer_mappable.txt; done
  ```
  Now the files contain two columns.
  ```
  0 false
  17000001 true
  17000013 false
  17000056 true
  17000127 false
  17003594 true
  ...
  ```
  The meaning is that positions 0 -17000001 are not mappable, 17000001 - 17000013 are mappable, 17000013 - 17000056 are again not mappable and so on.

  - **This step has to be improved**. At this point of the framework development you have to modify the script `mappable_randomIR` so that it corresponds to your data. There are hard coded things that have to be changed. Now the script is adjusted to generate 100000 IS on the hg38 with kmer = 100. Open the script for further explanations. If you follow the example you have to run:  
  `python scripts/mappable_randomIR.py `  
  After that the IS can be found under results/map100_IS100000.txt.

## RM 2

**Dependencies** (additional to the ones already mentioned)
- scan_for_matches
  Follow installation instruction on the download page: http://blog.theseed.org/servers/2010/07/scan-for-matches.html

1. Choose the restriction enzyme corresponding to the one that was used for the experimental IS retrieval. Here we will take an example of MseI. Its recognition pattern is 5'..TTAA..3'.

**Starting from here I couldn't redo all the steps on the GW laptop since I had problems with gcc installation, it was not preinstalled and was needed to compile scan_for_matches.c (sudo rights required).**

2. Extract starting positions of the cleavage sites for a particular enzyme using the tool scan_for_matches.
  - Create a pattern file containing the recognition sequence for the restriction enzyme:
  ```
  cat > MseI_pattern.txt
  TTAA
  ```
  - Find the positions of this pattern on the genome:
  ```
  scan_for_matches MseI_pattern.txt < data/genomes/hg38.fa | show hits
  output:
  chr1:[11533,11536]: ttaa
  chr1:[11556,11559]: ttaa
  ...
  ```
  - save only the first column under results/MseI_hg38output.txt
  ```
  scan_for_matches MseI_pattern.txt < data/genomes/hg38.fa | show_hits | awk '{print $1}' > results/MseI_hg38output.txt
  head MseI_hg38output.txt
  chr10:[100000032,100000035]
  chr10:[100000061,100000064]
  chr10:[100001232,100001235]
  chr10:[100001782,100001785]
  chr10:[100001876,100001879]
  chr10:[100002018,100002021]
  chr10:[100002080,100002083]
  chr10:[100002134,100002137]
  chr10:[100002596,100002599]
  chr10:[100002698,100002701]
  ...
  ```
  - For each chromosome extract all the starting positions of the restriction sites and write into a separate file
  ```
  declare -a chrom=("chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10" "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19" "chr20" "chr21" "chr22" "chrX" "chrY")  
  ```
  ```
  for i in ${chrom[@]}; do awk -F"[" -v chr=$i '$1==chr":" {print $2}' MseI_hg38output.txt | awk -F',' '{print $1}' > MseI_${i}_pos.txt ; done
  ```
  The output file contains only one column with the restriction sites start coordinates:
  ```
  100000132
  100000416
  100000561
  100000636
  100000860
  ...
  ```
3. Using the example script enzyme_matched_randomIR.py you can generate 100000 IS on the
hg38 matched to MseI restriction sites. Once your goal is different from this you have to modify the script manually.
```
python scripts/enzyme_matched_randomIR.py
```
For the statistical tests and further explanations please refer to the bachelor thesis under /doc/BachelorThesisFinal.pdf and to the notebooks that I was creating during my internship at NCT here: https://github.com/ElviraMingazova/RARE
