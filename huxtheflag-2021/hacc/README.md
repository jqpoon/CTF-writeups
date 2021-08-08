# HACC

All we have is a PDF file, which seems to be encrypted with a password. 

We can use [pdfcrack](https://github.com/robins/pdfcrack) to perform a dictionary attack using a well known password list, `rockyou.txt`.

```bash
$ pdfcrack --wordlist=~/Desktop/rockyou.txt HACCLangSpec.pdf
PDF version 1.5
Security Handler: Standard
V: 2
R: 3
P: -3904
Length: 128
Encrypted Metadata: True
FileID: 18a653269c3c062c9221364072ae7633
U: e59b6498275a1c5920fbba783d9077a300000000000000000000000000000000
O: 311038eaa82074495aa594c02aa085dd87087636c3c8202e2b9d6e13690914cf
Average Speed: 73559.2 w/s. Current Word: 'ms061104'
Average Speed: 73600.1 w/s. Current Word: 'vali4here'
found user-password: 'rockthanos@yahoo.gr'
```

The flag is found at the bottom of the file along with a photo of Thanos.

`HTF{1_4m_1_1n3v1t4bl3}`