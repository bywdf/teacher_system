# Generated by Django 5.2 on 2025-06-09 06:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='peteachersemester',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='eduadmin',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='deputyheadteacher',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='groupleadermidassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='itteacherfinalassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='teachermidassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='groupleaderfinalassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='teachersemesterassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='teacherfinalassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='headerteachermidassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='artteachermidassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='artteachersemesterassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='itteachermidassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='headerteachersemester',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='itteachersemester',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='groupleadersemester',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='peteacherfinalassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='artteacherfinalassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='peteachermidassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='headerteacherfinalassess',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='教师'),
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
