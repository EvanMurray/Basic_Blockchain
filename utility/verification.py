from utility.hash_util import hash_string_256, hash_block
from wallet import Wallet


class Verification:

    @staticmethod
    def valid_proof(open_tx, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in open_tx]) +
                 str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:2] == '00'

    # verifies the chain by comparing hashes between 2 adjacent blocks

    @classmethod
    def verify_chain(cls, bc):
        for (index, block) in enumerate(bc):
            if index == 0:
                continue
            if block.previous_hash != hash_block(bc[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid!")
                return False
        return True

    # verifies the transaction by ensuring that the sender has funds

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):

        if check_funds:
            sender_balance = get_balance(transaction.sender)
            return (sender_balance >= transaction.amount and
                    Wallet.verify_transaction(transaction))
        else:
            return Wallet.verify_transaction(transaction)

    # verifies all open open_transactions
    @classmethod
    def verify_transactions(cls, open_tx, get_balance):
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_tx])
