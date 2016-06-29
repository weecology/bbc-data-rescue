import os
import re
from glob import glob

def convert_pdf_to_images(filename, output_path):
    """Convert a pdf to images"""
    filename_w_path = os.path.splitext(filename)[0]
    filename_wo_path = os.path.split(filename_w_path)[-1]
    os.system("convert -density 350 -crop 0x0+0+330 {0}.pdf {1}.png".format(filename_w_path, os.path.join(output_path, filename_wo_path)))

def ocr(filename):
    """OCR a file using tesseract"""
    filename = os.path.splitext(filename)[0]
    os.system("tesseract {0}.png {0}".format(filename))

def convert_pdfs_to_text(pdf_path, output_path):
    """Convert all PDFs in a directory to text

    Use convert to convert to images and tesseract for OCR
    
    """
    pdfs = glob(os.path.join(pdf_path, "*.pdf"))
    for pdf in pdfs:
        convert_pdf_to_images(pdf, output_path)
        
        #multi-page pdfs create multiple png files so loop over them
        pngs = glob(os.path.join(output_path, "*.png"))
        for png in pngs:
            ocr(png)

def cleanup_nonpara_pages(path, para_starts):
    """Remove text and png files for pages that aren't the core paragraph data"""
    for year in para_starts:
        pages  = range(para_starts[year] - 1) #pages are not zero indexed
        for page in pages:
            os.remove(os.path.join(path, "BBC{}-{}.txt".format(year, page)))
            os.remove(os.path.join(path, "BBC{}-{}.png".format(year, page)))

def combine_txt_files_by_yr(path, years):
    """Combine multiple text files into a single file for each year

    File names have the general format: BBC1988-0.txt
    
    """
    for year in years:
        with open(os.path.join(path, "bbc_combined_{}.txt".format(year)), 'w') as outfile:
            filenames = glob(os.path.join(path, "BBC{}*.txt".format(year)))
            sorted_filenames = sorted_nicely(filenames)
            for fname in sorted_filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())

def sorted_nicely(l): 
    """ Sort the given iterable in the way that humans expect.

    From:
    http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    
    """ 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

para_starts = {1988: 4, 1989: 6, 1990: 6, 1991: 7,
               1992: 7, 1993: 7, 1994: 7, 1995: 6, 2009: 1}
pdf_path = "./pdfs/"
data_path = "./data/"
convert_pdfs_to_text(pdf_path, data_path)
cleanup_nonpara_pages(data_path, para_starts)
combine_txt_files_by_yr(data_path, para_starts.keys())
