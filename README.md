# Capsule Farmer Evolved

Are you tired of watching professional League of Legends games? Do you watch only for the drops? This is an revolution in farming of League of Legends Esports capsules!

**NO WEB BROWSER NEEDED!** The old [EsportsCapsuleFarmer](https://github.com/LeagueOfPoro/EsportsCapsuleFarmer) relied on a web browser to watch videos. *Capsule Farmer Evolved* simulates traffic to lolesports.com servers and tricks it into thinking the account is watching a stream. This approach drastically lowers the hardware requirements.

### Features
- Automatically logs user in
- Watches every live match
- Lightweight
- No web browser needed

## Configuration
Fill out your username and password in `config.yaml`. Name of the account groups is not important but I recommend entering something recognizable to better detect problems with the account. 
```yaml
accounts:
  accountname:
    username: "username"
    password: "password"
  anotheraccountname:
    username: "username"
    password: "password"
debug: True
```

## Installation (advanced)

### Prerequisities
- Python >= 3.10.1 (version 3.9 should work as well but is not officially supported)
- pipenv (`pip install pipenv`)

### Step by step
1. Clone this repo - `git clone https://github.com/LeagueOfPoro/CapsuleFarmerEvolved.git`
2. Move to the directory -  `cd CapsuleFarmerEvolved`
3. Install the Python virtual environment - `pipenv install`
4. (Optional) Edit the configuration file
5. Run the tool - `pipenv run python ./main.py`

### Update
In the CapsuleFarmerEvolved, run `git pull`
