#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import xml.etree.ElementTree as ET
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from lxml import etree
import sys


# In[5]:


#regexes:
p_fn = r'\[fn:fn(\d+)\]' #footnote in running text
p_tbl = r'\[tbl: tb(\d+)\]' #table
p_cptn = r'(?s)\*\_(.*?)\_\*' #caption for figure


# In[3]:


def apply_xslt(xml_path, xslt_path):
    """
    Apply XSLT transformation to an XML file and save the result to a text file.
    """
    xml_tree = etree.parse(xml_path)
    xslt_tree = etree.parse(xslt_path)
    transformer = etree.XSLT(xslt_tree)
    transformed_tree = transformer(xml_tree)
    
    return str(transformed_tree)


# In[4]:


def replace_tables(markup_file, xml_file):
    id_nos = re.findall(r'\[tbl: tb(\d+)\]', markup_file)
    for table_id in id_nos:
        table_id = 'tb' + table_id
        replacement = replace_table(table_id, xml_file)
        markup_file = markup_file.replace('[tbl: ' + table_id + ']', replacement)
    return markup_file


# In[6]:


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


# In[13]:


def main():
    try:
        input_file = sys.argv[1]
        style_file = sys.argv[2]
        
        markdown_file = apply_xslt(input_file, style_file)
        
        #replace tables here
        markdown_file = add_footnotes_bottom(markdown_file, input_file)
        markdown_file = add_fn(markdown_file, input_file)    
            
        with open('markdown.txt', 'w') as final_file:
            final_file.write(markdown_file)
            
    except IndexError:
        print('Please input all the necessary command line variables')


# In[11]:


main()


# In[ ]:




