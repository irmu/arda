import time
import hashlib

from threading import Thread
from lib.acestream.object import Extendable
from lib.acestream.object import Observable

from lib.utils import logger

class Stats(Extendable, Observable):

  def __init__(self, server):
    Extendable.__init__(self)
    Observable.__init__(self)

    self.stat_url       = None
    self.status         = None
    self.peers          = 0
    self.speed_down     = 0
    self.speed_up       = 0
    self.downloaded     = 0
    self.uploaded       = 0
    self.progress       = 0
    self.total_progress = 0
    self.server         = server

  def watch(self, stat_url):
    self.stat_url = stat_url
    poller_thread = Thread(target=self._poll_stats)

    poller_thread.setDaemon(True)
    poller_thread.start()

  def stop(self):
    self.stat_url = None

  def update(self):
    response = self.server.get(self.stat_url)
    #logger(response.__dict__)
    self._set_response_to_values(response)

  def _set_response_to_values(self, response):
    if response.success:
      self._set_attrs_to_values(response.data)
      self.emit('updated')

  def _poll_stats(self):
    while self.stat_url:
      time.sleep(1)
      self.update()


class Stream(Extendable, Observable):

  def __init__(self, server, id=None, url=None, infohash=None):
    Extendable.__init__(self)
    Observable.__init__(self)

    self.filename            = None
    self.status              = None
    self.is_live             = None
    self.playback_session_id = None
    self.command_url         = None
    self.playback_url        = None
    self.stat_url            = None
    self.server              = server
    self.stats               = Stats(server)

    self._check_required_args(id=id, url=url, infohash=infohash)
    self._parse_stream_params(id=id, url=url, infohash=infohash)

  def start(self, hls=False, **kwargs):
    kwparams = dict(kwargs, **self.params) if hls else self.params
    response = self.server.getstream(pid=self.pid, hls=hls, **kwparams)

    if response.success:
      self._set_attrs_to_values(response.data)
      self._start_watchers()

      self.emit('started')

      try:
        response = self.server.getserver(method='get_media_files', api_version=3, infohash=self.infohash)

        if response.success:
          self.filename = response.data['files'][0]['filename']

        if not self.id:
          response = self.server.getserver(method='get_content_id', infohash=self.infohash)
          if response.success:
            self.id = response.data.get('content_id','')
      except: pass

    else:
      self.emit('error', response.message)

  def stop(self):
    response = self.server.get(self.command_url, method='stop')

    if response.success:
      self._stop_watchers()
      self.emit('stopped')
    else:
      self.emit('error', response.message)

  @property
  def params(self):
    params = { 'id': self.id, 'url': self.url, 'infohash': self.infohash }
    params = dict(filter(lambda item: item[1] is not None, params.items()))

    return params

  def _start_watchers(self):
    if self.stat_url:
      self.stats.watch(self.stat_url)
      self.stats.connect('updated', self._on_stats_update)

  def _stop_watchers(self):
    self.stats.stop()

  def _check_required_args(self, **kwargs):
    values = list(filter(None, kwargs.values()))
    params = "'id' or 'url' or 'infohash'"

    if not any(values):
      banner = '__init__() missing 1 required positional argument'
      raise TypeError('{0}: {1}'.format(banner, params))

    if len(values) > 1:
      banner = '__init__() too many positional arguments, provide only one of'
      raise TypeError('{0}: {1}'.format(banner, params))

  def _parse_stream_params(self, **kwargs):
    sid_args = list(filter(None, kwargs.values()))
    self.pid = hashlib.sha1(sid_args[0].encode('utf-8')).hexdigest()

    self._set_attrs_to_values(kwargs)

  def _on_stats_update(self, **kwargs):
    prev_status = self.status
    self.status = self.stats.status

    self.emit('stats::updated')

    if prev_status != self.status:
      self.emit('status::changed', self.status)

  def get_available_players(self):
    list_name = list()
    list_id = list()

    response = self.server.getserver(method='get_available_players',infohash=self.infohash)
    logger(response.__dict__)
    if response.success:
      for ply in response.data.get('players'):
        list_name.append(ply['name'])
        list_id.append(ply['id'])
    else:
      self.emit('error', response.message)

    return  list_name, list_id

  def open_in_player(self, player_id):
    response = self.server.getserver(method='open_in_player', player_id=player_id, infohash=self.infohash)
