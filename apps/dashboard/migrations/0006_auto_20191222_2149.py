# Generated by Django 2.2.9 on 2019-12-22 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20191221_1155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clubcategory',
            options={'ordering': ['name'], 'verbose_name': 'kategoria klubów', 'verbose_name_plural': 'kategorie klubów'},
        ),
        migrations.AlterField(
            model_name='clubcategory',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='dashboard.ClubCategory', verbose_name='kategoria nadrzędna'),
        ),
    ]
