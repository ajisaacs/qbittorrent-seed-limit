import qbittorrentapi
import time

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(
    host='192.168.10.100',
    port=8080,
    username='admin',
    password='adminadmin',
)

max_seeds = 25

def login():
    # the Client will automatically acquire/maintain a logged-in state
    # in line with any request. therefore, this is not strictly necessary; 
    # however, you may want to test the provided login credentials.
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    # display qBittorrent info
    print(f'qBittorrent: {qbt_client.app.version}')
    print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')
    # for k,v in qbt_client.app.build_info.items(): print(f'{k}: {v}')

def dostuff():
    for torrent in qbt_client.torrents.info.all():
        if torrent.state_enum.is_downloading:
            continue

        if torrent.num_complete > max_seeds:
            torrent.pause()
        else:
            torrent.resume()

def update_seed_count():
    qbt_client.torrents.resume.all()
    print('Waiting 30 seconds for seeds to update...')
    time.sleep(30)

login()
update_seed_count()
dostuff()