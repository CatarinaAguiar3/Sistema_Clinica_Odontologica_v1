# 1 ª versão da classe `Consulta`
No arquivo: `clinica\models.py`
```python
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
    """ 
    STATUS = [
        ('Agendada','Agendada'),
        ('Realizada', 'Realizada'),
        ('Cancelada', 'Cancelada'),
        ('Faltou', 'Faltou')
    ]
    procedimento = models.ForeignKey('Procedimento', on_delete=models.SET_NULL, null=True) # SET_NULL: se o procedimento for excluído da tabela procedimento, será substituido com NULL aqui.
                                                                                           # null = True: permite que o campo seja nulo  
    data = models.DateField()
    horario_inicio = models.TimeField()
    #horario_fim = models.TimeField()
    status = models.CharField(max_length=20, choices = STATUS,default='Agendada') # O campo "status" é usado para indicar o status da consulta, como "Agendada", "Realizada", "Cancelada", etc. O valor padrão é "Agendada".
    dentista = models.ForeignKey(Dentista, on_delete=models.CASCADE) # O campo "dentista" é uma chave estrangeira que referencia a tabela "Dentista". O "on_delete=models.CASCADE" indica que, se um dentista for excluído, todos as consultas relacionados a ele também serão excluídos.
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE) # O campo "paciente" é uma chave estrangeira que referencia a tabela "Paciente". O "on_delete=models.CASCADE" indica que, se um paciente for excluído, todos as consultas relacionados a ele também serão excluídos.
   
    class Meta:
        """ 
        Esta é uma classe interna do django usada para configurar opções adicionais, como restrições.
        Neste caso, o objetivo é garantir que um dentista não possa ter dois consultas no mesmo horário.
            
        A restrição UniqueConstraint garante que um mesmo dentista não possa ter dois consultas na mesma data e horário.
        """    
        constraints = [
            models.UniqueConstraint(fields = ['dentista', 'data', 'horario_inicio'], name='unique_dentista_data_horario')
        ]

    def __str__(self):
        return f"Consulta de {self.paciente.nome} com {self.dentista.nome} em {self.data} às {self.horario_inicio} - Status: {self.get_status_display()}" 
    

```