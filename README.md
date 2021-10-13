PartsBox Inventory Tag Pipeline

<img src="https://user-images.githubusercontent.com/46428760/137186461-85a81e41-d6d7-4ee1-866c-b907d38069da.png" width="500">

This is a set of tools pieced together to automatically generate inventory tags for printing, for your PartsBox.com parts.  
My use case is to print a 3"x5" index card with the MPN, Manufacturer, Description, Storage Location, and a QR code for quickly looking up the part in PartsBox.  
My parts will go into 4"x6" plastic bags with the printed index cards inserted inside acting as the label.   
These plastic bags will then be stored on edge in 6 quart / 5.7 L (13 5/8" x 8 1/4" x 4 7/8" / 34.6 cm x 21 cm x 12.4 cm) plastic bins.  

You can modify my Scribus template or replace it with your own. Refer to the mail-merge.py docs (linked at the bottom) for how to specify your variables in Scribus.  

Warning: This will probably not work out of the box. You will very likely need to tweak generate-tags.py for your system.  
For example, the path to Scribus.exe is hard coded and probably won't match your system.  
Also, no testing has been done outside of Windows. There is no reason it can't work on Linux but I'm sure something will inevitability need to be fixed before it works.  
I'm not at all a professional developer so I guarantee this project does not conform to all best practices.  

Requirements:  
- Scribus (https://www.scribus.net/downloads/) (I'm using v1.5.7)  
- Python libraries/packages csv, qrcode, qrcode.image.svg, os, shutil, glob, re, PyPDF3, subprocess  

If you are missing a python package, there is a good change "pip install insert-package-name-here" will fix it.  

Instructions:

0) Download this repo as a .zip and then extract it  
1)	a) From PartsBox.com, go to the Parts > Parts page.  
	b) Check the boxes for the parts you want to export, or click the checkbox in the table header to select all parts.  
	c) Then click the "Selected..." menu and click "Download as CSV"  
2) Move the downloaded CSV into the extracted git repo folder and make sure the CSV is named "partsbox-parts.csv"   
3) (Optional) Open "partsbox-parts.csv" in LibreOffice Calc. Delete all lines except for the parts you want to print tags for. This is easier than filtering on the PartsBox.com site. When saving make sure the file name and format haven't changed.  
4) Run "generate-tags.py" from the command line. This will do the following:  
	- Prepend a line index value to the CSV  
	- Append the future QR code image file name  
	- Output the modified CSV to ./output_dir/output.csv  
	- Generate the QR codes in to ./output_dir/  
	- Create a variable placeholder QR code image file for Scribus (This might not really be necessary but it makes it easy to add the image variable into Scribus)
	- Start Scribus and execute mail_merge.py on the included template .sla file  
	- mail_merge.py will create one pdf for each line in CSV  
	- The script will then merge all the PDFs together and delete the original seperate pdfs  
	- The end result is a single output.pdf file in the main directory with the results  
	
You can test all of this on the PartsBox demo site if you'd like: https://partsbox.com/demo/parts  	
	
Credit:  
mail-merge.py was borrowed from https://github.com/aoloe/scribus-script-repository/tree/master/mail-merge. Some small tweaks were made to it (I think).  
