#!/usr/bin/env python3

import argparse
import requests
import json

def get_check_by_name(name):
    reqcheck = requests.get("https://api.pingdom.com/api/3.1/checks", 
        headers = {
            'Authorization': args['auth']
        }
    )

    if reqcheck.status_code != 200:
        raise Exception('Request check failed. Response code is :{}'.format(reqcheck.status_code))
        return False

    obj = json.loads(reqcheck.text)

    for check in obj["checks"]:
        if check["name"] == args["name"]:
            return check
    return None

def create_check(auth, json_check):
   
    headers = {
        'Authorization' : auth,
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }

    reqcreate = requests.post(
        'https://api.pingdom.com/api/3.1/checks', 
        headers = headers,
        data = json.dumps(json_check)
    )

    if reqcreate.status_code == 200:
        print("Check has been created.")
        exit(0)
    raise Exception('Unexpected error, Return code to create check is :{}'.format(reqcreate.status_code))

def update_check(auth, checkid, json_check):

    json_check.pop("type")

    headers = {
        'Authorization' : auth,
        'Content-type': 'application/json'
    }

    requpdate = requests.put(
        'https://api.pingdom.com/api/3.1/checks/'+str(checkid),
        headers = headers,
        data = json_check
    )

    if requpdate.status_code == 200:
        print("Check has been updated.")
        exit(0)

    raise Exception('Unexpected error, Return code to update check is :{}'.format(requpdate.status_code))

def delete_check(auth, checkid):
    
    headers = {
        'Authorization' : auth
    }

    reqdelete = requests.delete(
        'https://api.pingdom.com/api/3.1/checks/'+str(checkid),
        headers = headers
    )

    if reqdelete.status_code == 200:
        print("Check has been deleted")

def args2json(args):
    
    json_check = {
        "name" : args['name'],
        "host" : args['fqdn'],
        "type" : "http",
        "encryption" : "true"
    }

    return json_check

ap = argparse.ArgumentParser()

ap.add_argument("-n", "--name", required=True, help="Name of the check")
ap.add_argument("-f", "--fqdn", required=True, help="FQDN to check")
ap.add_argument("-a", "--auth", required=True, help="Auth for API")
ap.add_argument("-r", "--resolution", default=5, help="Resolution of check (default = 5)")
ap.add_argument("-d","--delete", action='store_true', help="If present, delete the check (target by name)" )

args = vars(ap.parse_args())

json_check = args2json(args)

# Verify if check already exists
check = get_check_by_name(args['name'])
if check == None and not(args['delete']):
    
    # It doesn't then let's create it
    create_check(args['auth'], json_check)

elif check != None:

    if args['delete']:
        delete_check(args['auth'], check['id'])

    elif check['hostname'] != args['fqdn']:
        update_check(args['auth'], check['id'], json_check)

    else:
        print('Check already exists ({}) and no update is needed '.format(check['id']))

exit()