# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor

from ..compat import compat_urlparse
from ..utils import remove_end

urljoin = compat_urlparse.urljoin


class FunkIE(InfoExtractor):
    __DEFAULT_PARTNER_ID = "1985051"
    __SITE_BASE_URL = "http://funk.net"
    _VALID_URL = r'https?://(?:www\.)?funk.net/formate/(?P<format_id>[^/]+)/items/(?P<id>[^/]+)'
    _TEST = {
        'url':
        'https://www.funk.net/formate/57d979a6e4b0cceb1f32525b/items/5795f790e4b024998601b326',
        'md5': '713849b6f0d2ea3f7c8dde57e0e6a23e',
        'info_dict': {
            'id': '5795f790e4b024998601b326',
            'ext': 'mp4',
            'title':
            'Fl\xfcchtlinge: CASH-COWS der Security-Branche | HEADLINEZ',
            'upload_date': '20160725',
            'description': 'md5:086efbc3b84d348f9e7143dce4b5668d',
            'uploader_id': 'jan.lind@ard.de',
            'timestamp': 1469446028
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        title = self._html_search_regex(
            r'<title>(.+?)</title>', webpage, 'title', fatal=False)
        title = remove_end(title, " | funk")

        description = self._html_search_meta(
            "description", webpage, fatal=False)

        redirect_meta = self._html_search_meta("refresh", webpage, fatal=True)
        redirect_url_rel = self._search_regex(
            r"url=([^\s]+)", redirect_meta, "refresh_url_regex", fatal=True)

        redirect_url = urljoin(self.__SITE_BASE_URL, redirect_url_rel)

        redirect_page = self._download_webpage(redirect_url, "redirect_page")

        kaltura_vid_id = self._html_search_regex(
            r"renderPlayer\(.*%s.*,\s*'([^']+)'.*\)" % (video_id, ),
            redirect_page, "kaltura_vid_id")

        kaltura_partner_id = self._html_search_regex(
            r'cdnapisec\.kaltura\.com.*/partner_id/([^/,^"]+)',
            redirect_page,
            "kaltura_partner_id",
            default=self.__DEFAULT_PARTNER_ID)

        return {
            '_type': 'url_transparent',
            'url': 'kaltura:%s:%s' % (kaltura_partner_id, kaltura_vid_id),
            'ie_key': 'Kaltura',
            'title': title,
            'id': video_id,
            'description': description
        }
