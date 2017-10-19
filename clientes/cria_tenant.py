#   TODO 0: python manage.py shell
#   TODO 1: import django
#   TODO 2: django.setup()

# TODO 3. Importar o modelo que vai ser criado
from clientes.models import Cliente

# TODO 4. Criar o tenant public
tenant = Cliente(
                # don't add your port or www here! on a local server you'll want to use localhost here
                domain_url='usesoft-saas.com',
                schema_name='public',
                nome='Usesoft do Brasil',
                pago_ate='3000-12-31',
                em_teste=False).save()

# TODO 4.1: >>> from django.contrib.sites.models import Site
# TODO 4.2: >>> Site.objects.create(name='usesoft-saas.com', domain='usesoft-saas.com.com')

# TODO 5. Criar o tenant sem ser public
tenant1 = Cliente(domain_url='comercialtoes-saas.com',
                  schema_name='comercial_toes',
                  nome='Comercial Toes',
                  pago_ate='2018-12-31',
                  em_teste=False).save()

# TODO 5.1: >>> from django.contrib.sites.models import Site
# TODO 5.2: >>> Site.objects.create(name='comercialtoes-saas.com', domain='comercialtoes-saas.com')


# TODO 6. Criar o outro tenant ser public
tenant2 = Cliente(domain_url='oleobahia-saas.com',
                  schema_name='oleo_bahia',
                  nome='Óleo Bahia',
                  pago_ate='2018-12-31',
                  em_teste=False).save()

# TODO 6.1: >>> from django.contrib.sites.models import Site
# TODO 6.2: >>> Site.objects.create(name='oleobahia-saas.com', domain='oleobahia-saas.com')
