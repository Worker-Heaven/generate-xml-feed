import requests
from lxml import html
import xml.etree.ElementTree as ET
import datetime

file_name = 'carsunlimitedmalta_feed.xml'

site_url = "https://www.carsunlimitedmalta.com/search-results/page/1/?search_order=DESC&search_orderby=title&manufacturer_level1=any&manufacturer_level2=any&body_type=any&reg_number&transmission=any&dealer_location=any&search_nonce=9a0b956dc6"

special_items = [
    'Dealer Location:',
    'Manufacturer:',
    'Body Type:',
]

infoDic = {
    'StockNumber': 'Stock Number #:',
    'DealerLocation': 'Dealer Location:',
    'Manufacturer': 'Manufacturer:',
    'BodyType': 'Body Type:',
    'Status': 'Status:',
    'YearBuilt': 'Year Built:',
    'EngineSize': 'Engine Size:',
    'Transmission': 'Transmission:',
    'ExteriorColor': 'Exterior Color:',
    'FuelType': 'Fuel Type:',
    'Doors': 'Doors:',
    'StandardSeating': 'Standard Seating:',
    'SteeringType': 'Steering Type:',
}

root = ET.Element('feed')
titleElement = ET.SubElement(root, 'title')
linkElement = ET.SubElement(root, 'link')
descriptionElement = ET.SubElement(root, 'description')
lastBuildDateElement = ET.SubElement(root, 'lastBuildDate')
itemsElement = ET.SubElement(root, 'items')

titleElement.text = 'Feeds'
linkElement.text = 'https://www.carsunlimitedmalta.com/'
descriptionElement.text = 'Generate the feed from https://www.carsunlimitedmalta.com/'
lastBuildDateElement.text = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

def start_scraping():
    response = requests.get(site_url)
    page = html.fromstring(response.text)

    contents = page.xpath('//div[@id="main-content"]//ul//li')

    for row in contents:
        title = row.xpath('.//h3[@class="entry-title"]/a/text()')
        link = row.xpath('.//h3[@class="entry-title"]/a/@href')
        
        if len(title) > 0:
            resultDic = {
                'title': title[0],
                'link': link[0],
            }

            detailed_response = requests.get(link[0])
            detailed_page = html.fromstring(detailed_response.text)

            image_links = detailed_page.xpath('//ul[@id="bx-pager"]//img/@src')
            
            # NOTE: Add image links
            resultDic['images'] = image_links

            detailed_content = detailed_page.xpath('//div[@id="tab-target-details"]//ul//li')

            print(title[0], link[0])

            for detailed_row in detailed_content:
                item = detailed_row.xpath('.//strong/text()')

                if (len(item) > 0):
                    if (item[0].strip() in special_items):
                        info = detailed_row.xpath('.//span//a/text()')
                    else:
                        info = detailed_row.xpath('.//span/text()')

                    # NOTE: Add detailed infomation about car
                    resultDic[item[0].strip()] = info[0].strip()
        
            print(resultDic)

            item = ET.Element('item')
            StockNumber = ET.SubElement(item, 'StockNumber')
            DealerLocation = ET.SubElement(item, 'DealerLocation')
            Manufacturer = ET.SubElement(item, 'Manufacturer')
            BodyType = ET.SubElement(item, 'BodyType')
            Status = ET.SubElement(item, 'Status')
            YearBuilt = ET.SubElement(item, 'YearBuilt')
            EngineSize = ET.SubElement(item, 'EngineSize')
            Transmission = ET.SubElement(item, 'Transmission')
            ExteriorColor = ET.SubElement(item, 'ExteriorColor')
            FuelType = ET.SubElement(item, 'FuelType')
            Doors = ET.SubElement(item, 'Doors')
            StandardSeating = ET.SubElement(item, 'StandardSeating')
            SteeringType = ET.SubElement(item, 'SteeringType')

            StockNumber.text = resultDic.get(infoDic['StockNumber'])
            DealerLocation.text = resultDic.get(infoDic['DealerLocation'])
            Manufacturer.text = resultDic.get(infoDic['Manufacturer'])
            BodyType.text = resultDic.get(infoDic['BodyType'])
            Status.text = resultDic.get(infoDic['Status'])
            YearBuilt.text = resultDic.get(infoDic['YearBuilt'])
            EngineSize.text = resultDic.get(infoDic['EngineSize'])
            Transmission.text = resultDic.get(infoDic['Transmission'])
            ExteriorColor.text = resultDic.get(infoDic['ExteriorColor'])
            FuelType.text = resultDic.get(infoDic['FuelType'])
            Doors.text = resultDic.get(infoDic['Doors'])
            StandardSeating.text = resultDic.get(infoDic['StandardSeating'])
            SteeringType.text = resultDic.get(infoDic['SteeringType'])

            itemsElement.append(item)
    
    tree = ET.ElementTree(root)
    tree.write(file_name)

if (__name__ == '__main__'):
    start_scraping()