# Fundamentus Scrapper

A lightweight API build to fetch stock dividends payment dates from the website Fundamentus.

## Built with

- Python
- Flask
- Virtualenv

## Building

You'll need Python and Virtualenv installed on your machine.

Install `virtualenv` with:

```sh
$ pip install virtualenv
```

Clone or download the repository

```sh
$ git clone git@github.com:ramos-ph/fundamentus-scrapper.git
$ cd fundamentus-scrapper
```

Create and activate the virtual env

```sh
$ virtualenv env
$ source env/bin/activate
```

Install the project dependencies

```sh
$ pip install -r requirements.txt
```

To deactivate the virtual enviroment, just run

```sh
$ deactivate
```

## Running

On the `virtualenv`, run

```sh
$ python3 api/app.py
```

This will start a Flask server on port 5000.

## Consuming the API

Browse to `http://localhost:5000/payments` and provide the symbols that you want.

Example:

```json
// GET: http://localhost:5000/payments?symbols=ITUB4,ITSA4

{
	"data": [
		{
			"symbol": "ITUB4",
			"pending_earnings": [
				{
					"value": "0,0177",
					"date": "01/04/2022",
					"type": "JRS CAP PROPRIO"
				}
			]
		},
		{
			"symbol": "ITSA4",
			"pending_earnings": [
				{
					"value": "0,1134",
					"date": "29/12/2023",
					"type": "JRS CAP PROPRIO"
				},
				{
					"value": "0,0235",
					"date": "01/04/2022",
					"type": "JRS CAP PROPRIO"
				}
			]
		}
	],
	"errors": []
}
```
