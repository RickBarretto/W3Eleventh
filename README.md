# W3Eleventh
W3 Eleventh is a continuation of the turn-based card game Eleventh, using Blockchain as data storage. This Project was intended for the TEC502 Concurrency &amp; Connectivity's 3rd Problem Based Learning.

## TODO

Since the trade is getting too much complex due to the way vyper and
the EVM works, limiting the capability of the language with better data structures,
I decided to replace trading via Auction to Sellings in the market place using coins.

So, you earn coins, you can buy cards with them.
You can also publish your card on market place, and people can buy it.

This will basically be a DynArray. Very simple, if someone has the money,
automatically approved. No need to 2-phase-commit.