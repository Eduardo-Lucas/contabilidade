from django.db import models

# Create your models here.

"""
 1 Modulo possui 1 ou n Processos
 Mas 1 Processo pertence a 1 Modulo

 1 Rotina está pertence a 1 Processo
 1 Processo pode ter 1 ou n Rotinas

"""

from django.urls import reverse


class Modulo(models.Model):
    descricao = models.CharField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('menu:modulo-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['descricao', ]
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'


class Processo(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, default=1)
    descricao = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('menu:processo-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['descricao', ]
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'


class Rotina(models.Model):
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    nome_reduzido = models.CharField(max_length=20)
    url = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('menu:rotina-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome', ]
        verbose_name = 'Rotina'
        verbose_name_plural = 'Rotinas'


class Aba(models.Model):
    rotina = models.ForeignKey(Rotina, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    nome_reduzido = models.CharField(max_length=20)
    url = models.CharField(max_length=20)


class Tarefa(models.Model):
    rotina = models.ForeignKey(Rotina, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    nome_reduzido = models.CharField(max_length=20)
    url = models.CharField(max_length=20)
