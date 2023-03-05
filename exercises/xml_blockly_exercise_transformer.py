# import OS module
import os
import xml.etree.ElementTree as ET

def makeDisabledLoop(toplevelelement):
    toplevelelement.set('editable', 'true')
    print('disabled found')
    print(toplevelelement.get('type'))
    toplevelelement.set('type','disabled_loop')
    toplevelelement.set('disabled','false')
    print(toplevelelement.get('type'))
    for secondlevelelement in reversed(toplevelelement):
        # if not the statement (inner block) delete
        if '}statement' not in secondlevelelement.tag:
            #   if child.get('name') == 'TIMES':
            toplevelelement.remove(secondlevelelement)
        # if secondlevelelement is statement inner block
        else:
            for statment_child in reversed(secondlevelelement):
                if '}block' in statment_child.tag:
                    statment_child.set('disabled','false')
                    statment_child.set('editable', 'true')
                    statment_child.set('movable','true')
                    for block_children in reversed(statment_child):
                        makeChildrenUneditable(block_children)
            # set everything that is a child of a statement editable (and also the statements)
            setFilteredChildrenEditableValue('true', toplevelelement,'}statement')
            setFilteredChildrenByParentEditableValue('true', toplevelelement,'}statement')
            # make the appending next bit of code editable
            setFilteredChildrenEditableValue('true', toplevelelement,'}next')
            setFilteredChildrenByParentEditableValue('true', toplevelelement,'}next')

def makeChildrenDisabledLoopIfNeeded(element, counter):
    if (counter >= 3):
        return
    if element.get('disabled') == 'true':
        makeDisabledLoop(element)
    counter = counter + 1
    children = reversed(element)
    for child in children:
        makeChildrenDisabledLoopIfNeeded(child, counter)
    return

def makeChildrenUneditable(element):
    children = reversed(element)
    for child in children:
        # print("child found")
        child.set('editable', 'false')
        child.set('movable','false')
        makeChildrenUneditable(child)
    return

def setFilteredChildrenEditableValue(value, element, filterString):
    children = reversed(element)
    for child in children:
        if filterString in child.tag:
            child.set('editable', value)
            child.set('movable',value)
        setFilteredChildrenEditableValue(value, child, filterString)
    return

def setFilteredChildrenByParentEditableValue(value, element, filterString):
    children = reversed(element)
    for child in children:
        if filterString in element.tag:
            child.set('editable', value)
            child.set('movable',value)
        setFilteredChildrenByParentEditableValue(value,child, filterString)
    return
 
# Get the list of all files and directories
path = "./original_xml"
dir_list = os.listdir(path)
 
print("Files and directories in '", path, "' :")

for filename in dir_list:
    print(filename)
    f = open('./original_xml/'+filename, "r")
    original_xml = f.read()
    f = open('./xml/'+filename, "w")
    f.write(original_xml.replace('`','-'))
    f.close()

    mytree = ET.parse('./xml/'+filename)
    myroot = mytree.getroot()

    for toplevelelement in myroot:
        if '}block' in toplevelelement.tag:
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
                    if 'Title: ' in child.text and (toplevelelement.get('type')!='group_title'):
                        child.text = child.text.replace('Title: ','')
                        toplevelelement.set('type','group_title')
                        y = int(toplevelelement.get('y'))
                        # print('Headline'+child.text)
                        # print(y)
                        y = y + 30
                        toplevelelement.set('y',str(y))
                        # print('new y: '+str(y))
                        # Make Headline or Grouptitle comments movable
                        # toplevelelement.set('movable','false')
                        makeChildrenUneditable(toplevelelement)
            if toplevelelement.get('disabled') == 'true':
                makeDisabledLoop(toplevelelement)
            # for everything that is not in the disabled bit
            else:
                # edit disabled piece to be own piece
                makeChildrenDisabledLoopIfNeeded(toplevelelement, 0)
                # set shadows fields and values uneditable
                setFilteredChildrenEditableValue('false', toplevelelement,'}shadow')
                setFilteredChildrenEditableValue('false', toplevelelement,'}field')
                setFilteredChildrenEditableValue('false', toplevelelement,'}value')
                setFilteredChildrenEditableValue('false', toplevelelement,'}block')
                # set everything that is a child of a statement editable (and also the statements)
                setFilteredChildrenEditableValue('true', toplevelelement,'}statement')
                setFilteredChildrenByParentEditableValue('true', toplevelelement,'}statement')
                # make the appending next bit of code editable
                setFilteredChildrenEditableValue('true', toplevelelement,'}next')
                setFilteredChildrenByParentEditableValue('true', toplevelelement,'}next')
            



    mytree.write('./xml/'+filename)
    transformed_f = open('./xml/'+filename, "r")
    transformed_xml = transformed_f.read()
    transformed_f.close()
    final_xml = transformed_xml.replace('ns0:','').replace(':ns0','') #.replace('disabled="true"','disabled="true" movable="false"')
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
                    parents.set('movable','true')
                    child.set('movable','true')


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

