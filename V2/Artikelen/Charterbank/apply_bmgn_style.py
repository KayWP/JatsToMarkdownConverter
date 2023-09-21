#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys


# In[11]:


def main():
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python apply_bmgn_style.py <input_html_file>")
        sys.exit(1)

    # Get the input HTML file name from the command line argument
    input_file = sys.argv[1]

    try:
        # Open the HTML file for reading
        with open(input_file, 'r', encoding="utf8") as file:
            # Read the content of the file
            html_content = file.read()

        # Perform your edits on the HTML content here
        # For example, you can replace some text
        edited_html_content = style_replace(html_content)

        # Open the HTML file for writing (this will overwrite the original file)
        with open(input_file, 'w', encoding="utf8") as file:
            # Write the edited content back to the file
            file.write(edited_html_content)

        print("HTML file has been successfully edited.")

    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# In[9]:


def style_replace(htmlfile):
    replace_dictionary = {'--jp-content-heading-font-weight: 500;':'--jp-content-heading-font-weight: bold;',
                         '--jp-content-font-size1: 14px;':'--jp-content-font-size1: 13px;',
                         '--jp-content-font-size3: 1.44em;':'--jp-content-font-size3: 13px;',
                         '--jp-content-font-size4: 1.728em;':'--jp-content-font-size4: 14px;',
                         '--jp-content-font-size5: 2.0736em;':'--jp-content-font-size5: 18px;'}
    output = htmlfile
    for replacement in replace_dictionary.keys():
        output = output.replace(replacement, replace_dictionary[replacement])
        
    return output


# In[6]:


main()


# In[ ]:




