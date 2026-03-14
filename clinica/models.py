from django.db import models
from django.core.exceptions import ValidationError # É utilizado no método "clean" da classe "Consulta" para indicar que o dentista já possui uma consulta agendada no mesmo horário.

# Create your models here.
class Dentista(models.Model): # O trecho "models.Model" explicíta para o django que esta classe se comporta como uma tabela
    nome = models.CharField(max_length=100) # O trecho "models.CharField" explicíta para o django que esta coluna se comporta como um campo de texto, e o "max_length" define o tamanho máximo do campo.
    registro = models.CharField(max_length=100, unique=True) # registro é um campo para colocar o registro do dentista (cro)
    especialidade = models.CharField(max_length=500)
    email = models.EmailField(max_length=254, unique=True)
    telefone = models.CharField(max_length=20)

    def __str__(self): # __str__ é um método especial do python que define a representação em string do objeto, ou seja, como ele aparece quando é impresso ou exibido no admin do django.
                       # self representa o próprio objeto que está sendo usado. Ou seja, self aponta para o dentista específico que está sendo representado.
        """    
        Define como o objeto aparece no admin do Django e no shell.
        Exemplo, sem isso apareceria:
            Dentista object (1)
            Dentista object (2)
        Com isso, aparecerá o nome do dentista:
            Dr. João
            Dra Maria    
        """
        return self.nome
    
class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    cpf= models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()    
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.nome

# OBS: Na classe consulta, estou usando o código ForeignKey para criar um relacionamento 1 para muitos:
#      Link 1: https://docs.djangoproject.com/en/6.0/ref/models/fields/#django.db.models.ForeignKey
#      Link 2: https://docs.djangoproject.com/en/6.0/topics/db/examples/many_to_one/ 
#
#      Se eu quisesse criar um relacionamento 1 para 1, usaria o código OneTooneField: https://docs.djangoproject.com/en/6.0/topics/db/examples/one_to_one/
#      E se eu quisesse criar um relacionamento muitos para muitos, usaria ManyToManyfield: https://docs.djangoproject.com/en/6.0/topics/db/examples/many_to_many/
class Consulta(models.Model):  
    """ Tabela de consulta

    A coluna status serve para indicar o status da consulta:
      - Agendado: consulta marcada, mas ainda não ocorreu.
      - Cancelado: paciente ou clínica cancelou
      - Realizado: consulta já ocorreu
      - Faltou: paciente não compareceu e não avisou com antecedência

    Existem duas colunas com chave estrangeira (ForeignKey): paciente e 
    dentista. 
    O relacionamento é 1 para muitos:
      - Paciente (1) --- (N) consulta : Um paciente pode ter vários consultas, mas cada consulta pertence a um único paciente.
      - Dentista (1) --- (N) consulta : Um dentista pode ter vários consultas, mas cada consulta pertence a um único dentista.  

    Essa classe tem mais funções que as outras, seu fluxo é o seguinte:
    Salvar consulta (Instanciar a classe Consulta)
        ↓
    Executar clean()
        ↓
    Se houver conflito → erro
        ↓
    Se não houver → salva no banco (função save())
    """ 
    STATUS = [
        ('Agendada','Agendada'),
        ('Realizada', 'Realizada'),
        ('Cancelada', 'Cancelada'),
        ('Faltou', 'Faltou')
    ]
    procedimento = models.ForeignKey('Procedimento', on_delete=models.SET_NULL, null=True,blank=True) # SET_NULL: se o procedimento for excluído da tabela procedimento, será substituido com NULL aqui.
                                                                                           # null = True: permite que o campo seja nulo  
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    status = models.CharField(max_length=20, choices = STATUS,default='Agendada') # O campo "status" é usado para indicar o status da consulta, como "Agendada", "Realizada", "Cancelada", etc. O valor padrão é "Agendada".
    dentista = models.ForeignKey(Dentista, on_delete=models.CASCADE) # O campo "dentista" é uma chave estrangeira que referencia a tabela "Dentista". O "on_delete=models.CASCADE" indica que, se um dentista for excluído, todos as consultas relacionados a ele também serão excluídos.
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE) # O campo "paciente" é uma chave estrangeira que referencia a tabela "Paciente". O "on_delete=models.CASCADE" indica que, se um paciente for excluído, todos as consultas relacionados a ele também serão excluídos.
   
    def clean(self):
        """ Método para validar se o dentista tem outra consulta no mesmo horário.
        OBS: 
        - clean() é um método especial usado no Django para validação personalizada. 
        - Ele pertence ao ciclo de validação executado pelo método full_clean().

        Essa função é semelhante a este código sql:
        SELECT *
        FROM consulta
        WHERE dentista = X
        AND data = Y
        AND horario_inicio < novo_fim
        AND horario_fim > novo_inicio
        """
        conflitos = self.__class__.objects.filter(
            dentista=self.dentista,
            data=self.data
        ).filter(
            horario_inicio__lt=self.horario_fim,
            horario_fim__gt=self.horario_inicio
        )

        if self.pk:
            conflitos = conflitos.exclude(pk=self.pk)

        if conflitos.exists():
            raise ValidationError(
                "Este dentista já possui consulta neste horário."
            )
    # Função que faz o Django executar a validação do horário antes de salvar a consulta. 
    # O método "full_clean" é um método do Django que executa todas as validações definidas no modelo, incluindo a validação personalizada que criamos no método "clean". 
    # Se a validação falhar, ele levantará uma exceção de ValidationError, impedindo que a consulta seja salva com um horário conflitante.    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
   
    def __str__(self):
        return f"Consulta de {self.paciente.nome} com {self.dentista.nome} em {self.data} às {self.horario_inicio} - Status: {self.get_status_display()}" 
    
# OBS: Na classe abaixo é utilizado uma variável constante que está toda em maiúscula (DIAS_SEMANA). Ela é usada para especificar as opções de dias da semana que os médicos vão trabalhar.
#      Esta variável é usada em "choices", na coluna dia_semana. 
#      Isso é importante para garantir que os dados armazenados sejam consistentes, evitando coisas como: domingo e Domingo.
#      
#     O link a seguir explica como fazer isso: https://docs.djangoproject.com/en/6.0/ref/models/fields/#choices
#     Este outro link também abordao assunto: https://www.treinaweb.com.br/blog/utilizando-choices-no-django-orm
#
#     Sintaxe da variável:
#     NOME_VARIAVEL = [
#         ('valor_armazenado1', 'Valor Exibido1'),
#         ('valor_armazenado2', 'Valor Exibido2'),
#         ]

class AgendaTrabalho(models.Model):
    """ Tabela com agenda de trabalho dos dentistas
        É importante fazê-la, pois um dentista pode trabalhar em mais de um consultório. 
    """
    DIAS_SEMANA = [
        ('SEG', 'Segunda-Feira'),
        ('TER', 'Terça-Feira'),
        ('QUA', 'Quarta-Feira'),
        ('QUI', 'Quinta-Feira'),
        ('SEX', 'Sexta-Feira'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo')     
          ]
    dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA) # Exemplo: Segunda-feira, Terça-feira, etc.
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    dentista = models.ForeignKey(Dentista, on_delete=models.CASCADE)

    def __str__(self):
        return f"Agenda de {self.dentista.nome}: {self.get_dia_semana_display()} das {self.horario_inicio} às {self.horario_fim}"
    
class Procedimento(models.Model):
    """ Tabela com o tempo estimada para realizar cada procedimento. 
        Isso é importante para evitar grandes filas de espera.
    """
    procedimento = models.CharField(max_length=500)
    tempo_estimado = models.DurationField()

    def __str__(self):
        return self.procedimento
