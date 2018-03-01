from uuid import uuid4

from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.request import Request

from blockchain.objects.blockchain import Blockchain

app = Sanic(__name__)

blockchain = Blockchain()
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


@app.route('/')
async def hello(request: Request) -> HTTPMethodView:
    return json({'success': True, 'request': request.headers})


@app.route('/mine', methods=['GET'])
async def mine():
    """
    Mine a new block
    :return:
    """
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(
        sender='0',
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    return json({
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    })


@app.route('/transactions/new', methods=['POST'])
async def new_transaction(request: Request):
    """
    Add a new trasaction to the block
    :return:
    """
    values: dict = request.json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return json({'error': 'Missing values'}), 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    return json({'message': f'Transaction will be added to Block {index}'}), 201


@app.route('/chain', methods=['GET'])
async def chain(request: Request):
    return {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
