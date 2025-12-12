import json
from tkinter.ttk import Frame, Label, Treeview


class RecentTrade(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=8, **kwargs)
        self.configure(borderwidth=2, relief="solid")
        self.columnconfigure(0, weight=1)

        Label(self, text="Trades", font="Arial 16 bold", anchor="center").grid(row=0, column=0, sticky="ew")

        self.trade_tree = Treeview(self, columns=("price", "qty"), show="headings", height=10)
        self.trade_tree.heading("price", text="Price")
        self.trade_tree.heading("qty", text="Qty")
        self.trade_tree.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        self.trade_tree.tag_configure(tagname="bids", foreground="green")
        self.trade_tree.tag_configure(tagname="asks", foreground="red")

        self._depth_event = None

    def bind_crypto(self, crypto):
        if len(self.trade_tree.get_children()) > 0:
            self.trade_tree.delete(*self.trade_tree.get_children())

        trade_event = crypto.ws_aggregate_trade.message_received

        if self._depth_event is trade_event:
            return

        if self._depth_event:
            self._depth_event -= self._handle_trade

        self._depth_event = trade_event
        self._depth_event += self._handle_trade

    def _handle_trade(self, message):
        data = json.loads(message)
        price = data["p"]
        quantity = data["q"]
        maker = data["m"]
        self.after(0, lambda: self._update_views(price, quantity, maker))

    def _update_views(self, price, qty, maker):
        self._populate_tree(self.trade_tree, price, qty, "bids" if not maker else "asks")

    @staticmethod
    def _populate_tree(tree, price, qty, tag):
        if len(tree.get_children()) > 10:
            tree.delete(tree.get_children()[0])

        tree.insert("", "end", values=(price, qty), tag=(tag,))