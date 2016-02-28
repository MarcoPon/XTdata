# Extract data from Bitcoin Unlimited debug log about
# Xtreme Thinblocks compression efficency

#adjust path and filenames as needed
debuglogfilename = r"/tank/bitcoin/debug.log"
csvfilename = r"graph.csv"
resultsfilename = r"results.txt"
#use this to start from a certain block...
startfromhash = ""

import re

blocksre = r"block for ([0-9a-z]+) \((\d+) \w+\). Message was (\d+)"
blocksnum = 0
totblocksize = 0
totxtsize = 0

calc = False
if startfromhash == "":
    calc = True

with open(csvfilename, "w") as fout:
    fout.write('"Block Size","XT Size"\n')
    with open(debuglogfilename, "r") as fin:
        for text in fin:
            if "compression" in text:
                res = re.findall(blocksre, text)[0]
                blockhash = res[0]
                blocksize = int(res[1])
                blockcomp = int(res[2])
                if calc == False:
                    if blockhash == startfromhash:
                        calc = True
                if calc == True:
                    print text.strip()
                    blocksnum += 1
                    totblocksize += blocksize
                    totxtsize += blockcomp
                    blockratio = float(blocksize) / blockcomp
                    print "(Size %i, compressed %i, ratio %.2f)" % (blocksize, blockcomp,
                                                             blockratio)
                    fout.write("%i, %i\n" % (blocksize, blockcomp))

if blocksnum > 0:

    text = ""
    text += "Blocks        : %i\n" % ( blocksnum )
    text += "Tot block size: %s\n" % ( "{:,}".format(totblocksize) )
    text += "Tot XT size   : %s\n" % ( "{:,}".format(totxtsize) )
    text += "Average blocksize: %s\n" % ( "{:,}".format(totblocksize / blocksnum) )
    text += "Average XT size  : %s\n" % ( "{:,}".format(totxtsize / blocksnum) )
    text += "Ratio         : %.2f\n" % ( float(totblocksize) / totxtsize )
    text += "Compression   : %.2f%% \n" % ( (totblocksize - totxtsize) * 100.0
                                      / totblocksize )
    print
    print text

    with open(resultsfilename, "w") as fout:
        fout.write(text)
