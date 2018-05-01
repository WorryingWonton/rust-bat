import re
import json

class AstElement:
    pass

class Expression(AstElement):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

class IntegerLiteral(Expression):
    def __init__(self, intx):
        self.intx = intx
        if not isinstance(intx, int):
            raise Exception(f'Expected integer as argument, got {intx}')
    def __str__(self):
        return 'IntegerLiteral(' + str(self.intx) + ')'

    def to_rust_code(self):
        return f'{self.intx}'

class FloatLiteral(Expression):
    def __init__(self, floatx):
        self.floatx = floatx

    def __str__(self):
        return 'FloatLiteral(' + str(self.floatx) + ')'

    def to_rust_code(self):
        return f'{self.floatx}'

class CharLiteral(Expression):
    def __init__(self, charx):
        self.charx = charx

    def __str__(self):
        return 'CharLiteral(\'' + str(self.charx) + '\')'

    def to_rust_code(self):
        return '\'' + f'{self.charx}' + '\''

class StringLiteral(Expression):
    def __init__(self, stringx):
        self.stringx = stringx

    def __str__(self):
        return 'StringLiteral("' + self.stringx + '")'

    def to_rust_code(self):
        return '"' + f'{self.stringx}' '"'

class BooleanLiteral(Expression):
    def __init__(self, boolx):
        self.boolx = boolx

    def __str__(self):
        return 'BooleanLiteral(' + str(self.boolx).lower() + ')'

    def to_rust_code(self):
        return f'{self.boolx}'.lower()

class ArrayLiteral(Expression):
    def __init__(self, arrayx):
        self.arrayx = arrayx
        self.item_type = None

    def __str__(self):
        string = 'ArrayLiteral('
        count = 0
        for elem in self.arrayx:
            if count < len(self.arrayx) - 1:
                string += str(elem) + ', '
                count += 1
            else:
                string += str(elem)
        return string + ')'

    def to_rust_code(self):
        if len(self.arrayx) > 0:
            string = 'vec!['
            count = 0
            for elem in self.arrayx:
                if count < len(self.arrayx) - 1:
                    string += elem.to_rust_code() + ', '
                    count += 1
                else:
                    string += elem.to_rust_code()
            return string + ']'
        else:
            return f'Vec::<{self.item_type}>::new()'

class TupleLiteral(Expression):
    def __init__(self, tuplex):
        self.tuplex = tuplex
        if not isinstance(tuplex, tuple):
            raise Exception(f'Expected tuple as argument, got {tuplex}')

    def __str__(self):
        string = 'TupleLiteral('
        count = 0
        for elem in self.tuplex:
            if count < len(self.tuplex) - 1:
                string += str(elem) + ', '
                count += 1
            else:
                string += str(elem)
        return string + ')'

    def to_rust_code(self):
        string = '('
        count = 0
        for elem in self.tuplex:
            if count < len(self.tuplex) - 1:
                string += elem.to_rust_code() + ', '
                count += 1
            else:
                string += elem.to_rust_code()
        return string + ')'

class MapLiteral(Expression):
    def __init__(self, mapx):
        self.mapx = mapx
        if not isinstance(json.loads(mapx[-1]), dict):
            raise Exception(f'Expected map object as argument, got {mapx}')
    #Will refactor while loop to be a step-by-2 for loop at some point
    def to_rust_code(self):
        string = '{let mut m = BTreeMap::new();\n'
        val_index = 1
        key_index = 0
        while key_index < len(self.mapx) - 2:
            string += f'm.insert({self.mapx[key_index].to_rust_code()}, {self.mapx[val_index].to_rust_code()});\n'
            val_index += 2
            key_index += 2
        string += 'm\n}'
        return string

def integer(s, index):
    m = re.match('-?([0-9]+)', s[index:])
    if m:
        token = m.group(0)
        return (IntegerLiteral(int(token)), index + len(token))
    else:
        return (f'ERROR: Expecting digit, got {s[index:index+1]}', index)

def floating_point(s, index):
    m = re.match('-?([0-9]+\.[0-9]*)', s[index:])
    if m:
        token = m.group(0)
        return (FloatLiteral(float(token)), index + len(token))
    else:
        return (f'ERROR: Expecting float, got {s[index:index+1]}', index)

def character(s, index):
    m = re.match('\'[^\']\'', s[index:])
    if m:
        token = m.group(0)
        return (CharLiteral(token[1]), index + len(token))
    else:
        return (f'ERROR: Expecting char, got {s[index:index+1]}', index)

def string(s, index):
    m = re.match('"[^"]*"', s[index:])
    if m:
        token = m.group(0)
        return (StringLiteral(token[1:-1]), index + len(token))
    else:
        return (f'ERROR: Expecting String, got {s[index:index+1]}', index)

def boolean(s, index):
    m = re.match('(true|false)', s[index:])
    if m:
        token = m.group(0)
        return (BooleanLiteral(token == 'true'), index + len(token))
    else:
        return (f'ERROR: Expecting bool, got {s[index:index+1]}', index)

def array(s, index):
    if index < len(s) and s[index] == '[':
        parsed_array = []
        s_index = index + 1
        while s_index < len(s):
            (value, new_index) = parse_literals(s, s_index)
            if s_index == new_index:
                return (ArrayLiteral(parsed_array), s_index + 1)
            else:
                parsed_array.append(value)
                s_index = new_index
            if s[s_index] == ',':
                s_index += 1
                if s[s_index] == ' ':
                    s_index += 1
            if s[s_index] == ']':
                return (ArrayLiteral(parsed_array), s_index + 1)
    else:
        return ('ERROR: Not an array.', index)

def parse_tuple(s, index):
    if index < len(s) and s[index] == '(':
        # Initially a list as tuples are immutable, will be converted to a tuple when returned.
        parsed_tuple = []
        s_index = index + 1
        while s_index < len(s):
            (value, new_index) = parse_literals(s, s_index)
            if s_index == new_index:
                return (TupleLiteral(tuple(parsed_tuple)), s_index + 1)
            else:
                parsed_tuple.append(value)
                s_index = new_index
            if s[s_index] == ',':
                s_index += 1
                if s[s_index] == ' ':
                    s_index += 1
            if s[s_index] == ')':
                return (TupleLiteral(tuple(parsed_tuple)), s_index + 1)
    else:
        return('ERROR: Not a tuple.', index)

def parse_map(s, index):
    if index < len(s) and s[index] == '{':
        ccb_index = index + 1
        parsed_map = []
        while ccb_index < len(s):
            (value, new_index) = parse_literals(s, ccb_index)
            if ccb_index == new_index:
                map_string = s[index:ccb_index + 1]
                parsed_map.append(map_string)
                return (MapLiteral(parsed_map), ccb_index + 1)
            else:
                parsed_map.append(value)
                ccb_index = new_index
            if s[ccb_index] == ':':
                ccb_index += 1
            if s[ccb_index] == ' ':
                ccb_index += 1
            if s[ccb_index] == ',':
                ccb_index += 1
            if s[ccb_index] == ' ':
                ccb_index += 1
            if s[ccb_index] == '}':
                map_string = s[index:ccb_index + 1]
                parsed_map.append(map_string)
                return (MapLiteral(parsed_map), ccb_index + 1)
    else:
        return ('ERROR: Not a map object', index)

def parse_scalar_literal(s, index):
    literal_list = [parse_fn(s, index) for parse_fn in [integer, floating_point, character, string, boolean]]
    largest_index = 0
    for tuple in literal_list:
        if tuple[1] > largest_index:
            largest_index = tuple[1]
    for final in literal_list:
        if final[1] == largest_index:
            return final

def parse_literals(s, index):
    (value, new_index) = parse_scalar_literal(s, index)
    (array_value, new_array_index) = array(s, index)
    (tuple_value, new_tuple_index) = parse_tuple(s, index)
    (map_value, new_map_index) = parse_map(s, index)
    if new_array_index > max(new_index, new_tuple_index, new_map_index):
        return (array_value, new_array_index)
    elif new_tuple_index > max(new_index, new_array_index, new_map_index):
        return (tuple_value, new_tuple_index)
    elif new_index > max(new_array_index, new_tuple_index, new_map_index):
        return (value, new_index)
    elif new_map_index > max(new_index, new_array_index, new_tuple_index):
        return (map_value, new_map_index)
    else:
        return (s, index)
