import json
from tkinter.ttk import Frame, Label, Treeview


class OrderBook(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=12, **kwargs)
        self.configure(borderwidth=1, relief="solid")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        Label(self, text="Bids", anchor="center").grid(row=0, column=0, sticky="ew")
        Label(self, text="Asks", anchor="center").grid(row=0, column=1, sticky="ew")

        self.bids_tree = Treeview(self, columns=("price", "qty"), show="headings", height=10)
        self.bids_tree.heading("price", text="Price")
        self.bids_tree.heading("qty", text="Qty")
        self.bids_tree.grid(row=1, column=0, sticky="nsew", padx=(0, 8))

        self.asks_tree = Treeview(self, columns=("price", "qty"), show="headings", height=10)
        self.asks_tree.heading("price", text="Price")
        self.asks_tree.heading("qty", text="Qty")
        self.asks_tree.grid(row=1, column=1, sticky="nsew", padx=(8, 0))

        self._depth_event = None

    def bind_crypto(self, crypto):
        depth_event = crypto.ws_depth.message_received

        if self._depth_event is depth_event:
            return

        if self._depth_event:
            self._depth_event -= self._handle_depth

        self._depth_event = depth_event
        self._depth_event += self._handle_depth

    def _handle_depth(self, message):
        data = json.loads(message)
        bids = data.get("b") or data.get("bids") or []
        asks = data.get("a") or data.get("asks") or []
        self.after(0, lambda: self._update_views(bids[:10], asks[:10]))

    def _update_views(self, bids, asks):
        self._populate_tree(self.bids_tree, bids)
        self._populate_tree(self.asks_tree, asks)

    @staticmethod
    def _populate_tree(tree, rows):
        tree.delete(*tree.get_children())
        for price, qty in rows:
            tree.insert("", "end", values=(price, qty))
