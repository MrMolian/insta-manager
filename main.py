import instaloader
import sys
from bs4 import BeautifulSoup
import requests
import time
import os
from io import StringIO
import shutil
import subprocess
#CTRL Alt C
#Shif alt C 


class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'    
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        def disable(self):
            self.HEADER = ''
            self.OKBLUE = ''
            self.OKGREEN = ''
            self.WARNING    = ''
            self.FAIL = ''
            self.ENDC = ''
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

class InstaManager():
    def __init__(self) -> None:
        self.loader = instaloader.Instaloader()
        self.logged_in_status = False
        self.name = None
        self.target = None
        self.user = None
        self.all = False
    def login_using_session(self,name):
        try :
            self.name = name
            self.loader.load_session_from_file(name)
            self.logged_in_status = True
            return self.logged_in_status
        except Exception as e:
            print(e)
            return self.logged_in_status
    def login_using_email(self,name,password):
        try :
            self.loader.login(user=name,passwd=password)
            self.logged_in_status = True
            return self.logged_in_status
        except : 
            return self.logged_in_status
    def find_account(self):
        self.user = instaloader.Profile.from_username(HANDLER.loader.context,self.target)
    def download_posts(self):
        try :
            wall = self.user.get_posts()
            r = requests.get("https://www.instagram.com/{}/".format(self.target))
            s = BeautifulSoup(r.text, "html.parser")
            meta = s.find("meta", property ="og:description")
            s = meta.attrs['content']
            s = s.split("-")[0]
            s = s.split(" ")
            longueur = int(s[4])


            if longueur :
                i = 1
                for post in wall :
                    with Capturing() as text :
                        self.loader.download_post(post,self.user.username+"posts")
                    print(f"[{i}/{longueur}]     :    ",text[0])
                    i += 1
                #
                print(STRING_BREAK)
                coloring_text("Réussite !\n",bcolors.OKGREEN)
                #
                download("posts")
                return True
                
            else :
                print(STRING_BREAK)
                coloring_text("L'utilisateur n'a pas de posts!",bcolors.WARNING)
                if not self.all :
                    print("Appuyez sur entrer pour retourner à l'outil")
                    input()
                return True
        except Exception as e :
            return False
    def download_stories(self):
            boolean = self.user.has_viewable_story
            try:
                
                #print(profile)
                if  boolean:
                        # story is a Story object
                        self.loader.download_stories(userids=[self.user.userid])
                        path1 = os.getcwd()+"\\"+"：stories"
                        path2 = PATH +"\\"+"data"+"\\"+ self.user.username+"\\"+"stories"
                        if os.path.isdir(path1) :
                        #for ite in self.loader.download_stories(userids=[self.loader.check_profile_id(self.user.username)]):
                            # item is a StoryItem object
                            #    self.loader.download_storyitem(ite)
                            move_and_rename_files(path1,path2)
                            os.rmdir(path1)
                            print("Les photos/vidéos se trouvent dans : ",path2)
                            if not self.all :
                                open_folder(path2)
                                coloring_text("Appuyez sur une touche pour poursuivre",bcolors.BOLD)
                                input()
                            
                            
                        else :
                            boolean = False
                #        self.loader.download_storyitem(item, ':stories')
                if not boolean :
                        print(STRING_BREAK)
                        coloring_text("L'utilisateur n'a pas de storys!",bcolors.WARNING)
                        if not self.all :
                            print("Appuyez sur entrer pour retourner à l'outil")
                            input()
                return True
                #else :
                #    coloring_text("L'utilisateur n'a pas de story.",bcolors.BOLD)
                #    loop_text("Retour à l'outil dans ", 5,bcolors.HEADER )
                #    tools_PAGE1()
            except Exception as e :
                print(e)
                return False
    def download_highlights(self):
            boolean = self.user.has_highlight_reels
            try :
                if boolean :
                    for highlight in self.loader.get_highlights(user=self.user):
            # highlight is a Highlight object
                        for item in highlight.get_items():
                # item is a StoryItem object
                            self.loader.download_storyitem(item,highlight.owner_username+"highlights")
                    path1 = os.getcwd()+"\\"+self.user.username+"highlights"
                    if os.path.isdir(path1) :
                        download("highlights")
                        return True
                    else : 
                        boolean = False
                if not boolean :
                    print(STRING_BREAK)
                    coloring_text("L'utilisateur n'a pas de storys à la une. ",bcolors.HEADER )
                    if not self.all :
                        coloring_text("Appuyez sur une touche pour revenir à l'outil.", bcolors.BOLD)
                        input()
                    return True
            except Exception as e: 
                if not self.all :
                    input(str(e))
                return False
        
    def download_pdp(self):
        try :
            self.loader.download_profile(self.user.username, profile_pic_only = True)
            download(name="",secondname="Photo de profil")
            return True
        except Exception as e :
            if not self.all :
                input(str(e))
            return False    
    def see_not_subbed(self):
        try :
            print("cc les gars ca va")
            fllandflwees = {"n" : self.user.followers,"s": self.user.followees}
            abonnés = []
            abonnements = []

            print("En train de compter les Abonnés... \n")
            print(f"        Abonnés : [0/{fllandflwees['n']}]\r")
            progress = [0,0]
            for follower in self.user.get_followers():
                abonnés.append(follower.username)
                progress[0] = progress[0] + 1
                clearlastline()
                print(f"        Abonnés : [{progress[0]}/{fllandflwees['n']}]")
            clearlastline()
            print(f"        Abonnés : [{fllandflwees['n']}/{fllandflwees['n']}]")

            print("\n\n")

            print("En train de compter les Abonnements... \n")
            print(f"        Abonnements : [0/{fllandflwees['s']}]\r")

            for followed in self.user.get_followees():
                abonnements.append(followed.username)
                progress[1] = progress[1] + 1
                clearlastline()
                print(f"        Abonnements : [{progress[1]},{fllandflwees['s']}]\r")
            clearlastline()
            print(f"        Abonnements : [{fllandflwees['s']}/{fllandflwees['s']}]\r")

            lesnonfollowbacks = [x for x in abonnements if x not in abonnés]
            print(lesnonfollowbacks) 
            input()
            return True   
        except :
            return False
    def is_logged_in(self,func):
        if self.logged_in_status :
            return func()
        else :
            if not self.all :
                clear_screen()
            print("Il faut être connecté pour utiliser cette fonctionnalité.\nAppuyez sur n'importe quelle touche pour revenir à l'outil")
            if not self.all :
                input()
            return True
