from django import forms
from django.core.exceptions import ObjectDoesNotExist

from project.scipycon.registration.models import SIZE_CHOICES
from project.scipycon.registration.models import OCCUPATION_CHOICES
from project.scipycon.registration.models import Accommodation
from project.scipycon.registration.models import Payment
from project.scipycon.registration.models import Wifi


class RegistrationSubmitForm(forms.Form):
    """SciPyCon registration form
    """
    #tshirt = forms.ChoiceField(choices=SIZE_CHOICES, required=True,
    #    label=u'T-shirt size', help_text=u'Yes, we all get a t-shirt!')
    organisation = forms.CharField(required=True, label=u'Organisation',
        help_text=u'The primary organisation that you are a member of.',
        max_length=255,
        widget=forms.TextInput(attrs={'size':'50'}))
    occupation = forms.ChoiceField(choices=OCCUPATION_CHOICES,
        required=True, label=u'Occupation',
        help_text=u'Title of your occupation')
    city = forms.CharField(required=False, label=u'City',
        help_text=u'Your city of residence',
        max_length=255,
        widget=forms.TextInput(attrs={'size':'50'}))
    postcode = forms.CharField(required=False, label=u'Postcode',
        help_text=u'PIN Code of your area',
        max_length=10,
        widget=forms.TextInput(attrs={'size':'10'}))
    phone_num = forms.CharField(required=False, label=u'Phone Number',
        help_text=u'Phone number. Although optional, please provide it for '
        'faster correspondence', max_length=14,
        widget=forms.TextInput(attrs={'size':'20'}))
    allow_contact = forms.BooleanField(required=False, label=u'Contact',
        help_text=u'May organizers of SciPy.in contact you after the event?')
    conference = forms.BooleanField(required=False, label=u'Conference',
        help_text=u"""Do you intend to attend SciPy.in 2010 conference?""")
    tutorial = forms.BooleanField(required=False, label=u'Tutorial',
        help_text=u'Do you intend to attend the tutorials?')
    sprint = forms.BooleanField(required=False, label=u'Sprint',
        help_text=u'Do you intend to attend the sprints?')

    def occupation_fields(self):
        return (self['organisation'],
                self['occupation'])

    def demographic_fields(self):
        return (self['city'],
                self['postcode'],
                self['phone_num'])

    def personal_fields(self):
        return (#self['tshirt'],
                self['conference'],
                self['tutorial'],
                self['sprint'],
                self['allow_contact'])


class RegistrationEditForm(RegistrationSubmitForm):
    id = forms.CharField(widget=forms.HiddenInput)

class WifiForm(forms.ModelForm):
    """SciPyCon wifi form
    """

    def save(self, user, scope):
        try:
            wifi = Wifi.objects.get(user=user, scope=scope)
        except ObjectDoesNotExist:
            wifi = Wifi(user=user, scope=scope)

        wifi.wifi = self.cleaned_data['wifi']
        wifi.registration_id = self.cleaned_data['registration_id']
        wifi.save()

        return wifi

    class Meta:
        model = Wifi
        fields = ('wifi', 'registration_id')


