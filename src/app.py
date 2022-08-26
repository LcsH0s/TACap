import pygraphviz as pgv
import matplotlib.pyplot as plt

from TwitterClient import TwitterClient

TEST_USERNAME = 'Luludc17'
TEST_FRIENDS = (['boulanger', 'ASUS_ROG_FR', 'SpottersMedia', 'KennyLeRetour', 'yungfilly1', 'Chunkz', 'tfadell', 'oneseconddrama', 'Lmfaoos', 'blczinedine', 'hourly_shitpost', 'heykahn', 'gaspardooo', 'maximebiaggi', 'winnterzuko', 'inesvarri', 'Crapauwer', '_Confessfantasm', 'LogitechGFrance', 'YassineTwt', 'ekWateur', 'MelHssn', 'itachi_rl', 'TopDesHagras', 'miakhalifa', 'Caedrel', 'MisterVonline', 'Eminem', 'Vandiril', '_IDVL', 'karmaaOfficiel', 'HxHVizuals', 'imdhav', 'ClmentBarbier3', 'VilebrequinAuto', 'Google', 'BBCWorld', 'NASA', 'SpaceX', 'JeffBezos', 'lolesports', 'FrMinecraft', 'elonmusk', 'c_bumstead', 'Marvel_Fit', 'AKG_Luffy', 'O_Robiii', 'PrimeTimeFUT', 'leroidesrats', 'LEC', 'Zack_Nani', 'Ricadam_lol', 'SKIDIDIPOPOFF', 'AlderiateTV', 'TrainerDouble', 'ghidraninja', 'EmirMalte', 'TeufeurSoff', 'Seb_Frit', 'AypierreMc', 'befreesh_', 'Chap_GG', 'Gotaga', 'LiveOverflow', 'KCORP_ULTRAS', 'Doigby', 'MaulCKX', 'RebeuDeter', 'PatrickAdemo', 'AmineMaTue', 'KametoTV', 'Cinkroflol', '113bumm', 'Domingo', 'Sardoche_Lol', 'LRB_LoL', 'TraYt0N', 'OTP_LoL', 'Karnagemvp', 'Xav_Oswald', 'Lockl34r', 'AREtoiles', 'CabochardLoL', 'KarmineCorp', 'Arkunir', 'Targamas', 'Kammeto', 'Twisted_Chips', 'kPeriods', 'Mickalow', 'Hanteralol', 'LEC_Wooloo', 'Saken_lol', 'RekklesLoL', 'JLMelenchon', 'GotagaTV', 'Bren_TM2', 'Fatiiiih_', 'ZeratoR', 'LoL_France', 'Striker_KC', 'Nuclear_int', 'KoteiZousa', 'LaureBuliiV', 'SamuelEtienne', 'Nisqy', 'EUMasters', 'Ilias__ll', 'Chrichribg', 'joedaou961', 'laura_bnvd'], [
                122333150, 493234748, 1152673482926370818, 1268888503577915392, 271594510, 546944457, 21576543, 1327615829668732928, 1370100517863571462, 1540895471085969410, 1370394029310017537, 1236801913179574282, 2574720804, 515697572, 1338608928666611713, 1511671705294585859, 1416421858564575233, 1222195059891875846, 960190681, 1506551148693622785, 4425309629, 404162009, 756842577983406085, 1248974437942210562, 2835653131, 3300282393, 25069929, 22940219, 1479983256, 1282423211880255493, 1027234681417347075, 1457871631460847618, 3331517595, 1171423546410598413, 858822768443498497, 20536157, 742143, 11348282, 34743251, 15506669, 614754689, 294864836, 44196397, 1395192591868731392, 925517804, 1525401989550596097, 1524876378155409414, 352604441, 570145241, 1076110847947300865, 463590027, 921679846513762304, 768533032806539264, 1112675460503269376, 850799848379101184, 1103634374103367680, 1318607455174144001, 2798855717, 421333672, 499087666, 2306126937, 377604735, 321388777, 3094698976, 1351997423372148736, 412659618, 1260898969472970753, 3390937060, 1229511182639390720, 755663732, 1083817714223927298, 734171294716076032, 1108779978223702016, 600903422, 898994539, 944283793, 700774256943038464, 1322466841978089472, 1925660413, 765259803929247744, 511273636, 3056720847, 2685541393, 1322196660232114177, 1708129158, 1042853304, 1043355650, 1410434772, 3300356219, 631669968, 2310116876, 1134862391181762560, 733849308689113088, 881827464, 80820758, 861124265000800257, 729257113407590400, 979437613168939008, 242263437, 2449561038])


tw = TwitterClient()
"""
tw.authenticate()

user = tw.get_user(TEST_USERNAME)
user.friends = tw.get_user_friends(user.name)
print(user.friends)

G = pgv.AGraph(strict=False, directed=True, splines="curved")
G.add_nodes_from(TEST_FRIENDS[0])

for f in TEST_FRIENDS[0]:
    G.add_edge(user.name, f)

G.edge_attr["color"] = "black"
G.node_attr["color"] = "blue"
G.node_attr["shape"] = "box"

G.draw("file.png", prog="circo")
"""
