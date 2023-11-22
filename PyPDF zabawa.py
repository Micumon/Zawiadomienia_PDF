import PyPDF2

pdffile = PyPDF2.PdfReader(r"C:\Users\admin\Desktop\proba\d1\Nukari Kamil.pdf")
page = pdffile.pages[0]
page_str = pdffile.pages[0].extract_text()

page_str = page_str.split("Z A W I")[0].split("/2023")[1].strip().split("\n")[0].strip()
print(page_str)


pdffile2 = PyPDF2.PdfReader(r"C:\Users\admin\Desktop\proba\d1\RaportPrzesylki_00659007730568158341.pdf")
page_str = pdffile2.pages[0].extract_text()
page_str = page_str[page_str.find("Nazwa")+5:page_str.find("Nazwa cd")].strip()

print(page_str)
