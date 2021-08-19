# Generated by Django 3.2.6 on 2021-08-19 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('CN', models.CharField(choices=[('', None), ('MILK', 'MILK'), ('SIZE', 'SIZE'), ('SHOTS', 'SHOTS'), ('KIND', 'KIND')], max_length=6, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('customization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customization')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customization', models.CharField(max_length=50, null=True)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text="Price would be calculated automatically.DON'T ENTER", max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('preparation', 'Preparation'), ('ready', 'Ready'), ('delivered', 'Delivered')], default='waiting', max_length=12)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.production')),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tag')),
            ],
        ),
        migrations.AddField(
            model_name='customization',
            name='production',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.production'),
        ),
    ]
