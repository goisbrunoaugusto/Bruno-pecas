import csv
import io
from celery import shared_task
from django.core.exceptions import ValidationError
from .models import Part

@shared_task
def import_parts_from_csv(csv_file):
    """
    Tarefa Celery para importar peças de um arquivo CSV.
    """
    try:
        csv_file = io.StringIO(csv_file)
        reader = csv.DictReader(csv_file)

        for row in reader:
            try:
                Part.objects.update_or_create(
                    part_number=row['part_number'],
                    defaults={
                        'name': row['name'],
                        'details': row['details'],
                        'price': float(row['price']),
                        'quantity': int(row['quantity']),
                    }
                )
            except (ValueError, KeyError) as e:
                print(f"Erro ao processar linha: {row}. Erro: {e}")
                continue

        return "Importação concluída com sucesso!"
    except Exception as e:
        print(f"Erro durante a importação: {e}")
        raise e