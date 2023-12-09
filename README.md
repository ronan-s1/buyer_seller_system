# Buyer-Seller System (Distributed Systems Assignment)

This system simulates an electronic food marketplace with buyers and sellers. It allows multiple buyers to connect to sellers and perform various actions which are: 
- buying items
- listing items and their stock
- joining a seller's stall
- leaving a seller's stall
- quiting (can't join the market again, socket gets disconnected!)
- Displaying a help menu

## Prerequisites

- This program was made using Python 3.10.0. I can't confirm this will work correctly with other versions but it most likely would.
- Windows OS (This README assumes Windows; slight modifications may be needed for other platforms)
- This program uses no external libraries, only ones part of Python's standard library.

## Configurations Setup

Modify the `config.ini` file to configure the system. You can specify the seller and buyer IDs and also the seller host and starting port (port increment by 1 each new seller in the market).

For the demo, the `config.ini` file would look like this:

```ini
[Server]
host = localhost
port = 5000

[Sellers]
seller1 = 1
; seller2 = 2

[Buyers]
buyer1 = 1
buyer2 = 2
buyer3 = 3
buyer4 = 4
```

## Running the System

Run the `main.py` in the project root directory (same directory where this README is located)
```bash
python src/main.py
```

After running the `main.py`, separate console windows will appear for both the sellers and buyers. You can engage with each buyer individually using the CLI specific to that buyer.

It is recommended to use a console that supports ANSI colour codes for text styling.

## Possible Issues

Be aware that the main.py file is for launching the client and server instances. It assumes that "python" is the keyword for executing Python scripts on your machine; however, if your system employs "py" or "python3" etc. you may need to modify `main.py` accordingly.

If there’s issues with using main.py for launching the instances, then you can run the them
manually in separate terminals:

```bash
python src/server.py localhost 5001 seller1 1
python src/client.py localhost "{\"seller1\": [\"1\", 5001]}" 1
python src/client.py localhost "{\"seller1\": [\"1\", 5001]}" 2
python src/client.py localhost "{\"seller1\": [\"1\", 5001]}" 3
```

## Code Directory Structure
```zsh
.
├── README.md
├── config.ini
└── src
    ├── client.py
    ├── colours.py
    ├── config.py
    ├── main.py
    └── server.py
```
