# cf-ddns

A basic dyanmic DNS background script for cloudflare domain registrar.

This script is used to update A records in cloudflare, it uses the public ip address of the device that is running the script.

The script will write out logs to a file inside the directory (`cf-ddns.log`), you can update this location if you want to inside the `src/ddns.py` file.

### Local Development

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

### Cron

If you want this script to run every reoccuring then setup a crontab on the serer you want to run it from

```bash
crontab -e
*/5 * * * * /usr/bin/python /path/to/script/ddns.py
```

### Environemnt Variables

The following environment variables need to be set before running the script.

- `CLOUDFLARE_API_KEY` [cloudflare global api key](https://developers.cloudflare.com/fundamentals/api/get-started/keys/)
- `CLOUDFLARE_EMAIL` email address associated with cloudflare account

### Tests

All files should have a corresponding unit test file arranged in the tests folder.

To run the tests run the following command.

```bash
python -m unittest discover tests
```

### CI/CD

CI/CD just simply runs the tests on push via Github Actions.

Updates to the actions pipeline can be done in `.github/workflows/cf-ddns.yaml`
