# s1-ad-diff
Small Python script to check which clients have SentinelOne agent installed.

To retrieve the CSV files from AD with powershell (only retrieve computers that have logged in within the last 30 days):

``Get-ADComputer -Filter * -Properties * | Where { $_.LastLogonDate -GT (Get-Date).AddDays(-30) } | Select -Property Name,DNSHostName,Enabled,LastLogonDate,Description,@{Name="ModifiedLastLogonDate";Expression={$_.LastLogonDate.ToString("yyyy-MM-dd HH:mm")}} | Export-CSV "ad-computers.csv" -NoTypeInformation -Encoding UTF8``

To get the CSV from SentinelOne: Make a full export 

The scripts wants these files:

- ``ad-computers.csv``: Powershell AD export
- ``s1export.csv``: S1 console export
- ``exclude.csv``: List of computers you would like to exclude like hosts that do not support the agent

After running the script you will get the result as a csv  file (``s1-ad-diff_%Y%m%d-%H%M%S.csv``) and you can filter it as you like.



