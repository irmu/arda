from typing import Optional

class Link:
    address: Optional[str]
    headers: Optional[dict]
    is_widevine: Optional[bool]
    is_ffmpegdirect: Optional[bool]
    is_hls: Optional[bool]
    is_mpd: Optional[bool]
    is_ddl: Optional[bool]
    is_msready: Optional[bool]
    is_resolveurl: Optional[bool]
    license_url: Optional[str]
    manifest_type: Optional[str]
    is_links: Optional[bool]
    is_direct: Optional[bool]
    jetproxy: Optional[bool]
    jetpmpeg: Optional[bool]
    name: Optional[str]

    def __init__(
        self, 
        address: str = "",
        headers: Optional[dict] = {},
        is_widevine: Optional[bool] = False,
        is_ffmpegdirect: Optional[bool] = False,
        is_hls: Optional[bool] = False,
        is_mpd: Optional[bool] = False,
        is_ddl: Optional[bool] = False,
        is_msready: Optional[bool] = False,
        is_resolveurl: Optional[bool] = False,
        license_url: Optional[str] = None,
        manifest_type: Optional[str] = None,
        is_links: Optional[bool] = False,
        is_direct: Optional[bool] = False,
        jetproxy: Optional[bool] = False,
        jetpmpeg: Optional[bool] = False,
        name: Optional[str] = None
    ) -> None:
        self.address = address
        self.headers = headers
        self.is_widevine = is_widevine
        self.is_ffmpegdirect = is_ffmpegdirect
        self.is_hls = is_hls
        self.is_mpd = is_mpd
        self.is_ddl = is_ddl
        self.is_msready = is_msready
        self.is_resolveurl = is_resolveurl
        self.license_url = license_url
        self.manifest_type = manifest_type
        self.is_links = is_links
        self.is_direct = is_direct
        self.jetproxy = jetproxy
        self.jetpmpeg = jetpmpeg
        self.name = name

    def to_dict(self) -> dict:
        res = {
            "address": self.address,
            "headers": self.headers,
        }

        if self.is_widevine: res["is_widevine"] = self.is_widevine
        if self.is_ffmpegdirect: res["is_ffmpegdirect"] = self.is_ffmpegdirect
        if self.is_hls: res["is_hls"] = self.is_hls
        if self.is_mpd: res["is_mpd"] = self.is_mpd
        if self.is_ddl: res["is_ddl"] = self.is_ddl
        if self.is_msready: res["is_msready"] = self.is_msready
        if self.is_resolveurl: res["is_resolveurl"] = self.is_resolveurl
        if self.license_url: res["license_url"] = self.license_url
        if self.manifest_type: res["manifest_type"] = self.manifest_type
        if self.is_direct: res["is_direct"] = self.is_direct
        if self.is_links: res["is_links"] = self.is_links
        if self.jetproxy: res["jetproxy"] = self.jetproxy
        if self.jetpmpeg: res["jetpmpeg"] = self.jetpmpeg
        if self.name: res["name"] = self.name

        return res

    @staticmethod
    def from_dict(d: dict) -> "Link":
        address = d.get("address", "")
        headers = d.get("headers", {})
        is_widevine = d.get("is_widevine", False)
        is_ffmpegdirect = d.get("is_ffmpegdirect", False)
        is_hls = d.get("is_hls", False)
        is_mpd = d.get("is_mpd", False)
        is_ddl = d.get("is_ddl", False)
        is_msready = d.get("is_msready", False)
        is_resolveurl = d.get("is_resolveurl", False)
        license_url = d.get("license_url", None)
        manifest_type = d.get("manifest_type", None)
        is_links = d.get("is_links", False)
        is_direct = d.get("is_direct", False)
        jetproxy = d.get("jetproxy", False)
        jetpmpeg = d.get("jetpmpeg", False)
        name = d.get("name", None)
        return Link(address, headers, is_widevine, is_ffmpegdirect, is_hls, is_mpd, is_ddl, is_msready, is_resolveurl, license_url, manifest_type, is_links, is_direct, jetproxy, jetpmpeg, name)
    
    def __str__(self) -> str:
        return self.address
