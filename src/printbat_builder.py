import bat_scraper_2
import sys
import re

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
    invocation_types = bat_scraper_2.get_invocation_types(bat)
    for row in responses:
         invocation_list.append(bat_scraper_2.get_invocation(row))
         expectation_list.append(bat_scraper_2.get_expected(row))
    return (fn_name, invocation_list, expectation_list)


#     for row in responses:
#         invocation_list.append(bat_scraper_2.get_invocation(row).to_rust_code())
#         expectation_list.append(bat_scraper_2.get_expected(row).to_rust_code())
#     #List of generic Java types in the invocation for the CodingBat problem.
#     final_invocation_list = []
#     final_expectation_list = []
#     for row in invocation_list:
#         final_invocation_list.append(inv_vec_handler(invocation_types, row))
#     for row in expectation_list:
#         final_expectation_list.append(exp_vec_handler(type, row))
#     return (fn_name, final_invocation_list, final_expectation_list)
#
def inv_vec_handler(inv_type_list, row):
    row_as_list = row[1:-1].split(', ')
    vec_dict = {'int[]': 'Vec::<i32>::new()', 'boolean[]': 'Vec::<bool>::new()', 'char[]': 'Vec::<char>::new()', 'float[]': 'Vec::<f32>::new()', 'String[]': 'Vec::<&str>::new()'}
    index = 0
    row_string = ''
    while index < len(row_as_list):
        if row_as_list[index] == 'Vec::<>::new()':
            row_as_list[index] = vec_dict[inv_type_list[index]]
        if index < len(row_as_list) - 1:
            row_string += f'{row_as_list[index]}, '
        else:
            row_string += f'{row_as_list[index]}'
        index += 1
    return '(' + row_string + ')'
#
# def exp_vec_handler(type, row):
#     vec_dict = {'int[]': 'Vec::<i32>::new()', 'boolean[]': 'Vec::<bool>::new()', 'char[]': 'Vec::<char>::new()', 'float[]': 'Vec::<f32>::new()', 'String[]': 'Vec::<&str>::new()'}
#     if row == 'Vec::<>::new()':
#         return vec_dict[type]
#     else:
#         return row

def build_string(input_tuple):
    master_string = f'printbat!({input_tuple[0]},'
    index = 0

    while index < len(input_tuple[1]):
        if index < len(input_tuple[1]) - 1:
            master_string += f'\n    {input_tuple[1][index][1:-1]} => {input_tuple[2][index]},'
            index += 1
        else:
            master_string += f'\n    {input_tuple[1][index][1:-1]} => {input_tuple[2][index]});'
            return master_string + '\n'

# run_all(sys.argv[1])

bad_test = build_input('p109660')[1][3]

print(bad_test)


