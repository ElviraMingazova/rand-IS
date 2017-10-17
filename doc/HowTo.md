
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



```python

```
