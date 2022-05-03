import qbittorrentapi
import time
import datetime

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(
    host='192.168.10.100',
    port=8080,
    username='admin',
    password='adminadmin',
)

unlimited_seed_threshold = 25

def login():
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    print(f'qBittorrent: {qbt_client.app.version}')
    print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')

def set_ratio_limits():
    for torrent in qbt_client.torrents.info.all():
        if torrent.state_enum.is_downloading:
            continue

        # -2  =  use the global value
        # -1  =  no limit
        x = -2

        if torrent.num_complete <= unlimited_seed_threshold:
            x = -1

        if x == torrent.ratio_limit:
            continue

        torrent.set_share_limits(ratio_limit=x, seeding_time_limit=-2)
        torrent.resume()

        log(f'{torrent.name}: set ratio limit to \'{torrent.ratio_limit}\'')


logfile = open(r"C:\Tools\qbittorrent\log.txt", "a")

def log(msg):
    logfile.write(f'[{datetime.datetime.now()}]  {msg}\n')
    logfile.flush()
    print(msg)

login()
set_ratio_limits()
