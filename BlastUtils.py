#!/usr/bin/python

import pandas as pd
import argparse

regex = '\s*(?P<SEGMENT>\S+)\s*:\s*(?P<SEGMENT_RANGE_LOW>\S+)\s*-\s*(?P<SEGMENT_RANGE_HIGH>\S+)\s*'

def parse(blast):
    df = pd.read_csv(blast, sep='\t', header=None)
    df.drop(columns=[0,4,5], inplace=True)
    df.iloc[:,0] = df.iloc[:,0].str.split('|', expand=True)
    df.rename(columns={1: "chr", 2: "start", 3: "stop"}, inplace = True)
    for index, row in df.iterrows():
        start = row.start
        if start > row.stop:
            stop = row.stop
            df.loc[index, 'start'] = stop
            df.loc[index, 'stop'] = start
    name = blast.split('.')
    out = name[1] + '.blast.algae.bed'
    df.to_csv(out, sep='\t', header=None, index=None)
    print(df)


import pysam

inbam = pysam.AlignmentFile("custom3.only.bam", "rb")
print(inbam.header)
for read in inbam.fetch():
    print(read.cigarstring)

outbam = pysam.AlignmentFile("custom3.only.NoHard.bam", 'wb', template=inbam)
for read in inbam.fetch(until_eof=True):
    if 'H' not in read.cigarstring:
        print(read.cigarstring)
        outbam.write(read)
outbam.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('blast', help='blast raw file')
    args = parser.parse_args()

    parse(args.blast)
