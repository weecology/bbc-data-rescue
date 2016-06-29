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

def convert_pdf_to_text(pdf_path, output_path):
    """Convert a non-OCR'd PDF into text

    Use convert to convert to images and tesseract for OCR

    """
    convert_pdf_to_images(pdf_path, output_path)

    #multi-page pdfs create multiple png files so loop over them
    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    pngs = glob(os.path.join(output_path, basename + "*.png"))
    for png in pngs:
        ocr(png)

def convert_pdf_to_text_no_ocr(pdf_path, output_path):
    """Convert a pdf to text when no OCR is needed

    Uses pdftotext from the shell to do the conversion

    """
    os.system("pdftotext -f 1 -l 1 -H 560 -W 500 -x 0 -y 90 {} {}".format(pdf_path, "first_page.txt"))
    os.system("pdftotext -f 2 -H 600 -W 500 -x 0 -y 50 {} {}".format(pdf_path, "other_pages.txt"))
    os.system("cat first_page.txt other_pages.txt > {}".format(output_path))
    os.remove("first_page.txt")
    os.remove("other_pages.txt")

def cleanup_nonpara_pages(path, start_page):
    """Remove text and png files for pages that aren't the core paragraph data"""
    pages  = range(start_page - 1) #pages are not zero indexed
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
pdf_dir = "./pdfs/"
data_dir = "./data/"

pdf_info = {1988: {'ocr': True, 'start_page': 4},
            1989: {'ocr': True, 'start_page': 6},
            1990: {'ocr': True, 'start_page': 6},
            1991: {'ocr': True, 'start_page': 7},
            1992: {'ocr': True, 'start_page': 7},
            1993: {'ocr': True, 'start_page': 7},
            1994: {'ocr': True, 'start_page': 7},
            1995: {'ocr': True, 'start_page': 6},
            2003: {'ocr': False, 'start_page': 1},
            2004: {'ocr': False, 'start_page': 1},
            2005: {'ocr': False, 'start_page': 1},
            2006: {'ocr': False, 'start_page': 1},
            2007: {'ocr': False, 'start_page': 1},
            2008: {'ocr': False, 'start_page': 1},
            2009: {'ocr': False, 'start_page': 1}}

for year in pdf_info:
    pdf_path = os.path.join(pdf_dir, "BBC{}.pdf".format(year))
    if pdf_info[year]['ocr']:
        convert_pdf_to_text(pdf_path, data_dir)
        cleanup_nonpara_pages(data_dir, pdf_info[year]['start_page'])
        combine_txt_files_by_yr(data_dir, para_starts.keys())
    else:
        output_file_path = os.path.join(data_dir, "bbc_combined_{}.txt".format(year))
        convert_pdf_to_text_no_ocr(pdf_path, output_file_path)
