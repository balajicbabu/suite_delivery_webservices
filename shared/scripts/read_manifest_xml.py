import xml.etree.cElementTree as etree
import test

def parsexml(local_manifest_file_path):
    test.log("parsexml")
    test.log("local_manifest_file_path : " + local_manifest_file_path)
    xmlDoc = open(local_manifest_file_path, 'r')
    xmlDocData = xmlDoc.read()
    root = etree.XML(xmlDocData)
    videoISRC = root.find('VideoISRC')
    text = videoISRC.text
    print(videoISRC.text)
    return text
