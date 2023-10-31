# Distributed Systems Assignment

Worth 30% of overall grade!

# Buyer-Seller System

This system simulates an electronic food marketplace with buyers and sellers. It allows multiple buyers to connect to a seller and perform various actions which are: 
- buying items,
- listing available items
- joining the marketplace
- leaving the marketplace
- quiting (can't join the market again, socket gets disconnected!)
- Displaying a help menu

The system uses multicast to notify connected nodes (buyers) about successful purchases.

## Prerequisites

- This program was made using Python 3.10.0. I can't confirm this will work correctly with other versions but it most likely would.
- Windows OS (This README assumes Windows; slight modifications may be needed for other platforms)
- This program uses no external libraries, only ones part of Python's standard library.

## Configurations Setup

Modify the config.ini file to configure the system. You can specify the host, port, and IDs for both sellers and buyers.

For the demo, the `config.ini` file would look like this:

```ini
[Server]
host = localhost
port = 5000

[Buyers]
buyer1 = 1
buyer2 = 2
buyer3 = 3
buyer4 = 4
```

## Running the System

Run the `main.py` in the project root director(same directory where this README is located)
```bash
python src/main.py
```

After running the `main.py`, separate console windows will appear for both the seller and each individual buyer. You can engage with each buyer individually using the CLI specific to that buyer.

It is recommended to use a console that supports ANSI colour codes for text styling.

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