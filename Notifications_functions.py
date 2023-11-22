import PyPDF2
import os


def _name_flipper(text, flag):
    if flag:
        text_list = text.split()
        text_list[0], text_list[1] = text_list[1], text_list[0]
        text = " ".join(text_list)
    return text


def _restricted_char_deleter(some_string):
    new_string = ""
    for letter in some_string:
        if letter in ("\"", "\\", "/", ":", "*", "?", "<", ">"):
            continue
        else:
            new_string += letter
    return new_string


def _uniq_name(file_name, names):
    counter = 0
    while 1:
        counter += 1
        if file_name in names:
            file_name += str(counter)
        else:
            break
    return file_name


def _new_file_name_notifications(pdf):
    pdffile = PyPDF2.PdfReader(pdf)
    page_str = pdffile.pages[0].extract_text()
    page_str = page_str.split("Z A W I")[0].split("/2023")[1].strip().split("\n")[0].strip()
    return page_str


def _new_file_name_receipt(path):
    pdffile2 = PyPDF2.PdfReader(path)
    page_str = pdffile2.pages[0].extract_text()
    page_str = page_str[page_str.find("Nazwa") + 5:page_str.find("Nazwa cd")].strip()
    return page_str


def new_file_name(path, names, change, flag):
    match flag:
        case "receipt":
            file_name = _new_file_name_receipt(path)
        case "note":
            file_name = _new_file_name_notifications(path)
        case other:
            file_name = "error in name creation"
    file_name = _restricted_char_deleter(file_name)
    file_name = _name_flipper(file_name, change)
    file_name = _uniq_name(file_name, names)
    names.append(file_name)
    file_name += ".pdf"
    return file_name


def mod_path(path):
    path = path[0:path.rfind(r"/")]
    return path


def merger(path_na, path_zw, lista_zw, names):
    all_names = zip(names, lista_zw)
    c = 1
    for m, n in all_names:
        merger = PyPDF2.PdfMerger()
        with open(path_na + "/" + m, 'rb') as f:
            merger.append(PyPDF2.PdfReader(f))
        with open(path_zw + "/" + n, 'rb') as f:
            merger.append(PyPDF2.PdfReader(f))
        merger.write(path_na + f"/{c}.pdf")
        c += 1


def spliter(path):
    reader = PyPDF2.PdfReader(path)
    path2 = mod_path(path)
    i = 1
    for page in range(len(reader.pages)):
        if page % 2 == 1:
            continue
        else:
            output = PyPDF2.PdfWriter()
            output.add_page(reader.pages[page])
            output.add_page(reader.pages[page + 1])
            with open(path2 + f"/{i}.pdf", "wb") as output_stream:
                output.write(output_stream)
            i += 1
    os.remove(path)
