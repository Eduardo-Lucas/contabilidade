# 3
from clientes.models import Cliente

# 1
import django

#2
django.setup()

# create your public tenant

tenant = Cliente(
                # don't add your port or www here! on a local server you'll want to use localhost here
                domain_url='usesoft-saas.com',
                schema_name='public',
                nome='Usesoft do Brasil',
                pago_ate='3000-12-31',
                em_teste=False).save()

# create your first real tenant
tenant1 = Cliente(domain_url='comercialtoes-saas.com',
                  schema_name='comercial_toes',
                  nome='Comercial Toes',
                  pago_ate='2018-12-31',
                  em_teste=False).save()

# create your SECOND real tenant
tenant2 = Cliente(domain_url='oleobahia-saas.com',
                  schema_name='oleo_bahia',
                  nome='Óleo Bahia',
                  pago_ate='2018-12-31',
                  em_teste=False).save()
