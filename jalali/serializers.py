import jdatetime
from django.utils import timezone
from rest_framework import serializers



class JalaliDateTimeField(serializers.DateTimeField):
    def to_internal_value(self, data):
        # Convert Jalali date string to a Gregorian datetime
        try:
            # Assuming the input format is "YYYY/MM/DD HH:MM:SS"
            jalali_date = jdatetime.datetime.strptime(data, '%Y/%m/%d %H:%M:%S')
            # Convert to Gregorian datetime
            gregorian_date = jalali_date.togregorian()
            return timezone.make_aware(gregorian_date)  # Make it timezone aware
        except ValueError:
            raise serializers.ValidationError("Datetime has wrong format. Use 'YYYY/MM/DD HH:MM:SS'.")

    def to_representation(self, value):
        # Convert the Gregorian datetime to Jalali datetime string
        if value:
            local_datetime = timezone.localtime(value)
            jalali_date = jdatetime.datetime.fromgregorian(
                year=local_datetime.year,
                month=local_datetime.month,
                day=local_datetime.day,
                hour=local_datetime.hour,
                minute=local_datetime.minute,
                second=local_datetime.second
            )
            return jalali_date.strftime('%Y/%m/%d %H:%M:%S')
        return None