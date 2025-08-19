from django import template
register=template.Library()
@register.filter
def get_index(sequence, index):
    try:
        return sequence[index]
    except (IndexError, TypeError ):
        return None
    
@register.filter
def get_final_note(note_sn,note_cc):
    try:
        return round(0.7*note_sn+0.3*note_cc, 2)
    except TypeError:
        return None

@register.filter
def get_grade(note):
    try:
        if note>=18:
            grade="A+"
        elif note>=16:
            grade="A"
        elif note>=14:
            grade="B+"
        elif note>=12:
            grade="B"
        elif note>=10:
            grade="B-"
        return grade
    except (TypeError, NameError):
        return None        

@register.filter
def get_decision(note):
    try:
        if note>=10:
            DEC="VA"
        else:
            DEC="NV"
        return DEC
    except (TypeError, NameError):
        return None        