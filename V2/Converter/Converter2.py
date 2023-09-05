#!/usr/bin/env python
# coding: utf-8

# In[2]:


import re
import xml.etree.ElementTree as ET
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from lxml import etree
import sys


# In[25]:


#regexes:
p_fn = r'\[fn:fn(\d+)\]' #footnote in running text
p_tbl = r'\[tbl: tb(\d+)\]' #table
p_cptn = r'(?s)\*\_(.*?)\_\*' #caption for figures
p_url = r'https?:\/\/[^\s()]+'


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


# In[55]:


def find_article_metadata_bmgn(xml):
    #this function is specific to the BMGN structure. Not sure how well it will work for other journals
    xml_tree = etree.parse(xml)
    article_title = xml_tree.find('//article-title')
    article_subtitle = xml_tree.find('//subtitle')
    author_names = []
    for contrib in xml_tree.xpath('//contrib[@contrib-type="author"]'):
        surname = contrib.find('.//surname').text
        given_names = contrib.find('.//given-names').text
        full_name = f"{given_names} {surname}"
        author_names.append(full_name)
        
    doi_element = xml_tree.find('.//article-id[@pub-id-type="doi"]')
    
    return article_title.text, article_subtitle.text, author_names, doi_element.text


# In[54]:


def replace_title_bmgn(markdown, xml):
    title_info = find_article_metadata_bmgn(xml)
    title = f"#{title_info[0]} \n##{title_info[1]} \n[{title_info[3]}]({title_info[3]})\n\n"
    for author in title_info[2]:
        title = title + f"{author}\n"
    markdown = markdown.split('### Inleiding')[1] #dit moet netter, je kunt hier niet van uitgaan. Body?
    return title + '\n' + markdown


# In[51]:





# In[4]:


def replace_tables(markup_file, xml_file):
    id_nos = re.findall(r'\[tbl: tb(\d+)\]', markup_file)
    for table_id in id_nos:
        table_id = 'tb' + table_id
        replacement = replace_table(table_id, xml_file)
        markup_file = markup_file.replace('[tbl: ' + table_id + ']', replacement)
    return markup_file


# In[27]:


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
        fntxt = activate_urls(fntxt)
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


# In[28]:


def activate_urls(text):
    urls = re.findall(p_url, text)
    formatted_text = text
    for url in urls:
        url = url.strip('.')
        markdown_link = f'[{url}]({url})'
        formatted_text = formatted_text.replace(url, markdown_link)
    return formatted_text


# In[53]:


def main():
    try:
        input_file = sys.argv[1]
        style_file = sys.argv[2]
            
    except IndexError:
        print('Please input all the necessary command line variables')
        
    markdown_file = apply_xslt(input_file, style_file)
        
        #replace tables here
    markdown_file = add_footnotes_bottom(markdown_file, input_file)
    markdown_file = add_fn(markdown_file, input_file)
    markdown_file = replace_title_bmgn(markdown_file, input_file)
            
    with open('markdown.txt', 'w') as final_file:
        final_file.write(markdown_file)


# In[11]:


main()


# In[ ]:




