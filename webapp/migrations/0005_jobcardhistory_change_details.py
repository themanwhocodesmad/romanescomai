# Generated by Django 4.1.7 on 2023-10-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_knowledgebase_remove_jobcardhistory_change_details_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcardhistory',
            name='change_details',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
