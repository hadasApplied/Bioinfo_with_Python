import sys
import os
import shutil
from Bio import SeqIO
import re
import boto3
import botocore
from subprocess import Popen, PIPE
import logging
import datetime


class FastaUtils:

    def batch_iterator(iterator, batch_size):
        """Returns lists of length batch_size.
        This can be used on any iterator, for example to batch up
        SeqRecord objects from Bio.SeqIO.parse(...), or to batch
        Alignment objects from Bio.AlignIO.parse(...), or simply
        lines from a file handle.
        This is a generator function, and it returns lists of the
        entries from the supplied iterator.  Each list will have
        batch_size entries, although the final list may be shorter.
        """
        entry = True  # Make sure we loop once
        while entry:
            batch = []
            while len(batch) < batch_size:
                try:
                    entry = next(iterator)
                except StopIteration:
                    entry = None
                if entry is None:
                    # End of file
                    break
                batch.append(entry)
            if batch:
                yield batch

    def splitFastq (infile, outdir, batch_size):
        record_iter = SeqIO.parse(open(infile),"fastq")
        for i, batch in enumerate(FastaUtils.batch_iterator(record_iter, batch_size)):
            filename = outdir + "/" + batch[0].id + ".fastq"
            #filename = outdir + "/chunk_%i.fastq" % (i + 1)
            with open(filename, "w") as handle:
                count = SeqIO.write(batch, handle, "fastq")
                print("Wrote %i records to %s" % (count, filename))

    def splitFasta (infile, outdir, batch_size):
        record_iter = SeqIO.parse(open(infile),"fasta")
        for i, batch in enumerate(FastaUtils.batch_iterator(record_iter, batch_size)):
            filename = outdir + "/" + batch[0].id + ".fasta"
            #filename = outdir + "/chunk_%i.fasta" % (i + 1)
            with open(filename, "w") as handle:
                count = SeqIO.write(batch, handle, "fasta")
                print("Wrote %i records to %s" % (count, filename))


    def validProteinSequence(infastafile):
        records = list(SeqIO.parse(infastafile, "fasta"))
        valid = 'ACTG'
        for letter in records[0].seq:
            if letter not in valid:
                return True
        return False


    def getFastaSeq(filename):
        ifile = open(filename, 'rU')
        seqs = []
        for record in SeqIO.parse(ifile, "fasta"):
            sequence = str(record.seq).upper()
            seqs.append(sequence)

        return seqs

    def multi2linefasta(indir, outdir, filelist):
#
# May accept single file in filelist
#
        for items in filelist:
            mfasta = outdir +"/"+re.sub('\..*','',items)+'_twoline.fasta'
            ifile = open(indir+'/'+items,'rU')
            with open(mfasta, 'w') as ofile:
                for record in SeqIO.parse(ifile, "fasta"):
                    sequence = str(record.seq)
                    ofile.write('>' + record.id + '\n' + sequence + '\n')