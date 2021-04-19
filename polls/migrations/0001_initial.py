# Generated by Django 3.1.7 on 2021-03-29 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('universities', models.ManyToManyField(to='polls.University')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_to_btn', models.CharField(max_length=300, unique=True)),
                ('link', models.CharField(max_length=300, unique=True)),
                ('journal_name', models.CharField(max_length=1900)),
                ('name', models.CharField(max_length=1500, unique=True)),
                ('abstract', models.CharField(max_length=4000, null=True)),
                ('publication_date', models.DateField(default='0000-1-1')),
                ('country', models.CharField(default='no country', max_length=50)),
                ('authors', models.ManyToManyField(to='polls.Author')),
                ('keywords', models.ManyToManyField(to='polls.Keyword')),
                ('universities', models.ManyToManyField(to='polls.University')),
            ],
        ),
    ]