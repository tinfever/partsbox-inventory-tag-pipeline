import csv, qrcode, qrcode.image.svg, os, shutil, glob, re, PyPDF3, subprocess

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

try:
    os.mkdir("output_dir")
except:
    None
    
    
try: 
    for file in os.scandir('./output_dir'):
        os.remove(file.path)
    for file in os.scandir('./'):
        if re.match("^.*\.pdf$", file.path):
            os.remove(file.path)
except:
    None


with open('partsbox-parts.csv', encoding="utf8") as csvFile:
    with open('./output_dir/output.csv', 'w', newline="", encoding="utf8") as newfile:
        csvReader = csv.reader(csvFile, delimiter=',')
        writer = csv.writer(newfile)
        firstlineparsed = 0
        line_index = 1
        for line in csvReader:
            if firstlineparsed == 0:
                URLcolumn = line.index('URL')
                line.append("ImageName")
                line.insert(0,"LineIndex")
                writer.writerow(line)
                firstlineparsed = 1
            else: 
                print(str(line_index)+", "+line[URLcolumn])
                qr.clear()
                qr.add_data(line[URLcolumn])
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                img.save("./output_dir/"+str(line_index)+".png")
                line.append(str(line_index)+".png")
                line.insert(0,line_index)
                line_index = line_index + 1
                writer.writerow(line)
shutil.copy("./output_dir/1.png","./output_dir/{ImageName}")

print("Executing mail_merge.py script within Scribus")
subprocess.run(["C:\Program Files\Scribus 1.5.7\Scribus.exe", "-g", "-ns", "-py", "mail-merge.py", "--", "PartsBox Inventory Card Template.sla"])

print("Merging created PDFs")
pdfFiles=[]
for filename in os.listdir('./'):
    if filename.endswith('.pdf'): 
        pdfFiles.append(os.path.join('./', filename))
        
pdfmerger = PyPDF3.PdfFileMerger()
for currentFile in pdfFiles: 
    fileobj = open(currentFile, "rb")
    pdfmerger.append(fileobj)
    
pdfOutput = open ("output.pdf", 'wb')
pdfmerger.write(pdfOutput)
pdfOutput.close()
pdfmerger.close()
fileobj.close()
   
print("Cleaning up...")

shutil.rmtree('./output_dir')
for file in os.scandir('./'):
    if re.match("^.*\.pdf$", file.path) and file.path != "./output.pdf":
        print("Deleting", file.path)
        os.remove(file.path)

print("Done!")
input("Press any key to exit...")
