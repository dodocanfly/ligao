# Generated by Django 2.2.9 on 2020-01-05 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20200105_1257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ('name',), 'verbose_name': 'organizacja', 'verbose_name_plural': 'organizacje'},
        ),
        migrations.AlterModelOptions(
            name='season',
            options={'ordering': ('name',), 'verbose_name': 'sezon rozgrywek', 'verbose_name_plural': 'sezony rozgrywek'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='season',
            unique_together={('organization', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together={('category', 'name')},
        ),
    ]
