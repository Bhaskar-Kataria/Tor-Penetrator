import time
import pyfiglet
from colorama import Fore
import concurrent.futures as executor
import os
import pandas as pd
from searchEngines import Scanner
from database import Database

def display(engine:str, urldict:dict) -> None:
    print(f"\nActive Links from {engine} search engine:\n")
    j = 0
    link_len = 0
    
    for k in urldict.keys():
        
        if j != 0:
            print("\t", "-" * link_len)
        
        print("\t", urldict[k], " : ", k)
        link_len = (len(k) + len(urldict[k]) + 5)
        j = 1

def saveToCsv(fName:str, csvDict:dict) -> None:
    fileName = fName + '.csv'
            
    df = pd.DataFrame(csvDict)

    if fileName in os.listdir():
        df2 = pd.read_csv(fileName)
        rows = df2.shape[0]
        df.index += rows + 1
        df.to_csv(fileName, mode = 'a', header = False)
    else:
        df.index += 1
        df.to_csv(fileName)

def main() -> None:
    try:
        start_time = time.time()
        print(Fore.LIGHTCYAN_EX + pyfiglet.figlet_format('THE'))
        time.sleep(0.3)
        print(pyfiglet.figlet_format('TOR'))
        time.sleep(0.3)
        print(pyfiglet.figlet_format('SCANNER'))
        time.sleep(1)
        
        if os.getuid()!=0:
            print("The Program must run as root")
            exit()

        attempt = 0
        subAttempt = 0
        valid = 0
        n =0
        q = ''
        ahmiaDict = dict()
        torchDict = dict()
        deepsearchDict = dict()

        while attempt < 2:
            print('MENU')
            print('1. Solo-search-engine scanning')
            print('2. Multi-search-engine scanning')

            try:
                choice1 = int(input("\nEnter your choice: "))

            except:
                print('Invalid Input!!!\n')
                attempt += 1
                continue

            if choice1 == 1:
                
                while subAttempt < 2:
                    print('\nSUB-MENU')
                    print('Search Engines:')
                    print('1. Ahmia')
                    print('2. Torch')
                    print('3. Deepsearch')

                    try:
                        subchoice = abs(int(input("\nEnter your search engine choice: ")))

                    except:
                        print('Invalid Input!!!\n')
                        subAttempt += 1
                        continue

                    if subchoice > 0 and subchoice < 4:
                        subAttempt = attempt = 2

                        try:
                            q = input("Enter a query to search: ")
                            n = abs(int(input("Enter number of links to extract(max: 50): ")))

                        except:
                            print('Invalid Input!!!\n')
                            continue

                        db = Database()
                        dbUrlList = db.getColumn(3)
                        print()
                        scan = Scanner(n, q, dbUrlList)

                    if subchoice == 1:
                        print('\nStarting ahmia-search-engine scan\n')
                        ahmiaDict = scan.ahmiaScan()
                        display('Ahmia', ahmiaDict)
                        print(f"\nExtracted {len(ahmiaDict)} links from ahmia")
                        valid = 1

                    elif subchoice == 2:
                        print('\nStarting torch-search-engine scan\n')
                        torchDict = scan.torchScan()
                        display('Torch', torchDict)
                        print(f"\nExtracted {len(torchDict)} links from ahmia")
                        valid = 1

                    elif subchoice == 3:
                        print('\nStarting deepsearch-search-engine scan\n')
                        deepsearchDict = scan.deepSearch()
                        display('Deepsearch', deepsearchDict)
                        print(f"\nExtracted {len(deepsearchDict)} links from ahmia")
                        valid = 1

                    else:
                        print('Invalid Choice!!!\n')
                        subAttempt += 1
            
            elif choice1 == 2:
                attempt = 2

                try:
                    q = input("Enter a query to search: ")
                    n = abs(int(input("Enter number of links to extract(per search engine, max: 50): ")))

                except:
                    print('Invalid Input!!!\n')
                    continue
                
                db = Database()
                dbUrlList = db.getColumn(3)

                print('\nStarting multi-search-engine scan\n')
                scan = Scanner(n, q, dbUrlList)

                pool = executor.ThreadPoolExecutor(max_workers= 3)
                ahmia = pool.submit(scan.ahmiaScan)
                torch = pool.submit(scan.torchScan)
                deepsearch = pool.submit(scan.deepSearch)
                pool.shutdown(wait = True)

                ahmiaDict = ahmia.result(timeout = None)
                torchDict = torch.result(timeout = None)
                deepsearchDict = deepsearch.result(timeout = None)

                display('Ahmia', ahmiaDict)
                display('Torch', torchDict)
                display('Deepsearch', deepsearchDict)

                print('\n')
                print(f"Extracted {len(ahmiaDict)} links from ahmia")
                print(f"Extracted {len(torchDict)} links from torch")
                print(f"Extracted {len(deepsearchDict)} links from deepsearch")
                valid = 1
            
            else:
                print('Invalid Choice!!!\n')
                attempt += 1

        if valid == 1:
            urlList = []
            urlTitle = []
            urlEngine = []
            urlQuery =[]

            for item in ahmiaDict.keys():
                urlList.append(item)
                title = ahmiaDict[item].encode('ascii', 'ignore').decode('ascii')
                urlTitle.append(title)
                urlEngine.append('ahmia')
                urlQuery.append(q)
                
            for item in torchDict.keys():
                urlList.append(item)
                title = torchDict[item].encode('ascii', 'ignore').decode('ascii')
                urlTitle.append(title)
                urlEngine.append('torch')
                urlQuery.append(q)

            for item in deepsearchDict.keys():
                urlList.append(item)
                title = deepsearchDict[item].encode('ascii', 'ignore').decode('ascii')
                urlTitle.append(title)
                urlEngine.append('deepsearch')
                urlQuery.append(q)
                    
            for i in range(2):
                
                try:
                    ch = input("\n\nDo you want to scan these websites for illegal content(Y/N): ")

                except:
                    print('Invalid Input!!!\n')
                    continue
                
                if ch == 'Y' or ch == 'y':
                    break
                
                elif ch != 'N' or ch != 'n':
                    break
                
                else:
                    print("Invalid Input!!!")
                    i += 1
            
            if ch == 'Y' or ch == 'y':
                print("\nStarting Scan...")
                scan.scrap(urlList)
            
            csvDict = {'SiteTitle' : urlTitle, 'SiteUrl' : urlList, 'SearchEngine' : urlEngine, 'Query' : urlQuery}
            
            db.insertData(csvDict)

            fName = input("\nEnter name of file to save results: ")
            saveToCsv(fName, csvDict)

        print("\nExecution time = ", round((time.time() - start_time)), "second(s)")
    
    except KeyboardInterrupt:
        print("\nKeyboard interruption occurred")
        print("Exiting program...")
        time.sleep(1)
        os._exit(1)


if __name__ == "__main__":
    main()
