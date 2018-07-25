import threading
from threading import Thread
from blockchain import Block, Transaction, get_genisis
from crypto import sign
from wallet import load_blockchain, generate_keys
from constants import WALLET_FILE, TXN_FILE, REWARD
from utils import gen_uuid, get_route
from pyfiglet import Figlet

import datetime
import json
import os
import shutil
import jsonpickle

public = None
private = None
blockchain = None
hash_found = False

def print_header():
    """Why not.
    """
    f = Figlet(font='big')
    print f.renderText('HackMiner')
    print "Version 0.2.1"

def try_mine(block):
    """Updates the nonce and sees if it's valid.
    """
    block.nonce += 1
    return block.is_valid()

def mine_till_found(block):
    """Keep guessing and checking the nonce in hopes
    we mine the provided block.
    """
    print "\n\n" + ("-" * 40)
    print "Mining now with %i transactions." % len(block.transactions)
    hashes_done = 0

    start = datetime.datetime.now()
    threads = []
    def mine(block, start, hashes_done):
        while not try_mine(block):
            hashes_done += 1
            if hashes_done % 100000 == 0:
                print(hashes_done)
                new_chain = load_blockchain()
                # print("server hasn't fucked us yet")
                if new_chain.head.hash_block() != blockchain.head.hash_block():
                    print("aborting early")
                    return True
            if hashes_done % 300000 == 0:
                end = datetime.datetime.now()
                seconds = (end - start).total_seconds()

                print "Hash Rate: %i hashes/second      \r" % (300000 / seconds),

                start = end
    # threads = [Thread(target=mine(block, start, hashes_done)) for i in range(3)]
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    mine(block, start, hashes_done)
    # threads = [Thread(target=mine(block, start, hashes_done)) for i in range(4)]
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    print "\nMined block:", block.hash_block(), "with nonce", block.nonce

    return True

def load_wallet():
    """Load the wallet.json file and load the
    keys from there.
    """

    global public
    global private

    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, 'r') as f:
            wallet_json = f.read()
        wallet_obj = json.loads(wallet_json)

        public = wallet_obj['public']
        private = wallet_obj['private']
    else:
        print "First run the wallet.py file!"
        exit()

def load_transactions():
    """If there were any transactions queued by wallet.py
    we load these into a list here.
    """
    if os.path.exists(TXN_FILE):
        with open(TXN_FILE, 'r') as f:
            txn_json = f.read()
        txn_obj = jsonpickle.decode(txn_json)
        return txn_obj

    return []

def delete_queue(txns):
    """Remove transactions from txn_queue.json
    that we have already processed.
    """

    # These ids have already been processed.
    ids = set([t.id for t in txns])

    # Go through the transaction file.
    if os.path.exists(TXN_FILE):
        with open(TXN_FILE, 'r') as f:
            txn_json = f.read()

        # Read current transactions.
        txn_obj = jsonpickle.decode(txn_json)

        # Go through and delete onces we
        # haven't processed.
        new_txns = []
        for t in txn_obj:
            if t.id not in ids:
                new_txns.append(t)

        # Dump.
        with open(TXN_FILE, 'w') as f:
            f.write(jsonpickle.encode(new_txns))


def run_sample():
    """Testing code.
    """
    # Mine a sample block.
    b = Block(
        timestamp = datetime.datetime.now(),
        transactions = [],
        previous_hash = get_genisis().hash_block()
    )

    mine_till_found(b)

def run_miner():
    """Run the main miner loop.
    """
    my_address = "2cb4fc5902917e58e531cfbe1d909727aaf331b4856bf8627e09bf8941b69a40"
    my_private = "610af1630bf08b0072d97bdaf71882cd0a2c86e7af72296b4ee73f508b812c28"
    my_address_2 = "a173fd8d2330cc2b4776730891f50099204376217c67b7b23254aca04fbeb5a3"
    my_private_2 = "d0f783f01ac0df1799856964fe74f702763932e1edf3e9d0074646de885d5559"
    public = my_address_2
    private = my_private_2
    donor = None
    while True:
        print("new public", public)
        print("new private", private)
        global blockchain
        global real_b1
        global fake_b1
        global fake_b2
        blockchain = load_blockchain()

        # Add reward to us yay.

        # my_address_3 =  "5adbd7137903135fa2cc5a2de2035a326319e42188a9c6714b26fa016c6ac1bb"
        # my_private_3 = "91f233e1218135b772ddc87a199e6d3cc18233753623f95385dde62e886304c7"

        amount_1 = blockchain.get_wallet_amount(my_address)
        amount_2 = blockchain.get_wallet_amount(my_address_2)
        # amount_3 = blockchain.get_wallet_amount(my_address_3)
        if amount_1 < 0:
            my_private, my_address = generate_keys()
            public = my_address
            private = my_private
            donor_pub = my_address_2
            donor_private = my_private_2
            donor_amount = amount_2
        else:
            my_private_2, my_address_2 = generate_keys()
            public = my_address_2
            private = my_private_2
            donor_pub = my_address
            donor_private = my_private
            donor_amount = amount_1

        # Add reward to us yay.
        reward = Transaction(
            id = gen_uuid(),
            owner = "mined",
            receiver = public,
            coins = REWARD,
            signature = None
        )
        txns = []
        reward.signature = sign(reward.comp(), private)
        txns.append(reward)

        donation1 = Transaction(
            id = gen_uuid(),
            owner = donor_pub,
            receiver = "3119281c76dc54009925c9208bedc5bd0162c27034a1649fd7e2e5df62dba557",
            coins = donor_amount,
            signature = None
        )
        donation1.signature = sign(donation1.comp(), donor_private)
        donation2 = Transaction(
            id = gen_uuid(),
            owner = donor_pub,
            receiver = public,
            coins = donor_amount,
            signature = None
        )
        donation2.signature = sign(donation2.comp(), donor_private)
        txns.append(donation1)
        txns.append(donation2)
        # Construct a new block.
        real_b1 = Block(
            timestamp = datetime.datetime.now(),
            transactions = txns,
            previous_hash = blockchain.head.hash_block()
        )

        mine_till_found(real_b1)

        new_chain = load_blockchain()
        # print "Adding real block now"
        # resp1 = get_route('add', data=str(real_b1))
        # if resp1['success']:
        #     print "Added real block1!"
        # else:
        #     print "Couldn't add block:", resp1['message']
        if new_chain.head.hash_block() == blockchain.head.hash_block():
            print "Adding real block now"
            resp1 = get_route('add', data=str(real_b1))
            if resp1['success']:
                print "Added real block1!"
            else:
                print "Couldn't add block:", resp1['message']
        else:
            print "Someone else mined the block before us :("
        # print("\nREAL DONE")
        # Let's mine this block.
        # Is this _the_ new block?
        # or did the server swoop us :(
if __name__ == '__main__':
    print_header()
    load_wallet()
    run_miner()
