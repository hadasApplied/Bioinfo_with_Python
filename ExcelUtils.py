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


class ExcelUtils:

    def read_sheet1(xfile):

        df = pd.read_excel(xfile,sheet_name='Sheet1', index_col=None)
        Name=df['User'][0]
        Email=df['Email'][0]
        Service=df['Service'][0]
        return Name, Email, Service

    def to_csv(xfile, sheetname):
        df = pd.read_excel(xfile,sheet_name=sheetname, index_col=None)
#        xpath = os.path.dirname(os.path.abspath(xfile))
        xfilename = os.path.splitext(xfile)[0]
        csvfile = xfilename + '.csv'
        df.to_csv(csvfile, header=True, index=None)
        return csvfile

    def copy_sheet(xsrcfile, srcsheetname, xdstfile, dstsheetname):
        df = pd.read_excel(xsrcfile,sheet_name=srcsheetname, index_col=None)
        # This section is sample code that creates a worbook in the current directory with 3 worksheets
        #df = pd.DataFrame(np.random.randn(10, 3), columns=list('ABC'))
        writer = pd.ExcelWriter(xdstfile, engine='xlsxwriter')
        df.to_excel(writer, sheet_name=dstsheetname, index=False)
        writer.close()