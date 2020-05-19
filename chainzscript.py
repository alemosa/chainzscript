import requests,json,mysql.connector,ftplib,os,csv,sys

## CONNECTIONS ---------
#DB Connection
try:
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="coins")
	db = mydb.cursor()
	print("DB connection successful!")
except:
	print("DB connection failed")

#FTP connection
try:
	ftp = ftplib.FTP("ftp.smartdexsolutions.net")
	ftp.login("smartdexsolutions.net","bugsbunny94")
	ftp.cwd("/wallettracker/coinbase/images/coins")
	print("FTP connection successful!")
except:
	print("FTP connection failed")


#Getting chainz info
url = "https://chainz.cryptoid.info/explorer/api.dws?q=summary"
r= requests.get(url)
data = r.json()
coins={}

for key in data.keys():
	#Setting database structure 
	coins[key] = {"WalletType" : data[key]["name"], "cryptoSymbol" : key.upper(), \
	"apiURL" : "https://chainz.cryptoid.info/" + str(key) + "/api.dws?key=72a06c093a4f&q=multiaddr&n=0&active=", \
	"tokenString" : "final_balance", "divider" : 100000000, "cryptoName" : str(key), "cryptoImage" : str(key)}

## FUNCTIONS ----------

#progress bar function
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '■' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  

#function for uploading files
def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftp.storlines("STOR " + file, open("images/" + file))
    else:
        ftp.storbinary("STOR " + file, open("images/" + file, "rb"), 1024)

#function for creating CSV file
def createCSV():
	with open('coins.csv','w', newline = '') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
		for key in coins.keys():
			spamwriter.writerow([', '.join('"' + str(x) + '"' for x in coins[key].values())])
	print("Data saved to coins.csv!")

#function for getting images and uploading them
def retrieveImages():
	total = len(coins.keys())
	i=1
	for key in coins.keys():
		progress(i, total, status='Retrieving and uploading coin logos...')
		imageurl = "https://chainz.cryptoid.info/logo/" + str(key) + ".png"
		ri = requests.get(imageurl)
		open("images/coin_" + str(key) + ".png", "wb").write(ri.content)
		upload(ftp,"coin_" + str(key) + ".png")
		i+=1
	print()
	print("Coin logos saved to directory and uploaded to server!")


print()
print("	Welcome to the Chainz Script!")

while True:
	print()
	print("		#1 Get CSV file with all coins")
	print("		#2 Retrieve coin logos and upload to server")
	print("		#3 Exit")
	print()
	try:
		option = int(input("	Please, choose an option: "))
		if option == 1:
			print()
			createCSV()
			continue
		elif option == 2:
			print()
			retrieveImages()
			continue
		elif option == 3:
			print()
			print("Goodbye!")
			break
	except Exception as e:
		raise e
		print("That wasn't an option.")
		continue





#Database insertion
	# columns = ', '.join("`" + str(x) + "`" for x in coins[key].keys())
	# values = ', '.join("'" + str(x) + "'" for x in coins[key].values())
	# sql = "INSERT INTO cointable ( %s ) VALUES ( %s )" % (columns, values)
	# db.execute(sql)


#mydb.commit()