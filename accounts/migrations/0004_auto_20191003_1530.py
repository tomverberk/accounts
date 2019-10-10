# Generated by Django 2.2.5 on 2019-10-03 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_exam_exercise_module_submodule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapterIntelligence', models.IntegerField(default=0)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Chapter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Module_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currentModule', models.BooleanField(default=False)),
                ('amountCorrect', models.IntegerField(default=0)),
                ('amountWrong', models.IntegerField(default=0)),
                ('amountHints', models.IntegerField(default=0)),
                ('moduleScore', models.IntegerField(default=0)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generalIntelligence', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Score',
        ),
    ]
