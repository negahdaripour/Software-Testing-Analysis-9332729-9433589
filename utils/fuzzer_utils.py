import inspect
import re
import types


def replace_for(line):     
    """
    Parameters
    ----------
    line : String
        a String that contains one line of code

    Returns
    -------
    String
        this function get a line of code and replace for statment with while if exist
    """
    t = "    "
    findex = line.find("for ") +4
    if(findex != 3):
        t_size = re.match(r"\s*", line).group()
        rindex = line.find("in")-1
        c_i = line[findex:rindex]
        counter_str = re.search("range\([a-zA-Z]\):", line).group(0)
        if(counter_str):
            counter = re.search(r'\((.*?)\)', counter_str).group(1)
        new = re.sub('for [a-zA-Z] in range\([a-zA-Z]\):',c_i + ': int =0\n' + t_size +'while '+ c_i+'<'+ counter+':\n'+ t + t_size +c_i + "=" + c_i + "+1", line)
        return new 
    return line

def loopconverter(fn):
    """
    Parameters
    ----------
    fn : Function Object
        a function obejct.

    Returns
    -------
    Function Object
        return a fuction with replaced loop.
    """
    lines = inspect.getsourcelines(fn)
    new_source = ""
    for line in lines[0]:
       new_source = new_source + replace_for(line)
    with open('E:\git\Software-Testing-Analysis-9332729-9433589\examples\converted_functions.py', 'a') as f:
        f.write(new_source)   
    code = compile(new_source,'<string>', 'exec')
    return  types.FunctionType(code.co_consts[1], globals())



def for_test_function(a: int,b: int) -> int:
    for i in range(a):
        if i == a:
            return "End"
    return "No End"
        
        
def main():
    loopconverter(for_test_function)
    
