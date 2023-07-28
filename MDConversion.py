#!/usr/bin/env python
# coding: utf-8

# In[1]:


from lxml import etree
import re
import xml.etree.ElementTree as ET
import sys
from markdownify import markdownify as md


# In[2]:


def main():
    try:
        inp = sys.argv[1]
        style = sys.argv[2]
    #get paths
        with open('markdown.txt', 'w') as output_file:
            output_file.write(do_it_all(inp, style))
    except IndexError:
        print('please input all the necessary command line variables')


# In[3]:


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


# In[5]:


def extract_table_wrap_elements(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    table_wrap_dict = {}
    for table_wrap in root.findall(".//table-wrap"):
        table_wrap_id = table_wrap.attrib.get("id")
        if table_wrap_id:
            table_wrap_dict[table_wrap_id] = ET.tostring(table_wrap, encoding="unicode")

    return table_wrap_dict


# In[24]:


from bs4 import BeautifulSoup

def html_table_to_markdown(html_table):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_table, 'html.parser')

    # Extract the table header (thead) and rows (tbody)
    table_header = soup.thead
    table_rows = soup.tbody.find_all('tr')

    # Initialize the markdown table
    markdown_table = ""

    # Process the table header
    if table_header:
        headers = [th.text.strip() for th in table_header.find_all('th')]
        markdown_table += "| " + " | ".join(headers) + " |\n"
        markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    # Process the table rows
    for row in table_rows:
        cells = [td.text.strip() for td in row.find_all(['td', 'th'])]
        markdown_table += "| " + " | ".join(cells) + " |\n"

    return markdown_table


# In[6]:


def get_table_by_id(table_id, xmlfile):
    table_dict = extract_table_wrap_elements(xmlfile)
    return table_dict[table_id]


# In[46]:


def replace_table(table_id, xmlfile):
    tablepattern = r'<table>[\S\s]*<\/table>'
    labelpattern = r'<label>.*<\/label>'
    captionpattern = r'<caption><p>.*<\/p><\/caption>'
    og_table = get_table_by_id(table_id, xmlfile)
    new_table = og_table
    
    #fix the label
    label = re.search(labelpattern, og_table).group()
    print(label)
    new_label = label.replace('<label>', '**')
    new_label = new_label.replace('</label>', '**')
    new_table = new_table.replace(label, new_label)
    
    #fix the caption
    caption = re.search(captionpattern, og_table).group()
    print(caption)
    new_caption = caption.replace('<caption><p>', '_')
    new_caption = new_caption.replace('</p></caption>', '_')
    new_table = new_table.replace(caption, new_caption)
    
    #fix the table
    tabeldeel = re.search(tablepattern, og_table).group()
    new_tabeldeel = html_table_to_markdown(tabeldeel)
    new_table = new_table.replace(tabeldeel, new_tabeldeel)
    new_table = new_table.replace('</table-wrap>', '')
    new_table = new_table.replace(re.search(r'<table-wrap .*>', new_table).group(), '')
    
    return new_table


# In[45]:


print(replace_table('tb001', 'bmgn.xml'))


# **Tabel 1.**
# _Overzicht van de verdeling van charters over verschillende archiefdiensten._
# | Aantal charters | Aantal diensten | Totaal aantal charters | Procent |
# | --- | --- | --- | --- |
# | > 20.000 | 2 | 46.629 | 26 |
# | 10.000-20.000 | 3 | 45.079 | 25 |
# | 5.000-10.000 | 4 | 28.794 | 16 |
# | 1.000-5.000 | 13 | 45.687 | 25 |
# | 100-1.000 | 30 | 11.124 | 6 |
# | <100 | 32 | 941 | 0,5 |

# In[47]:


def replace_tables(markupfile, xmlfile):
    id_nos = re.findall(p_tbl, markupfile)
    for table in id_nos:
        tblid = 'tb' + table
        #print(table)
        replacement = replace_table(tblid, xmlfile)
        #print()
        #print(replacement)
        tobereplaced = '[tbl: ' + tblid + ']'
        markupfile = markupfile.replace(tobereplaced, replacement)
    return markupfile


# In[10]:


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


# In[11]:


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


# In[12]:


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


# In[14]:


main()


# | > 20.000 | 2 | 46.629 | 26 |
# | 10.000-20.000 | 3 | 45.079 | 25 |
# | 5.000-10.000 | 4 | 28.794 | 16 |
# | 1.000-5.000 | 13 | 45.687 | 25 |
# | 100-1.000 | 30 | 11.124 | 6 |
# | <100 | 32 | 941 | 0,5 |

# In[ ]:




