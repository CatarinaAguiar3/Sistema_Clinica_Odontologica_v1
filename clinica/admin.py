from django.contrib import admin
from .models import Dentista, Paciente, Consulta, Procedimento, AgendaTrabalho
from .forms import AgendaTrabalhoForm, ProcedimentoForm
from django import forms

# Register your models here.
# Dá permissão/acesso para o administrador manipular as models no admin site
# admin.site.register(Dentista)
# admin.site.register(Paciente)
# admin.site.register(Consulta)
# admin.site.register(Procedimento)


# Decorator que registra a model "AgendaTrabalho" no no admin do Django usando a a classe "AgendaTrabalhoAdmin"
@admin.register(AgendaTrabalho)
# Classe para controlar a exibição e o comportamento da model "AgendaTrabalho" no admin do Django.
class AgendaTrabalhoAdmin(admin.ModelAdmin):
    form = AgendaTrabalhoForm
    list_display = ("dentista", "dia_semana", "horario_inicio", "horario_fim")
    list_filter = ("dentista", "dia_semana")


class DentistaAdmin(admin.ModelAdmin):
    list_display = ("nome","especialidade", "telefone")
    list_filter = ("especialidade",)
    search_fields = ("nome", "especialidade")


class PacienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone","email")
    search_fields = ("nome", "cpf", "email")    


class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("data", "horario_inicio", "status", "paciente", "dentista","procedimento")
    search_fields = ("paciente__nome", "dentista__nome", "procedimento__nome")    

@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    form = ProcedimentoForm
    list_display = ("procedimento", "tempo_estimado")    

if admin.site is not None:
    admin.site.register(Dentista, DentistaAdmin)
    admin.site.register(Paciente, PacienteAdmin)
    admin.site.register(Consulta, ConsultaAdmin)
    #admin.site.register(Procedimento, ProcedimentoAdmin)    