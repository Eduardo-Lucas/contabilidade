from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.db import transaction
from django.db.models.signals import post_save, pre_delete

from choices.models import DEBITO_CREDITO_CHOICES, TIPO_CONTA_CHOICES, TIPO_EMPRESA_CHOICES, SIM_NAO_CHOICES, \
    STATUS_CHOICES
from glb.models import GlobContaReferencialDinamica, GlobContaReferencialSusep, \
    GlobalContaReferencialBacen, GlobalMunicipio, GlobalCodigoEstado, GlobalCodigoCnae, GlobalNaturezaJuridica


# Validators
def validate_maior_que_zero(value):
    if value <= 0:
        raise ValidationError(
            'O código da Conta tem que ser MAIOR QUE ZERO',
            params={'value': value},
        )


def validate_valor_minimo(value):
    if value <= 0:
        raise ValidationError(
            'O valor do lançamento NÃO PODE SER ZERO ou MENOR QUE ZERO. O valor mínimo permitido é: R$ 0,01',
            params={'value': value},
        )


valor_numerico = RegexValidator(r'^[0-9]*$', 'Apenas valores numéricos, de 0 até 9, são permitidos.')


# Create your models here.

# **********************************************************************************************
# ARQUIVO DE EMPRESAS USUARIAS DO SISTEMA - TABELAS GENERICAS DO SISTEMA USESOFT-R3
# (usesoft=KSBIUS)
# Tabela base default = usesoftR3\TabelasGlobais\glob_naturezas_de_custos.txt
# **********************************************************************************************
class Empresa(models.Model):
    codigo = models.CharField("Código", max_length=15, null=False, default="MATRIZ", unique=True)
    razao_social = models.CharField("Razão Social", max_length=60, null=False)
    nome_fantasia = models.CharField("Nome Fantasia", max_length=60, null=False)
    endereco = models.CharField('Endereço', max_length=60, null=False)
    complemento = models.CharField(max_length=60, default='', null=True, blank=True)
    numero = models.CharField('Número', max_length=10)
    bairro = models.CharField(max_length=30, null=False)
    cep = models.PositiveIntegerField("CEP", null=False, validators=[MaxValueValidator(99999999)])
    municipio = models.ForeignKey(GlobalMunicipio, default=2927408)
    estado = models.ForeignKey(GlobalCodigoEstado)
    telefone1 = models.CharField("Telefone #1", max_length=15, default=0)
    telefone2 = models.CharField("Telefone #2", max_length=15, default=0)

    data_processamento = models.DateField(null=True, blank=True, auto_now_add=True)
    data_competencia = models.DateField('Data de Competência', null=True, blank=True)

    natureza_juridica = models.ForeignKey(GlobalNaturezaJuridica)

    site_empresa = models.CharField("Site da Empresa", max_length=100, blank=True, null=True)
    email_empresa = models.EmailField("Email da Empresa", max_length=100, blank=True, null=True)

    # -----------------------------------------------------------------------------------------------------------------
    # A regra básica para seleção do tipo quando eles podem ser confundidos é para que vai usá - los.Números representam
    # quantidades.CPF ou CNPJ são quantidades? Não, são identificadores que podem até mesmo mudar, que podem um dia ter
    # letras.A semântica correta para este dado é o varchar.
    # -----------------------------------------------------------------------------------------------------------------
    cnpj = models.CharField("CNPJ", unique=True, null=False, max_length=14)

    inscricao_estadual = models.CharField('Inscrição Estadual', max_length=15)
    inscricao_municipal = models.CharField('Inscrição Municipal', max_length=15, blank=True, null=True)
    codigo_cnae = models.ForeignKey(GlobalCodigoCnae)
    # "SN" - simples nacional
    # "LP" - Lucro presumido
    # "LR" - Lucro REAL
    tipo_empresa = models.CharField(max_length=2, choices=TIPO_EMPRESA_CHOICES, default='LR')
    gerente_empresa = models.ForeignKey(User, related_name='gerente', blank=True, null=True)
    diretor_empresa = models.ForeignKey(User, related_name='diretor', blank=True, null=True)
    contador_empresa = models.ForeignKey(User, related_name='contador', blank=True, null=True)

    # configuracoes customizaveis por empresa
    # "S" neste campo para que sistema agrupe numero de itens na venda balcao por codigo se houver codigos repetidos
    agrupa_itens_pedido = models.CharField(max_length=1, choices=SIM_NAO_CHOICES, default="N")

    # "S" neste campo para que o cliente seja automaticamente bloqueado durante"
    # o fechamento de uma venda no balcao ou no caixa
    bloqueia_clientes_em_atraso = models.CharField(max_length=1, choices=SIM_NAO_CHOICES, default="S")
    grau_conta = models.PositiveIntegerField("Grau da Conta Contábil", null=False, validators=[MaxValueValidator(9)],
                                             default=5)
    mascara_conta = models.CharField(max_length=15, default="9.9.99.99.999")

    def get_absolute_url(self):
        return reverse('ctb:empresa-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.codigo) + " - " + str(self.razao_social)

    class Meta:
        ordering = ('codigo',)
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


# **********************************************************************************************
# HISTORICO PADRAO
# **********************************************************************************************
class Historico(models.Model):
    codigo_historico = models.PositiveSmallIntegerField('Código do Histórico', validators=[MaxValueValidator(999)])
    descricao = models.CharField(max_length=60)
    ativo = models.CharField(max_length=1, choices=SIM_NAO_CHOICES, default="S")

    def get_absolute_url(self):
        return reverse('ctb:historico-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.codigo_historico) + " - " + str(self.descricao)

    class Meta:
        ordering = ['descricao']
        unique_together = ('codigo_historico', 'descricao')
        verbose_name = 'Histórico Padrão'
        verbose_name_plural = 'Históricos Padrões'


# **********************************************************************************************
# ARQUIVO DE CONTAS CONTABEIS
# (usesoft=KCGI03)
# **********************************************************************************************
class Conta(models.Model):
    codigo_conta = models.CharField("Código da Conta", max_length=9, unique=True, null=False,
                                    validators=[valor_numerico])
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

    data_inclusao = models.DateField("Data de Inclusão", null=False, blank=True, auto_now_add=True)
    conta_referencial_bacen = models.ForeignKey(GlobalContaReferencialBacen, related_name='Referencial_BACEN',
                                                blank=True, null=True)
    conta_referencial_dinamica = models.ForeignKey(GlobContaReferencialDinamica, related_name='Referencial_Dinamica',
                                                   blank=True, null=True)
    conta_referencial_susep = models.ForeignKey(GlobContaReferencialSusep, related_name='Referencial_Susep',
                                                blank=True, null=True)

    def get_absolute_url(self):
        return reverse('ctb:conta-detail', kwargs={'pk': self.pk})

    def conta_negrito(self):
        if self.grau_conta == 4:
            return False
        else:
            return True

    def __str__(self):
        return str(self.codigo_conta) + " " + str(self.descricao)

    class Meta:
        ordering = ['codigo_conta']
        unique_together = ('codigo_conta', 'descricao')
        verbose_name = 'Plano de Conta'
        verbose_name_plural = 'Plano de Contas'


# **********************************************************************************************
# DATAS DE FECHAMENTO DAS COMPETÊNCIAS
# **********************************************************************************************
class Competencia(models.Model):
    # neste campo data o dia será sempre o último dia do mes
    data_competencia = models.DateField(unique=True, help_text='Digite no formato: dd/mm/aaaa')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="A")

    def get_absolute_url(self):
        return reverse('ctb:competencia-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.data_competencia.strftime('%Y-%m-%d'))
        # return str(self.data_competencia.strftime('%d/%m/%Y'))

    class Meta:
        ordering = ['-data_competencia']
        verbose_name = 'Competência'
        verbose_name_plural = 'Competências'


class Modulo(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return str(self.descricao)

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'


class Participante(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return str(self.descricao)

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'


class TipoMovimento(models.Model):
    descricao = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.descricao) + " - " + str(self.modulo)

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Tipo de Movimento'
        verbose_name_plural = 'Tipos de Movimentos'


class TipoDocumento(models.Model):
    sigla = models.CharField(max_length=3, unique=True, default='CHQ')
    descricao = models.CharField(max_length=50, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.sigla) + " - " + str(self.descricao)

    class Meta:
        unique_together = ['sigla', 'descricao']
        ordering = ['descricao']
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'


# MOVIMENTOS CONTABEIS HEADER
class MovimentoContabilHeader(models.Model):
    tipo_movimento = models.ForeignKey(TipoMovimento, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User)
    data_lancamento = models.DateField(null=False, blank=False, auto_now_add=True)
    data_competencia = models.ForeignKey(Competencia)
    total_debito = models.DecimalField(max_length=16, max_digits=16, decimal_places=2, default=0.00)
    total_credito = models.DecimalField(max_length=16, max_digits=16, decimal_places=2, default=0.00)

    def get_absolute_url(self):
        return reverse('ctb:movimento-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "Comp.: " + str(self.data_competencia) + " - " + "Mov.: " + str(self.tipo_movimento) + \
               " Seq.: " + str(self.id)

    def status_header(self):
        if self.total_debito != self.total_credito:
            return False
        elif self.total_debito + self.total_credito == 0:
            return False
        else:
            return True

    class Meta:
        ordering = ['-id']
        verbose_name = 'Movimento Contábil'
        verbose_name_plural = 'Movimentos Contábeis (Header)'


# LANCAMENTOS CONTABEIS
class LancamentoContabil(models.Model):
    header = models.ForeignKey(MovimentoContabilHeader, on_delete=models.CASCADE)
    conta = models.ForeignKey(Conta)
    saldo_anterior = models.DecimalField(max_length=16, max_digits=16, decimal_places=2, default=0.00)
    valor = models.DecimalField(max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                validators=[validate_valor_minimo], help_text='Informe valor positivo.')
    d_c = models.CharField('D/C', max_length=1, choices=DEBITO_CREDITO_CHOICES, default='D')
    saldo_final = models.DecimalField(max_length=16, max_digits=16, decimal_places=2, default=0.00)
    codigo_historico = models.ForeignKey(Historico)
    historico = models.TextField('Histórico', max_length=200)
    codigo_participante = models.ForeignKey(Participante, blank=True, null=True, default='')
    tipo_documento = models.ForeignKey(TipoDocumento, max_length=3, blank=True, null=True, on_delete=models.CASCADE)
    numero_documento = models.CharField('Número do Documento', max_length=10, blank=True, null=True, default='')
    data_documento = models.DateField('Data do Documento', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('ctb:lancamento-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "Header: " + str(self.header) + " Conta: " + str(self.conta) + " Valor: " + str(
            self.valor) + " D_C: " + str(self.d_c)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Lançamento Contábil'
        verbose_name_plural = 'Lançamentos Contábeis (Lançamentos)'


class SaldoContaContabil(models.Model):
    data_competencia = models.ForeignKey(Competencia)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    natureza = models.CharField(max_length=1, default='D')
    saldo_inicial = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    debitos = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    creditos = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    def get_absolute_url(self):
        return reverse('ctb:saldo-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "Competência: " + str(self.data_competencia) + " Conta Contábil: " + str(self.conta) + \
               " Saldo Inicial: " + str(self.saldo_inicial) + \
               " - Total de Débitos: " + str(self.debitos) + \
               " - Total de Créditos:" + str(self.creditos) + \
               " Saldo Final: " + str(self.saldo_inicial + self.debitos - self.creditos)

    def saldo_final(self):
        if self.natureza == 'D':
            return self.saldo_inicial + self.debitos - self.creditos
        else:
            return self.saldo_inicial + self.creditos - self.debitos

    class Meta:
        ordering = ['conta', '-data_competencia', ]
        unique_together = ['data_competencia', 'conta']
        verbose_name = 'Saldo da Conta Contábil'
        verbose_name_plural = 'Saldos das Contas Contábeis'


"""
    SIGNALS
"""


def aumenta_saldo(sender, **kwargs):
    if kwargs['instance'].d_c == 'D':
        saldo, created = SaldoContaContabil.objects.get_or_create(data_competencia=kwargs['instance'].
                                                                  header.data_competencia,
                                                                  conta=kwargs['instance'].conta,
                                                                  defaults={'debitos': kwargs['instance'].valor})
    else:
        saldo, created = SaldoContaContabil.objects.get_or_create(data_competencia=kwargs['instance'].
                                                                  header.data_competencia,
                                                                  conta=kwargs['instance'].conta,
                                                                  defaults={'creditos': kwargs['instance'].valor})

    if not created:
        with transaction.atomic():
            saldo = (
                SaldoContaContabil.objects.select_for_update().get(data_competencia=kwargs['instance'].header.
                                                                   data_competencia,
                                                                   conta=kwargs['instance'].conta))
        if kwargs['instance'].d_c == 'D':
            saldo.debitos += kwargs['instance'].valor
        else:
            saldo.creditos += kwargs['instance'].valor
        saldo.save()

    atualiza_meses_subsequentes(kwargs['instance'].header.data_competencia, conta=kwargs['instance'].conta)


def diminui_saldo(sender, **kwargs):
    with transaction.atomic():
        saldo = (SaldoContaContabil.objects.select_for_update().get(data_competencia=kwargs['instance'].
                                                                    header.data_competencia,
                                                                    conta=kwargs['instance'].conta))
    if saldo:
        if kwargs['instance'].d_c == 'D':
            saldo.debitos -= kwargs['instance'].valor
        else:
            saldo.creditos -= kwargs['instance'].valor
        saldo.save()

    atualiza_meses_subsequentes(kwargs['instance'].header.data_competencia, conta=kwargs['instance'].conta)


def cria_saldo_contabil(sender, **kwargs):
    """
    Para cada conta criada, são criados registros na class SaldosContabil, com um registro para cada registro da
    Competencia, dentro de um ano
    :param conta:
    :return:
    """
    if kwargs['created']:
        for m in Competencia.objects.all():
            # print(type(m.id))
            # print(m.data_competencia)
            saldo = SaldoContaContabil(data_competencia=m, conta=kwargs['instance'],
                                       natureza=kwargs['instance'].natureza)
            saldo.save()


def atualiza_meses_subsequentes(data_competencia, conta):
    """
        AUMENTA SALDO DOS MESES SUBSEQUENTES
    """
    saldo_final = 0
    for idx, s in enumerate(SaldoContaContabil.objects.filter(
            data_competencia__gte=data_competencia, conta=conta
    )
    ):
        if idx == 0:
            if s.natureza == 'D':
                saldo_final = s.saldo_inicial + s.debitos - s.creditos
            else:
                saldo_final = s.saldo_inicial + s.creditos - s.debitos
        else:
            s.saldo_inicial = saldo_final
            s.save()
            if s.natureza == 'D':
                saldo_final = s.saldo_inicial + s.debitos - s.creditos
            else:
                saldo_final = s.saldo_inicial + s.creditos - s.debitos


"""
    AQUI SAO LISTADOS OS EVENTOS QUE DISPARAM AS FUNÇÕES
"""
post_save.connect(cria_saldo_contabil, sender=Conta)
post_save.connect(aumenta_saldo, sender=LancamentoContabil)
pre_delete.connect(diminui_saldo, sender=LancamentoContabil)


# TODO Contas Redutoras do Ativo:
# TODO Também chamadas de retificadoras, as contas redutoras são contas que, embora apareçam num determinado
# TODO grupo patrimonial (Ativo ou Passivo), TÊM SALDO CONTRÁRIO EM RELAÇÃO ÀS DEMAIS CONTAS DESSE GRUPO.
# TODO Desse modo, uma conta redutora do Ativo terá natureza credora, bem como uma conta redutora do Passivo terá
# TODO natureza devedora.
# TODO As contas retificadoras reduzem o saldo total do grupo em que aparecem. A seguir, veremos algumas contas
# TODO retificadoras do grupo Ativo:

# TODO Consolidar a estrutura da class LancamentoContabil
# TODO Criar uma class chamada SaldoContabil para acumular o valor dos LancamentoContabil
# TODO Cada vez que uma Conta for criada, a class SaldoContaContabil deve ser atualizada com os registros
# TODO Criar um Signal para atualizar SaldoContabil a cada transação na class LancamentoContabil
# TODO Prever as seguintes transações na class LancamentoContabil: create, update and delete
# TODO A tela de LancamentoContabil deve usar formset
# TODO Criar uma class UserSession para controlar quantas sessões ativas um Usuário pode ter
# TODO Criar rotinas para inserir nas tabelas a partir de arquivos
