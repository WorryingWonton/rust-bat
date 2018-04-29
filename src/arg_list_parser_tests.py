import unittest
import arg_list_parser
from arg_list_parser import *

class TestLiteralFunctions(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(('ERROR: Expecting digit, got ', 0), arg_list_parser.integer('', 0))
        self.assertEqual((IntegerLiteral(12345), 5), arg_list_parser.integer('12345', 0))
        self.assertEqual((IntegerLiteral(234), 4), arg_list_parser.integer('1234', 1))
        self.assertEqual((IntegerLiteral(1234), 4), arg_list_parser.integer('1234.5678', 0))
        self.assertEqual((IntegerLiteral(123), 3), arg_list_parser.integer('123a345.789', 0))
        self.assertEqual(('ERROR: Expecting digit, got .', 0), arg_list_parser.integer('.1234', 0))

    def test_floating_point(self):
        self.assertEqual(('ERROR: Expecting float, got ', 0), arg_list_parser.floating_point('', 0))
        self.assertEqual(('ERROR: Expecting float, got 1', 0), arg_list_parser.floating_point('1', 0))
        self.assertEqual(('ERROR: Expecting float, got ', 4), arg_list_parser.floating_point('', 4))
        self.assertEqual(('ERROR: Expecting float, got ', 4), arg_list_parser.floating_point('1.0', 4))
        self.assertEqual(('ERROR: Expecting float, got .', 0), arg_list_parser.floating_point('.234', 0))
        # self.assertEqual((1., 2), arg_list_parser.floating_point('1..0', 0))
        self.assertEqual((FloatLiteral(1.), 2), arg_list_parser.floating_point('1..0', 0))
        self.assertEqual((FloatLiteral(1.1), 3), arg_list_parser.floating_point('1.1', 0))
        self.assertEqual((FloatLiteral(1234.0), 6), arg_list_parser.floating_point('1234.0', 0))
        self.assertEqual((FloatLiteral(1234.56789), 10), arg_list_parser.floating_point('1234.56789', 0))
        self.assertEqual((FloatLiteral(234.56789), 10), arg_list_parser.floating_point('1234.56789', 1))

    def test_character(self):
        self.assertEqual(('ERROR: Expecting char, got ', 0), arg_list_parser.character('', 0))
        self.assertEqual(('ERROR: Expecting char, got a', 0), arg_list_parser.character('ab', 0))
        self.assertEqual(('ERROR: Expecting char, got \'', 0), arg_list_parser.character('\'ab\'', 0))
        self.assertEqual(('ERROR: Expecting char, got \'', 0), arg_list_parser.character('\'\'', 0))
        self.assertEqual(('ERROR: Expecting char, got a', 1), arg_list_parser.character('\'a\'', 1))
        self.assertEqual(('ERROR: Expecting char, got b', 0), arg_list_parser.character('bcd\'a\'', 0))
        self.assertEqual((CharLiteral('a'), 3), arg_list_parser.character('\'a\'', 0))
        self.assertEqual((CharLiteral('b'), 3), arg_list_parser.character('\'b\'', 0))
        self.assertEqual((CharLiteral('"'), 3), arg_list_parser.character('\'"\'', 0))
        self.assertEqual((CharLiteral('v'), 3), arg_list_parser.character('\'v\'', 0))

    def test_string(self):
        self.assertEqual(('ERROR: Expecting String, got ', 0), arg_list_parser.string('', 0))
        self.assertEqual(('ERROR: Expecting String, got a', 0), arg_list_parser.string('a""', 0))
        self.assertEqual(('ERROR: Expecting String, got ', 4), arg_list_parser.string('a""', 4))
        self.assertEqual(('ERROR: Expecting String, got "', 0), arg_list_parser.string('"', 0))
        self.assertEqual((StringLiteral(""), 2), arg_list_parser.string('""', 0))
        self.assertEqual((StringLiteral(""), 2), arg_list_parser.string('"""', 0))
        self.assertEqual((StringLiteral(""), 3), arg_list_parser.string('"""', 1))
        self.assertEqual((StringLiteral("Hello"), 8), arg_list_parser.string('""Hello"', 1))

    def test_boolean(self):
        self.assertEqual(('ERROR: Expecting bool, got ', 0), arg_list_parser.boolean('', 0))
        self.assertEqual(('ERROR: Expecting bool, got r', 1), arg_list_parser.boolean('true', 1))
        self.assertEqual(('ERROR: Expecting bool, got a', 1), arg_list_parser.boolean('false', 1))
        self.assertEqual((BooleanLiteral(True), 4), arg_list_parser.boolean('true', 0))
        self.assertEqual((BooleanLiteral(False), 5), arg_list_parser.boolean('false', 0))
        self.assertEqual((BooleanLiteral(True), 4), arg_list_parser.boolean('truetruetruetrue', 0))
        self.assertEqual((BooleanLiteral(True), 8), arg_list_parser.boolean('truetruetruetrue', 4))
        self.assertEqual((BooleanLiteral(False), 5), arg_list_parser.boolean('falsefalsefalsefalse', 0))
        self.assertEqual((BooleanLiteral(False), 10), arg_list_parser.boolean('falsefalsefalsefalse', 5))

    def test_array(self):
        self.assertEqual((ArrayLiteral([]), 2), arg_list_parser.array('[]', 0))
        self.assertEqual((ArrayLiteral([IntegerLiteral(1)]), 3), arg_list_parser.array('[1]', 0))
        self.assertEqual((ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(2)]), 9), arg_list_parser.array('[1, 2, 2]', 0))
        self.assertEqual((ArrayLiteral([
            CharLiteral('a'),
            CharLiteral('b'),
            CharLiteral('c'),
            CharLiteral('d')]
        ), 20), arg_list_parser.array('[\'a\', \'b\', \'c\', \'d\']', 0))
        self.assertEqual((ArrayLiteral([
            StringLiteral("Hello,"),
            StringLiteral(" there "),
            StringLiteral("Dave!")]
        ), 30), arg_list_parser.array('["Hello,", " there ", "Dave!"]', 0))
        self.assertEqual((ArrayLiteral([
            FloatLiteral(1.2),
            FloatLiteral(1.),
            FloatLiteral(2.3456)]
        ), 17), arg_list_parser.array('[1.2, 1., 2.3456]', 0))
        self.assertEqual((ArrayLiteral([
            BooleanLiteral(True),
            BooleanLiteral(False),
            BooleanLiteral(True),
            BooleanLiteral(False)]
        ), 26), arg_list_parser.array('[true, false, true, false]', 0))
        self.assertEqual((ArrayLiteral([
            BooleanLiteral(True),
            IntegerLiteral(12345),
            CharLiteral('a'),
            StringLiteral("SAD"),
            BooleanLiteral(False),
            FloatLiteral(1.234)]
        ), 39), arg_list_parser.array('[true, 12345, \'a\', "SAD", false, 1.234]', 0))

    def test_parse_tuple(self):
        self.assertEqual((TupleLiteral(()), 2), arg_list_parser.parse_tuple('()', 0))
        #This is an interesting result.
        self.assertEqual((TupleLiteral((IntegerLiteral(1),)), 3), arg_list_parser.parse_tuple('(1)', 0))
        self.assertEqual((TupleLiteral((
            IntegerLiteral(1),
            IntegerLiteral(2)
        )), 6), arg_list_parser.parse_tuple('(1, 2)', 0))

    def test_parse_scalar_literal(self):
        self.assertEqual((IntegerLiteral(12345), 5), arg_list_parser.parse_scalar_literal('12345', 0))
        self.assertEqual((FloatLiteral(123.456), 7), arg_list_parser.parse_scalar_literal('123.456', 0))
        self.assertEqual((CharLiteral('c'), 3), arg_list_parser.parse_scalar_literal('\'c\'', 0))
        self.assertEqual((StringLiteral("Hi Alice!"), 11), arg_list_parser.parse_scalar_literal('"Hi Alice!"', 0))
        self.assertEqual((BooleanLiteral(False), 5), arg_list_parser.parse_scalar_literal('false', 0))

    def test_parse_literal(self):
        #Non-Nested tests.
        self.assertEqual(('', 0), arg_list_parser.parse_literals('', 0))
        self.assertEqual((IntegerLiteral(123), 3), arg_list_parser.parse_literals('123', 0))
        self.assertEqual((ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), 9), arg_list_parser.parse_literals('[1, 2, 3]', 0))
        #Nested Tests
        self.assertEqual((ArrayLiteral([
            IntegerLiteral(1),
            IntegerLiteral(2),
            IntegerLiteral(3),
            ArrayLiteral([
                IntegerLiteral(1),
                FloatLiteral(2.2),
                ArrayLiteral([IntegerLiteral(1)])
            ])
        ]), 24), arg_list_parser.parse_literals('[1, 2, 3, [1, 2.2, [1]]]', 0))
        self.assertEqual(((']'), 0), arg_list_parser.parse_literals(']', 0))
        # This test fails, arg_list_parser.array() does not have any fallback if it encounters a '[' without also encountering a ']'.
        # self.assertEqual((CharLiteral('['), 0), arg_list_parser.parse_literals('[', 0))
        self.assertEqual((ArrayLiteral([
            IntegerLiteral(1),
            TupleLiteral((
                IntegerLiteral(1),
                IntegerLiteral(2),
                IntegerLiteral(3)
            ))
        ]), 14), arg_list_parser.parse_literals('[1, (1, 2, 3)]', 0))
        self.assertEqual((ArrayLiteral([
            IntegerLiteral(1),
            IntegerLiteral(2),
            IntegerLiteral(2),
            ArrayLiteral([
                IntegerLiteral(2),
                TupleLiteral((
                    IntegerLiteral(3),
                    IntegerLiteral(4)
                ))
            ])
        ]), 22), arg_list_parser.parse_literals('[1, 2, 2, [2, (3, 4)]]', 0))
        self.assertEqual((ArrayLiteral([
            IntegerLiteral(1),
            IntegerLiteral(2),
            IntegerLiteral(2),
            ArrayLiteral([
                IntegerLiteral(2),
                TupleLiteral((
                    IntegerLiteral(3),
                    IntegerLiteral(4),
                    ArrayLiteral([
                        IntegerLiteral(5)
                    ]
                    ))
                )
            ])
        ]), 26), arg_list_parser.parse_literals('[1, 2, 2, [2, (3, 4,[5])]]', 0))

