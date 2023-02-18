from django.core.exceptions import ValidationError
from	django.utils.translation	import	gettext_lazy	as	_
from .fake_emails import FakeEmailsList




def phone_number_validation(phone):  # dz phone number validator.
    try:
        number = int(phone)
    except:
        raise ValidationError(_("phone number is not correct"))

    condition2 = ( ( int(phone[0]) == 0 ) and ( (int(phone[1])) >= 5 and (int(phone[1])) <= 7 ) )
    condition3  = ( (int(phone[0])) >= 5 and (int(phone[0])) <= 7 )
    valide = (  ( (len(phone) == 9 ) and condition3 ) or ( ( len(phone) == 10 ) and condition2 ) )
    if not valide:
        raise ValidationError(_("phone number is not correct"))
    else:
        return phone

def fake_email_validation(email):
    for Email in FakeEmailsList:
        if Email in email:
            raise ValidationError(_("invalide email"))

    return email.lower()
