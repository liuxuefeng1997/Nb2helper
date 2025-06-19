import xmltodict


def xml_load(filePath, encoding="utf8") -> dict | None:
    """
    加载XML文件
    :param filePath: XML文件路径
    :param encoding: 编码类型
    """
    with open(filePath, 'r', encoding=encoding) as f:
        xml_data = f.read()
        f.close()
    return xmltodict.parse(xml_data)


def xml_loads(xml_data) -> dict | None:
    """
    加载XML文本
    :param xml_data: XML文本数据
    """
    return xmltodict.parse(xml_data)
