#!/usr/bin/env python3
"""
REST API Uptime Monitor
========================
Monitors REST API endpoints defined in a YAML config file.
Logs response times, status codes, and sends console alerts on failure.

User Story: As a DevOps engineer, I want an automated API monitor
so that I am notified when endpoints go down or respond slowly.
"""

import time
import logging
import threading
import yaml
import requests
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s"
)
logger = logging.getLogger("api-monitor")


@dataclass
class EndpointConfig:
    name: str
    url: str
    method: str = "GET"
    expected_status: int = 200
    timeout_seconds: float = 5.0
    interval_seconds: int = 60
    headers: dict = field(default_factory=dict)
    alert_on_slow_ms: int = 2000


@dataclass
class CheckResult:
    endpoint: str
    url: str
    timestamp: str
    status_code: Optional[int]
    response_time_ms: float
    success: bool
    error: Optional[str] = None

    def __str__(self):
        status = "✅" if self.success else "❌"
        slow = " ⚠️ SLOW" if self.response_time_ms > 2000 else ""
        return (f"{status} [{self.endpoint}] {self.status_code} "
                f"| {self.response_time_ms:.0f}ms{slow}")


class EndpointChecker:
    """Performs a single health check on an endpoint."""

    def check(self, config: EndpointConfig) -> CheckResult:
        ts = datetime.utcnow().isoformat()
        start = time.monotonic()
        try:
            resp = requests.request(
                method=config.method,
                url=config.url,
                headers=config.headers,
                timeout=config.timeout_seconds,
                allow_redirects=True
            )
            elapsed_ms = (time.monotonic() - start) * 1000
            success = (resp.status_code == config.expected_status)
            return CheckResult(
                endpoint=config.name, url=config.url,
                timestamp=ts, status_code=resp.status_code,
                response_time_ms=elapsed_ms, success=success
            )
        except requests.exceptions.Timeout:
            elapsed_ms = (time.monotonic() - start) * 1000
            return CheckResult(
                endpoint=config.name, url=config.url,
                timestamp=ts, status_code=None,
                response_time_ms=elapsed_ms, success=False,
                error="Timeout"
            )
        except requests.exceptions.RequestException as e:
            elapsed_ms = (time.monotonic() - start) * 1000
            return CheckResult(
                endpoint=config.name, url=config.url,
                timestamp=ts, status_code=None,
                response_time_ms=elapsed_ms, success=False,
                error=str(e)
            )


class ConfigLoader:
    """Loads endpoint configuration from YAML."""

    def load(self, yaml_path: str) -> List[EndpointConfig]:
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        endpoints = []
        for ep in data.get("endpoints", []):
            endpoints.append(EndpointConfig(
                name=ep["name"],
                url=ep["url"],
                method=ep.get("method", "GET"),
                expected_status=ep.get("expected_status", 200),
                timeout_seconds=ep.get("timeout", 5.0),
                interval_seconds=ep.get("interval", 60),
                headers=ep.get("headers", {}),
                alert_on_slow_ms=ep.get("alert_on_slow_ms", 2000)
            ))
        return endpoints


class Monitor:
    """Orchestrates concurrent endpoint monitoring."""

    def __init__(self, configs: List[EndpointConfig]):
        self.configs = configs
        self.checker = EndpointChecker()
        self._stop_event = threading.Event()

    def _monitor_endpoint(self, config: EndpointConfig):
        while not self._stop_event.is_set():
            result = self.checker.check(config)
            logger.info(str(result))
            if not result.success:
                logger.error(f"🚨 ALERT: {config.name} is DOWN! "
                             f"Status={result.status_code}, Error={result.error}")
            elif result.response_time_ms > config.alert_on_slow_ms:
                logger.warning(f"⚠️  SLOW: {config.name} responded in "
                               f"{result.response_time_ms:.0f}ms")
            self._stop_event.wait(timeout=config.interval_seconds)

    def start(self):
        logger.info(f"🚀 Starting monitor for {len(self.configs)} endpoint(s)")
        threads = []
        for config in self.configs:
            t = threading.Thread(
                target=self._monitor_endpoint,
                args=(config,),
                daemon=True,
                name=f"monitor-{config.name}"
            )
            t.start()
            threads.append(t)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("⏹ Stopping monitor...")
            self._stop_event.set()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="REST API Uptime Monitor")
    parser.add_argument("--config", default="endpoints.yaml",
                        help="Path to YAML config file")
    args = parser.parse_args()

    loader = ConfigLoader()
    configs = loader.load(args.config)
    monitor = Monitor(configs)
    monitor.start()


if __name__ == "__main__":
    main()