PATH  = os.getcwd()
HANDLER  = InstaManager()
PREMIER_ECRAN = ['--------------------------------------------------------------------\n', 'Insta-manager - 1.0.0 - https://github.com/MrMolian/insta-manager --\n', '--------------------------------------------------------------------\n', "⣿⣿⣿⣿⣿⠟⠋⠄⠄⠄⠄⠄⠄⠄⢁⠈⢻⢿⣿⣿⣿⣿⣿⣿⣿ | Merci d'utiliser la première version\n", '⣿⣿⣿⣿⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⡀⠭⢿⣿⣿⣿⣿ | de ce programme !\n', '⣿⣿⣿⣿⡟⠄⢀⣾⣿⣿⣿⣷⣶⣿⣷⣶⣶⡆⠄⠄⠄⣿⣿⣿⣿ |\n', "⣿⣿⣿⣿⡇⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠄⠄⢸⣿⣿⣿⣿ | En cas de bugs avec l'app, contactez\n", '⣿⣿⣿⣿⣇⣼⣿⣿⠿⠶⠙⣿⡟⠡⣴⣿⣽⣿⣧⠄⢸⣿⣿⣿⣿ | moi sur https://bit.ly/MrMolian\n', '⣿⣿⣿⣿⣿⣾⣿⣿⣟⣭⣾⣿⣷⣶⣶⣴⣶⣿⣿⢄⣿⣿⣿⣿⣿ |\n', '⣿⣿⣿⣿⣿⣿⣿⣿⡟⣩⣿⣿⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ |\n', '⣿⣿⣿⣿⣿⣿⣹⡋⠘⠷⣦⣀⣠⡶⠁⠈⠁⠄⣿⣿⣿⣿⣿⣿⣿ | Bonne utilisation :)\n', '⣿⣿⣿⣿⣿⣿⣍⠃⣴⣶⡔⠒⠄⣠⢀⠄⠄⠄⡨⣿⣿⣿⣿⣿⣿ |\n', '⣿⣿⣿⣿⣿⣿⣿⣦⡘⠿⣷⣿⠿⠟⠃⠄⠄⣠⡇⠈⠻⣿⣿⣿⣿ |\n', '⣿⣿⣿⣿⡿⠟⠋⢁⣷⣠⠄⠄⠄⠄⣀⣠⣾⡟⠄⠄⠄⠄⠉⠙⠻ |\n', '⡿⠟⠋⠁⠄⠄⠄⢸⣿⣿⡯⢓⣴⣾⣿⣿⡟⠄⠄⠄⠄⠄⠄⠄⠄ |\n', '⠄⠄⠄⠄⠄⠄⠄⣿⡟⣷⠄⠹⣿⣿⣿⡿⠁⠄⠄⠄⠄⠄⠄⠄⠄ |\n', '------------------------------------\n', 'Choisissez une des options ci-dessous :\n', '    [1] Se connecter via une session active (avec firefox seulement)\n', '    [2] Se connecter via email\n', "    [3] Utiliser l'outil sans se connecter\n","    [4] Quitter l'application"]
STRING_BREAK = "----------------------------------------------------------"
EMAIL_ECRAN = [""]
SESSION_ECRAN = [""]
MAINTOOL_ECRAN = ['--------------------------------------------------------------------\n', 'Insta-manager - 1.0.0 - https://github.com/MrMolian/insta-manager --\n', '--------------------------------------------------------------------\n', '⢿⣿⣿⣿⣭⠹⠛⠛⠛⢿⣿⣿⣿⣿⡿⣿⠷⠶⠿⢻⣿⣛⣦⣙⠻⣿    \n', '⣿⣿⢿⣿⠏⠀⠀⡀⠀⠈⣿⢛⣽⣜⠯⣽⠀⠀⠀⠀⠙⢿⣷⣻⡀⢿   Hola,              11/11/23\n', '⠐⠛⢿⣾⣖⣤⡀⠀⢀⡰⠿⢷⣶⣿⡇⠻⣖⣒⣒⣶⣿⣿⡟⢙⣶⣮ \n', '⣤⠀⠀⠛⠻⠗⠿⠿⣯⡆⣿⣛⣿⡿⠿⠮⡶⠼⠟⠙⠊⠁⠀⠸⢣⣿\n', '⣿⣷⡀⠀⠀⠀⠀⠠⠭⣍⡉⢩⣥⡤⠥⣤⡶⣒⠀⠀⠀⠀⠀⢰⣿⣿        How much for a kidney. \n', '⣿⣿⡽⡄⠀⠀⠀⢿⣿⣆⣿⣧⢡⣾⣿⡇⣾⣿⡇⠀⠀⠀⠀⣿⡇⠃         \n', '⣿⣿⣷⣻⣆⢄⠀⠈⠉⠉⠛⠛⠘⠛⠛⠛⠙⠛⠁⠀⠀⠀⠀⣿⡇⢸\n', '⢞⣿⣿⣷⣝⣷⣝⠦⡀⠀⠀⠀⠀⠀⠀⠀⡀⢀⠀⠀⠀⠀⠀⠛⣿⠈                 MrMolian.\n', '⣦⡑⠛⣟⢿⡿⣿⣷⣝⢧⡀⠀⠀⣶⣸⡇⣿⢸⣧⠀⠀⠀⠀⢸⡿⡆\n', '⣿⣿⣷⣮⣭⣍⡛⠻⢿⣷⠿⣶⣶⣬⣬⣁⣉⣀⣀⣁⡤⢴⣺⣾⣽⡇\n', '---------------------------------------------------------------------\n', 'Choisissez une des options ci-dessous :\n', '    [1] Choisir un utilisateur cible\n', "    [2] Retourner à l'accueil\n", "    [3] Quitter l'application\n"]
FONCTIONS_ECRAN = ['--------------------------------------------------------------------\n', 'Insta-manager - 1.0.0 - https://github.com/MrMolian/insta-manager --\n', '--------------------------------------------------------------------\n', '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n', '⠀⠀⠀⠀⣠⠞⠉⢉⠩⢍⡙⠛⠋⣉⠉⠍⢉⣉⣉⣉⠩⢉⠉⠛⠲⣄⠀⠀⠀⠀   \n', "⠀⠀⠀⡴⠁⠀⠂⡠⠑⠀⠀⠀⠂⠀⠀⠀⠀⠠⠀⠀⠐⠁⢊⠀⠄⠈⢦⠀⠀⠀J'ai vraiment aucune idée\n", "⠀⣠⡾⠁⠀⠀⠄⣴⡪⠽⣿⡓⢦⠀⠀⡀⠀⣠⢖⣻⣿⣒⣦⠀⡀⢀⣈⢦⡀⠀  d'illustrations à ajouter.\n", '⣰⠑⢰⠋⢩⡙⠒⠦⠖⠋⠀⠈⠁⠀⠀⠀⠀⠈⠉⠀⠘⠦⠤⠴⠒⡟⠲⡌⠛⣆\n', '⢹⡰⡸⠈⢻⣈⠓⡦⢤⣀⡀⢾⠩⠤⠀⠀⠤⠌⡳⠐⣒⣠⣤⠖⢋⡟⠒⡏⡄⡟\n', '⠀⠙⢆⠀⠀⠻⡙⡿⢦⣄⣹⠙⠒⢲⠦⠴⡖⠒⠚⣏⣁⣤⣾⢚⡝⠁⠀⣨⠞⠀\n', '⠀⠀⠈⢧⠀⠀⠙⢧⡀⠈⡟⠛⠷⡾⣶⣾⣷⠾⠛⢻⠉⢀⡽⠋⠀⠀⣰⠃⠀⠀\n', '⠀⠀⠀⠀⠑⢤⡠⢂⠌⡛⠦⠤⣄⣇⣀⣀⣸⣀⡤⠼⠚⡉⢄⠠⣠⠞⠁⠀⠀⠀\n', '⠀⠀⠀⠀⠀⠀⠉⠓⠮⣔⡁⠦⠀⣤⠤⠤⣤⠄⠰⠌⣂⡬⠖⠋⠀⠀⠀⠀⠀⠀    \n', '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠤⢤⣀⣀⡤⠴⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀     \n', '---------------------------------------------------------------------\n', 'Choisissez une des options ci-dessous :\n', '    [1] Télécharger les posts du compte\n', '    [2] Télécharger les storys actives du compte (requiert une connexion à Instagram)\n', '    [3] Télécharger les storys à la une du compte (requiert une connexion à Instagram)\n', '    [4] Télécharger la photo de profil du compte\n', '    [5] Télécharger tout par rapport au compte\n', '    -\n', '    [6] Poursuivre à la page 2\n', "    [7] Retourner à l'accueil\n", "    [8] Quitter l'application\n"]
PAGE2 = ['--------------------------------------------------------------------\n', 'Insta-manager - 1.0.0 - https://github.com/MrMolian/insta-manager --\n', '--------------------------------------------------------------------\n', '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n', '⠀⠀⠀⠀⣠⠞⠉⢉⠩⢍⡙⠛⠋⣉⠉⠍⢉⣉⣉⣉⠩⢉⠉⠛⠲⣄⠀⠀⠀⠀   \n', "⠀⠀⠀⡴⠁⠀⠂⡠⠑⠀⠀⠀⠂⠀⠀⠀⠀⠠⠀⠀⠐⠁⢊⠀⠄⠈⢦⠀⠀⠀J'ai vraiment aucune idée\n", "⠀⣠⡾⠁⠀⠀⠄⣴⡪⠽⣿⡓⢦⠀⠀⡀⠀⣠⢖⣻⣿⣒⣦⠀⡀⢀⣈⢦⡀⠀  d'illustrations à ajouter.\n", '⣰⠑⢰⠋⢩⡙⠒⠦⠖⠋⠀⠈⠁⠀⠀⠀⠀⠈⠉⠀⠘⠦⠤⠴⠒⡟⠲⡌⠛⣆\n', '⢹⡰⡸⠈⢻⣈⠓⡦⢤⣀⡀⢾⠩⠤⠀⠀⠤⠌⡳⠐⣒⣠⣤⠖⢋⡟⠒⡏⡄⡟\n', '⠀⠙⢆⠀⠀⠻⡙⡿⢦⣄⣹⠙⠒⢲⠦⠴⡖⠒⠚⣏⣁⣤⣾⢚⡝⠁⠀⣨⠞⠀\n', '⠀⠀⠈⢧⠀⠀⠙⢧⡀⠈⡟⠛⠷⡾⣶⣾⣷⠾⠛⢻⠉⢀⡽⠋⠀⠀⣰⠃⠀⠀\n', '⠀⠀⠀⠀⠑⢤⡠⢂⠌⡛⠦⠤⣄⣇⣀⣀⣸⣀⡤⠼⠚⡉⢄⠠⣠⠞⠁⠀⠀⠀\n', '⠀⠀⠀⠀⠀⠀⠉⠓⠮⣔⡁⠦⠀⣤⠤⠤⣤⠄⠰⠌⣂⡬⠖⠋⠀⠀⠀⠀⠀⠀    \n', '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠤⢤⣀⣀⡤⠴⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀     \n', '---------------------------------------------------------------------\n', 
         'Choisissez une des options ci-dessous :\n', '    [1] Vérifier les follows back\n', '    [2] Surveiller les abonnements/désabonnements (Ne fonctionne pas encore)\n', '    -\n', '    [3] Retourner à la page 1\n', "    [4] Retourner à l'accueil\n", "    [5] Quitter l'application"]
