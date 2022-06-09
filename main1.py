import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np
from os import path, makedirs

x = np.linspace(-100, 100, 10**3)
y = np.cos(x)*np.exp(-((x-np.pi)**2))


data = ET.Element('data')

for i in range(x.size):

    data_i = ET.SubElement(data, 'row')
    _x = ET.SubElement(data_i, 'x')
    _x.text = str(x[i])
    _y = ET.SubElement(data_i, 'y')
    _y.text = str(y[i])


xml_data = ET.ElementTree(data)

if not path.exists('results'):
    makedirs('results')

with open("results/Res.xml", 'wb') as out:
    xml_data.write(out, encoding='utf-8')
    out.close()

plt.plot(x, y)
plt.show()