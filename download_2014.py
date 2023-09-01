import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup as BS
import math
import time

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


con = sqlite3.connect("db.sqlite")
cur = con.cursor()

year = 2014
print(year)

columns = []
uni_id_list = []
uni = []

start = time.time()

ids = [1, 11, 111, 111126, 111185, 111186, 111187, 111188, 1112, 111233, 112, 112814, 113, 114, 1158, 116, 117, 118, 119, 12, 122, 123, 124, 126, 127, 129, 13, 131, 132, 133, 134, 137, 138, 14, 141, 143, 144, 146, 147, 148, 149, 15, 151, 1519, 152, 1527, 153, 154, 1544, 155, 1556, 1558, 156, 1562, 1563, 1564, 1566, 1569, 157, 1572, 1574, 1576, 1577, 1578, 1579, 158, 1581, 1582, 1584, 1585, 1586, 1587, 1588, 1589, 159, 1591, 1593, 1594, 1595, 1596, 1597, 1599, 16, 161, 1612, 1616, 1618, 1619, 162, 1621, 1622, 1624, 1626, 163, 1631, 1632, 1633, 1634, 1635, 1636, 1637, 1638, 1639, 164, 1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648, 1649, 165, 1651, 1652, 1653, 1654, 1655, 1656, 1657, 1658, 1659, 166, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668, 1669, 167, 1671, 1672, 1673, 1674, 1675, 1676, 1677, 1678, 1679, 168, 1681, 1682, 1683, 1685, 1686, 1687, 1688, 1689, 169, 1691, 1693, 1694, 1695, 1696, 1697, 1698, 1699, 17, 171, 1711, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 172, 1722, 1723, 1724, 1725, 1727, 1728, 1729, 173, 1731, 1734, 1735, 1736, 1737, 1738, 1739, 174, 1741, 1742, 1743, 1745, 1747, 1748, 1749, 175, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 176, 1761, 1762, 1763, 1764, 1765, 1766, 1767, 1768, 177, 1771, 1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 178, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 179, 1791, 1792, 1793, 1794, 1795, 1796, 1798, 1799, 18, 181, 1812, 1816, 1817, 1818, 1819, 182, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 183, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 184, 1841, 1842, 1843, 1845, 1846, 1847, 1848, 1849, 185, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 186, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 187, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 188, 1881, 1882, 1883, 1885, 1886, 1887, 1888, 1889, 189, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 19, 191, 1911, 1912, 1913, 1915, 1916, 1917, 1918, 1919, 192, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 193, 1932, 1933, 1935, 1937, 1938, 194, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 195, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 196, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 197, 1971, 1972, 1973, 1975, 1976, 1977, 1978, 1979, 198, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 199, 1991, 1992, 1994, 1995, 1996, 1997, 1998, 1999, 2, 21, 211, 212, 213, 214, 215, 2151, 216, 217, 218, 2183, 2189, 219, 2197, 2198, 22, 222, 223, 227, 228, 229, 23, 231, 232, 233, 234, 236, 237, 239, 24, 241, 242, 243, 245, 247, 249, 25, 251, 252, 253, 254, 255, 257, 258, 26, 261, 265, 266, 267, 269, 27, 271, 272, 273, 276, 278, 28, 281, 282, 283, 284, 286, 287, 288, 29, 291, 292, 293, 294, 295, 296, 297, 298, 299, 3, 31, 311, 312, 313, 315, 317, 318, 319, 32, 321, 322, 323, 324, 325, 326, 327, 328, 329, 33, 331, 333, 334, 336, 337, 34, 341, 342, 35, 36, 38, 39, 4, 41, 42, 43, 44, 45, 46, 48, 49, 5, 51, 52, 53, 54, 55, 555118, 5572, 56, 5616, 5618, 5625, 5631, 5635, 5636, 5637, 5664, 57, 58, 59, 6, 61, 62, 63, 64, 66, 67, 7, 72, 76, 77, 78, 79, 8, 81, 82, 83, 84, 85, 86, 87, 88, 9, 91, 92, 93, 95, 96, 97, 99]