PAGE3 = []
def clear_screen():
    os.system("cls")
    return
def clearlastline(amount=1):
    for x in range(amount):
        sys.stdout.write("\033[F") 
        sys.stdout.write("\033[K")
    return 

def blockPrint():
    sys.stdout = open(os.devnull, 'w')
def enablePrint():
    sys.stdout = sys.__stdout__

def coloring_text(text :str, color: bcolors):
    print(color)
    clearlastline()
    print(text)
    print(bcolors.ENDC)
    clearlastline()
    return 
def loop_text(text :str ,loops : int, color : bcolors= None):
    if color : 
        print(color)
        clearlastline()
    print()
    for i in range(loops):
        clearlastline(1)
        print(text,loops-i)
        time.sleep(1)
    print(bcolors.ENDC)
    clearlastline()
    return
def create_session()-> str:
    from argparse import ArgumentParser
    from glob import glob
    from os.path import expanduser
    from platform import system
    from sqlite3 import OperationalError, connect

    try:
        from instaloader import ConnectionException, Instaloader
    except ModuleNotFoundError:
        raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")


    def get_cookiefile():
        default_cookiefile = {
            "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
            "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
        }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
        cookiefiles = glob(expanduser(default_cookiefile))
        if not cookiefiles:
            raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
        return cookiefiles[0]
        

    def import_session(cookiefile, sessionfile):
        print("Using cookies from {}.".format(cookiefile))
        conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
        try:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
            )
        except OperationalError:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
            )
        instaloader = Instaloader(max_connection_attempts=1)
        instaloader.context._session.cookies.update(cookie_data)
        username = instaloader.test_login()
        if not username:
            raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
        print("Imported session cookie for {}.".format(username))
        instaloader.context.username = username
        with Capturing() as output:
            instaloader.save_session_to_file(sessionfile)
        print(output[0])
        return username


    p = ArgumentParser()
    p.add_argument("-c", "--cookiefile")
    p.add_argument("-f", "--sessionfile")
    args = p.parse_args()
    try:
        username = import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
        return username
    except (ConnectionException, OperationalError) as e:
        raise SystemExit("Cookie import failed: {}".format(e))

