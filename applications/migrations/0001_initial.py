import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0002_jobaddress_jobpostphoto_job'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_letter', models.TextField(blank=True, null=True)),
                ('application_date_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('NotSeen', 'Not seen'), ('Seen', 'Seen'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='NotSeen', max_length=50)),
                ('agreed_price', models.FloatField()),
                ('currency_type', models.CharField(choices=[('Birr', 'Birr'), ('USD', 'USD')], default='Birr', max_length=20)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='jobs.job')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker_applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('paid_price', models.FloatField()),
                ('currency_type', models.CharField(choices=[('Birr', 'Birr'), ('USD', 'USD')], default='Birr', max_length=20)),
                ('score', models.PositiveIntegerField(default=0)),
                ('was_paid', models.BooleanField(default=False)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.application')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobs.job')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
