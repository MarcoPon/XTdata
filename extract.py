# Extract data from Bitcoin Unlimited debug log about
# Xtreme Thinblocks compression efficency

#adjust path and filenames as needed
debuglogfilename = r"p:\bitcoin-full\debug.log"
csvfilename = r"graph.csv"
resultsfilename = r"results.txt"
windowsize = 288 #last n blocks to consider (144 = ~1 day)

import re

blocksre = r"block for ([0-9a-z]+) \((\d+) \w+\). Message was (\d+)"
blocksnum = 0
totblocksize = 0
totxtsize = 0

blocksdata = []
with open(debuglogfilename, "r") as fin:
    for text in fin:
        if "compression" in text:
            res = re.findall(blocksre, text)[0]
            blockhash = res[0]
            blocksize = int(res[1])
            blockcomp = int(res[2])
            print text.strip()
            blocksdata.append(( blockhash, blocksize, blockcomp ))

if windowsize > 0:
    blocksdata = blocksdata[-windowsize:]

with open(csvfilename, "w") as fcsv:
    fcsv.write('"Block Size","Xthin Size"\n')
    blocksnum = len(blocksdata)
    for block in blocksdata:                
        blocksize = block[1]
        blockcomp = block[2]
        totblocksize += blocksize
        totxtsize += blockcomp
        blockratio = float(blocksize) / blockcomp
        print "(Size %i, compressed %i, ratio %.2f)" % (blocksize, blockcomp,
                                                 blockratio)
        fcsv.write("%i, %i\n" % (blocksize, blockcomp))

if blocksnum > 0:
    text = ""
    text += "Blocks: %i\n" % ( blocksnum )
    text += "Tot block size    : %s\n" % ( "{:>12,}".format(totblocksize) )
    text += "Tot Xthin size    : %s\n" % ( "{:>12,}".format(totxtsize) )
    text += "Average block size: %s\n" % ( "{:>12,}".format(totblocksize / blocksnum) )
    text += "Average Xthin size: %s\n" % ( "{:>12,}".format(totxtsize / blocksnum) )
    text += "Ratio      : %.2f\n" % ( float(totblocksize) / totxtsize )
    text += "Compression: %.2f%% \n" % ( (totblocksize - totxtsize) * 100.0
                                      / totblocksize )
    print
    print text

    with open(resultsfilename, "w") as fres:
        fres.write(text)

    
