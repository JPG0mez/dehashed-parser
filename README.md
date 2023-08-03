ChatGPT wrote this readme

# Dehashed API Tool

This is a Python script to fetch and process data from the Dehashed API. The script allows you to query the API for a specific domain and retrieve email-password and email-hash pairs. It then saves the results in separate files with the format "email:value" for both passwords and hashes.

## Usage

### Prerequisites
- Python 3.x

### Installation
1. Clone this repository to your local machine:

```
git clone https://github.com/your-username/dehashed-api-tool.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```


### How to Use
1. Make sure you have obtained your Dehashed API credentials (email and API key) from the Dehashed website.

2. Run the script using the following command:

```
python3 dehashed_tool.py <domain> <email> <api_key>
```


Replace `<domain>`, `<email>`, and `<api_key>` with your desired domain, email, and API key respectively.

3. The script will fetch data from the Dehashed API and save the results in files with the following names:
- `example.passw` (contains email:password pairs)
- `example.hashes` (contains email:hash pairs)

### Output Files
The script will generate two output files (`example.passw` and `example.hashes`) in the same directory as the script. These files will contain email-password and email-hash pairs found in the Dehashed API response. Entries with password or hash values equal to "xxx" or "temp" will be skipped.

## License
[MIT License](LICENSE)
