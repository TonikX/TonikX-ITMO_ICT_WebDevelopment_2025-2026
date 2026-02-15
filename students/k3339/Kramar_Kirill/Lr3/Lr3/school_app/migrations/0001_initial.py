import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('parallel', models.IntegerField()),
                ('class_number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('subject_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(max_length=10)),
                ('klass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.class')),
            ],
        ),
        migrations.CreateModel(
            name='QuarterGrade',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('grade', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school_app.classroom')),
                ('subject', models.ManyToManyField(to='school_app.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('weekday', models.CharField(max_length=50)),
                ('lesson_number', models.CharField(max_length=2)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.classroom')),
                ('klass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.class')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='class_teacher',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_leader', to='school_app.teacher'),
        ),
    ]