def move_and_rename_files(src_folder, dest_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    # Get the file extension and counter
    counter = 1
    file_ext = None
    for filename in os.listdir(src_folder):
    # Get the full path of the source and destination files
        src_file = os.path.join(src_folder, filename)
        dest_file = os.path.join(dest_folder, str(counter))

        # If the current file is a directory, skip it
        if os.path.isdir(src_file):
            continue

        # Get the file extension
        file_ext = os.path.splitext(filename)[1]

        # If the destination file exists, append a number to its name
        while os.path.exists(dest_file + file_ext):
            counter += 1
            dest_file = os.path.join(dest_folder, str(counter))

        # Move and rename the file
        shutil.move(src_file, dest_file + file_ext)

    # Reset the counter and file extension for the next file
        counter = 1
        file_ext = None
def open_folder(folder_path):
    subprocess.Popen(f'explorer.exe "{folder_path}"')

def download(name,secondname = ""):
    path = os.getcwd()+"\\"+HANDLER.user.username+name
    path2 = PATH +"\\"+"data"+"\\"+HANDLER.user.username+"\\"+name+secondname
    move_and_rename_files(path,path2)
    os.rmdir(path)
    print("Les photos/vidéos se trouvent dans : ",path2)
    if not HANDLER.all :
        open_folder(path2)
        coloring_text("Appuyez sur une touche pour poursuivre",bcolors.BOLD)
        input()


#STEP 1 
def accueil():
    clear_screen()
    for line in PREMIER_ECRAN :
        print(line.strip())
    choix = input("Entrez le numéro de l'option choisie :\n")
    try :
        choix = choix.split()[0]
        if int(choix) == 1:
            connexion_via_session()
        elif int(choix) == 2:
            connexion_via_email()
        elif int(choix) == 3:
            maintool()
        elif int(choix) == 4:
            loop_text("Fermeture de cette fenêtre dans",3,bcolors.FAIL)
            sys.exit()
        else :
            print("Ce paramètre n'existe pas, réessayez.")
            time.sleep(1)
            accueil()
    
    except Exception as e:
        coloring_text("Erreur dans votre saisie, veuillez recommencer.",bcolors.FAIL)
        time.sleep(1)
        accueil()
#STEP 2 
def connexion_via_session():
    clear_screen()
    print(bcolors.BOLD,bcolors.OKCYAN)
    clearlastline()
    print("Récupération de la session Instagram Firefox...",bcolors.ENDC)
    print(STRING_BREAK)
    try : 
        name = create_session()
        print(STRING_BREAK)
        #print(bcolors.HEADER)
        #clearlastline()
        print("Tentative de connexion ...")
        blockPrint()
        if not HANDLER.login_using_session(name) :
            enablePrint()
            coloring_text("Il y a eu une erreur lors de la connexion, verifiez bien que vous êtes connecté à Instagram sur Firefox \nou essayez une autre méthode de connexion."
                          ,bcolors.FAIL)
            loop_text("Retour à l'accueil dans : ",3,bcolors.UNDERLINE)
            accueil()
        enablePrint()
        print("Réussite !")
        print(STRING_BREAK)
        loop_text("Vous allez poursuivre dans : ",3,bcolors.UNDERLINE)
        maintool()
    except Exception as e:
        print(STRING_BREAK)

        print("Il y a eu une erreur lors de l'importation, verifiez bien que vous êtes connecté à Instagram sur Firefox \nou essayez une autre méthode de connexion.")
        print("Logs Erreur : {}".format(e))
        input("Appuyez sur n'importe quelle touche pour retourner à l'acceuil.")
        accueil()
    return
def connexion_via_email():
    clear_screen()
    print(bcolors.BOLD,bcolors.OKCYAN)
    clearlastline()
    print("Connexion via pseudo et mot de passe...",bcolors.ENDC)
    print(STRING_BREAK)
    username = input("écrivez votre nom d'utilisateur :\n").strip()
    password = input("écrivez votre mot de passe :\n").strip()
    HANDLER.target = username
    print(STRING_BREAK)
    if not HANDLER.login_using_email(username,password) :
        try :
            #
            instaloader.Profile.from_username(HANDLER.loader.context,username)
            coloring_text("Le mot de passe est incorrect, veuillez réessayer.",bcolors.FAIL)
            print(STRING_BREAK)
            loop_text("Retour à l'accueil dans ",5,bcolors.HEADER)
            accueil()
        except :
            print(STRING_BREAK)
            coloring_text("Le compte n'existe pas, vérifiez que vous l'avez bien écrit.",bcolors.FAIL)
            print(STRING_BREAK)
            loop_text("Retour à l'accueil dans ",5,bcolors.HEADER)
            accueil()
    print("Réussite !")
    print(STRING_BREAK)
    loop_text("Vous allez poursuivre dans : ",3,bcolors.UNDERLINE)
    maintool()
#STEP 3 
def maintool():
    clear_screen()
    for line in MAINTOOL_ECRAN :
        print(line.strip())
    choix = input("Entrez le numéro de l'option choisie :\n")
    try :
        choix = choix.split()[0]
        if int(choix) == 1:
            locate_account()
        elif int(choix) == 2:
            accueil()
        elif int(choix) == 3:
            print(STRING_BREAK)
            loop_text("Fermeture de cette fenêtre dans",3,bcolors.FAIL)
            sys.exit()
        else :
            print("Ce paramètre n'existe pas, réessayez.")
            time.sleep(1)
            maintool()

    except Exception as e:
        coloring_text("Erreur dans votre saisie, veuillez recommencer.",bcolors.FAIL)
        time.sleep(1)
        maintool()
#STEP 4 
def locate_account():
    clear_screen()
    choix = input("Entrez le nom du compte à target :\n").strip()
    print(STRING_BREAK)
    try :
            HANDLER.target = choix
            HANDLER.find_account()
            tools_PAGE1()

    except :
            coloring_text("Le nom est incorrect, veuillez réessayer.",bcolors.FAIL)
            print(STRING_BREAK)
            loop_text("Retour à l'outil dans ",3,bcolors.HEADER)
            maintool()
#STEP 5 
def error_PAGE(index,value):
    if not value :
        coloring_text("Erreur lors de l'opération, merci de réessayer ou de me communiquer le bug",bcolors.FAIL)
        loop_text("Retour dans ",3,bcolors.BOLD)
    if index == 1 :
        tools_PAGE1()
    else : 
        tools_PAGE2()

def tools_PAGE1():
    clear_screen()
    for line in FONCTIONS_ECRAN :
        print(line.strip())
    choix = input("Entrez le numéro de l'option choisie :\n")
    try :
        choix = choix.split()[0]
        print(STRING_BREAK)
        if int(choix) == 1:
            error_PAGE(1,HANDLER.download_posts())
            # télécharger les posts  du compte
        if int(choix) == 2:
            error_PAGE(1,HANDLER.is_logged_in(HANDLER.download_stories))
            # storys actives du copte
        if int(choix) == 3:
            error_PAGE(1,HANDLER.is_logged_in(HANDLER.download_highlights))
            # storys à la une
        if int(choix) == 4:
            error_PAGE(1,HANDLER.download_pdp())
            # photo de profil
        elif int(choix) == 5:
            HANDLER.all = True
            actions = [HANDLER.download_posts,
                       lambda : HANDLER.is_logged_in(HANDLER.download_stories),
                       lambda : HANDLER.is_logged_in(HANDLER.download_highlights),
                       HANDLER.download_pdp]
            texte = ["TELECHARGEMENT DES POSTS",
                     "TELECHARGEMENT DES STORYS",
                     "TELECHARGEMENT DES STORYS A LA UNE",
                     "TELECHARGEMENT DE LA PHOTO DE PROFIL"]
            
            for i in range(len(actions)) :
                coloring_text(STRING_BREAK+"\n"+STRING_BREAK,bcolors.OKGREEN)
                print(f"{texte[i]}")
                coloring_text(STRING_BREAK+"\n"+STRING_BREAK,bcolors.OKGREEN)
                if not actions[i]():
                    print(f"La fonction {actions[i].__name__} a buté sur un problème")
            open_folder(PATH+"\\"+"data"+"\\"+HANDLER.user.username)
            HANDLER.all = False
            coloring_text("\nAppuyez sur entrer pour continuer...",bcolors.WARNING)
            input()
            tools_PAGE1()
        elif int(choix) == 6:
            tools_PAGE2()
        elif int(choix) == 7:
            accueil()
        elif int(choix) == 8:
            print(STRING_BREAK)
            loop_text("Fermeture de cette fenêtre dans",3,bcolors.FAIL)
            sys.exit()
        elif int(choix) not in range(1,7):
            print("Ce paramètre n'existe pas, réessayez.")
            time.sleep(1)
            tools_PAGE1()
    except Exception as e:
        print(e)
        coloring_text("Erreur dans votre saisie, veuillez recommencer.",bcolors.FAIL)
        time.sleep(1)
        tools_PAGE1()
def tools_PAGE2():   
    clear_screen()
    for line in PAGE2 :
        print(line.strip())
    choix = input("Entrez le numéro de l'option choisie :\n")
    try :
        choix = choix.split()[0]
        if int(choix) == 1:
            # storys actives du copt
            error_PAGE(2,HANDLER.is_logged_in(HANDLER.see_not_subbed))
        elif int(choix) == 2:
            #désabonnements abonnements
            error_PAGE(2,True)
        elif int(choix) == 3:
            tools_PAGE1()
        elif int(choix) == 4:
            accueil()
        elif int(choix) == 5:
            print(STRING_BREAK)
            loop_text("Fermeture de cette fenêtre dans",3,bcolors.FAIL)
            sys.exit()
        else :
            print("Ce paramètre n'existe pas, réessayez.")
            time.sleep(1)
            tools_PAGE2()

    except Exception as e:
        coloring_text("Erreur dans votre saisie, veuillez recommencer.",bcolors.FAIL)
        time.sleep(1)
        tools_PAGE2()
#-------------------------CONNEXION SESSION------------------------------
def main():
    accueil()
    return

if __name__ == "__main__" :
    main()