for uni_id in ids:  # through unis
    uni_url = 'https://monitoring.miccedu.ru/iam/'+str(year)+'/materials/inst_'+str(uni_id)'.htm'
    r = session.get(uni_url)
    r.encoding = r.apparent_encoding
    uni_page = BS(r.content, features = 'lxml')
    name, address, ministry, website, owner = '', '', '', '', ''

    for indicator in uni_page.select('table#info tr'): # инфа
        fields = []
        for td in indicator.select('td'):
            fields.append(td.get_text(separator = ', '))
        if fields[0] == 'Наименование образовательной организации' and name == '':
            name = fields[1]
        elif fields[0] == 'Регион,, адрес':
            address = fields[1]
        elif fields[0] == 'Ведомственная принадлежность':
            ministry = fields[1]
        elif fields[0] == 'web-сайт':
            website = fields[1]
        elif fields[0] == 'Учредитель(и)':
            owner = fields[1]
    cur.execute('INSERT OR IGNORE INTO universities(uid, name, address, ministry, website, owner, fdid) VALUES(?,?,?,?,?,?, (SELECT fdid FROM federal_districts WHERE name = ?))', (uni_id, name, address, ministry, website, owner, regionname))
    con.commit()

    for indicator in uni_page.select('table#analis_dop tr'):  # доппоказатели
        fields = []
        td_num = len(indicator.find_all('td'))
        if td_num < 3:
            continue
        number, name, unit, value = '', '', '', 0
        for td in indicator.select('td'):
            fields.append(td.get_text(separator=' '))
        if fields[1] == 'Наименование показателя' or fields[1] == '2':
            continue
        if td_num == 4:
            cur.execute('INSERT OR IGNORE INTO indicators(number, name, unit) VALUES(?,?,?)',
                (fields[0], fields[1], fields[2]))
            value = fields[3].replace(' ','').replace(',','.')
            if value == 'да':
                value = 1
            elif value == 'нет':
                value = 0
            cur.execute('''INSERT INTO data(uid, iid, year, value) VALUES(?,
               (SELECT iid FROM indicators WHERE name = ?), ?, ?)''', (uni_id, fields[1], year, value))
        if td_num == 3:
            cur.execute('INSERT OR IGNORE INTO indicators(name, unit) VALUES(?,?)',
                (fields[0], fields[1]))
            value = fields[2].replace(' ','').replace(',','.')
            cur.execute('''INSERT INTO data(uid, iid, year, value) VALUES(?,
               (SELECT iid FROM indicators WHERE name = ?), ?, ?)''', (uni_id, fields[0], year, value))
    con.commit()

    for indicator in uni_page.select('table.napde tr'):  # мониторинг
        fields = []
        td_num = len(indicator.find_all('td'))
        if td_num == 4:  # skip headings and not full rows
            for td in indicator.select('td'):
                fields.append(td.get_text(separator=' '))
            if fields[1] == 'Наименование показателя' or fields[1] == '2':
                continue
            cur.execute('INSERT OR IGNORE INTO indicators(number, name, unit) VALUES(?,?,?)',
                (fields[0], fields[1], fields[2]))
            value = fields[3].replace(' ','').replace(',','.')
            cur.execute('''INSERT INTO data(uid, iid, year, value) VALUES(?,
               (SELECT iid FROM indicators WHERE name = ?), ?, ?)''', (uni_id, fields[1], year, value))
    con.commit()

    for indicator in uni_page.select('table#analis_reg tr'):  # УГНС
        fields = []
        td_num = len(indicator.find_all('td'))
        if td_num < 4:  # skip headings and not full rows
            continue;
        for td in indicator.select('td'):
            fields.append(td.get_text(separator=' '))
        if fields[0] == 'Реализуемые  УГН(С)' or fields[0] == 'Реализуемые УГН(С)':
            continue
        cur.execute('INSERT OR IGNORE INTO ugn(name) VALUES (?)', (fields[0],))
        value = fields[1].replace(' ','').replace(',','.')
        cur.execute('''INSERT INTO uni_ugn(ugnid, uid, year, people) VALUES((SELECT ugnid FROM ugn WHERE name = ?), ?, ?, ?)''', (fields[0], uni_id, year, value))
    con.commit()

con.close()