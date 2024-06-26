# Generated by Django 4.2.2 on 2024-06-10 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeBaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('knowledge_base_name', models.CharField(max_length=4, unique=True, verbose_name='知识库名')),
                ('maximum_block_length', models.IntegerField(verbose_name='每块最大长度')),
                ('repeated_character_length', models.IntegerField(verbose_name='重复字符长度')),
            ],
            options={
                'db_table': 'tb_knowledge_base',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='ModelClassModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='大模型种类名')),
            ],
            options={
                'db_table': 'tb_model_class',
            },
        ),
        migrations.CreateModel(
            name='SessionWindowModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('show_content', models.CharField(max_length=30, null=True, verbose_name='展示内容')),
            ],
            options={
                'db_table': 'tb_session_window',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='SessionRecordsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('session_content', models.TextField(verbose_name='单条会话记录')),
                ('model_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records_model_class', to='app.modelclassmodel', verbose_name='所属大模型类')),
                ('session_window', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='window_records', to='app.sessionwindowmodel', verbose_name='所属窗口')),
            ],
            options={
                'db_table': 'tb_session_records',
                'ordering': ['create_time'],
            },
        ),
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('file_name', models.CharField(max_length=20, verbose_name='文件名')),
                ('file_type', models.CharField(max_length=10, verbose_name='文件类型')),
                ('file_content', models.TextField()),
                ('knowledge_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_knowledge_base', to='app.knowledgebasemodel', verbose_name='所属知识库')),
            ],
            options={
                'db_table': 'tb_knowledge_base_file',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='FileChunkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('file_chunk_content', models.TextField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_chunk', to='app.filemodel', verbose_name='所属文件')),
                ('knowledge_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_chunk_knowledge_base', to='app.knowledgebasemodel', verbose_name='所属知识库')),
            ],
            options={
                'db_table': 'tb_file_chunk',
                'ordering': ['create_time'],
            },
        ),
    ]
