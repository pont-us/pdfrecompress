#!/usr/bin/python3

# By Pontus Lurcock, 2017. Released into the public domain.

"""
Force CCITT4 compression upon a PDF file.

Requires econvert, pdfimages, tiffcp, and tiff2pdf.
"""

import argparse
import os
import os.path
import glob
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory

def split_into_images(input_file, tempdir):
  prefix = os.path.join(tempdir, "a")
  pdfimages = Popen(
      ["pdfimages", input_file, prefix]
  )
  pdfimages.wait()

def convert_to_bilevel_tiffs(tempdir):
  for input_file in os.listdir(tempdir):
    if input_file[-4:] not in (".ppm", ".pbm"):
      continue
    args = ["econvert", "-i", input_file, "--colorspace", "bilevel",
            "-o", input_file[:-4]+".tiff"]
    econvert = Popen(args, cwd = tempdir)
    econvert.wait()

def tiffs_to_pdf(tempdir, output_file):
  tiffs = sorted(glob.glob(os.path.join(tempdir, "*.tiff")))
  print(tiffs)
  combined_tiff = os.path.join(tempdir, "all.tiff")
  args = ["tiffcp"] + tiffs + [combined_tiff]
  tiffcp = Popen(args)
  tiffcp.wait()
  
  tiff2pdf = Popen(["tiff2pdf", "-o", output_file, combined_tiff])
  tiff2pdf.wait()

def main():

  parser = argparse.ArgumentParser(description = 
      "Recompress a PDF file consisting of images",
      formatter_class = argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument("input_file",
                      type=str, nargs=1,
                      help="input filename")

  parser.add_argument("output_file",
                      type=str, nargs=1,
                      help="output filename")

  args = parser.parse_args()

  with TemporaryDirectory() as tempdir:

      split_into_images(args.input_file[0], tempdir)

      convert_to_bilevel_tiffs(tempdir)

      tiffs_to_pdf(tempdir, args.output_file[0])

if __name__=="__main__":
  main()
