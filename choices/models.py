from django.db import models

# Create your models here.

DEBITO_CREDITO_CHOICES = (('D', 'Débito'), ('C', 'Crédito'))

FISICA_JURIDICA_CHOICES = (('F', 'Pessoa Física'), ('J', 'Pessoa Jurídica'))

MES_COMPETENCIA_CHOICES = ((1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'),
                           (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'),
                           (12, 'Dezembro'))

RECEITA_DESPESA_CHOICES = (('R', 'Receita'), ('C', 'Custos'), ('D', 'Despesas'))

SIM_NAO_CHOICES = (('S', 'Sim'), ('N', 'Não'))

STATUS_CHOICES = (('A', 'Aberta'), ('F', 'Fechada'), ('B', 'Bloqueada pela Contabildade'))

TIPO_CONTA_CHOICES = (('A', 'Analítica'), ('S', 'Sintética'), ('G', 'Grupo'))

TIPO_CONTA_REFERENCIAL_CHOICES = (('A', 'Analítica'), ('S', 'Sintética'),)

TIPO_EMPRESA_CHOICES = (('SN', 'Simples Nacional'),  ('LP', 'Lucro presumido'), ('LR', 'Lucro Real'),)

