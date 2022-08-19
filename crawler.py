import json
import dns.resolver
import concurrent.futures
import sys
from datetime import datetime
import requests

api_url_base = 'http://127.0.0.1:5000'
newHeaders = {'Content-type': 'application/json'}


def postQuery(query):
    json_data = json.dumps(query)
    response = requests.post(api_url_base+'/dns_query',
                             json_data, headers=newHeaders)

    print(response.status_code)
    if response.status_code != 201:
        print(json_data)
        print(response.text)

def updateQuery(query):
    json_data = json.dumps(query)
    response = requests.post(api_url_base+'/dns_query',
                             json_data, headers=newHeaders)

    print(response.status_code)
    if response.status_code != 201:
        print(json_data)
        print(response.text)


def getSimpleARecord(address):
    try:
        answers = dns.resolver.resolve(address, 'A')
        records = []
        for rdata in answers:
            records.append(rdata.to_text())
        return records
    except Exception as e:
        domainErrorDict.add(address)
        print(address, e)
        return None

def getSimpleAAAARecord(address):
    try:
        answers = dns.resolver.resolve(address, 'AAAA')
        records = []
        for rdata in answers:
            records.append(rdata.to_text())
        return records
    except Exception as e:
        domainErrorDict.add(address)
        print(address, e)
        return None


def getARecord(address):
    try:
        answers = dns.resolver.resolve(address, 'A')
        record = []
        for rdata in answers:
            record.append(rdata.to_text())

            now = datetime.now()
            query = {}
            query['domain'] = address
            query['version_id'] = 1
            query['query_name'] = address
            query['query_type'] = 'A'    
            query['ipv4_address'] = rdata.to_text()
            query['ipv6_address'] = None
            query['as_number'] = None
            query['as_name'] = None
            query['bgp_prefix'] = None
            query['worker_id'] = None
            query['created_at'] = now.isoformat()
            query['updated_at'] = now.isoformat()

            print('query A', query)

        postQuery(query)

        return True
    except Exception as e:
        domainErrorDict.add(address)
        print(address, e)
        return None


def getAAAARecord(address):
    try:
        answers = dns.resolver.resolve(address, 'AAAA')
        record = []
        for rdata in answers:
            record.append(rdata.to_text())

            now = datetime.now()
            query = {}
            query['domain'] = address
            query['version_id'] = 1
            query['query_name'] = address
            query['query_type'] = 'AAAA'    
            query['ipv4_address'] = None
            query['ipv6_address'] = rdata.to_text()
            query['as_number'] = None
            query['as_name'] = None
            query['bgp_prefix'] = None
            query['worker_id'] = None
            query['created_at'] = now.isoformat()
            query['updated_at'] = now.isoformat()

            print('query AAAA', query)

            postQuery(query)

        return True
    except Exception as e:
        domainErrorDict.add(address)
        print(address, e)
        return None


def getNSRecord(address):
    try:
        answers = dns.resolver.resolve(address, 'NS')
        for rdata in answers:
            now = datetime.now()
            query = {}
            query['domain'] = address
            query['version_id'] = 1
            query['query_name'] = rdata.to_text()
            query['query_type'] = 'NS'    
            query['ipv4_address'] = ",".join(getSimpleARecord(rdata.to_text())).join(("[","]"))
            query['ipv6_address'] = ",".join(getSimpleAAAARecord(rdata.to_text())).join(("[","]"))
            query['as_number'] = None
            query['as_name'] = None
            query['bgp_prefix'] = None
            query['worker_id'] = None
            query['created_at'] = now.isoformat()
            query['updated_at'] = now.isoformat()

            print('query NS', query)

            postQuery(query)

        return True
    except Exception as e:
        domainErrorDict.add(address)
        print(address, e)
        return None


def getMXRecord(address):
    try:
        answers = dns.resolver.resolve(address, 'MX')
        for rdata in answers:
            now = datetime.now()
            mx_split = rdata.to_text().split()
            a_records = getSimpleARecord(mx_split[1])
            aaaa_records = getSimpleAAAARecord(mx_split[1])
            for a_record in a_records:
                query = {}
                query['domain'] = address
                query['version_id'] = 1
                query['query_name'] = mx_split[1]
                query['query_type'] = 'MX'    
                query['ipv4_address'] = a_record
                query['ipv6_address'] = None
                query['as_number'] = None
                query['as_name'] = None
                query['bgp_prefix'] = None
                query['worker_id'] = None
                query['created_at'] = now.isoformat()
                query['updated_at'] = now.isoformat()

                print('query MX', query)
                postQuery(query)

            for aaaa_record in aaaa_records:
                query = {}
                query['domain'] = address
                query['version_id'] = 1
                query['query_name'] = mx_split[1]
                query['query_type'] = 'MX'    
                query['ipv4_address'] = None
                query['ipv6_address'] = aaaa_record
                query['as_number'] = None
                query['as_name'] = None
                query['bgp_prefix'] = None
                query['worker_id'] = None
                query['created_at'] = now.isoformat()
                query['updated_at'] = now.isoformat()

                print('query MX', query)
                postQuery(query)            

        return True
    except Exception as e:
        domainErrorDict.add(address)
        print(address, e)
        return None


def getRecordsFromAuth(fqdn):
    print(f'Processing {fqdn}')

    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = [resolver]
    dns.resolver.timeout = 5

    getARecord(fqdn)
    getAAAARecord(fqdn)
    # getNSRecord(fqdn)
    getMXRecord(fqdn)

    return True



if len(sys.argv) != 3:
    print("Wrong number of parameters\n")
    print(str(len(sys.argv)))
    print("Usage:  python crawler.py  $listOfDomainsFile  $resolverAddress")

else:
    today = datetime.now()
    domainList = []
    distinct_domain = []
    processedDomain = set()
    domainErrorDict = set()

    resolver = sys.argv[2]

    domains_obj_list = []

    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        for k in lines[:30000]:
            sp = k.split(",")
            domain = sp[1].strip()
            ip = resolver
            domainList.append(domain)
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
        for result in executor.map(getRecordsFromAuth, domainList):
            pass


            
