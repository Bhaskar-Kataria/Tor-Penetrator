from requiredLibraries import *
import urllib

class Scanner:

    """A library for scanning top dark web search engines with built-in functionalities to securely extract urls of websites hosting illegal services onto the tor networks."""

    linkCount = 0
    query = ''
    session = None
    header = None
    discardUrlList = None

    def __init__(self, numOfLinks:int, query:str, purgeUrlList:list = []) -> None:
        try:
            self.discardUrlList = purgeUrlList
            print(Fore.GREEN + "Starting tor service")
            os.system("service tor restart")

            if numOfLinks > 50:
                self.linkCount = 50
            else:
                self.linkCount = numOfLinks

            self.query = query
            self.ses()
            self.tor()

        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured at initialisation\nError: ', e)
            exit()
        
    def ses(self) -> None:
        try:
            self.session = requests.Session()
            retry = Retry(connect = 3, backoff_factor = 0.5)
            adapter = HTTPAdapter(max_retries = retry)
            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)
            self.session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
        
        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured in session\nError: ', e)
            exit()

    def tor(self) -> None:
        try:
            on_url = "https://html.duckduckgo.com/"
            test = "http://ident.me"
            self.header = {'User-Agent' : UserAgent().random}
            self.header['Accept-Encoding'] = 'gzip'
            r = self.session.get(on_url, headers=self.header)

            if r.status_code != 200:
                print("URL not responding")

            with Controller.from_port(port = 9051) as c:
                    c.authenticate()
                    c.signal(Signal.NEWNYM)
                    t = self.session.get(test)
                    print("Tor-IP: ", t.text, self.header['User-Agent'])
        
        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured in tor\nError: ', e)
            exit()
        
    def ahmiaScan(self) -> dict:
        try:
            on_url = "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search"
            r = self.session.get(on_url, headers=self.header)

            if r.status_code == 200:
                params = {'q' : self.query}
            
                req=self.session.get(on_url, headers = self.header, params = params)
                links_desc = BeautifulSoup(req.content,features = "lxml", parse_only = SoupStrainer('h4')).find_all('h4', limit = 100)
                links_on = BeautifulSoup(req.content,features = "lxml", parse_only = SoupStrainer('cite')).find_all('cite', limit = 100)
                count_ind = 0
                count = 0
                returnDict = dict()

                for info in links_on:

                    if count < self.linkCount:
                        link = "http://" + info.getText().strip()
                        repeatFlag = 0
                        
                        if len(self.discardUrlList) > 0:
                            for url in self.discardUrlList:
                                if link == url:
                                    repeatFlag = 1
                                    break

                        if repeatFlag == 0:
                            try:
                                self.header['User-Agent'] = UserAgent().random
                                req=self.session.get(link, headers = self.header, timeout = 20)

                                if req.status_code == 200:
                                    returnDict[link] = links_desc[count_ind].getText().strip()
                                    count += 1
                                    print("Ahmia: Successful")
                                    count_ind += 1
                                    continue
                                else:
                                    count_ind += 1
                                    continue

                            except KeyboardInterrupt:
                                    print("\nKeyboard interruption occurred")
                                    print("Exiting program...")
                                    time.sleep(1)
                                    exit()

                            except:
                                print("Ahmia: exception occured")
                                continue

                    else:
                        break

            else:
                print('Ahmia not responding')
        
        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured in ahmia\nError: ', e)
            os._exit(1)

        if len(returnDict) > 0:
            return returnDict

    def torchScan(self) -> dict:
        try:
            on_url = "http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search"
            r = self.session.get(on_url, headers=self.header)

            if r.status_code == 200:
                params = {'query' : self.query}
            
                req=self.session.get(on_url, headers = self.header, params = params)
                links_desc = BeautifulSoup(req.content,features = "lxml", parse_only = SoupStrainer('h5')).find_all('h5', limit = 100)
                i = 0
                count = 0
                flag = 0
                returnDict = dict()

                for info in links_desc:
                    nes = info.find_all('a')

                    for i in nes:

                        if count < self.linkCount:
                            link = i.get('href').strip()
                            repeatflag = 0

                            if len(self.discardUrlList) > 0:
                                for url in self.discardUrlList:
                                    if link == url:
                                        repeatflag = 1
                                        break

                            if repeatflag == 0:

                                try:
                                    self.header['User-Agent'] = UserAgent().random
                                    req = self.session.get(link, headers = self.header, timeout = 20)

                                    if req.status_code == 200:
                                        print("Torch: Successful")
                                        returnDict[link.strip()] = i.getText().strip()
                                        count += 1
                                    else:
                                        continue

                                except KeyboardInterrupt:
                                    print("\nKeyboard interruption occurred")
                                    print("Exiting program...")
                                    time.sleep(1)
                                    exit()

                                except:
                                    print("Torch: exception occured")
                                    continue
                                    
                        else:
                            flag = 1
                            break

                    if flag == 1:
                        break
            else:
                print('Torch not responding')
        
        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured in torch\nError: ', e)
            os._exit(1)

        if len(returnDict) > 0:
            return returnDict
    
    def deepSearch(self) -> dict:
        try:
            on_url = "http://search7tdrcvri22rieiwgi5g46qnwsesvnubqav2xakhezv4hjzkkad.onion/result.php"
            r = self.session.get(on_url, headers = self.header)

            if r.status_code == 200:
                params = {'search' : self.query}
                req = self.session.get(on_url, headers = self.header, params = params)
                links_desc = BeautifulSoup(req.content, features = "lxml", parse_only = SoupStrainer('a', {'class':'title'})).find_all('a', {'class':'title'},limit = 100)
                list_on = []
                list_des = []
                tempUrlList = []
                returnDict = {}
                count = 0

                for i in links_desc:
                        href = i.get('href').strip()
                        parsed_url = urllib.parse.urlparse(href)
                        query_params = urllib.parse.parse_qs(parsed_url.query)
                        
                        if 'url' in query_params:
                            extracted_link = query_params['url'][0]
                            list_on.append(extracted_link)
                            list_des.append(i.getText())

                a = zip(list_on, list_des)
                dict1 = dict(a)

                for i in dict1.keys():

                    if count < self.linkCount:
                        link = i.strip()
                        repeatflag = 0

                        if len(self.discardUrlList) > 0:
                            for url in self.discardUrlList:
                                if link == url:
                                    repeatflag = 1
                                    break

                        if repeatflag == 0:
                        
                            try:
                                self.header['User-Agent'] = UserAgent().random
                                req = self.session.get(link, headers = self.header, timeout = 20)

                                if req.status_code == 200:
                                    count += 1
                                    print('Deepsearch: Successful')
                                    tempUrlList.append(i)
                                else:
                                    continue

                            except KeyboardInterrupt:
                                print("\nKeyboard interruption occurred")
                                print("Exiting program...")
                                time.sleep(1)
                                exit()

                            except:
                                print("DeepSearch: exception occured")
                                continue
                            
                    else:
                        break   

                for i in tempUrlList:
                    returnDict[i] = dict1[i]

        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured in deepSearch\nError: ', e)
            os._exit(1)

        if len(returnDict) > 0:
            return returnDict
    
    def scrap(self, urlList:list) -> None:
        try:
            illegalKeywords = illegalWords
            foundWord = []

            for scrapLink in urlList:
                    wordCount = 0

                    try:
                        req = self.session.get(scrapLink, headers = self.header, timeout = (20,None))
                        
                        if req.status_code == 200:
                            links_desc = BeautifulSoup(req.content, features = "lxml")
                            content = (links_desc.getText()).split()

                            for string in content:

                                for word in illegalKeywords:

                                    if re.findall(word, string, re.IGNORECASE):
                                        wordCount += 1
                                        foundWord.append(string)
                                        
                            print(f"\nResult for {scrapLink}:")
                            print(f"\tTotal keywords found = {wordCount}")
                            a = 0

                            for i in foundWord:
                                
                                if a == 0:
                                    print("\tKeywords: ", i, end = "")
                                    a = 1
                                else:
                                    print(", ", i, end = "")

                            print()
                            foundWord.clear()

                        else:
                            print(f"Could not connect to {scrapLink}")
                    
                    except KeyboardInterrupt:
                            print("\nKeyboard interruption occurred")
                            print("Exiting program...")
                            time.sleep(1)
                            exit()

                    except:
                        print("Exception occured")

        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured in scanning\nError: ', e)
            exit()
