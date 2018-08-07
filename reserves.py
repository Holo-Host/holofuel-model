"""
Proof-of-concept reserve accounts code

This code comprises of a reserve class and a script to test FX rate arbitrage if exchange rates change. It will need to get integrated into the PoC network
to test the money supply function
"""
from collections import deque

class ReserveAccount:
    """
    The reserves_account class generates a reserves_account object for a specified currency pair
    Reserves accounts are initialised with an order book that starts at ICO price unless otherwise specified, and a reserve balance of 0

    Reserve accounts have 4 function calls:
    - quote: returns the current marginal price and the order book volume at that price
    - issue: adds reserves to the reserve balance and subtracts corresponding orderbook volume
    - retire: subtracts reserves from the reserve balance and adds corresponding orderbook volume
    - update_supply: changes the supply factor variable that determines the order book volume available at each price band
    """

    def __init__(self, currency_pair, supply_factor=1.0, start_price=0.0001, reserve_balance=0.0):
        """
        :currency_pair  : the currency pair that Holo Fuel is traded against at this account
        :supply_factor  : Each price tranch of the order book has a volume of supply_factor * 1,000,000 Fuel
        :start_price    : the starting lowest price offered by the reserve order book denominated in {currency_pair}
        :reserve_balance: sets the amount of {currency_pair} held in the reserve at start
        """

        self.supply_factor = supply_factor

        self.order_book = deque() # Create orderbook as double-ended queue and append tranches
        for ii in range(5):
            issue_price = start_price * (1 + ii/100 # Reserve tranches need increment in % of price, otherwise at higher prices you get ludicrous volumes available before meaningful price change
            order_book_tranch = [issue_price, self.supply_factor * 1000000]
            self.order_book.append(order_book_tranch)

        self.reserves = deque() # Create reserve as double-ended queue and append tranches
        retire_price = start_price
        reserve_tranch = [retire_price, self.supply_factor * 1000000]
        self.reserves.append(retire_price)

    def quote(self, order_type):
        """
        :order_type: 'buy' to buy fuel from reserve (issue) or 'sell' to sell and retire fuel at reserve
        """
        if order_type == 'buy':
            tranch = self.order_book[0]

        elif order_type == 'sell':
            tranch = self.reserves[-1]

        else:
            print('No order type specified. Please specify "buy" or "sell"')
            return

        price = tranch[0]
        volume = tranch[1]

        return price, volume

    def issue(self, volume):
        """
        :volume: Volume of Fuel to be issued
        """










reserve_t               = collections.namedtuple(
    'Reserve', [
        'rate',     # Exchange rate used for these funds
        'amount',   # The total value of the amount executed at .rate
     ] )            #   and the resultant credit in Holo Fuel == amount * rate

reserve                 = {
    'EUR':          [],     # LIFO stack of reserves available
    'USD':          [ reserve_t( .0004, 200 ), reserve_t( .0005, 250 ) ], # 1,000,000 Holo Fuel
    'HOT ERC20':    [ reserve_t( 1, 1000000 ) ], # 1,000,000 Holo Fuel
}

def reserves( reserve ):
    return [ [ "Currency", "Rate avg.", "Reserves", "Holo Fuel Credits", ], None, ] \
           + [ [ c, "%8.6f" % ( sum( r.amount * r.rate for r in reserve[c] )
                               / ( sum( r.amount for r in reserve[c] ) or 1 ) ),
                 "%8.2f" % sum( r.amount for r in reserve[c] ),
                 "%8.2f" % sum( r.amount / r.rate for r in reserve[c] ) ]
               for c in reserve ] \
           + [ None,
               [ '', '', '', sum( sum( r.amount / r.rate for r in reserve[c] ) for c in reserve ) ]]

summary                 = reserves( reserve )
summary # summary[-1][-1] is the total amount of reserves credit available, in Holo Fuel
