# Breeding Bird Census Data Rescue

The Breeding Bird Census is a long-term study of avian distribution and
abundance started by the U.S. Bureau of Biological Survey in 1914. For more
details see
[http://www.pwrc.usgs.gov/birds/bbc.html](http://www.pwrc.usgs.gov/birds/bbc.html).

The data is published as text paragraphs in journals, which is difficult to work
with for analysis purposes. This repository is the home of a text-mining project
working to extract this valuable data and make it available in a useful form for
researchers.

## Adding the pdfs

Because the data is published in non-open access journals we cannot redistribute
the raw pdfs here. Follow the directions in `README.md` in the `pdfs` directory
to place the pdfs in the correct location.

## Running the code

The code is written in Python 3.

We use
[`tesseract`](https://github.com/tesseract-ocr/tesseract/blob/master/README.md)
for optical character recognition (OCR) and this will need to be installed on
your system and on the path.

The code can the be run from the root directory using:

`python bbc-text-mining.py`

## Current functionality

The code has been successfully used to extract data from the 1988-1995 pdfs,
which are all single column format. We are working to expand this to other years
of the data, but typically adding additional years requires additional tweaking
to accommodate changes in the data format and special cases involving issues
with the OCR. If you try to run the code on other years of data and run into
issues please open an issue.
