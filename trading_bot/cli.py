import argparse
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import logging
from trading_bot.basic_bot import BasicBot

console = Console()

def pretty_print_order(order):
    if not order:
        console.print("[red]Order failed![/red]")
        return
    if isinstance(order, dict) and "orderId" in order:
        table = Table(title="Order Details")
        for k, v in order.items():
            table.add_row(str(k), str(v))
        console.print(table)
    elif isinstance(order, dict):
        console.print(order)

def print_table(title, data: list[dict]):
    """Helper to print list of dicts as a Rich table"""
    if not data:
        console.print(f"[bold yellow]No {title} found.[/bold yellow]")
        return
    
    table = Table(title=title, show_lines=True)
    for key in data[0].keys():
        table.add_column(key, style="cyan")
    for row in data:
        table.add_row(*[str(v) for v in row.values()])
    console.print(table)

def interactive_cli():
    bot = BasicBot()
    console.print("\n[bold cyan]=== Interactive Trading Bot ===[/bold cyan]")
    console.print("1. Market Order\n2. Limit Order\n3. Stop-Market Order\n4. OCO Order")
    choice = Prompt.ask("Choose order type", choices=["1", "2", "3", "4"])
    symbol = Prompt.ask("Enter symbol (default=BTCUSDT)", default="BTCUSDT")
    side = Prompt.ask("Side", choices=["BUY", "SELL"])
    qty = float(Prompt.ask("Quantity", default="0.001"))
    if choice == "1":
        order = bot.place_order(symbol, side, "MARKET", qty)
    elif choice == "2":
        price = float(Prompt.ask("Price"))
        order = bot.place_order(symbol, side, "LIMIT", qty, price=price)
    elif choice == "3":
        stop = float(Prompt.ask("Stop Price"))
        order = bot.place_order(symbol, side, "STOP_MARKET", qty, stop_price=stop)
    elif choice == "4":
        ticker = bot.client.ticker_price(symbol=symbol)
        current_price = float(ticker["price"])
        console.print(f"[yellow]Current {symbol} price: {current_price}[/yellow]")
        buffer = current_price * 0.02
        if side.upper() == "BUY":
            tp_default = round(current_price + buffer, 1)
            sl_default = round(current_price - buffer, 1)
        else:
            tp_default = round(current_price - buffer, 1)
            sl_default = round(current_price + buffer, 1)

        tp = float(Prompt.ask("Take-Profit Price", default=str(tp_default)))
        sl = float(Prompt.ask("Stop-Loss Price", default=str(sl_default)))
        order = bot.place_order(symbol, side, "OCO", qty, price=tp, stop_price=sl)

    pretty_print_order(order)

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Bot CLI")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive mode")
    args, unknown = parser.parse_known_args()
    if args.interactive:
        interactive_cli()
    else:
        console.print("[red]Use --interactive for menu mode[/red]")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()