from django.forms import DateTimeInput


class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = "Owner/xdsoft_datetimepicker.html"
