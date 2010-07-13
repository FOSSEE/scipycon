

def test_save_to_pdf():
    """
    >>> from .pdf import save_invoice
    >>> from django.db.models.loading import get_model
    >>> userModel =  get_model('auth', 'user')
    >>> user = userModel(username='joe', email='joe@gmail.com',
    ...         first_name='Joe', last_name='Bloggs')
    >>> user.save()
    >>> regModel =  get_model('registration', 'registration')
    >>> registration = regModel(registrant=user, amount=40,
    ...          slug='NZPYCON-0001')
    >>> registration.save()

    >>> save_invoice(user, registration, 'registration/invoice.html')

    """
    pass
