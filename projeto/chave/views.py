from django.views.generic import DetailView

from chave.models import Chave, ChaveDupla
from dupla.models import Dupla
from etapa.models import Etapa
from utils.decorators import LoginRequiredMixin, TreinadorRequiredMixin


class ProcessamentoChaveDetailView(LoginRequiredMixin, TreinadorRequiredMixin, DetailView):
    model = Etapa
    template_name = 'chave/chaves_etapa.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.gerar_chaves()

    def gerar_chaves(self):
        if not Chave.objects.filter(etapa=self.object).exists() and \
                Dupla.objects.filter(atleta_direita__etapa=self.object).count() == self.object.total_duplas:
            indice_chaves = range(1, self.object.total_chaves + 1)
            j = 1
            for dupla in Dupla.objects.filter(atleta_direita__etapa=self.object):
                if j == len(indice_chaves):
                    j = 1
                chave = Chave.objects.get_or_create(etapa=self.object, nome=str(j))
                ChaveDupla.objects.create(chave=chave, dupla=dupla)
                j += 1

