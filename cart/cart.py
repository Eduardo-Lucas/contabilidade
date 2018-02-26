from decimal import Decimal

from django.conf import settings

from ctb.models import Conta


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # def __len__(self):
    #     """
    #     Count all items in the cart.
    #     """
    #     return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        conta_ids = self.cart.keys()
        # get the conta objects and add them to the cart
        contas = Conta.objects.filter(id__in=conta_ids)
        for conta in contas:
            self.cart[str(conta.id)]['conta'] = conta

        for item in self.cart.values():
            item['conta'] = item['conta']
            item['valor'] = item['valor']
            item['d_c'] = item['d_c']
            item['codigo_historico'] = item['codigo_historico']
            item['historico'] = item['historico']
            yield item

    def add(self, conta, valor, d_c, codigo_historico, historico):
        """
        Adiciona um lancamento no cart ou atualiza seu valor.
        """
        conta_id = str(conta.id)
        if conta_id not in self.cart:
            self.cart[conta_id] = {'valor': str(valor),
                                   'd_c': d_c,
                                   'codigo_historico': str(codigo_historico),
                                   'historico': historico}
        self.save()

    def remove(self, conta):
        """
        Remove a product from the cart.
        """
        conta_id = str(conta.id)
        if conta_id in self.cart:
            del self.cart[conta_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_debito(self):
        return sum(Decimal(item['valor']) for item in self.cart.values() if item['d_c'] == 'D')

    def get_total_credito(self):
        return sum(Decimal(item['valor']) for item in self.cart.values() if item['d_c'] == 'C')

    def get_diferenca(self):
        return self.get_total_debito() - self.get_total_credito()
