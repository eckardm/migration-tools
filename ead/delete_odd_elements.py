# import what we need
import os
from os.path import join

# you'll need and want, respectively, to import the following python modules, i.e., pip install lxml and pip install tqdm
from lxml import etree as ET
from tqdm import *

# where are the eads?
ead_path_test = 'C:/Users/Public/Documents/Real_Masters_all'
ead_path_production = 'C:/Users/eckardm/GitHub/vandura/Real_Masters_all'

# xpath to where we'll be looking in each ead
container_xpath = '//container'

# # writes headers to report
# with open('C:/Users/Public/Documents/culprits.csv', 'w') as culprits:
    # culprits.write('Filename,Container Type,Container Label,Container Text,<odd> text')

# go through all thie files in that directory
for filename in tqdm(os.listdir(ead_path_test)):
    # but only look at the xml files
    if filename.endswith('.xml'):
        # create a lxml etree version of the ead
        ead_tree = ET.parse(join(ead_path_test, filename))
        
        # look at each of the container elements
        for container_element in ead_tree.xpath(container_xpath):
            try: 
                # find "cousin" paragraph tags in odd, first by getting xpath for that particular container
                oversize_volume_xpath = ead_tree.getpath(container_element)
                # then replacing did/container with odd/p to get cousin paragraph xpath
                cousin_paragraph_xpath = oversize_volume_xpath.replace('did/container', 'odd/p')
                # we'll need to check the text at that xpath, so let's create variable
                cousin_paragraph = ead_tree.xpath(cousin_paragraph_xpath)[0].text
                # and then check to see if it starts with "(O" or "(o" or "(V" or "(v" for oversize and volume (since we say those two things many different ways), respectively, if it contains the number, and skipping some known exceptions by filename
                if cousin_paragraph.endswith(' ' + container_element.text + ')') and 'includes' not in cousin_paragraph and container_element.attrib['label'] != 'Box' and filename != 'steerejb.xml' and filename != 'palmera2.xml' and filename != 'kellomic.xml' and filename != 'gmwill.xml' and filename != 'fpresbir.xml' and filename != 'finneyea.xml':
                    # # generate report
                    # with open('C:/Users/Public/Documents/culprits.csv', 'a') as culprits:
                        # culprits.write('\n' + filename + ',' + str(container_element.attrib).replace("{'type': ", '').replace("{'label': ", '').replace("'", '').replace(' label: ', '').replace('}', '') + ',' + str(container_element.text) + ',' + cousin_paragraph)
                        
                    # delete the odd tag, first by finding the odd
                    odd_to_delete_xpath = cousin_paragraph_xpath.replace('/p', '')
                    # then by using this: http://stackoverflow.com/questions/7981840/how-to-remove-an-element-in-lxml
                    for odd_to_delete in ead_tree.xpath(odd_to_delete_xpath):
                        odd_to_delete.getparent().remove(odd_to_delete)
                    # then by rewriting the xml
                    outfile = open(join(ead_path_test, filename), 'w')
                    outfile.write(ET.tostring(ead_tree, pretty_print=True, encoding="utf-8", xml_declaration=True))
                    outfile.close()
                        
            # if not, don't worry about it, just continue on
            except:
                continue
