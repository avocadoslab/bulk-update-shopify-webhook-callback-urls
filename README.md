## What's the problem?

Currently when app URL changes for some reason, Shopify would keep sending webhook callbacks to old URL. This would result in webhook failures and potential removals if apps don't ack in 24 hours. Currently Shopify doesn't allow you to bulk update callback URL.

## How to solve it?

Script that goes through all stores where your app is installed and then updates the webhook callback URL.

## Underlying Shopify APIs:

1. [Retrieves a list of webhooks](https://shopify.dev/docs/api/admin-rest/2024-04/resources/webhook#get-webhooks)
2. [Modify an existing Webhook](https://shopify.dev/docs/api/admin-rest/2024-04/resources/webhook#put-webhooks-webhook-id)

### Prerequisite 

1. Shopify domain names for all stores that has your app installed. (refer `data.json`)
2. Access token of each token to make mutation call.
3. Python
4. Patience :)

## How to use this script?

1. Populate `data.json` with relevant store URL along with access token.
2. Update old & new callback URLs in `script.py` at line 19 & 20
3. Install python dependencies.
```
pip install requests
pip install colorama
```
4. Run script using 
```
python script.py
```
5. Sit back & relax.

## How long would script take for 5000 stores?

The script introduces a 1-second delay between requests to avoid rate limiting and let's assume the time taken for each API request to complete (including network latency and server processing time) is approximately 1 second. So, it would take approximately 2.78 hours to process 5000 objects with the current script.
