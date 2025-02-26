from dewiki_functions import *

wiki_xml_file = 'xml.xml'  # update this
json_save_dir = './text/'
wiki_xml_path = "../"
daFile = wiki_xml_path + wiki_xml_file

if __name__ == '__main__':
    process_file_text(wiki_xml_file)
