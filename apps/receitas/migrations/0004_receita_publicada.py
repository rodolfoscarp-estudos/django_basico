# Generated by Django 2.2.6 on 2022-05-27 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receitas', '0003_receita_pessoa'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='publicada',
            field=models.BooleanField(default=False),
        ),
    ]