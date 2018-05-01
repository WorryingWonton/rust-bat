import bat_scraper_2
from arg_list_parser import ArrayLiteral
import sys
import time

def run_section(sec_name):
    prob_tup = bat_scraper_2.get_pids_names(sec_name)
    for prob in prob_tup[0]:
        print(build_string(build_input(prob)))
        print('println!();\n')

def run_all():
    section_list = bat_scraper_2.scrape_sections()
    start_time = time.gmtime()
    md_file = open(f'rust_bats_{start_time.tm_mon}_{start_time.tm_mday}_{start_time.tm_year}_{start_time.tm_hour}_{start_time.tm_min}_{start_time.tm_sec}.txt', 'w')
    clean_file =open(f'clean_rust_bats_{start_time.tm_mon}_{start_time.tm_mday}_{start_time.tm_year}_{start_time.tm_hour}_{start_time.tm_min}_{start_time.tm_sec}.txt', 'w')
    bat_formatter_string_md = ''
    bat_formatter_string_clean = ''
    for section in section_list:
        prob_tup = bat_scraper_2.get_pids_names(section)
        pt_index = 0
        bat_formatter_string_md += f'/// start: {section}'
        bat_formatter_string_clean += f'/// start: {section}'
        for pid in prob_tup[0]:
            problem_info = f'---section: {section} pid: {pid} prob_name: {prob_tup[1][pt_index]}---'
            prob_string = build_string(build_input(pid))
            bat_formatter_string_clean += f'{prob_string}\nprintln!();\n'
            bat_formatter_string_md += f'{problem_info}\n{prob_string}\nprintln!();\n'
        bat_formatter_string_md += f'end: {section} ///'
        bat_formatter_string_clean += f'end: {section} ///'
    md_file.write(bat_formatter_string_md)
    md_file.close()
    clean_file.write(bat_formatter_string_clean)
    clean_file.close()


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
        new_args.append(fill_type_param(inv_type_list[i], args_tuple.tuplex[i]))
    return new_args

def fill_type_param(type_param, generic_type):
    java_rust_types = {
        'int[]': 'i32',
        'List<Integer>': 'i32',
        'List<String>': '&str',
        'boolean[]': 'bool',
        'char[]': 'char',
        'float[]': 'f32',
        'String[]': '&str',
    }
    if isinstance(generic_type, ArrayLiteral):
        array_literal = generic_type
        if len(array_literal.arrayx) == 0:
            array_literal.item_type = java_rust_types[type_param]
    return generic_type

def build_string(input_tuple):
    master_string = f'printbat!({input_tuple[0]},'
    index = 0
    while index < len(input_tuple[1]):
        arg_list = input_tuple[1][index]
        master_string += f'\n   '
        master_string += ', '. join(map(lambda inv: inv.to_rust_code(), arg_list))
        master_string += ' => '
        master_string += input_tuple[2][index].to_rust_code()
        if index < len(input_tuple[1]) - 1:
            master_string += ','
            index += 1
        else:
            master_string += ');'
            return master_string + '\n'

if __name__ == '__main__':
    if sys.argv[1].lower() == 'all':
        run_all()
    if sys.argv[1].lower() == 'section':
        run_section(sys.argv[2])
    elif sys.argv[1].lower() == 'problem':
        print(build_string(build_input(sys.argv[2].lower())))
    else:
        print(f'ERROR: Enter \'Section\' followed by a section name (e.g. \'Array-1\') or \'Problem\' followed by a problem number (e.g. \'p159531\').\nYou entered \'{sys.argv[1]}\', which is neither section nor problem.')

