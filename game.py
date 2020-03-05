import json
import requests
import sys
import os
import time
import winsound
import hashlib

# run inside pipenv shell
token = os.environ['API_KEY']

url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv'





def init():
    r = requests.get(
        url=url+'/init/',
        headers={'Authorization': f'Token {token}'}
    )
    try:
        data = r.json()
        return data
    except:
        data = r.json
        return data


def move(dir, room_id=None):
    if room_id == None:
        dirs = {'direction': f'{dir}'}
    else:
        dirs = {'direction': f'{dir}', 'next_room_id': f'{room_id}'}
    r = requests.post(
        url=url+'/move/',
        headers={
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        },
        json=dirs
    )
    try:
        data = r.json()
        return data
    except:
        data = r.json
        print('Error')
        return data


def mine(proof):
    dirs = {'proof': proof}
    r = requests.post(
        url='https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/',
        headers={
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        },
        json=dirs
    )
    try:
        data = r.json()
        print(data)
        return data
    except:
        print('Error')
        print(r)
        
        
def get_last_proof():
    r = requests.get(
        url='https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/',
        headers={
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
    )
    try:
        data = r.json()
        print(data)
        return data
    except:
        print('Error')
        print(r)

def proof_of_work(last_proof, diff):
    proof = 0
    while not valid_proof(last_proof, proof, diff):
        proof += 1
    return proof



def valid_proof(last_proof, proof, diff):

    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    equals_string = '0' * diff
    return guess_hash[:diff] == equals_string

if __name__ == '__main__':
    current_room = init()
    print(current_room)
    while True:
        print(current_room)
        print('COOLDOWN REMAINING: ' + str(current_room['cooldown']))
        time.sleep(current_room['cooldown'])
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        user_input = input("-> ").lower().split(" ")
        print(user_input)
        if user_input[0] in ["n", "s", "e", "w"]:
            if len(user_input) == 1:
                current_room = move(user_input[0])  
            else:
                current_room = move(user_input[0], user_input[1])
        elif user_input[0] == 'mine':
            proof_data = get_last_proof()
            last_proof = proof_data['proof']
            diff = int(proof_data['difficulty'])
            
            proof = proof_of_work(last_proof, diff)
            mine(proof)
        elif user_input[0] == 'q':
            sys.exit(0)
        else:
            print("Invalid command. Please try again.")
