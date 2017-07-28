from django.core.validators import MaxValueValidator
from django.db import models
from django.core.urlresolvers import reverse

from choices.models import DEBITO_CREDITO_CHOICES, TIPO_CONTA_CHOICES
from glb.models import GlobalEmpresa, GlobContaReferencialDinamica, GlobContaReferencialSusep, \
    GlobalContaReferencialBacen

SIM_NAO_CHOICES = (('S', 'Sim'), ('N', 'Não'))


# Create your models here.

# **********************************************************************************************
# HISTORICO PADRAO
# **********************************************************************************************
class Historico(models.Model):
    empresa = models.ForeignKey(GlobalEmpresa, default=1)
    codigo_historico = models.PositiveSmallIntegerField(validators=[MaxValueValidator(999)])
    descricao = models.CharField(max_length=60)
    ativo = models.CharField(max_length=1, choices=SIM_NAO_CHOICES, default="S")

    def get_absolute_url(self):
        return reverse('ctb:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.codigo_historico) + " - " + str(self.descricao)

    class Meta:
        ordering = ['descricao']
        unique_together = ('codigo_historico', 'descricao')
        # unique_together = ("empresa", 'codigo_historico',)
        verbose_name = 'Histórico Padrão'
        verbose_name_plural = 'Históricos Padrões'


# **********************************************************************************************
# ARQUIVO DE CONTAS CONTABEIS
# (usesoft=KCGI03)
# **********************************************************************************************
class Conta(models.Model):
    empresa = models.ForeignKey(GlobalEmpresa)
    codigo_conta = models.PositiveSmallIntegerField("Código da Conta", unique=True, null=False)
    descricao = models.CharField("Descrição da Conta", max_length=80, null=False)
    # [A] Analitica [S] Sintetica [G] Grupo
    tipo_conta = models.CharField("Tipo da Conta", max_length=1, choices=TIPO_CONTA_CHOICES)
    # True = ativa False = inativa
    conta_ativa = models.BooleanField("Ativa", default=True)
    grau_conta = models.PositiveSmallIntegerField("Grau da Conta", null=False, validators=[MaxValueValidator(9)])
    # codigo da conta de grau imediatamente superior ao grau desta conta
    # tem como objetivo acumular valores no plano de contas automaticamente a cada lançamento
    conta_superior = models.ForeignKey('self', related_name='Superior', blank=True, null=True)
    # codigo da conta do passivo para onde irão automaticamente os saldos de receita e despesa
    # quando for feita a apuração do resultado periódica
    # apuração zera receita e despesa e transfere resultado para conta de balanço
    conta_saldo_balanco = models.ForeignKey('self', related_name='Resultado', blank=True, null=True)
    # "M" = RAZAO E DIARIO SÃO CONCENTRADOS EM 1 LANÇAMENTO POR MÊS
    # "D" = RAZAO E DIARIO SERÃO CONCENTRADOS EM LANÇAMENTO POR DIA
    # ****************************************************************
    # diario_razao = models.CharField(max_length=1, null=False)
    # "D" = PARA CONTA PREDOMINANTEMENTE DEVEDORA
    # "C" = PREDOMINANCIA CREDORA
    # ****************************************************************
    origem = models.CharField("Origem da Conta", max_length=1, choices=DEBITO_CREDITO_CHOICES, default='D')
    natureza = models.CharField("Natureza da Conta", max_length=1, choices=DEBITO_CREDITO_CHOICES, default='D')

    data_inclusao = models.DateField("Data de Inclusão", null=False, auto_now_add=True)
    conta_referencial_bacen = models.ForeignKey(GlobalContaReferencialBacen, related_name='Referencial_BACEN',
                                                blank=True, null=True)
    conta_referencial_dinamica = models.ForeignKey(GlobContaReferencialDinamica, related_name='Referencial_Dinamica',
                                                   blank=True, null=True)
    conta_referencial_susep = models.ForeignKey(GlobContaReferencialSusep, related_name='Referencial_Susep',
                                                blank=True, null=True)

    def __str__(self):
        return str(self.codigo_conta) + " " + str(self.descricao)

    class Meta:
        ordering = ["codigo_conta"]
        unique_together = (('empresa', 'codigo_conta'),)
        verbose_name = 'Plano de Conta'
        verbose_name_plural = 'Plano de Contas'
