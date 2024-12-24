import os
import requests  # Not used in this script but kept in case of future expansion
from bip_utils import (
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip39WordsNum,
    Bip39MnemonicGenerator,
    Bip44Changes,
)
import time

# -----------------------------------------------------------------------------------
# Script Purpose:
# 1. Generate a secure BIP-39 mnemonic (seed phrase).
# 2. Derive a Bitcoin address from the seed phrase using the BIP-44 standard.
# 3. Match the derived Bitcoin address against a list of addresses stored in a file.
# 4. Save the seed phrase and address if a match is found.
# -----------------------------------------------------------------------------------

# Step 1: Generate a BIP-39 seed phrase
def generate_seed_phrase():
    """
    Generates a 12-word BIP-39 mnemonic (seed phrase) for cryptocurrency wallets.

    Returns:
        str: The generated mnemonic.
    """
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
    return mnemonic


# Step 2: Derive a Bitcoin address from the seed phrase
def get_bitcoin_address(seed_phrase):
    """
    Derives a Bitcoin address from the given seed phrase using the BIP-44 standard.

    Args:
        seed_phrase (str): The 12-word mnemonic.

    Returns:
        str: The generated Bitcoin address.
    """
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


# Step 3: Match address to a list from a file
def match_address_to_file(address, file_name):
    """
    Matches a given Bitcoin address to a list of addresses in a file.

    Args:
        address (str): The Bitcoin address to search for.
        file_name (str): The file containing a list of Bitcoin addresses.

    Returns:
        list: List of matching addresses found in the file.
    """
    matching_lines = []
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Compare each line to the generated address
        for line in lines:
            if line.strip() == address:  # Strip removes extra spaces/newlines
                matching_lines.append(line.strip())
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return matching_lines


# Step 4: Save the seed phrase and address if a match is found
def save_seed_phrase(seed_phrase, address, folder_path="Wallet_Phrases1"):
    """
    Saves the seed phrase and corresponding Bitcoin address to a file.

    Args:
        seed_phrase (str): The BIP-39 mnemonic.
        address (str): The Bitcoin address.
        folder_path (str): The folder where the results will be saved.
    """
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "matched_phrases.txt")

    try:
        with open(file_path, "a") as file:
            file.write(f"Seed Phrase: {seed_phrase}\nAddress: {address}\n\n")
        print(f"Results saved to {file_path}")
    except Exception as e:
        print(f"Failed to save results: {e}")


# Main Function
def main():
    """
    Main execution function to tie all steps together.
    """
    print("Generating a new seed phrase...")
    seed_phrase = generate_seed_phrase()
    print(f"Seed Phrase: {seed_phrase}")

    print("Deriving Bitcoin address...")
    address = get_bitcoin_address(seed_phrase)
    print(f"Bitcoin Address: {address}")

    file_name = input("Enter the path to the file containing Bitcoin addresses: ")

    print("Checking for matches...")
    matches = match_address_to_file(address, file_name)

    if matches:
        print(f"Match found! Address: {address}")
        save_seed_phrase(seed_phrase, address)
    else:
        print("No matches found.")

# Run the script
if __name__ == "__main__":