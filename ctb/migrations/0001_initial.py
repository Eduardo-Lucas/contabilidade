# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 19:19
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('glb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_conta', models.PositiveSmallIntegerField(unique=True, verbose_name='Código da Conta')),
                ('descricao', models.CharField(max_length=80, verbose_name='Descrição da Conta')),
                ('tipo_conta', models.CharField(choices=[('A', 'Analítica'), ('S', 'Sintética'), ('G', 'Grupo')], max_length=1, verbose_name='Tipo da Conta')),
                ('conta_ativa', models.BooleanField(default=True, verbose_name='Ativa')),
                ('grau_conta', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(9)], verbose_name='Grau da Conta')),
                ('origem', models.CharField(choices=[('D', 'Débito'), ('C', 'Crédito')], default='D', max_length=1, verbose_name='Origem da Conta')),
                ('natureza', models.CharField(choices=[('D', 'Débito'), ('C', 'Crédito')], default='D', max_length=1, verbose_name='Natureza da Conta')),
                ('data_inclusao', models.DateField(auto_now_add=True, verbose_name='Data de Inclusão')),
                ('conta_referencial_bacen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Referencial_BACEN', to='glb.GlobalContaReferencialBacen')),
                ('conta_referencial_dinamica', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Referencial_Dinamica', to='glb.GlobContaReferencialDinamica')),
                ('conta_referencial_susep', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Referencial_Susep', to='glb.GlobContaReferencialSusep')),
                ('conta_saldo_balanco', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Resultado', to='ctb.Conta')),
                ('conta_superior', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Superior', to='ctb.Conta')),
            ],
            options={
                'verbose_name': 'Plano de Conta',
                'verbose_name_plural': 'Plano de Contas',
                'ordering': ['codigo_conta'],
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(default='MATRIZ', max_length=15, verbose_name='Código')),
                ('razao_social', models.CharField(max_length=60, verbose_name='Razão Social')),
                ('nome_fantasia', models.CharField(max_length=60, verbose_name='Nome Fantasia')),
                ('endereco', models.CharField(max_length=60, verbose_name='Endereço')),
                ('complemento', models.CharField(blank=True, default='', max_length=60, null=True)),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('bairro', models.CharField(max_length=30)),
                ('cep', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99999999)], verbose_name='CEP')),
                ('telefone1', models.CharField(default=0, max_length=15, verbose_name='Telefone #1')),
                ('telefone2', models.CharField(default=0, max_length=15, verbose_name='Telefone #2')),
                ('data_processamento', models.DateField(max_length=8)),
                ('data_competencia', models.DateField(max_length=8, verbose_name='Data de Competência')),
                ('site_empresa', models.CharField(blank=True, max_length=100, null=True, verbose_name='Site da Empresa')),
                ('email_empresa', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email da Empresa')),
                ('cnpj', models.PositiveSmallIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(99999999999999)], verbose_name='CNPJ')),
                ('inscricao_estadual', models.CharField(max_length=15, verbose_name='Inscrição Estadual')),
                ('inscricao_municipal', models.CharField(blank=True, max_length=15, null=True, verbose_name='Inscrição Municipal')),
                ('tipo_empresa', models.CharField(choices=[('SN', 'Simples Nacional'), ('LP', 'Lucro presumido'), ('LR', 'Lucro Real')], default='LR', max_length=2)),
                ('agrupa_itens_pedido', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], default='N', max_length=1)),
                ('bloqueia_clientes_em_atraso', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], default='S', max_length=1)),
                ('grau_conta', models.PositiveIntegerField(default=5, validators=[django.core.validators.MaxValueValidator(9)], verbose_name='Grau da Conta Contábil')),
                ('mascara_conta', models.CharField(default='9.9.99.99.999', max_length=15)),
                ('codigo_cnae', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glb.GlobalCodigoCnae')),
                ('contador_empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contador', to=settings.AUTH_USER_MODEL)),
                ('diretor_empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diretor', to=settings.AUTH_USER_MODEL)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glb.GlobalCodigoEstado')),
                ('gerente_empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gerente', to=settings.AUTH_USER_MODEL)),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glb.GlobalMunicipio')),
                ('natureza_juridica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glb.GlobalNaturezaJuridica')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'ordering': ('codigo',),
            },
        ),
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_historico', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(999)])),
                ('descricao', models.CharField(max_length=60)),
                ('ativo', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], default='S', max_length=1)),
            ],
            options={
                'verbose_name': 'Histórico Padrão',
                'verbose_name_plural': 'Históricos Padrões',
                'ordering': ['descricao'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='historico',
            unique_together=set([('codigo_historico', 'descricao')]),
        ),
        migrations.AlterUniqueTogether(
            name='conta',
            unique_together=set([('codigo_conta', 'descricao')]),
        ),
    ]