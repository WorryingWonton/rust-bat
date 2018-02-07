are_you_sure = input('''This program will capture every JavaBat on the CodingBat website.  
Running it will take time and may result in a ban from CodingBats.  Proceed? (Y/N): ''')

class BuildHTML:

    @staticmethod
    def scrape_main_page():
        top_url = 'http://codingbat.com/java'
        sections = []
        return sections

    @staticmethod
    def scrape_sections(sections):
        #Keys in problems are section names, values a are problem names
        problems = {}
        return problems

    def scrape_problems(self, problems):
        #initial_html is a dictionary of dictionaries.
        #The outer dictionaries' keys are section names whose values are dictionaries whose keys are problem names.'
        #The two values assigned to the inner dictionaries' keys are the pid# and the HTML for each problem.  The values are a 2 element string list.
        initial_html = {}
        return initial_html

    def generate_responses(self, initial_html):
        for sections in initial_html:
            for problems in sections:
                pass
        problem_dict = {}
        return problem_dict

    def post_responses(problem_dict):
        #table_dict is a dictionary of dictionaries.
        #The outer dictionaries keys are section names, whose values are dictionaries whose keys are problem names.
        #The inner dictionaries' values are strings representing the response tables from each bat.
        table_dict = {}
        return table_dict

    #This should be called just before the return statement for scrape_main_page(), scrape_sections(), scrape_problems(), and
    def text_writer(self, file_name):
        pass

    def sequencer(self):
        sections = BuildHTML.scrape_main_page()
        problems = BuildHTML.scrape_sections(sections)
        
class BuildRust:
    pass
