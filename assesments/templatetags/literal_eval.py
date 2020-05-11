from django import template
register = template.Library()
import ast

from utility import swaple_constants

import re 

from django import template
register = template.Library()

@register.filter
def replace_literals(string):
    #import pdb;pdb.set_trace();
    if string:
        string =  re.sub('[u \]\'\[]',  '',string)
    else:
        return ''
    return string


@register.filter
def replace ( string, args ): 
    search  = args.split(args[0])[1]
    replace = args.split(args[0])[2]

    return re.sub( search, replace, string )


@register.simple_tag(name='get_correct_answer_obj')
def get_correct_answer_obj(string_obj):
    obj_val = ast.literal_eval(string_obj)
    if len(obj_val) == 1:
        return int(obj_val[0])
    else:
        ''.join(obj_val)
    return obj_val 


class CurrentAnswerNode(template.Node):
    def __init__(self, answer_list_in_str, question_type):
        self.obj_val = ast.literal_eval(answer_list_in_str)
        
        self.question_type = question_type
    def render(self, context):
        context['selected_answer'] = list(self.obj_val)
        return ''
    
@register.simple_tag(takes_context=True)
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])    

class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""


@register.tag(name='set')
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])