from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ZABBIX_DATA_SOURCE = Path("/etc/grafana/provisioning/datasources/zabbix.yml")


@dataclass(frozen=True)
class Config:
    target: str
    zabbix_api_url: str
    zabbix_user: str
    zabbix_password: str
    host_identity_model: str = "global-ip"
    hop_group_name: str = "Transit / Hop"
    icmp_template_group: str = "Templates/Network devices"
    icmp_template_name: str = "ICMP Ping"
    map_prefix: str = "MTR ASN - "
    map_icon_name: str = "Cloud_(96)"
    map_icon_id: int = 5
    asn_lookup_mode: str = "online"
    asn_lookup_timeout_seconds: int = 5
    asn_cache_path: Path = ROOT_DIR / "data" / "cache" / "asn_company_cache.json"
    map_width: int = 2200
    map_height: int = 360
    icon_size: int = 96
    hop_spacing: int = 155
    left_margin: int = 40
    top_margin: int = 130


def _load_zabbix_datasource() -> dict[str, str]:
    if not DEFAULT_ZABBIX_DATA_SOURCE.exists():
        return {}
    data = yaml.safe_load(DEFAULT_ZABBIX_DATA_SOURCE.read_text()) or {}
    datasources = data.get("datasources") or []
    if not datasources:
        return {}
    ds = datasources[0]
    return {
        "zabbix_api_url": ds.get("url", ""),
        "zabbix_user": ds.get("jsonData", {}).get("username", ""),
        "zabbix_password": ds.get("secureJsonData", {}).get("password", ""),
    }


def load_config(target: str | None = None) -> Config:
    defaults = _load_zabbix_datasource()
    return Config(
        target=target or os.environ.get("POC_TARGET", "observabilidade.escossio.dev.br"),
        zabbix_api_url=os.environ.get("ZABBIX_API_URL", defaults.get("zabbix_api_url", "http://127.0.0.1:8081/api_jsonrpc.php")),
        zabbix_user=os.environ.get("ZABBIX_USER", defaults.get("zabbix_user", "Admin")),
        zabbix_password=os.environ.get("ZABBIX_PASSWORD", defaults.get("zabbix_password", "")),
        host_identity_model=os.environ.get("HOST_IDENTITY_MODEL", "global-ip"),
        hop_group_name=os.environ.get("HOP_GROUP_NAME", "Transit / Hop"),
        icmp_template_group=os.environ.get("ICMP_TEMPLATE_GROUP", "Templates/Network devices"),
        icmp_template_name=os.environ.get("ICMP_TEMPLATE_NAME", "ICMP Ping"),
        map_prefix=os.environ.get("MAP_PREFIX", "MTR ASN - "),
        map_icon_name=os.environ.get("MAP_ICON_NAME", "Cloud_(96)"),
        map_icon_id=int(os.environ.get("MAP_ICON_ID", "5")),
        asn_lookup_mode=os.environ.get("ASN_LOOKUP_MODE", "online"),
        asn_lookup_timeout_seconds=int(os.environ.get("ASN_LOOKUP_TIMEOUT_SECONDS", "5")),
        asn_cache_path=Path(os.environ.get("ASN_CACHE_PATH", str(ROOT_DIR / "data" / "cache" / "asn_company_cache.json"))),
    )
