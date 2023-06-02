# ETH WALLET TRACKER 
Python, Flask project which enables you to track specific Ethereum wallets with feed of newest transactions and check balance + transaction history for every eth wallet. Txn and wallet data fetched with etherscan API, user details saved in postgres database.

Main functionalities:
- register/ log in
- look for specific wallet's transaction history with more details (eth amount, time etc.)
- add wallets to the "followed" list
- feed with most recent transactions of the wallets that are tracked by you

To run the project you need:
- python with installed libraries from *requirements.txt* file,
- etherscan key saved as "*etherscan_key*" environment variable
- postgres database (*DATABASE*)

Issues that I am working on:
- 
