import sys

import bat_scraper_2
from arg_list_parser import ArrayLiteral

def run_all(sec_name):
    master_tup = bat_scraper_2.get_pids_names(sec_name)
    for prob in master_tup[0]:
        print(build_string(build_input(prob)))
        print('println!();\n')

#Will refactor build_input, inv_vec_handler and exp_vec_handler.
def build_input(pid):
    #bat, type and signature are used to build the code variable, which in turn will be submitted to CodingBat to get the results table.
    bat = bat_scraper_2.get_bat(pid)
    type = bat_scraper_2.get_return_type(bat)
    return_statement = bat_scraper_2.generate_return(type)
    code = bat_scraper_2.generate_code(bat, return_statement)
    #Response is a list of strings, containing the rows from the results table on the CodingBat website.
    responses = bat_scraper_2.submit_code(code, pid)
    fn_name = bat_scraper_2.get_fn_name(responses[0])
    #List of tuples containing the various ivocations for the pid.
    invocation_list = []
    #List of tuples containing the expected results for the pid.
    expectation_list = []
    for row in responses:
        invocation_list.append(bat_scraper_2.get_invocation(row))
        expectation_list.append(bat_scraper_2.get_expected(row))
    #List of generic Java types in the invocation for the CodingBat problem.
    invocation_types = bat_scraper_2.get_invocation_types(bat)
    final_invocation_list = []
    final_expectation_list = []
    for row in invocation_list:
        final_invocation_list.append(fill_type_params(invocation_types, row))
    for row in expectation_list:
        final_expectation_list.append(fill_type_param(type, row))
    return (fn_name, final_invocation_list, final_expectation_list)

def fill_type_params(inv_type_list, args_tuple):
    new_args = []
    for i, arg in enumerate((args_tuple.tuplex)):
        # Reuse the logic in fill_type_param
        new_args.append(fill_type_param(inv_type_list[i], args_tuple.tuplex[i]))
    return new_args

def fill_type_param(type_param, generic_type):
    java_type_to_rust_type = {
        'int[]': 'i32',
        'boolean[]': 'bool',
        'char[]': 'char',
        'float[]': 'f32',
        'String[]': '&str',
    }
    if isinstance(generic_type, ArrayLiteral):
        # assign the argument to a variable with a different name, for clarity
        array_literal = generic_type
        # We only need to augment the type if the array is empty (in which case, Rust will not be able to infer the item type)
        if len(array_literal.arrayx) == 0:
            # use the map to lookup the appropriate item type based on the type from the bat's method signature
            array_literal.item_type = java_type_to_rust_type[type_param]

    return generic_type

def build_string(input_tuple):
    """
    builds a string with the rust code that invokes printbat! for the bat function specified in input_tuple[0]
    and the test cases in input_tuple[1]
    """
    master_string = f'printbat!({input_tuple[0]},'
    index = 0

    while index < len(input_tuple[1]):
        arg_list = input_tuple[1][index]

        # Indent each test row
        master_string += f'\n    '

        # Append the list of arguments, separated by commas
        master_string += ', '.join(map(lambda a: a.to_rust_code(), arg_list))

        # Separator, required by the macro syntax
        master_string += ' => '

        # Append the expected return value
        master_string += input_tuple[2][index].to_rust_code()

        # Separate each test row with a comma, and end it all with a semicolon
        if index < len(input_tuple[1]) - 1:
            master_string += ','
            index += 1
        else:
            master_string += ');'
            return master_string + '\n'

if sys.argv[1] == 'problem':
    print(build_string(build_input(sys.argv[2])))
else:
    run_all(sys.argv[1])
