from changedetectionio.pluggy_interface import resolve_watch_browser_connection_url


def _configure_extra_browser(
    datastore, name='custom browser URL', url='wss://custom-browser.example/ws'
):
    datastore.data['settings']['requests']['extra_browsers'] = [
        {'browser_name': name, 'browser_connection_url': url}
    ]
    return name, url


def test_browsersteps_uses_watch_extra_browser_over_env(client, monkeypatch):
    datastore = client.application.config.get('DATASTORE')
    browser_name, browser_url = _configure_extra_browser(datastore)
    monkeypatch.setenv('PLAYWRIGHT_DRIVER_URL', 'wss://env-browser.example/ws')

    uuid = datastore.add_watch(
        url='https://example.com',
        extras={'fetch_backend': f'extra_browser_{browser_name}', 'paused': True},
    )
    watch = datastore.data['watching'][uuid]

    assert resolve_watch_browser_connection_url(watch, datastore) == browser_url


def test_browsersteps_falls_back_to_env_url(client, monkeypatch):
    datastore = client.application.config.get('DATASTORE')
    monkeypatch.setenv('PLAYWRIGHT_DRIVER_URL', 'wss://env-browser.example/ws')

    uuid = datastore.add_watch(
        url='https://example.com',
        extras={'fetch_backend': 'html_webdriver', 'paused': True},
    )
    watch = datastore.data['watching'][uuid]

    assert resolve_watch_browser_connection_url(watch, datastore) == 'wss://env-browser.example/ws'