class TestCharLiteral(unittest.TestCase):
    def test_eq(self):
        self.assertTrue(CharLiteral('a') == CharLiteral('a'))
        self.assertFalse(CharLiteral('a') == CharLiteral('b'))
        self.assertFalse(CharLiteral('H') == 'H')
        self.assertFalse(CharLiteral('a') != CharLiteral('a'))
        self.assertTrue(CharLiteral('a') != CharLiteral('b'))
        self.assertTrue(CharLiteral('H') != 'H')

class Test_to_rust_code(unittest.TestCase):
    def test_stringification(self):
        self.assertEqual('1', arg_list_parser.IntegerLiteral(1).to_rust_code())
        self.assertEqual('vec![1, 2, 3]', arg_list_parser.ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]).to_rust_code())
        self.assertEqual('"Hello"', arg_list_parser.StringLiteral("Hello").to_rust_code())
        self.assertEqual('\'c\'', arg_list_parser.CharLiteral('c').to_rust_code())
        self.assertEqual('1.234', arg_list_parser.FloatLiteral(1.234).to_rust_code())
        self.assertEqual('(1, 2, 3)', arg_list_parser.TupleLiteral((IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3))).to_rust_code())
        self.assertEqual('true', arg_list_parser.BooleanLiteral(True).to_rust_code())

    def test_complex(self):
        self.assertEqual('()', arg_list_parser.parse_literals('()', 0)[0].to_rust_code())
        self.assertEqual('vec![]', arg_list_parser.parse_literals('[]', 0)[0].to_rust_code())
        self.assertEqual('(1, 2, 3)', arg_list_parser.parse_literals('(1, 2, 3)', 0)[0].to_rust_code())
        self.assertEqual('vec![1, 2, 3]', arg_list_parser.parse_literals('[1, 2, 3]', 0)[0].to_rust_code())
        self.assertEqual('vec![(1, 2, 3), vec![1, 2, "Hello"], 2, 3, 4, \'a\']', arg_list_parser.parse_literals('[(1, 2, 3), [1, 2, "Hello"], 2, 3, 4, \'a\']', 0)[0].to_rust_code())

class TestStr(unittest.TestCase):
    def test_str(self):
        self.assertEqual('TupleLiteral()', str(TupleLiteral(())))
        self.assertEqual('ArrayLiteral()', str(ArrayLiteral([])))
        self.assertEqual('IntegerLiteral(1)', str(IntegerLiteral(1)))
        self.assertEqual('StringLiteral("Hello")', str(StringLiteral('Hello')))
        self.assertEqual('BooleanLiteral(true)', str(BooleanLiteral(True)))
        self.assertEqual('CharLiteral(\'a\')', str(CharLiteral('a')))
        self.assertEqual('FloatLiteral(1.1)', str(FloatLiteral(1.1)))

    # def test_complex(self):
    #     self.assertEqual('ArrayLiteral(StringLiteral("Hello"))', str(arg_list_parser.array('["Hello"]', 0)[0]))
    #     my_tuple = arg_list_parser.parse_tuple('(1, 2.2, [2, "Hello"])', 0)
    #     self.assertEqual('TupleLiteral(IntegerLiteral(1), FloatLiteral(2.2), ArrayLiteral(IntegerLiteral(2), StringLiteral("Hello")))', str(my_tuple[0]))

if __name__ == '__main__':
    unittest.main()

