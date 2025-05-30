import random
import faker
from typing import Dict, Any
from .base_agent import BaseAgent
from ..exceptions.simulation_exceptions import DataGenerationError

fake = faker.Faker('pt_BR')

class DataGeneratorAgent(BaseAgent):
    async def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Geração de dados aleatórios realistas
            nome = fake.name()
            email = fake.email()
            # Gera DDD realista e número no padrão brasileiro (11 dígitos)
            ddd = fake.random_element(elements=("11","21","31","41","51","61","71","81","91"))
            numero = fake.numerify(text="9########")
            telefone = f"{ddd}{numero}"
            cep = fake.postcode().replace('-', '').zfill(8)

            context['form_data'] = {
                'nome': nome,
                'email': email,
                'telefone': telefone,
                'cep': cep
            }
            return await self._handle_next(context)
        except Exception as e:
            raise DataGenerationError(f"Erro ao gerar dados aleatórios: {e}") 