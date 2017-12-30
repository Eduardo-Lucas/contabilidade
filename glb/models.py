from django.core.validators import MaxValueValidator
from django.db import models

from choices.models import SIM_NAO_CHOICES, TIPO_CONTA_REFERENCIAL_CHOICES, DEBITO_CREDITO_CHOICES


# Create your models here.

# *********************************************************************************************************************
# Código CNAE|Descrição do CNAE|Tipo de Atividade Econômica|O CNAE está no Simples?|Anexo Simples Nacional|Alíquota (%)
#  de Imposto|Precisa de Inscrição Estadual?|Observação sobre a Inscrição
# 0111-3/01|Cultivo de arroz||Sim|I|0,04|Sim|
# 0111-3/02|Cultivo de milho||Sim|I|0,04|Sim|
# Tabela base default = usesoftR3\TabelasGlobais\glob_naturezas_juridicas.txt
# *********************************************************************************************************************
class GlobalCodigoCnae(models.Model):
    codigo = models.CharField("Código", unique=True, max_length=10, null=False)
    descricao = models.CharField("Descrição", max_length=80, null=False)
    tipo_atividade = models.CharField("Tipo de Atividade", max_length=80, null=True, blank=True)
    # True = cnae do simples False = Nao é do simples
    simples_nacional = models.BooleanField("Simples Nacional", default=False)
    anexo_simples_nacional = models.CharField("AnexoSimples Nacional", max_length=3, default='')
    per_imposto = models.DecimalField("Percentual de Imposto", max_digits=4, decimal_places=2, default=0)
    # True = cnae precisa de inscricao estadual False = Nao precisa
    inscricao_estadual = models.BooleanField("Inscrição Estadual", default=False)

    def __str__(self):
        return self.codigo + " - " + self.descricao

    class Meta:
        unique_together = ('codigo', 'descricao')
        ordering = ('descricao',)
        verbose_name = 'Código do CNAE'
        verbose_name_plural = 'Códigos do CNAE'


# **********************************************************************************************************************
# TABELA DE NATUREZA JURÍDICA 2016   DOU nº 82, de 02 de maio de 2016, no qual foi publicada a Resolução Concla nº 1,
# de 28 de abril de 2016
# 101-5|1.Administração Pública|Órgão Público do Poder Executivo Federal
# 102-3|1.Administração Pública|Órgão Público do Poder Executivo Estadual ou do Distrito Federal
# Tabela base default = usesoftR3\TabelasGlobais\glob_naturezas_juridicas.txt
# *********************************************************************************************************************
class GlobalNaturezaJuridica(models.Model):
    codigo = models.CharField(unique=True, max_length=5, null=False)
    # 1.Administração Pública
    # 2.Entidades Empresariais
    # 3.Entidades sem Fins Lucrativos
    # 4.Pessoas Físicas
    # 5.Organizações Internacionais
    grupo = models.CharField(max_length=40, null=False)
    descricao = models.CharField(max_length=80, null=False)

    def __str__(self):
        return self.codigo + " - " + self.descricao

    class Meta:
        ordering = ('descricao',)
        verbose_name = 'Código de Natureza Jurídica'
        verbose_name_plural = 'Códigos de Naturezas Jurídicas'


# *********************************************************************************************************************
# TABELA SISTEMA FISCAL SEFAZ - NFE
# TABELAS GLOBAIS -   tb25.txt	- CodEstados
# Conteúdo da tabela: UF Código IBGE - Sigla
# 12|AC|01012009|
# 27|AL|01012009|
# 16|AP|01012009|
# *********************************************************************************************************************
class GlobalCodigoEstado(models.Model):
    codigo = models.PositiveIntegerField(null=False, unique=True, validators=[MaxValueValidator(99)])
    estado = models.CharField(null=False, max_length=2)
    data_inicial = models.DateField(max_length=10, default='2009-01-01')

    def __str__(self):
        return self.estado

    class Meta:
        ordering = ('estado',)
        verbose_name = 'Estado Brasileiro'
        verbose_name_plural = 'Estados Brasileiros'


# *********************************************************************************************************************
# TABELA SISTEMA FISCAL SEFAZ - NFE
# TABELAS GLOBAIS - tb1325.txt	- 	Municipios
# Conteúdo da tabela: Tabela de Municípios do IBGE
# versão=11 COD_MUN, NOM_MUN, DT_INI, DT_FIM
# 5300108|Brasília|01012009|
# 1400050|Alto Alegre|01012009|
# 1400027|Amajari|01012009|
# *********************************************************************************************************************
class GlobalMunicipio(models.Model):
    codigo = models.PositiveIntegerField(null=False, unique=True, validators=[MaxValueValidator(9999999)])
    descricao = models.CharField(null=False, max_length=256)
    data_inicial = models.DateField(max_length=8, default='2009-01-01')

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ('descricao',)
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'


