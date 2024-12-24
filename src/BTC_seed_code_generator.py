import os 
import requests
from bip_utils import (
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip39WordsNum,
    Bip39MnemonicGenerator,
    Bip44Changes,
)
import time



# Step 1: Generate a BIP-39 seed phrase
def generate_seed_phrase():
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
    return mnemonic


# Step 2: Derive a Bitcoin address from the seed phrase
def get_bitcoin_address(seed_phrase):
    # Generate the seed from the mnemonic
    seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()

    # Create a Bip44 wallet for Bitcoin
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)

    # Derive the first receiving address (account 0, external chain, address index 0)
    bip44_acc = (
        bip44_mst.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )

    # Get the address
    address = bip44_acc.PublicKey().ToAddress()
    return address


# Step 3: Match address to list from file
file_name = '/home/home/Desktop/BTC/BTC Lists/BTCtestlist.txt'
matching_lines = []

with open(file_name, 'r') as file:
    # Read each line in the file
    lines = file.readlines()

# Compare each line to the Python output
for line in lines:
    if line.strip() == address:  # Strip to remove any extra spaces/newlines
        matching_lines.append(line.strip())


# Step 4: Save the seed phrase and address if match is found
def save_seed_phrase(seed_phrase, address):
    folder_path = "Wallet_Phrases1"

