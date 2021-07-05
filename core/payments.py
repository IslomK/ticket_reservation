from collections import namedtuple


class CardError(Exception):
   pass


class PaymentError(Exception):
   pass


class CurrencyError(Exception):
   pass


PaymentResult = namedtuple('PaymentResult', ('amount', 'currency'))


class PaymentGateway:
   supported_currencies = ('EUR',)

   def charge(self, amount, token, currency='EUR'):
       if token == 'card_error':
           raise CardError("Your card has been declined")
       elif token == 'payment_error':
           raise PaymentError("Something went wrong with your transaction")
       elif currency not in self.supported_currencies:
           raise CurrencyError(f"Currency {currency} not supported")
       else:
           return PaymentResult(amount, currency)


payment_service = PaymentGateway()