# *********************************************************************************************************************
# plano de contas reverencial BACEN - glob_contas_referenciais_Bacen.txt
# versão=1 Codigo, Nome, DataInicio, DataFim, Tipo_Conta, COD_CTA_SU, NÍVEL_CONT, COD_NAT, Utilizacao
# 33|TOTAL GERAL DO ATIVO|01072005||S||1|1|S
# 95|TOTAL GERAL DO PASSIVO|01072005||S||1|2|S
# 39999993|TOTAL GERAL DO ATIVO|01061988|01071991|S||1||S
# *********************************************************************************************************************
class GlobalContaReferencialBacen(models.Model):
    codigo_conta = models.CharField("Código da Conta", unique=True, max_length=20, null=False)
    descricao = models.CharField("Descrição", max_length=80, null=False)
    data_inicio = models.DateField("Data de Início", max_length=8)
    data_fim = models.DateField("Data Final", max_length=8, null=True, blank=True)
    tipo_conta = models.CharField("Tipo de Conta", max_length=1, choices=TIPO_CONTA_REFERENCIAL_CHOICES)

    conta_superior = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    nivel_contabil = models.IntegerField("Nível Contábil")
    codigo_natureza = models.CharField("Natureza", max_length=1, choices=DEBITO_CREDITO_CHOICES, default='D')
    utilizacao = models.CharField("Utilização", max_length=1, choices=SIM_NAO_CHOICES, default='S')

    def __str__(self):
        return self.codigo_conta + self.descricao

    class Meta:
        ordering = ('codigo_conta',)
        verbose_name = 'Conta Referencial BACEN'
        verbose_name_plural = 'Contas Referenciais BACEN'


# *********************************************************************************************************************
# plano de contas reverencial BACEN - glob_contas_referenciais_Dinamica.txt
# versão=6 CODIGO, DESCRICAO, DT_INI, DT_FIM, ORDEM, TIPO, COD_SUP, NIVEL, NATUREZA
# 1.0.0.0.0.00.00|ATIVO GERAL|01012014||1|S||1|01
# 1.1.0.0.0.00.00|ATIVO|01012014||2|S|1.0.0.0.0.00.00|2|01
# *********************************************************************************************************************
class GlobContaReferencialDinamica(models.Model):
    codigo_conta = models.CharField("Código da Conta", unique=True, max_length=20, null=False)
    descricao = models.CharField("Descrição", max_length=80, null=False)
    data_inicio = models.DateField("Data de Início", max_length=8)
    data_fim = models.DateField("Data Final", max_length=8, null=True, blank=True)
    tipo_conta = models.CharField("Tipo de Conta", max_length=1)

    conta_superior = models.ForeignKey('self', on_delete=models.CASCADE)

    nivel_contabil = models.PositiveSmallIntegerField("Nível Contábil", validators=[MaxValueValidator(9)])
    codigo_natureza = models.CharField("Natureza", max_length=1, choices=DEBITO_CREDITO_CHOICES, default='D')
    utilizacao = models.CharField("Utilização", max_length=1, choices=SIM_NAO_CHOICES, default='S')

    def __str__(self):
        return self.codigo_conta + self.descricao

    class Meta:
        ordering = ('codigo_conta',)
        verbose_name = 'Conta Referencial Dinâmica BACEN'
        verbose_name_plural = 'Contas Referenciais Dinâmicas BACEN'


# *********************************************************************************************************************
# plano de contas reverencial BACEN - glob_contas_referenciais_Susep.txt
# versão=1 Codigo, Nome, DataInicio, DataFim, Tipo_Conta, COD_CTA_SU, NÍVEL_CONT, COD_NAT, Utilizacao
# 1|ATIVO|||S||1|1|S
# 11|CIRCULANTE|||S|1|2|1|S
# *********************************************************************************************************************
class GlobContaReferencialSusep(models.Model):
    codigo_conta = models.CharField("Código da Conta", unique=True, max_length=20, null=False)
    descricao = models.CharField("Descrição", max_length=80, null=False)
    data_inicio = models.DateField("Data de Início", max_length=8)
    data_fim = models.DateField("Data Final", max_length=8)
    tipo_conta = models.CharField("Tipo de Conta", max_length=1)

    conta_superior = models.ForeignKey('self', on_delete=models.CASCADE)

    nivel_contabil = models.IntegerField("Nível Contábil")
    codigo_natureza = models.CharField("Natureza", max_length=1, choices=DEBITO_CREDITO_CHOICES, default='D')
    utilizacao = models.CharField("Utilização", max_length=1, choices=SIM_NAO_CHOICES, default='S')

    def __str__(self):
        return self.codigo_conta + self.descricao

    class Meta:
        ordering = ('codigo_conta',)
        verbose_name = 'Conta Referencial SUSEP'
        verbose_name_plural = 'Contas Referenciais SUSEP'
