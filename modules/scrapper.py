import os
import docx
import pptx
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

def get_file_content (path):
    # get the file extension
    _, extension = os.path.splitext(path)
    # make it lowercase
    extension = extension.lower()
    # the content
    content = []

######### if pdf #############################################
    
    if extension == ".pdf":
        try:
            # for each page in pdf
            for page_layout in extract_pages(path):
                # save every page
                page = ""
                # for each element in page
                for element in page_layout:
                    # if is text
                    if isinstance(element, LTTextContainer):
                        # then save it on content
                        page += element.get_text()
                # save the page
                content.append(page)
        # in case of error
        except Exception as e:
            print(f"Error Reading PDF: {e}")

######### if word ############################################

    elif extension == ".docx":
        try:
            page = ""
            # try to open it
            document = docx.Document(path)
            # for each paragraph
            for i, paragraph in enumerate(document.paragraphs):
                # save the paragraph
                page += paragraph.text + "\n\n"
                # and every three pages save it
                if (i+1) % 3 == 0:
                    content.append(page)
                    page = ""
        # in case of error
        except Exception as e:
            print(f"Error Reading DOCX: {e}")

######### if power point #####################################

    elif extension == ".pptx":
        try:
            # try to open the presentation
            presentation = pptx.Presentation(path)
            # for each slide
            for slide in presentation.slides:
                # set the text for every slide
                text = ""
                # for each item on slide
                for shape in slide.shapes:
                    # if it has text
                    if shape.has_text_frame:
                        # sum it to text
                        text += shape.text + ". "
                # and append to content
                content.append(text.strip())
        except Exception as e:
            print(f"Error Reading PPTX: {e}")

######### if txt ############################################

    elif extension in [".txt", ".md"]:
        text = ""
        try:
            # open the txt file
            with open(path, "r", encoding="utf-8") as file:
                # for each line
                for line in file:
                    # add the line to text
                    text += line
            # save text in content
            content.append(text)
        except Exception as e:
            print(f"Error Reading TXT: {e}")

    else:
        print(f"File not supported, only .pdf .docx .pptx .txt .md")

##############################################################

    return content