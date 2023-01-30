# import OS module
import os
import xml.etree.ElementTree as ET

 
# Get the list of all files and directories
path = "./original_xml"
dir_list = os.listdir(path)
 
print("Files and directories in '", path, "' :")

for filename in dir_list:
    f = open('./original_xml/'+filename, "r")
    original_xml = f.read()
    f = open('./xml/'+filename, "w")
    f.write(original_xml.replace('`','-'))
    f.close()

    mytree = ET.parse('./xml/'+filename)
    myroot = mytree.getroot()
    counter1 = 0
    count = 0
    for toplevelelement in myroot:
        if '}block' in toplevelelement.tag:
            counter1 += 1
            # Make lower level BLOCK-blocks not editable or deletable
            #original_xml.replace("bock ", "block editable="false" deletable="false" ")
            #original_xml.replace("shadow ", "shadow editable="false" ")
            toplevelelement.set('editable', 'false')
            toplevelelement.set('deletable', 'false')
            toplevelelement.set('contextMenu','false')
            toplevelelement.set('enableContextMenu','false')
            # Make all FIELD-blocks that supposed to be headlines to be seen as such
            for child in toplevelelement.findall('.//{https://developers.google.com/blockly/xml}field'):
                if child.text != None:
                    # Headline or Grouptitle comments as new block called group_title
                    if 'Title: ' in child.text:
                        count += 1
                        child.text = child.text.replace('Title: ','')
                        toplevelelement.set('type','group_title')
                        # Make Headline or Grouptitle comments movable
                        # toplevelelement.set('movable','false')

    counter2 = 0
    # set all top level BLOCK-blocks that are editable to be not movable or editable or deletable
    for block in myroot.findall('.//{https://developers.google.com/blockly/xml}block'):
        if block.get('editable') != 'false':
            counter2 += 1
            block.set('movable','false')
            block.set('editable', 'false')
            block.set('deletable', 'false')
            block.set('contextMenu','false')
            block.set('enableContextMenu','false')

    for block in myroot.findall('.//{https://developers.google.com/blockly/xml}field'):
        block.set('contextMenu','false')
        block.set('enableContextMenu','false')

    for block in myroot.findall('.//{https://developers.google.com/blockly/xml}value'):
        block.set('contextMenu','false')
        block.set('enableContextMenu','false')
    
    # set all shadow-blocks in the lower levels to not be deletable
    for shadow in myroot.findall('.//{https://developers.google.com/blockly/xml}shadow'):
        shadow.set('deletable', 'false')
        shadow.set('contextMenu','false')
        shadow.set('enableContextMenu','false')

    print('renamed blocks '+str(count))
    print(counter1)
    print(counter2)

    mytree.write('./xml/'+filename)
    transformed_f = open('./xml/'+filename, "r")
    # print(f.read())
    transformed_xml = transformed_f.read()
    transformed_f.close()
    final_xml = transformed_xml.replace('ns0:','').replace(':ns0','').replace('disabled="true"','disabled="true" movable="false"')
    transformed_f = open('./xml/'+filename, "w")
    transformed_f.write(final_xml)
    transformed_f.close()
    # BasetitleXML    

    # Create only titles Files
    mytree = ET.parse('./xml/'+filename)
    myroot = mytree.getroot()
    def iterator(parents, nested=False):
        for child in reversed(parents):
            if nested:
                if len(child) >= 1:
                    iterator(child)
            if child.attrib.get('type', None) != None:
                parents.set('contextMenu','false')
                child.set('contextMenu','false')
                parents.set('enableContextMenu','false')
                child.set('enableContextMenu','false')

                if 'group' not in child.attrib['type']:  # Add your entire condition here
                    parents.remove(child)
                else:
                    # Make Headline or Grouptitle comments movable
                    parents.set('movable','false')
                    child.set('movable','false')


    iterator(myroot, nested=True)

    mytree.write('./xml_titles/'+filename)
    transformed_titles_f = open('./xml_titles/'+filename, "r")
    transformed_titles_xml = transformed_titles_f.read()
    transformed_titles_f.close()
    final_xml_titles = transformed_titles_xml.replace('ns0:','').replace(':ns0','')
    # print(final_xml_titles)
    transformed_titles_f = open('./xml_titles/'+filename, "w")
    transformed_titles_f.write(final_xml_titles)
    transformed_titles_f.close()

