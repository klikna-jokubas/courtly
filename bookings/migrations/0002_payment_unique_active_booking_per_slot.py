from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    status__in=['PENDING', 'CONFIRMED']
                ),
                fields=('time_slot',),
                name='unique_active_booking_per_slot',
            ),
        ),
    ]