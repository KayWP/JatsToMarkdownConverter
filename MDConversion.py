#!/usr/bin/env python
# coding: utf-8

# In[63]:


from lxml import etree
import re
import xml.etree.ElementTree as ET
import sys


# In[65]:


def main():
    try:
        inp = sys.argv[1]
        style = sys.argv[2]
    #get paths
        with open('markdown.txt', 'w') as output_file:
            output_file.write(do_it_all(inp, style))
    except IndexError:
        print('please input all the necessary command line variables')


# In[56]:


def apply_xslt(xml_path, xslt_path, output_path):
    # Load the XML and XSLT files
    xml_tree = etree.parse(xml_path)
    xslt_tree = etree.parse(xslt_path)

    # Create the XSLT transformer
    transformer = etree.XSLT(xslt_tree)

    # Apply the XSLT transformation to the XML
    transformed_tree = transformer(xml_tree)

    # Save the result as a .txt file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(str(transformed_tree))


# In[4]:


#regexes:
p_fn = r'\[fn:fn(\d+)\]' #footnote in running text
p_tbl = r'\[tbl: tb(\d+)\]' #table
p_cptn = r'(?s)\*\_(.*?)\_\*' #caption for figure


# In[58]:


def extract_table_wrap_elements(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    table_wrap_dict = {}
    for table_wrap in root.findall(".//table-wrap"):
        table_wrap_id = table_wrap.attrib.get("id")
        if table_wrap_id:
            table_wrap_dict[table_wrap_id] = ET.tostring(table_wrap, encoding="unicode")

    return table_wrap_dict


# In[6]:


def get_table_by_id(table_id, xmlfile):
    table_dict = extract_table_wrap_elements(xmlfile)
    return table_dict[table_id]


# In[7]:


def replace_tables(markupfile, xmlfile):
    id_nos = re.findall(p_tbl, markupfile)
    for table in id_nos:
        tblid = 'tb' + table
        #print(table)
        replacement = get_table_by_id(tblid, xmlfile)
        #print()
        #print(replacement)
        tobereplaced = '[tbl: ' + tblid + ']'
        markupfile = markupfile.replace(tobereplaced, replacement)
    return markupfile


# In[60]:


def get_text_recursively(element):
    text = element.text or ""
    for child in element:
        text += get_text_recursively(child)
        text += child.tail or ""
    return text

def extract_fn_contents(xml_file):
    # Initialize an empty dictionary to store the extracted content
    fn_dict = {}

    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find all <fn> elements within the <fn-group>
    for fn in root.findall('.//fn-group/fn'):
        fn_id = fn.get('id')  # Get the fn id
        fn_label = fn.find('label').text  # Get the fn label
        fn_content = get_text_recursively(fn.find('p'))  # Get the fn content

        # Store the content in the dictionary using the label as the key
        fn_dict[fn_label] = fn_content

    return fn_dict


# In[49]:


def add_footnotes_bottom(txt, basexml):
    footnote_list = extract_fn_contents(basexml)
    for fn in footnote_list.keys():
        fnno = fn
        fntxt = footnote_list[fn]
        fnformula = "<p><a href=\"#_ftnref"+ fnno +'" name="_ftn' + fnno + '">[' + fnno +'] </a>' + fntxt + '</p>'
        txt += '\n'
        txt += '\n'
        txt += fnformula
    return txt


# In[61]:


def add_fn(txt, xmlfile):
    footnote_list = extract_fn_contents(xmlfile)
    for fn in footnote_list.keys():
        fnid = 'fn' + fn
        #print(table)
        replacement = '<a href="#_ftn' + fn + '" name="_ftnref' + fn + '">[' + fn +  ']</a>'
        #print()
        #print(replacement)
        tobereplaced = '[fn:' + fnid + ']'
        #print(tobereplaced)
        txt = txt.replace(tobereplaced, replacement)
    return txt


# In[2]:


def do_it_all(input_path, style_path):
    p_fn = r'\[fn:fn(\d+)\]' #footnote in running text
    p_tbl = r'\[tbl: tb(\d+)\]' #table
    p_cptn = r'(?s)\*\_(.*?)\_\*' #caption for figure
    apply_xslt(input_path, style_path, 'temp.txt')
    with open('temp.txt', 'r', encoding='utf-8') as file:
    # Read the entire content of the file
        markdownfile = file.read()
    markdownfile = replace_tables(markdownfile, input_path)
    markdownfile = add_footnotes_bottom(markdownfile, input_path)
    markdownfile = add_fn(markdownfile, input_path)
    
    return markdownfile


# In[ ]:


main()


# 

# In[ ]:




