from datetime import date
from django import forms 
from django.utils import timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# validate the data from the submitted birth chart generation form
class BirthChartForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)

    birth_month = forms.IntegerField(min_value=1, max_value=12)
    birth_day = forms.IntegerField(min_value=1, max_value=31)
    birth_year = forms.IntegerField(min_value=1900)

    birth_time = forms.TimeField(
        required=False,
        input_formats=['%H:%M', '%H:%M:%S'],
    )

    birthplace = forms.CharField(max_length=300)
    location_id = forms.CharField(max_length=1000)

    latitude = forms.FloatField(min_value=-90, max_value=90)
    longitude = forms.FloatField(min_value=-180, max_value=180)

    birth_timezone = forms.CharField(max_length=100)

    # check if time zone is in a recognized zone
    def clean_birth_timezone(self):
        timezone_name = self.cleaned_data["birth_timezone"]

        try:
            ZoneInfo(timezone_name)
        except (ZoneInfoNotFoundError, ValueError):
            raise forms.ValidationError("Select a location with a valid time zone.")

        return timezone_name

    def clean(self):
        cleaned_data = super().clean()

        year = cleaned_data.get("birth_year")
        month = cleaned_data.get("birth_month")
        day = cleaned_data.get("birth_day")

        # only check the full date if all three fields passed validation.
        if year is not None and month is not None and day is not None:
            try:
                birth_date = date(year, month, day)
            except ValueError:
                self.add_error(
                    "birth_day",
                    "Enter a valid date of birth.",
                )
            else:
                if birth_date > timezone.localdate():
                    self.add_error(
                        "birth_year",
                        "Date of birth cannot be in the future.",
                    )
                else:
                    cleaned_data["birth_date"] = birth_date

        return cleaned_data