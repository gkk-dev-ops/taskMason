import xml.etree.ElementTree as ET
from xml.dom import minidom
import getpass
import os
import argparse

def replace_username_in_plist(plist_path):
    try:
        # Parse the existing .plist XML file
        tree = ET.parse(plist_path)
        root = tree.getroot()

        # Find the dictionary
        dictionary = root.find('dict')

        # Initialize keys and values list
        keys = []
        values = []

        # Populate keys and values
        for elem in dictionary:
            if elem.tag == 'key':
                keys.append(elem)
            else:
                values.append(elem)

        # Go through all key-value pairs to find the "Label"
        for key, value in zip(keys, values):
            if key.text == 'Label':
                # Replace 'yourusername' with the current username
                old_text = value.text
                username = getpass.getuser()
                new_text = old_text.replace('yourusername', username)
                 # GPT sometimes adds spaces between characters, which is illegal for launchctl process name
                new_text = new_text.replace(' ', '')
                value.text = new_text
                print(new_text)

        # Convert the modified XML content to a string
        xml_str = ET.tostring(root, encoding='UTF-8')
        xml_str = xml_str.replace(b'> <', b'><')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="\t", newl="\n")

        # Re-add the XML declaration and DOCTYPE
        lines = [
            b'<?xml version="1.0" encoding="UTF-8"?>\n',
            b'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
            pretty_xml.encode('utf-8')
        ]
        new_lines = []
        # filter out duplicate XML declaration
        for line in lines:
            if b'<?xml version="1.0" ?>' in line:
                new_line = line.replace(b'<?xml version="1.0" ?>', b'')
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        lines = new_lines
        print(lines)

        # Write back to the file
        with open(plist_path, 'wb') as f:
            for line in lines:
                f.write(line)
        print(f"Replaced 'yourusername' with current username in {plist_path}.")
    except ET.ParseError as e:
        print(f"Error parsing the XML file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replace "yourusername" with the current username in a .plist file.')
    parser.add_argument('plist_path', help='Path to the .plist file')

    args = parser.parse_args()
    plist_path = args.plist_path

    if os.path.exists(plist_path):
        replace_username_in_plist(plist_path)
    else:
        print(f"The file {plist_path} does not exist.")
