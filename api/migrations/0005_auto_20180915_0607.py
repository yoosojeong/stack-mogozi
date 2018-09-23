# Generated by Django 2.1.1 on 2018-09-15 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170620_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('value1', models.CharField(max_length=255)),
                ('value2', models.CharField(max_length=255)),
                ('value3', models.CharField(max_length=255)),
                ('value4', models.CharField(max_length=255)),
                ('reg_date', models.DateField(auto_now_add=True, verbose_name='REG_DATE')),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('u_id', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RemoveField(
            model_name='history',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='history',
            name='user',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='category',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='distance',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='weather',
        ),
        migrations.RemoveField(
            model_name='star',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='star',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='star',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='restaurant',
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserModel'),
        ),
        migrations.DeleteModel(
            name='Distance',
        ),
        migrations.DeleteModel(
            name='History',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
        migrations.DeleteModel(
            name='Star',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Weather',
        ),
        migrations.AddField(
            model_name='comment',
            name='PostModel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.PostModel'),
            preserve_default=False,
        ),
    ]
