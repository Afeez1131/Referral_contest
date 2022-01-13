import string
import random


def code_generator(size=4, chars=string.ascii_letters + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_shortcode(instance):
    new_code = code_generator()
    klass = instance.__class__  # This will return the name of the model class
    code_exist = klass.objects.filter(ref_shortcode=new_code).exists()

    if code_exist:
        return create_shortcode()
    else:
        return new_code
