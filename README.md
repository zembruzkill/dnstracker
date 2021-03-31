<h1 align="center">DNSTracker</h1>

## Technologies

This project was developed with the following technologies and libraries:

- [Python](https://www.python.org/)
- [Flask](https://reactjs.org)
- [SQLite3](https://www.sqlite.org/index.html)


- [DNSPython](https://www.dnspython.org/)


## Project

The DNSTracker is a project that allow us to measure the DNS infrastructure in the wild. The project is composed of a server and a crawler. 

* The server provides API endpoints that are used to write and read the DNS queries.
* The crawler uses a list of domains and performs DNS queries for each of these and save using a API endpoint.

## DNS Query exemple for a "NS"
```JSON
{
	"version_id": 1,
	"domain": "google.com.br",
	"query_type": "NS", 
	"query_name": "ns1.google.com", 
	"ipv4_address": "[192.168.0.1, '192.168.1.1']", 
	"ipv6_address": "null", 
	"as_number": "null",
	"as_name": "null", 
	"bgp_prefix": "null", 
	"worker_id": "wes-aws1", 
	"created_at": "2021-03-30 22:34:16.805160", 
	"updated_at": "2021-03-30 22:34:16.805160"
}
```

## Development environment setup
To setup your development environment, please follow the steps below.

1. Install [Git](https://git-scm.com/).
2. Install Python3, Pip3 and Pipenv.
    * `sudo apt-get install python3.8 python3-pip`
    * `sudo pip install pipenv autopep8`
3. Clone this repo.
    * `git clone https://github.com/zembruzkill/dnstracker`
4. Inside the repository directory, run the following commands.
    * `pipenv install --dev`
    * `pipenv shell`



## How to contribute

- Fork this repository;
- Create a branch with your feature: `git checkout -b my-feature`;
- Commit your changes: `git commit -m 'feat: my new feature'`;
- Push to your branch: `git push origin my-feature`.

After the merge of your pull request is done, you can delete your branch.


Desenvolvido by [zembruzkill](https://zembruzkill.github.io/)
