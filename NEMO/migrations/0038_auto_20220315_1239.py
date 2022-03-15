# Generated by Django 2.2.27 on 2022-03-15 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NEMO', '0037_version_3_16_0'),
    ]

    def migrate_staff_availability_categories(apps, schema_editor):
        # We are creating new staff availability categories based on the previous char fields and setting them
        StaffAvailability = apps.get_model("NEMO", "StaffAvailability")
        StaffAvailabilityCategory = apps.get_model("NEMO", "StaffAvailabilityCategory")
        categories = list(set(list(StaffAvailability.objects.filter(category__isnull=False).values_list("category", flat=True))))
        categories.sort()
        for staff_availability in StaffAvailability.objects.all():
            print(staff_availability.category)
            if staff_availability.category:
                category, created = StaffAvailabilityCategory.objects.get_or_create(name=staff_availability.category, display_order=categories.index(staff_availability.category))
                staff_availability.category_link = category
                staff_availability.save()


    operations = [
        migrations.CreateModel(
            name='StaffAvailabilityCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('display_order', models.IntegerField(help_text="Staff availability categories are sorted according to display order. The lowest value category is displayed first in the 'Staff status' page.")),
            ],
            options={
                'verbose_name_plural': 'Staff availability categories',
                'ordering': ['display_order', 'name'],
            },
        ),
        migrations.AlterModelOptions(
            name='landingpagechoice',
            options={'ordering': ['display_order']},
        ),
        migrations.RenameField(
            model_name='configuration',
            old_name='display_priority',
            new_name='display_order',
        ),
        migrations.RenameField(
            model_name='landingpagechoice',
            old_name='display_priority',
            new_name='display_order',
        ),
        migrations.AddField(
            model_name='staffavailability',
            name='category_link',
            field=models.ForeignKey(blank=True, help_text='The category for this staff member.', null=True, on_delete=django.db.models.deletion.CASCADE, to='NEMO.StaffAvailabilityCategory'),
        ),
        migrations.RunPython(migrate_staff_availability_categories),
        migrations.RemoveField(
            model_name='staffavailability',
            name='category',
        ),
        migrations.RenameField(
            model_name='staffavailability',
            old_name='category_link',
            new_name='category',
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='staff_status_view',
            field=models.CharField(choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month')], max_length=100, default='day', help_text='Preferred view for staff status page', verbose_name='staff_status_view'),
        ),
    ]
