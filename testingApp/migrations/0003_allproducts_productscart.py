# Generated by Django 3.2.21 on 2023-10-21 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testingApp', '0002_alter_captchacpde_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='allProducts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(default='', upload_to='img/allProducts/%Y/%m')),
                ('price', models.IntegerField(default=0, max_length=10)),
                ('category', models.CharField(default='Other', max_length=50)),
                ('desc', models.TextField(default='', max_length=5000)),
                ('time', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='productsCart',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('prod_ids', models.CharField(default='[]', max_length=100)),
                ('usrname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
