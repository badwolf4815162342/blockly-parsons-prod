# import OS module
import os, sys
import xml.etree.ElementTree as ET
import json
 
# Get the list of all files and directories
path = "./original_xml"
dir_list = os.listdir(path)
 
print("Files and directories in '", path, "' :")
 
# prints all files
print(dir_list)

for filename in dir_list:
    f = open('./original_xml/'+filename, "r")
    original_xml = f.read()
    f = open('./xml/'+filename, "w")
    f.write(original_xml.replace('`','-'))
    f.close()

    #original_xml.replace("bock ", "block editable="false" deletable="false" ")
    #original_xml.replace("shadow ", "shadow editable="false" ")

    mytree = ET.parse('./xml/'+filename)
    myroot = mytree.getroot()
    counter1 = 0
    count = 0
    for toplevelelement in myroot:
        if '}block' in toplevelelement.tag:
            counter1 += 1
            toplevelelement.set('editable', 'false')
            toplevelelement.set('deletable', 'false')
            for child in toplevelelement.findall('.//{https://developers.google.com/blockly/xml}field'):
                print(child.tag)
                if child.text != None:
                    if 'Title: ' in child.text:
                        print('Text '+child.text)
                        count += 1
                        child.text = child.text.replace('Title: ','')
                        toplevelelement.set('type','group_title')
                        toplevelelement.set('movable','false')
        #for secondlevel in toplevelelement:
            #print(secondlevel)
        #    for thirdlevel in secondlevel:
                #print(thirdlevel)

    counter2 = 0
    for block in myroot.findall('.//{https://developers.google.com/blockly/xml}block'):
        if block.get('editable') != 'false':
            counter2 += 1
            block.set('movable','false')
            block.set('editable', 'false')
            block.set('deletable', 'false')

    

    for shadow in myroot.findall('.//{https://developers.google.com/blockly/xml}shadow'):
        shadow.set('deletable', 'false')

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