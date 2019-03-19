import xml.etree.ElementTree as ET
import datetime

filename = "test_xml.xml"

root = ET.Element('feed')
titleElement = ET.SubElement(root, 'title')
linkElement = ET.SubElement(root, 'link')
descriptionElement = ET.SubElement(root, 'description')
lastBuildDateElement = ET.SubElement(root, 'lastBuildDate')
itemsElement = ET.SubElement(root, 'items')

titleElement.text = 'Feeds'
linkElement.text = str([
    'https://www.carsunlimitedmalta.com/',
    'https://www.carsunlimitedmalta.com/',
])
descriptionElement.text = 'Generate the feed from https://www.carsunlimitedmalta.com/'
lastBuildDateElement.text = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

ET.dump(root)

# a = ET.Element('a')
# b = ET.SubElement(a, 'b')
# c = ET.SubElement(a, 'c')
# d = ET.SubElement(c, 'd')

tree = ET.ElementTree(root)

tree.write(filename)
