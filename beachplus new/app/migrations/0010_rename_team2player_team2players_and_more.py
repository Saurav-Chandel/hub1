# Generated by Django 4.0.2 on 2022-02-08 12:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_hostinvitation_unique_together'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Team2Player',
            new_name='Team2Players',
        ),
        migrations.RenameField(
            model_name='team2players',
            old_name='hostmatch',
            new_name='host_match',
        ),
        migrations.CreateModel(
            name='PlayersRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('host_match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hostmatch')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
            ],
        ),
    ]
