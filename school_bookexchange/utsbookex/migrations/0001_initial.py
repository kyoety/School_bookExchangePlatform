# Generated by Django 3.1.5 on 2021-05-24 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BeUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=100)),
                ('upickup', models.CharField(max_length=50)),
                ('ugrade', models.CharField(blank=True, max_length=2, null=True)),
                ('udate', models.DateField(auto_now_add=True)),
                ('uimage', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('umail', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bookforsale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bimage', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('bname', models.CharField(max_length=50)),
                ('bqual', models.CharField(max_length=10)),
                ('bgrade', models.CharField(max_length=5)),
                ('bsubject', models.CharField(max_length=10)),
                ('bprice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bdescript', models.CharField(blank=True, max_length=255, null=True)),
                ('bdate', models.DateField(auto_now_add=True)),
                ('buser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsbookex.beuser')),
            ],
        ),
    ]
