# Generated by Django 3.2.9 on 2022-04-10 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChessBoard',
            new_name='SuokuGame',
        ),
        migrations.RenameField(
            model_name='suokugame',
            old_name='game',
            new_name='game_board',
        ),
    ]
