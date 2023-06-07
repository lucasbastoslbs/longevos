from __future__ import unicode_literals

from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from datetime import timedelta, datetime

from utils.gerador_hash import gerar_hash


class AdministradorAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='ADMINISTRADOR', is_active=True)


class TreinadorAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='TREINADOR', is_active=True)


class AtletaAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='ATLETA', is_active=True)        


class Usuario(AbstractBaseUser):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    TIPOS_USUARIOS = (
        ('ADMINISTRADOR', 'Administrador'),
        ('TREINADOR', 'Treinador' ),
        ('ATLETA', 'Atleta' ),
    )    
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    POSICAO = (
        ('DIREITA', 'Direita'),
        ('ESQUERDA', 'Esquerda' ),
        ('AMBAS', 'Ambas' ),
    )

    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    GRUPO = (
        ('A', 'A'),
        ('B', 'B' ),
        ('AMBAS','Ambas')
    )
 
    USERNAME_FIELD = 'celular'

    tipo = models.CharField('Tipo do usuário *', max_length=15, choices=TIPOS_USUARIOS, default='ATLETA', help_text='* Campos obrigatórios')
    grupo = models.CharField('Turma Longeva', max_length=5, choices=GRUPO, null=True, blank=False)
    nome = models.CharField('Nome completo *', max_length=100)
    apelido = models.CharField('Apelido', max_length=50, null = True, blank= False, help_text='Se não tem apelido, colocar o primeiro nome')
    data_nascimento = models.DateField('Data nascimento *', null = True, blank = True, help_text="Use dd/mm/aaaa")
    email = models.EmailField('Email ', max_length=100, null = True, blank = True, help_text="O email é fundamental para recuperar senha")
    celular = models.CharField('Número celular com DDD', unique=True, max_length=11, db_index=True, help_text="Use DDD, por exemplo 55987619832")
    
    posicao = models.CharField('Posição na quadra *', max_length=8, choices=POSICAO)
    pontuacao = models.IntegerField('Pontuação do atleta', null=True, blank=True, default=0)
    qtd_etapas_jogadas = models.IntegerField('Quantidade de etapas que participou', null=True, blank=True, default=0)
    
    is_active = models.BooleanField(_('Ativo'), default=False, help_text='Se ativo, o usuário tem permissão para acessar o sistema')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = UserManager()
    administradores = AdministradorAtivoManager()
    treinadores = TreinadorAtivoManager()
    atletas = AtletaAtivoManager()
    

    class Meta:
        ordering            =   ['-is_active','tipo','grupo', '-pontuacao', '-qtd_etapas_jogadas', 'apelido']
        verbose_name        =   ('longevo')
        verbose_name_plural =   ('longevos')

    def __str__(self):
        if self.apelido:
            return '%s: %s. %s' % (self.grupo, self.apelido, self.posicao)
        return '%s: %s. %s' % (self.grupo, self.apelido, self.posicao)


    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def get_short_name(self):
        return self.nome[0:15].strip()

    def get_full_name(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.nome = self.nome.upper()
        if self.apelido:
            self.apelido = self.apelido.upper()        
        if not self.id:
            self.set_password(self.password) #criptografa a senha digitada no forms
        super(Usuario, self).save(*args, **kwargs)

    def get_id(self):
        return self.id
    
    @property
    def idade(self):
        try:
            return  datetime.now().year - self.data_nascimento.year
        except:
            return 0

    @property
    def get_primeiro_nome(self):
        lista = self.nome.split(" ")
        return lista[0]

    @property
    def is_staff(self):
        if self.tipo == 'ADMINISTRADOR':
            return True
        return False

    @property
    def get_absolute_url(self):
        return reverse('usuario_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('usuario_delete', args=[str(self.id)])

    @property
    def get_usuario_register_activate_url(self):
        return '%s%s' % (settings.DOMINIO_URL, reverse('usuario_register_activate', kwargs={'slug': self.slug}))
