import re
import requests
from bs4 import BeautifulSoup
import arg_list_parser

def scrape_sections():
    response = requests.get('http://codingbat.com/java')
    response.raise_for_status()
    sections = re.findall('/java/([A-Z]+[a-z]*-[0-9])', response.text)
    return sections

def get_pids_names(sec_name):
    response = requests.get(f'http://codingbat.com/java/{sec_name}')
    response.raise_for_status()
    pids = re.findall('/prob/(p[0-9]*)', response.text)
    names = re.findall('/prob/p[0-9]*\'>([^<]*)', response.text)
    return (pids, names)

def get_bat(pid):
    response = requests.get(f'http://codingbat.com/prob/{pid}')
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser').select('#ace_div')[0].text

def get_return_type(text):
    my_reg = re.search('(public|private|protected) ((static|final) )?([0-9a-zA-Z<>\[\]]*)', text)
    if my_reg:
        return my_reg.group(4)
    else:
        return 'UnhandledType'

#re.search('(Map<[A-Z]*[a-z]+, [A-Z]*[a-z]+>)', deez_nutz)

def get_invocation_types(text):
    inner = text[text.index('(') + 1:text.index(')')].split(', ')
    #Do NOT rearrange the items in generic_type_list
    generic_type_list = [
                         'List<Integer>',
                         'List<String>',
                         'List<char>',
                         'List<boolean>',
                         'int[]',
                         'boolean[]',
                         'String[]',
                         'float[]',
                         'String',
                         'char[]',
                         'boolean',
                         'float',
                         'int',
                         'char',
                         'List',
                         'UnhandledType']
    local_type_list = []
    for parameter in inner:
        for item in generic_type_list:
            if parameter[0:len(item)] in generic_type_list:
                local_type_list.append(parameter[0:len(item)])
                break
    return local_type_list

def generate_return(type):
    generic_return_dict = {'int': 'return 0;',
                           'String': 'return null;',
                           'String[]': 'return new String[]{};',
                           'int[]': 'return new int[]{};',
                           'boolean': 'return true;',
                           'List<Integer>': 'return new ArrayList<Integer>();',
                           'List<String>': 'return new ArrayList<String>();',
                           'List<char>': 'return new ArrayList<char>();',
                           'List<boolean>': 'return null);',
                           'char': 'return null;',
                           'char[]': 'return null;',
                           'boolean[]': 'return null;',
                           'float': 'return null;;',
                           'float[]': 'return null;;',
                           'List': 'return null;',
                           'UnhandledType': 'return null;'
                           }
    if type in generic_return_dict:
        return generic_return_dict[type]
    else:
        return 'return null;'

def generate_code(text, return_statement):
    return text[0:text.index('}')] + return_statement + '}'

def submit_code(code, pid):
    response = requests.post('http://codingbat.com/run', data={"id": pid, 'code':code})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('div table tr')
    row_list = []
    for row in list(rows)[1:]:
        invocation_td = next(row.children)
        row_list.append(invocation_td.text.strip())
    if len(row_list) == 1:
        return row_list
    else:
        return row_list[0:-1]

def get_expected(row):
    expected = re.search('→ (.*)', row).group(1)
    return arg_list_parser.parse_literals(expected, 0)[0]

def get_fn_name(row):
    return re.search('([^(]*)', row).group(0)

def get_invocation(row):
    inv = re.search('(\(.*\))', row).group(1)
    return arg_list_parser.parse_literals(inv, 0)[0]
