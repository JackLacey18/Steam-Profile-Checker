'''

Fed up with cheaters pleading ignorance in Left 4 Dead 2, I have created a script
that scrapes any suspicious information from a player's profile page that can then 
be copied into the game's chat to prove to the other players that the cheater is cheating.

Run directly in command line. You will be prompted to paste the Steam profile URL of the player
you are looking into. This will return a number of details to you.

Details include:
    * Their Steam name.
    * Notify if the Steam profile is private.
    * The number of suspicious comments made.
    * And any VAC bans they have against their profile.
    * Any suspicious comments left on their profile page.

'''



if __name__ == ('__main__'):  
    # Imports
    import requests
    import bs4
    import pyperclip

    url = ''
    while url != 'q':

        # Enter the URL of the player's profile page.
        url = input("Please enter URL of the Steam profile you wish to check or type 'q' to quit. ")

        if url == 'q':
            break
            
        if url[-1] !='/':
            url = str(url) + '/'

        try:
            # Making the request and creating the soup.
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
            request = requests.get(str(url) + 'allcomments',headers=headers)
            soup = bs4.BeautifulSoup(request.content,'lxml')

            # Parsing for the name of the player.
            name = [i.text.strip() for i in soup.find_all('a',class_='whiteLink persona_name_text_content')][0]

            # Parsing the soup for authors and their comments.
            authors = [''.join(''.join(''.join(i.text.strip().split('\t')).split('\n')).split('\r')) for i in soup.find_all('div',class_='commentthread_comment_author')]
            text = [''.join(''.join(''.join(i.text.strip().split('\t')).split('\n')).split('\r')) for i in soup.find_all('div',class_='commentthread_comment_text')]
            comments = list(zip(authors,text))

            # Suspicious keywords list.
            keywords = ['cheat','cheating','cheats','cheatz','cheater',
                       'hack','hacking','hacks','hackz','hax','hacker',
                       'script','scripting','scripts','scriptz','scripter',
                       'aimbot','wallhacks','wallhackz',
                       'Cheat','Cheating','Cheats','Cheatz','Cheater',
                       'Hack','Hacking','Hacks','Hackz','Hax','Hacker',
                       'Script','Scripting','Scripts','Scriptz','Scripter',
                       'Aimbot','Wallhacks','Wallhackz']

            # Looking for keywords in all the comments and appending to the list of callouts.
            callouts = []
            for comment in comments:
                for keyword in keywords:
                    if keyword in comment[1]:
                        if comment not in callouts:
                            callouts.append(comment)

            # VAC ban check.
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
            request = requests.get(url,headers=headers)
            soup = bs4.BeautifulSoup(request.content,'lxml')
            VAC_ban = [''.join(''.join(i.text.strip().split('\t')).split('\n\r\n')) for i in soup.find_all('div',class_='profile_ban_status')]

            # Private check.
            private_check = [i.text.strip() for i in soup.find_all('div', class_='profile_private_info')]

            # Dots to try to ensure personal details are not copied into the clipboard from the CLI.
            for i in range(40):
                print('.')

            string = ''

            # Begin joining the results starting with the player's name.
            string = string + 'Player name: ' + name + ', '

            # Concat private check.
            if len(private_check) > 0:
                string = string + str(private_check[0])

            else:
                # Concat the number of suspicious comments.
                string = string + 'Comments on profile page that mention cheats, hacks or scripts: ' + str(len(callouts)) + ', '

                # Concat any VAC ban on record or print that none were found.
                if len(VAC_ban) > 0:
                    string = string + str(VAC_ban[0])
                else:
                    string = string + 'No VAC ban on record.'

            print(string)
            pyperclip.copy(string)
            print('Copied to clipboard!')

            for callout in callouts:
                print(' Comment:','"' + str(callout[1]) + '", ')

        except:
             print('No user found with that URL.')