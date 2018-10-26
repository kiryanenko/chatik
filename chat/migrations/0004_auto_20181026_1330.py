# Generated by Django 2.1.1 on 2018-10-26 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chat_last_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='has_read',
            field=models.BooleanField(default=False, help_text='Было ли прочитано данное сообщение.'),
        ),
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.Chat'),
        ),
    ]