class AccommodationForm(forms.ModelForm):
    """SciPyCon Accommodation form
    """

    def save(self, user, scope):
        try:
            acco = Accommodation.objects.get(user=user, scope=scope)
        except ObjectDoesNotExist:
            acco = Accommodation(user=user, scope=scope)

        sex = self.cleaned_data['sex']
        accommodation_required = self.cleaned_data['accommodation_required']

        a1 = self.cleaned_data['accommodation_on_1st']
        a2 = self.cleaned_data['accommodation_on_2nd']
        a3 = self.cleaned_data['accommodation_on_3rd']
        a4 = self.cleaned_data['accommodation_on_4th']
        a5 = self.cleaned_data['accommodation_on_5th']
        a6 = self.cleaned_data['accommodation_on_6th']

        accommodation_days = [a1, a2, a3, a4, a5, a6].count(True)

        acco.sex = sex
        acco.accommodation_required = accommodation_required
        acco.accommodation_days = accommodation_days

        acco.accommodation_on_1st = a1
        acco.accommodation_on_2nd = a2
        acco.accommodation_on_3rd = a3
        acco.accommodation_on_4th = a4
        acco.accommodation_on_5th = a5
        acco.accommodation_on_6th = a6


        acco.save()

        return acco

    def clean(self):
        """Makes sure that accommodation form is correct, i.e. sex
        and number of days required are filled in when the accommodation
        is required.
        """
        cleaned = self.cleaned_data

        sex = self.cleaned_data['sex']
        accommodation_required = self.cleaned_data['accommodation_required']

        a1 = self.cleaned_data['accommodation_on_1st']
        a2 = self.cleaned_data['accommodation_on_2nd']
        a3 = self.cleaned_data['accommodation_on_3rd']
        a4 = self.cleaned_data['accommodation_on_4th']
        a5 = self.cleaned_data['accommodation_on_5th']
        a6 = self.cleaned_data['accommodation_on_6th']

        selected_a_date = any([a1, a2, a3, a4, a5, a6])

        if accommodation_required and (not sex or not selected_a_date):
            #or accommodation_days == 0):
            raise forms.ValidationError(
                u"If accommodation is required please specify gender and" 
                " select the days number for which accommodation is required.")

        return super(AccommodationForm, self).clean()

    class Meta:
        model = Accommodation
        fields = ('accommodation_required',
                  'sex', 
                  'accommodation_on_1st',
                  'accommodation_on_2nd',
                  'accommodation_on_3rd',
                  'accommodation_on_4th',
                  'accommodation_on_5th',
                  'accommodation_on_6th',
                 )


class PaymentForm(forms.ModelForm):
    """SciPyCon Payment form
    """

    paid = forms.BooleanField(
        required=False, label="Amount paid",
        help_text="Check this box if you have already paid the fees.")

    def save(self, user, scope):
        try:
            payment = Payment.objects.get(user=user, scope=scope)
        except ObjectDoesNotExist:
            payment = Payment(user=user, scope=scope)

        paid = self.cleaned_data['paid']
        type = self.cleaned_data['type']
        details = self.cleaned_data['details']

        payment.type = type
        payment.details = details

        payment.save()

        return payment

    def clean(self):
        """Makes sure that payment form is correct, i.e. type and details
        are filled in when the required fees is paid.
        """

        paid = self.cleaned_data['paid']
        type = self.cleaned_data['type']
        details = self.cleaned_data['details']

        if paid and (not type or not details):
            raise forms.ValidationError(
                u"If you have already paid the fee it is mandatory to "
                "fill in the type and mandatory fields.")

        return super(PaymentForm, self).clean()

    class Meta:
        model = Payment
        fields = ('paid', 'type', 'details')


PC = (
        ('all', 'all'),
        ('paid', 'paid'),
        ('not paid', 'not paid')
        )
HC = (
        ('all', 'all'),
        ('party', 'party'),
        ('no party', 'no party')
        )
AC = (
        ('all', 'all'),
        ('0', '0'),
        ('10', '10'),
        ('20', '20'),
        ('40', '40'),
        )
OC = (
        ('email', 'email'),
        ('amount', 'amount'),
        )

IC = (
        ('Name', 'name'),
        ('Email', 'email'),
        ('Amount', 'amount'),
        ('Organisation', 'organisation'),
        ('Conference', 'conference'),
        ('Tutorial', 'tutorial'),
        ('Sprint', 'sprint'),
        ('T-size', 'tshirt'),
        )


class RegistrationAdminSelectForm(forms.Form):
    """
    Used to make selection for csv download
    """
    by_payment = forms.ChoiceField(choices=PC, required=False,
        label=u'By payment')
    by_amount = forms.MultipleChoiceField(choices=AC, required=False,
        label=u'By amount')
    by_party = forms.ChoiceField(choices=HC, required=False,
        label=u'by party')
    by_tshirt = forms.ChoiceField(choices=SIZE_CHOICES, required=False,
        label=u'by tshirt size')
    order_by = forms.ChoiceField(choices=OC, required=False,
        label=u'order results')
    include = forms.MultipleChoiceField(choices=IC, required=False,
        label=u'Include fields')
