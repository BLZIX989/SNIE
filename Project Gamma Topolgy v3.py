#!/usr/bin/env python3
"""
Project Gamma Infrastructure Intelligence Terminal

This module replaces the prior static reachability plot with a live, API-ready
Gamma engine that can power an interactive terminal UI.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from statistics import median
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
import json
import math
import os

try:
    import numpy as np
except Exception:  # pragma: no cover - optional dependency fallback
    np = None

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.responses import HTMLResponse, JSONResponse
except Exception:  # pragma: no cover - optional dependency fallback
    FastAPI = None
    HTTPException = Exception
    Query = None
    HTMLResponse = None
    JSONResponse = None


APP_TITLE = "Project Gamma Infrastructure Intelligence Terminal"
DATA_DIR = Path(__file__).resolve().parent
DEFAULT_PORT = int(os.getenv("PORT", "8000"))


def _year_from_timestamp(timestamp: str) -> int:
    try:
        return datetime.fromisoformat(timestamp).year
    except ValueError:
        return int(str(timestamp)[:4])


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _round(value: float, digits: int = 1) -> float:
    return round(float(value), digits)


@dataclass
class GammaSnapshot:
    ticker: str
    name: str
    sector: str
    necessity: float
    gamma_1: float
    gamma_2: float
    invariance: float
    systemic_score: float = 0.0
    classification: str = "Platform"
    lifecycle_state: str = "Stable Regime"
    thesis_status: str = "Supported"
    timestamp: str = "2026-06-11"
    supporting_signals: List[str] = field(default_factory=list)
    contradictory_signals: List[str] = field(default_factory=list)

    @property
    def year(self) -> int:
        return _year_from_timestamp(self.timestamp)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["year"] = self.year
        return payload


@dataclass
class GammaEntityView:
    snapshot: GammaSnapshot
    x: float
    y: float
    size: float
    border: str
    fill: str
    zone: str
    composite_gamma: float
    structural_gravity: float
    thesis_health: float

    def to_dict(self) -> Dict[str, Any]:
        payload = self.snapshot.to_dict()
        payload.update(
            {
                "x": _round(self.x),
                "y": _round(self.y),
                "size": _round(self.size),
                "border": self.border,
                "fill": self.fill,
                "zone": self.zone,
                "composite_gamma": _round(self.composite_gamma),
                "structural_gravity": _round(self.structural_gravity),
                "thesis_health": _round(self.thesis_health),
            }
        )
        return payload


class GammaEngine:
    def __init__(self, seed_snapshots: Optional[Sequence[Dict[str, Any]]] = None) -> None:
        self.snapshots: List[GammaSnapshot] = []
        self.watchlists: Dict[str, List[str]] = {
            "Core Infrastructure": ["NVDA", "ASML", "META", "AAPL"],
            "Expansion Frontier": ["OPENA", "STRIP"],
        }
        self.layouts: Dict[str, Dict[str, Any]] = {}
        self.dependency_edges: List[Dict[str, Any]] = []
        self._load_seed_data(seed_snapshots or self._default_seed_rows())
        self._build_dependency_graph()

    def _default_seed_rows(self) -> List[Dict[str, Any]]:
        return [
            {"ticker": "NVDA", "name": "NVIDIA", "sector": "Semiconductors", "necessity": 48.0, "gamma_1": 58.0, "gamma_2": 32.0, "invariance": 61.0, "systemic_score": 51.0, "classification": "Platform", "lifecycle_state": "Expansion State", "thesis_status": "Supported", "timestamp": "2015-01-01"},
            {"ticker": "NVDA", "name": "NVIDIA", "sector": "Semiconductors", "necessity": 55.0, "gamma_1": 67.0, "gamma_2": 40.0, "invariance": 71.0, "systemic_score": 60.0, "classification": "Platform", "lifecycle_state": "Expansion State", "thesis_status": "Supported", "timestamp": "2018-01-01"},
            {"ticker": "NVDA", "name": "NVIDIA", "sector": "Semiconductors", "necessity": 63.5, "gamma_1": 81.0, "gamma_2": 49.0, "invariance": 84.0, "systemic_score": 71.0, "classification": "Substrate", "lifecycle_state": "Expansion State", "thesis_status": "Supported", "timestamp": "2021-01-01"},
            {"ticker": "NVDA", "name": "NVIDIA", "sector": "Semiconductors", "necessity": 69.4, "gamma_1": 97.6, "gamma_2": 54.7, "invariance": 95.9, "systemic_score": 72.8, "classification": "Substrate", "lifecycle_state": "Expansion State", "thesis_status": "Intact", "timestamp": "2026-06-11"},
            {"ticker": "NVDA", "name": "NVIDIA", "sector": "Semiconductors", "necessity": 74.5, "gamma_1": 99.0, "gamma_2": 63.0, "invariance": 96.8, "systemic_score": 82.0, "classification": "Substrate", "lifecycle_state": "Frontier State", "thesis_status": "Supported", "timestamp": "2030-01-01"},
            {"ticker": "ASML", "name": "ASML", "sector": "Semiconductor Equipment", "necessity": 69.0, "gamma_1": 84.0, "gamma_2": 28.0, "invariance": 89.0, "systemic_score": 66.0, "classification": "Bottleneck", "lifecycle_state": "Stable Regime", "thesis_status": "Supported", "timestamp": "2015-01-01"},
            {"ticker": "ASML", "name": "ASML", "sector": "Semiconductor Equipment", "necessity": 70.5, "gamma_1": 86.0, "gamma_2": 29.0, "invariance": 90.0, "systemic_score": 68.0, "classification": "Bottleneck", "lifecycle_state": "Stable Regime", "thesis_status": "Supported", "timestamp": "2018-01-01"},
            {"ticker": "ASML", "name": "ASML", "sector": "Semiconductor Equipment", "necessity": 71.2, "gamma_1": 87.5, "gamma_2": 29.5, "invariance": 91.0, "systemic_score": 69.0, "classification": "Bottleneck", "lifecycle_state": "Stable Regime", "thesis_status": "Supported", "timestamp": "2021-01-01"},
            {"ticker": "ASML", "name": "ASML", "sector": "Semiconductor Equipment", "necessity": 72.2, "gamma_1": 88.1, "gamma_2": 29.5, "invariance": 91.3, "systemic_score": 71.0, "classification": "Bottleneck", "lifecycle_state": "Stable Regime", "thesis_status": "Supported", "timestamp": "2026-06-11"},
            {"ticker": "ASML", "name": "ASML", "sector": "Semiconductor Equipment", "necessity": 73.0, "gamma_1": 88.4, "gamma_2": 30.0, "invariance": 92.0, "systemic_score": 72.0, "classification": "Bottleneck", "lifecycle_state": "Stable Regime", "thesis_status": "Supported", "timestamp": "2030-01-01"},
            {"ticker": "OPENA", "name": "OpenAI", "sector": "AI Infrastructure", "necessity": 42.0, "gamma_1": 54.0, "gamma_2": 88.0, "invariance": 45.0, "systemic_score": 49.0, "classification": "Frontier", "lifecycle_state": "Frontier State", "thesis_status": "Supported", "timestamp": "2015-01-01"},
            {"ticker": "OPENA", "name": "OpenAI", "sector": "AI Infrastructure", "necessity": 50.0, "gamma_1": 62.0, "gamma_2": 82.0, "invariance": 55.0, "systemic_score": 58.0, "classification": "Frontier", "lifecycle_state": "Frontier State", "thesis_status": "Supported", "timestamp": "2018-01-01"},
            {"ticker": "OPENA", "name": "OpenAI", "sector": "AI Infrastructure", "necessity": 62.0, "gamma_1": 72.0, "gamma_2": 74.0, "invariance": 68.0, "systemic_score": 69.0, "classification": "Platform", "lifecycle_state": "Expansion State", "thesis_status": "Supported", "timestamp": "2021-01-01"},
            {"ticker": "OPENA", "name": "OpenAI", "sector": "AI Infrastructure", "necessity": 64.9, "gamma_1": 71.5, "gamma_2": 89.2, "invariance": 62.4, "systemic_score": 76.2, "classification": "Frontier", "lifecycle_state": "Frontier State", "thesis_status": "Supported", "timestamp": "2026-06-11"},
            {"ticker": "OPENA", "name": "OpenAI", "sector": "AI Infrastructure", "necessity": 79.0, "gamma_1": 88.0, "gamma_2": 61.0, "invariance": 82.0, "systemic_score": 84.0, "classification": "Substrate", "lifecycle_state": "Substrate State", "thesis_status": "Intact", "timestamp": "2030-01-01"},
            {"ticker": "META", "name": "Meta", "sector": "Internet Platforms", "necessity": 46.1, "gamma_1": 60.2, "gamma_2": 71.4, "invariance": 54.0, "systemic_score": 59.3, "classification": "Platform", "lifecycle_state": "Frontier State", "thesis_status": "Under Stress", "timestamp": "2026-06-11"},
            {"ticker": "AAPL", "name": "Apple", "sector": "Consumer Electronics", "necessity": 83.2, "gamma_1": 79.5, "gamma_2": 20.1, "invariance": 96.7, "systemic_score": 78.8, "classification": "Substrate", "lifecycle_state": "Stable Regime", "thesis_status": "Intact", "timestamp": "2026-06-11"},
            {"ticker": "STRIP", "name": "Stripe", "sector": "Payments", "necessity": 52.4, "gamma_1": 67.9, "gamma_2": 78.4, "invariance": 57.2, "systemic_score": 63.6, "classification": "Platform", "lifecycle_state": "Expansion State", "thesis_status": "Supported", "timestamp": "2026-06-11"},
            {"ticker": "LINUX", "name": "Linux Base", "sector": "Operating Systems", "necessity": 92.0, "gamma_1": 97.0, "gamma_2": 10.0, "invariance": 99.0, "systemic_score": 88.4, "classification": "Substrate", "lifecycle_state": "Substrate State", "thesis_status": "Intact", "timestamp": "2026-06-11"},
        ]

    def _load_seed_data(self, rows: Sequence[Dict[str, Any]]) -> None:
        for row in rows:
            self.ingest_snapshot(row)

    def ingest_snapshot(self, raw: Dict[str, Any]) -> GammaSnapshot:
        snapshot = GammaSnapshot(
            ticker=str(raw["ticker"]).upper(),
            name=str(raw.get("name", raw["ticker"])),
            sector=str(raw.get("sector", "Unknown")),
            necessity=_clamp(float(raw.get("necessity", 0.0))),
            gamma_1=_clamp(float(raw.get("gamma_1", 0.0))),
            gamma_2=_clamp(float(raw.get("gamma_2", 0.0))),
            invariance=_clamp(float(raw.get("invariance", 0.0))),
            systemic_score=_clamp(float(raw.get("systemic_score", 0.0))),
            classification=str(raw.get("classification") or ""),
            lifecycle_state=str(raw.get("lifecycle_state") or ""),
            thesis_status=str(raw.get("thesis_status") or ""),
            timestamp=str(raw.get("timestamp", "2026-06-11")),
            supporting_signals=list(raw.get("supporting_signals", [])),
            contradictory_signals=list(raw.get("contradictory_signals", [])),
        )

        snapshot.systemic_score = self.compute_systemic_score(snapshot)
        snapshot.classification = snapshot.classification or self.classify(snapshot)
        snapshot.lifecycle_state = snapshot.lifecycle_state or self.resolve_lifecycle(snapshot)
        snapshot.thesis_status = snapshot.thesis_status or self.resolve_thesis_status(snapshot)

        self.snapshots.append(snapshot)
        return snapshot

    def compute_structural_gravity(self, snapshot: GammaSnapshot) -> float:
        return _clamp(0.43 * snapshot.necessity + 0.37 * snapshot.gamma_1 + 0.20 * snapshot.invariance)

    def compute_composite_gamma(self, snapshot: GammaSnapshot) -> float:
        gravity = self.compute_structural_gravity(snapshot)
        return _clamp(0.35 * gravity + 0.25 * snapshot.gamma_2 + 0.20 * snapshot.invariance + 0.20 * snapshot.systemic_score)

    def compute_systemic_score(self, snapshot: GammaSnapshot) -> float:
        return _clamp(0.30 * snapshot.necessity + 0.30 * snapshot.gamma_1 + 0.20 * snapshot.gamma_2 + 0.20 * snapshot.invariance)

    def classify(self, snapshot: GammaSnapshot) -> str:
        gravity = self.compute_structural_gravity(snapshot)
        if snapshot.gamma_2 >= 75 and gravity < 55:
            return "Frontier"
        if snapshot.necessity >= 75 and snapshot.gamma_1 >= 75 and snapshot.invariance >= 75:
            return "Substrate"
        if snapshot.gamma_1 >= 70 and snapshot.gamma_2 <= 45:
            return "Bottleneck"
        if snapshot.gamma_2 >= 65 and snapshot.gamma_1 >= 55:
            return "Platform"
        return "Extractor"

    def resolve_lifecycle(self, snapshot: GammaSnapshot) -> str:
        gravity = self.compute_structural_gravity(snapshot)
        if snapshot.gamma_2 >= 75 and gravity >= 55:
            return "Expansion State"
        if gravity >= 75 and snapshot.gamma_2 <= 35:
            return "Substrate State"
        if gravity >= 55 and snapshot.gamma_2 <= 55:
            return "Stable Regime"
        if snapshot.gamma_2 >= 70 and gravity < 55:
            return "Frontier State"
        return "Extraction Spiral"

    def resolve_thesis_status(self, snapshot: GammaSnapshot) -> str:
        score = self.compute_thesis_health(snapshot)
        if score >= 80:
            return "Intact"
        if score >= 65:
            return "Supported"
        if score >= 45:
            return "Under Stress"
        return "Invalidated"

    def compute_thesis_health(self, snapshot: GammaSnapshot) -> float:
        support = 0.45 * snapshot.invariance + 0.35 * snapshot.necessity + 0.20 * snapshot.gamma_1
        contradiction = 0.30 * max(0.0, 100.0 - snapshot.gamma_2)
        return _clamp(support - 0.35 * contradiction)

    def active_snapshots(self, year: Optional[int] = None) -> List[GammaSnapshot]:
        if year is None:
            latest_by_ticker: Dict[str, GammaSnapshot] = {}
            for snapshot in sorted(self.snapshots, key=lambda item: (item.ticker, item.year, item.timestamp)):
                latest_by_ticker[snapshot.ticker] = snapshot
            return list(latest_by_ticker.values())

        snapshots_by_ticker: Dict[str, List[GammaSnapshot]] = {}
        for snapshot in sorted(self.snapshots, key=lambda item: (item.ticker, item.year, item.timestamp)):
            if snapshot.year <= year:
                snapshots_by_ticker.setdefault(snapshot.ticker, []).append(snapshot)

        resolved = [history[-1] for history in snapshots_by_ticker.values() if history]
        if resolved:
            return resolved
        return []

    def _zone_thresholds(self, snapshots: Sequence[GammaSnapshot]) -> Tuple[float, float, float, float]:
        xs = [snapshot.gamma_2 for snapshot in snapshots]
        ys = [self.compute_structural_gravity(snapshot) for snapshot in snapshots]
        if len(xs) < 4:
            return 50.0, 65.0, 35.0, 55.0
        xs_sorted = sorted(xs)
        ys_sorted = sorted(ys)
        q1_x, q3_x = xs_sorted[len(xs_sorted) // 4], xs_sorted[(3 * len(xs_sorted)) // 4]
        q1_y, q3_y = ys_sorted[len(ys_sorted) // 4], ys_sorted[(3 * len(ys_sorted)) // 4]
        return q1_x, q3_x, q1_y, q3_y

    def zone_for(self, snapshot: GammaSnapshot, snapshots: Sequence[GammaSnapshot]) -> str:
        x_low, x_high, y_low, y_high = self._zone_thresholds(snapshots)
        x = snapshot.gamma_2
        y = self.compute_structural_gravity(snapshot)
        if x >= x_high and y >= y_high:
            return "Substrate Core"
        if x <= x_low and y >= y_high:
            return "Legacy Anchors"
        if x >= x_high and y <= y_low:
            return "Expansion Frontier"
        if x <= x_low and y <= y_low:
            return "Extraction Endpoints"
        return "Competitive Basin"

    def active_views(self, year: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> List[GammaEntityView]:
        filters = filters or {}
        views: List[GammaEntityView] = []
        snapshots = self.active_snapshots(year)
        for snapshot in snapshots:
            if filters.get("sector") and snapshot.sector != filters["sector"]:
                continue
            if filters.get("classification") and snapshot.classification != filters["classification"]:
                continue
            if filters.get("lifecycle_state") and snapshot.lifecycle_state != filters["lifecycle_state"]:
                continue
            if filters.get("ticker") and snapshot.ticker != str(filters["ticker"]).upper():
                continue

            structural_gravity = self.compute_structural_gravity(snapshot)
            composite_gamma = self.compute_composite_gamma(snapshot)
            thesis_health = self.compute_thesis_health(snapshot)
            zone = self.zone_for(snapshot, snapshots)
            views.append(
                GammaEntityView(
                    snapshot=snapshot,
                    x=snapshot.gamma_2,
                    y=structural_gravity,
                    size=20.0 + 0.55 * composite_gamma,
                    border=snapshot.classification,
                    fill=snapshot.lifecycle_state,
                    zone=zone,
                    composite_gamma=composite_gamma,
                    structural_gravity=structural_gravity,
                    thesis_health=thesis_health,
                )
            )
        return views

    def company_detail(self, ticker: str) -> Dict[str, Any]:
        ticker = ticker.upper()
        history = [snapshot for snapshot in self.snapshots if snapshot.ticker == ticker]
        if not history:
            raise KeyError(ticker)
        latest = sorted(history, key=lambda item: (item.year, item.timestamp))[-1]
        return {
            "latest": self._snapshot_detail(latest),
            "history": [self._snapshot_detail(snapshot) for snapshot in sorted(history, key=lambda item: (item.year, item.timestamp))],
            "trajectory": self.trajectory(ticker),
            "thesis": self.thesis_tracker(ticker),
            "invariants": self.invariant_profile(ticker),
            "lifecycle": self.lifecycle_observatory(ticker),
            "dependency_network": self.dependency_network(ticker),
            "validation": self.validation_report(ticker),
        }

    def _snapshot_detail(self, snapshot: GammaSnapshot) -> Dict[str, Any]:
        gravity = self.compute_structural_gravity(snapshot)
        composite = self.compute_composite_gamma(snapshot)
        thesis = self.compute_thesis_health(snapshot)
        return {
            **snapshot.to_dict(),
            "x": _round(snapshot.gamma_2),
            "y": _round(gravity),
            "composite_gamma": _round(composite),
            "structural_gravity": _round(gravity),
            "thesis_health": _round(thesis),
            "zone": self.zone_for(snapshot, self.active_snapshots(snapshot.year)),
            "signals": {
                "supporting": snapshot.supporting_signals or self._supporting_signals(snapshot),
                "contradictory": snapshot.contradictory_signals or self._contradictory_signals(snapshot),
            },
        }

    def _supporting_signals(self, snapshot: GammaSnapshot) -> List[str]:
        signals = []
        if snapshot.invariance >= 80:
            signals.append("High invariance across regime cycles")
        if snapshot.necessity >= 70:
            signals.append("Structural necessity remains elevated")
        if snapshot.gamma_1 >= 70:
            signals.append("Dependency density is concentrated")
        if snapshot.gamma_2 >= 65:
            signals.append("Reachability expansion continues")
        return signals or ["Baseline operating profile remains coherent"]

    def _contradictory_signals(self, snapshot: GammaSnapshot) -> List[str]:
        signals = []
        if snapshot.gamma_2 <= 40:
            signals.append("Reachability expansion is constrained")
        if snapshot.invariance <= 50:
            signals.append("Regime stability is vulnerable")
        if snapshot.necessity <= 45:
            signals.append("Non-substitutability is weakening")
        return signals or ["No dominant contradictions detected"]

    def trajectory(self, ticker: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        ticker = ticker.upper()
        history = sorted([snapshot for snapshot in self.snapshots if snapshot.ticker == ticker and (year is None or snapshot.year <= year)], key=lambda item: item.year)
        return [
            {
                "year": snapshot.year,
                "timestamp": snapshot.timestamp,
                "x": _round(snapshot.gamma_2),
                "y": _round(self.compute_structural_gravity(snapshot)),
                "composite_gamma": _round(self.compute_composite_gamma(snapshot)),
                "lifecycle_state": snapshot.lifecycle_state,
                "thesis_status": snapshot.thesis_status,
            }
            for snapshot in history
        ]

    def thesis_tracker(self, ticker: str, year: Optional[int] = None) -> Dict[str, Any]:
        ticker = ticker.upper()
        history = sorted([snapshot for snapshot in self.snapshots if snapshot.ticker == ticker and (year is None or snapshot.year <= year)], key=lambda item: item.year)
        if not history:
            raise KeyError(ticker)
        records = []
        for snapshot in history:
            records.append(
                {
                    "year": snapshot.year,
                    "status": snapshot.thesis_status,
                    "health_score": _round(self.compute_thesis_health(snapshot)),
                    "supporting_signals": snapshot.supporting_signals or self._supporting_signals(snapshot),
                    "contradictory_signals": snapshot.contradictory_signals or self._contradictory_signals(snapshot),
                }
            )
        return {
            "current_thesis": f"{history[-1].name} remains a {history[-1].classification.lower()} with {history[-1].lifecycle_state.lower()} characteristics.",
            "current_status": history[-1].thesis_status,
            "current_health": _round(self.compute_thesis_health(history[-1])),
            "records": records,
        }

    def reachability_field(self, ticker: Optional[str] = None) -> Dict[str, Any]:
        snapshots = self.active_snapshots()
        if ticker:
            snapshots = [snapshot for snapshot in snapshots if snapshot.ticker == ticker.upper()]
        if not snapshots:
            return {"cones": [], "vectors": []}

        cones = []
        vectors = []
        for snapshot in snapshots:
            gravity = self.compute_structural_gravity(snapshot)
            cone_strength = _clamp(snapshot.gamma_2 * 1.1 + snapshot.invariance * 0.2)
            cones.append(
                {
                    "ticker": snapshot.ticker,
                    "origin": [_round(snapshot.gamma_2), _round(gravity)],
                    "aperture": _round(10.0 + (100.0 - snapshot.invariance) * 0.25),
                    "reachability": _round(cone_strength),
                    "zone": self.zone_for(snapshot, snapshots),
                }
            )
            vectors.append(
                {
                    "ticker": snapshot.ticker,
                    "from": [_round(snapshot.gamma_2), _round(gravity)],
                    "to": [_round(_clamp(snapshot.gamma_2 + 10.0 + snapshot.gamma_2 * 0.15)), _round(_clamp(gravity + 7.0 + snapshot.necessity * 0.08))],
                    "magnitude": _round(snapshot.gamma_2 * 0.8 + snapshot.gamma_1 * 0.2),
                }
            )
        return {"cones": cones, "vectors": vectors}

    def attractor_field(self, year: Optional[int] = None, grid_size: int = 36) -> Dict[str, Any]:
        views = self.active_views(year)
        xs = [view.x for view in views]
        ys = [view.y for view in views]
        if not xs or not ys:
            return {"x": [], "y": [], "z": []}

        x_min, x_max = min(xs) - 10.0, max(xs) + 10.0
        y_min, y_max = min(ys) - 10.0, max(ys) + 10.0
        x_axis = [x_min + i * (x_max - x_min) / (grid_size - 1) for i in range(grid_size)]
        y_axis = [y_min + i * (y_max - y_min) / (grid_size - 1) for i in range(grid_size)]
        field: List[List[float]] = []

        for y in y_axis:
            row = []
            for x in x_axis:
                potential = 0.0
                for view in views:
                    dx = x - view.x
                    dy = y - view.y
                    sigma = 12.0 + (100.0 - view.thesis_health) * 0.12
                    weight = 1.0 + view.composite_gamma / 100.0
                    potential += weight * math.exp(-((dx * dx + dy * dy) / (2.0 * sigma * sigma)))
                row.append(_round(potential, 4))
            field.append(row)

        return {"x": [_round(value, 3) for value in x_axis], "y": [_round(value, 3) for value in y_axis], "z": field}

    def dependency_network(self, ticker: Optional[str] = None) -> Dict[str, Any]:
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []
        active = self.active_snapshots()
        if ticker:
            active = [snapshot for snapshot in active if snapshot.ticker == ticker.upper()]
        ticker_set = {snapshot.ticker for snapshot in active}
        for snapshot in active:
            degree = sum(1 for edge in self.dependency_edges if edge["source"] == snapshot.ticker or edge["target"] == snapshot.ticker)
            nodes.append(
                {
                    "id": snapshot.ticker,
                    "label": snapshot.name,
                    "type": "company",
                    "sector": snapshot.sector,
                    "centrality": _round(0.5 + degree * 0.2 + snapshot.gamma_1 / 100.0),
                    "criticality": _round(snapshot.necessity * 0.6 + snapshot.invariance * 0.4),
                    "systemic_leverage": _round(snapshot.gamma_2 * 0.5 + snapshot.gamma_1 * 0.5),
                }
            )

        for edge in self.dependency_edges:
            if ticker and edge["source"] not in ticker_set and edge["target"] not in ticker_set:
                continue
            edges.append(edge)

        return {"nodes": nodes, "edges": edges}

    def validation_report(self, ticker: Optional[str] = None, year: Optional[int] = None) -> Dict[str, Any]:
        active = self.active_snapshots(year)
        if ticker:
            active = [snapshot for snapshot in active if snapshot.ticker == ticker.upper()]
        rows = []
        for snapshot in active:
            health = self.compute_thesis_health(snapshot)
            hit_rate = _clamp(health * 0.88)
            false_positive = _clamp(100.0 - hit_rate - snapshot.gamma_2 * 0.08)
            false_negative = _clamp(100.0 - hit_rate - snapshot.invariance * 0.05)
            rows.append(
                {
                    "ticker": snapshot.ticker,
                    "year": snapshot.year,
                    "blind_test_rank": _round(100.0 - false_positive),
                    "hit_rate": _round(hit_rate),
                    "false_positive": _round(false_positive),
                    "false_negative": _round(false_negative),
                    "prediction": snapshot.lifecycle_state,
                    "result": "Passed" if hit_rate >= 60 else "Review",
                }
            )
        return {"rows": rows}

    def invariant_profile(self, ticker: str, year: Optional[int] = None) -> Dict[str, Any]:
        ticker = ticker.upper()
        history = sorted([snapshot for snapshot in self.snapshots if snapshot.ticker == ticker and (year is None or snapshot.year <= year)], key=lambda item: item.year)
        if not history:
            raise KeyError(ticker)
        series = {
            "year": [snapshot.year for snapshot in history],
            "gamma_1": [snapshot.gamma_1 for snapshot in history],
            "gamma_2": [snapshot.gamma_2 for snapshot in history],
            "invariance": [snapshot.invariance for snapshot in history],
            "gravity": [self.compute_structural_gravity(snapshot) for snapshot in history],
        }
        drift = max(series["gamma_1"]) - min(series["gamma_1"])
        collapse = max(series["invariance"]) - min(series["invariance"])
        stability = _clamp(100.0 - 0.55 * drift - 0.45 * collapse)
        return {"series": series, "stability": _round(stability), "drift": _round(drift), "collapse": _round(collapse)}

    def lifecycle_observatory(self, ticker: Optional[str] = None, year: Optional[int] = None) -> Dict[str, Any]:
        active = [snapshot for snapshot in self.snapshots if year is None or snapshot.year <= year]
        if ticker is not None:
            active = [snapshot for snapshot in active if snapshot.ticker == ticker.upper()]
        if not active:
            return {"states": [], "transitions": [], "probabilities": {}}

        state_order = ["Substrate State", "Stable Regime", "Expansion State", "Frontier State", "Extraction Spiral"]
        state_counts = {state: 0 for state in state_order}
        transitions: Dict[Tuple[str, str], int] = {}
        by_ticker: Dict[str, List[GammaSnapshot]] = {}
        for snapshot in active:
            by_ticker.setdefault(snapshot.ticker, []).append(snapshot)

        for history in by_ticker.values():
            history.sort(key=lambda item: item.year)
            for index, snapshot in enumerate(history):
                state_counts[snapshot.lifecycle_state] = state_counts.get(snapshot.lifecycle_state, 0) + 1
                if index + 1 < len(history):
                    nxt = history[index + 1].lifecycle_state
                    transitions[(snapshot.lifecycle_state, nxt)] = transitions.get((snapshot.lifecycle_state, nxt), 0) + 1

        transition_rows = []
        source_totals: Dict[str, int] = {}
        for (source, target), count in transitions.items():
            source_totals[source] = source_totals.get(source, 0) + count
        for (source, target), count in transitions.items():
            transition_rows.append(
                {
                    "source": source,
                    "target": target,
                    "count": count,
                    "probability": _round(100.0 * count / max(1, source_totals[source])),
                }
            )

        total_states = sum(state_counts.values())
        states = [
            {
                "state": state,
                "count": count,
                "share": _round(100.0 * count / max(1, total_states)),
            }
            for state, count in state_counts.items()
            if count > 0
        ]
        probabilities = {
            state: _round(100.0 * count / max(1, total_states))
            for state, count in state_counts.items()
            if count > 0
        }
        return {"states": states, "transitions": transition_rows, "probabilities": probabilities}

    def _build_dependency_graph(self) -> None:
        seed_edges = [
            {"source": "NVDA", "target": "CUDA", "type": "platform", "weight": 0.96, "criticality": 0.94},
            {"source": "NVDA", "target": "TSMC", "type": "supply", "weight": 0.90, "criticality": 0.88},
            {"source": "ASML", "target": "TSMC", "type": "infrastructure", "weight": 0.95, "criticality": 0.97},
            {"source": "AAPL", "target": "iOS", "type": "platform", "weight": 0.98, "criticality": 0.93},
            {"source": "META", "target": "Llama", "type": "platform", "weight": 0.91, "criticality": 0.82},
            {"source": "STRIP", "target": "Payments Rails", "type": "infrastructure", "weight": 0.88, "criticality": 0.79},
            {"source": "OPENA", "target": "Model Stack", "type": "infrastructure", "weight": 0.93, "criticality": 0.87},
            {"source": "LINUX", "target": "Kernels", "type": "standard", "weight": 0.99, "criticality": 0.98},
        ]
        self.dependency_edges = seed_edges

    def search(self, query: str) -> List[Dict[str, Any]]:
        query = query.lower().strip()
        matches = []
        for snapshot in self.active_snapshots():
            haystack = " ".join([snapshot.ticker, snapshot.name, snapshot.sector, snapshot.classification, snapshot.lifecycle_state, snapshot.thesis_status]).lower()
            if query in haystack:
                matches.append(self._snapshot_detail(snapshot))
        return matches

    def summary(self) -> Dict[str, Any]:
        active = self.active_snapshots()
        return {
            "title": APP_TITLE,
            "entity_count": len(active),
            "snapshot_count": len(self.snapshots),
            "latest_year": max((snapshot.year for snapshot in self.snapshots), default=None),
            "watchlists": self.watchlists,
        }


ENGINE = GammaEngine()


def build_dashboard_html() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Project Gamma Infrastructure Intelligence Terminal</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    :root {
      --bg: #06111d;
      --panel: rgba(7, 19, 33, 0.92);
      --panel-2: rgba(10, 25, 42, 0.95);
      --line: rgba(130, 190, 255, 0.18);
      --text: #d7e7fb;
      --muted: #7f96b4;
      --accent: #67d4ff;
      --accent-2: #8ee38a;
      --warn: #ffb36b;
      --danger: #ff6b8b;
      --shadow: 0 18px 48px rgba(0, 0, 0, 0.45);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 15% 20%, rgba(73, 153, 255, 0.20), transparent 28%),
        radial-gradient(circle at 85% 10%, rgba(54, 213, 177, 0.14), transparent 24%),
        linear-gradient(180deg, #050b12 0%, #071622 50%, #05080d 100%);
      color: var(--text);
      min-height: 100vh;
    }
    .shell {
      display: grid;
      grid-template-rows: 72px 1fr;
      min-height: 100vh;
    }
    .topbar {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 14px 18px;
      background: linear-gradient(180deg, rgba(5,11,18,0.98), rgba(7,18,28,0.96));
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(18px);
    }
    .brand {
      display: flex;
      flex-direction: column;
      min-width: 240px;
    }
    .brand strong { font-size: 15px; letter-spacing: 0.14em; text-transform: uppercase; }
    .brand span { color: var(--muted); font-size: 12px; }
    .search {
      flex: 1;
      display: flex;
      gap: 8px;
      align-items: center;
      border: 1px solid var(--line);
      background: rgba(4, 13, 22, 0.72);
      border-radius: 14px;
      padding: 10px 12px;
      box-shadow: var(--shadow);
    }
    .search input, .search select {
      background: transparent;
      border: 0;
      color: var(--text);
      outline: none;
      font-size: 14px;
      width: 100%;
    }
    .search input::placeholder { color: #90a5c0; }
    .pill {
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 8px 12px;
      color: var(--text);
      background: rgba(8, 21, 35, 0.78);
      font-size: 12px;
      white-space: nowrap;
    }
    .layout {
      display: grid;
      grid-template-columns: 260px 1fr 340px;
      gap: 14px;
      padding: 14px;
    }
    .sidebar, .rightbar, .main, .card {
      border: 1px solid var(--line);
      border-radius: 20px;
      background: var(--panel);
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }
    .sidebar, .rightbar { padding: 14px; overflow: hidden; }
    .main { padding: 14px; display: grid; grid-template-rows: auto 1fr auto; gap: 12px; min-height: calc(100vh - 112px); }
    .section-title { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px; }
    .section-title h3 { margin: 0; font-size: 13px; letter-spacing: 0.12em; text-transform: uppercase; color: #a7c3df; }
    .section-title span { color: var(--muted); font-size: 12px; }
    .watch-item, .filter-item, .metric-row {
      display: flex; justify-content: space-between; align-items: center;
      padding: 10px 12px; border-radius: 14px; margin-bottom: 8px;
      background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.04);
      font-size: 13px;
    }
    .watch-item:hover, .filter-item:hover { background: rgba(103, 212, 255, 0.08); }
    .tiny { color: var(--muted); font-size: 12px; }
    .chart-grid {
      display: grid;
      grid-template-columns: 1.6fr 1fr;
      gap: 12px;
      min-height: 620px;
    }
    .chart-card { padding: 12px; border-radius: 18px; border: 1px solid var(--line); background: var(--panel-2); }
    .chart { width: 100%; height: 560px; }
    .mini-chart { width: 100%; height: 250px; }
    .detail { display: grid; gap: 10px; }
    .metric-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .metric { padding: 12px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.03); }
    .metric .label { display: block; color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; }
    .metric .value { display: block; font-size: 24px; margin-top: 5px; font-weight: 700; }
    .metric .sub { color: var(--muted); font-size: 12px; margin-top: 6px; }
    .footer-line { color: var(--muted); font-size: 12px; display: flex; justify-content: space-between; }
    .timeline { display: grid; gap: 10px; }
    input[type="range"] { width: 100%; accent-color: var(--accent); }
    .entity-title { font-size: 22px; margin: 0; }
    .badge { display: inline-flex; align-items: center; gap: 6px; border-radius: 999px; padding: 6px 10px; background: rgba(103,212,255,0.12); border: 1px solid rgba(103,212,255,0.18); color: var(--text); font-size: 12px; }
    .scroll { overflow: auto; max-height: calc(100vh - 180px); padding-right: 6px; }
  </style>
</head>
<body>
  <div class="shell">
    <div class="topbar">
      <div class="brand">
        <strong>Gamma Terminal</strong>
        <span>Infrastructure intelligence for structural necessity, reachability, and thesis health</span>
      </div>
      <div class="search">
        <input id="query" placeholder="Search ticker, company, sector, classification..." />
        <select id="yearSelect"></select>
        <button class="pill" id="searchBtn">Search</button>
      </div>
      <div class="pill" id="liveIndicator">Live stream ready</div>
    </div>
    <div class="layout">
      <aside class="sidebar">
        <div class="section-title"><h3>Watchlists</h3><span>Saved views</span></div>
        <div id="watchlists"></div>
        <div class="section-title"><h3>Filters</h3><span>Universe cuts</span></div>
        <div class="filter-item"><span>Sector</span><span class="tiny">All</span></div>
        <div class="filter-item"><span>Classification</span><span class="tiny">All</span></div>
        <div class="filter-item"><span>Lifecycle</span><span class="tiny">All</span></div>
        <div class="filter-item"><span>Gamma</span><span class="tiny">All</span></div>
        <div class="section-title"><h3>Metrics</h3><span>Live universe</span></div>
        <div id="summary"></div>
      </aside>
      <main class="main">
        <div class="timeline card" style="padding: 14px;">
          <div class="section-title"><h3>Time Engine</h3><span><span id="yearLabel"></span></span></div>
          <input id="timeline" type="range" min="2018" max="2030" step="1" value="2026" />
        </div>
        <div class="chart-grid">
          <div class="chart-card">
            <div class="section-title"><h3>Gamma State-Space Map</h3><span>Γ₂ vs Structural Gravity</span></div>
            <div id="stateSpace" class="chart"></div>
          </div>
          <div class="chart-card detail">
            <div>
              <div class="section-title"><h3>Entity Drilldown</h3><span>Selected company</span></div>
              <h2 class="entity-title" id="entityName">NVIDIA</h2>
              <div class="tiny" id="entityMeta">Semiconductors · Substrate</div>
            </div>
            <div class="metric-grid" id="metrics"></div>
            <div class="chart-card" style="padding: 10px;">
              <div class="section-title"><h3>Historical Evolution</h3><span>Trajectory</span></div>
              <div id="trajectory" class="mini-chart"></div>
            </div>
                        <div class="chart-card" style="padding: 10px;">
                            <div class="section-title"><h3>Structural Stability Monitor</h3><span>Invariant layer</span></div>
                            <div id="invariant" class="mini-chart"></div>
                        </div>
                        <div class="chart-card" style="padding: 10px;">
                            <div class="section-title"><h3>Lifecycle Observatory</h3><span>State transitions</span></div>
                            <div id="lifecycle" class="mini-chart"></div>
                        </div>
          </div>
        </div>
        <div class="chart-card">
          <div class="section-title"><h3>Attractor Landscape</h3><span>Potential field</span></div>
          <div id="attractor" class="mini-chart"></div>
        </div>
      </main>
      <aside class="rightbar">
        <div class="section-title"><h3>Thesis Intelligence</h3><span>Audit trail</span></div>
        <div id="thesis" class="scroll"></div>
        <div class="section-title" style="margin-top: 14px;"><h3>Validation Layer</h3><span>Hit rates</span></div>
        <div id="validation" class="scroll"></div>
      </aside>
    </div>
  </div>
  <script>
    const appState = { ticker: "NVDA", year: 2026, universe: [] };

    function metricCard(label, value, sub) {
      return `<div class="metric"><span class="label">${label}</span><span class="value">${value}</span><div class="sub">${sub || ""}</div></div>`;
    }

    async function loadSummary() {
      const summary = await fetch('/api/live').then(r => r.json());
      document.getElementById('summary').innerHTML = `
        <div class="metric-row"><span>Entities</span><strong>${summary.entity_count}</strong></div>
        <div class="metric-row"><span>Snapshots</span><strong>${summary.snapshot_count}</strong></div>
        <div class="metric-row"><span>Latest Year</span><strong>${summary.latest_year}</strong></div>
      `;
      const watchlists = document.getElementById('watchlists');
      watchlists.innerHTML = Object.entries(summary.watchlists).map(([name, items]) => `<div class="watch-item"><span>${name}</span><span class="tiny">${items.length} names</span></div>`).join('');
    }

    async function loadYears() {
      const years = Array.from({length: 13}, (_, i) => 2018 + i);
      const select = document.getElementById('yearSelect');
      select.innerHTML = years.map(year => `<option value="${year}">${year}</option>`).join('');
      select.value = appState.year;
      document.getElementById('timeline').value = appState.year;
      document.getElementById('yearLabel').textContent = String(appState.year);
    }

    async function loadStateSpace() {
      const params = new URLSearchParams({ year: String(appState.year) });
      const payload = await fetch(`/api/state-space?${params}`).then(r => r.json());
      appState.universe = payload.items;
      const trace = {
        x: payload.items.map(item => item.x),
        y: payload.items.map(item => item.y),
        mode: 'markers+text',
        text: payload.items.map(item => item.ticker),
                customdata: payload.items.map(item => item.customdata),
        textposition: 'top center',
        marker: {
          size: payload.items.map(item => item.size),
          color: payload.items.map(item => item.fill_color),
          line: { color: payload.items.map(item => item.border_color), width: 2 },
          opacity: 0.92
        },
        hovertemplate: '<b>%{text}</b><br>Γ₂=%{x:.1f}<br>Gravity=%{y:.1f}<extra></extra>'
      };
      const shapes = payload.zones.map(zone => ({
        type: 'rect', xref: 'x', yref: 'y', x0: zone.x0, x1: zone.x1, y0: zone.y0, y1: zone.y1,
        line: { width: 1, color: zone.color }, fillcolor: zone.fillcolor, layer: 'below'
      }));
      Plotly.newPlot('stateSpace', [trace], {
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', margin: { l: 58, r: 20, t: 20, b: 58 },
        xaxis: { title: 'Γ₂ Reachability Expansion', gridcolor: 'rgba(255,255,255,0.08)', zerolinecolor: 'rgba(255,255,255,0.12)' },
        yaxis: { title: 'Structural Gravity Index', gridcolor: 'rgba(255,255,255,0.08)', zerolinecolor: 'rgba(255,255,255,0.12)' },
        shapes,
        annotations: payload.zones.map(zone => ({ x: zone.label_x, y: zone.label_y, text: zone.label, showarrow: false, font: { color: zone.color, size: 11 } }))
      }, { displayModeBar: false, responsive: true });

      const plot = document.getElementById('stateSpace');
      plot.on('plotly_click', async evt => {
        const ticker = evt.points[0].customdata;
        if (ticker) {
          appState.ticker = ticker;
          await loadEntity(ticker);
        }
      });
    }

    async function loadEntity(ticker) {
      const data = await fetch(`/api/company/${ticker}`).then(r => r.json());
      const latest = data.latest;
      document.getElementById('entityName').textContent = latest.name;
      document.getElementById('entityMeta').textContent = `${latest.sector} · ${latest.classification} · ${latest.lifecycle_state}`;
      document.getElementById('metrics').innerHTML = [
        metricCard('Necessity', latest.necessity.toFixed(1), 'Structural necessity'),
        metricCard('Γ₁', latest.gamma_1.toFixed(1), 'Dependency density'),
        metricCard('Γ₂', latest.gamma_2.toFixed(1), 'Reachability expansion'),
        metricCard('Invariance', latest.invariance.toFixed(1), 'Structural stability'),
        metricCard('Composite Gamma', latest.composite_gamma.toFixed(1), 'Combined intensity'),
        metricCard('Thesis Health', latest.thesis_health.toFixed(1), latest.thesis_status),
      ].join('');

      Plotly.newPlot('trajectory', [{
        x: data.trajectory.map(row => row.year),
        y: data.trajectory.map(row => row.composite_gamma),
        mode: 'lines+markers',
        line: { color: '#67d4ff', width: 3 },
        marker: { size: 8, color: '#8ee38a' },
        hovertemplate: '%{x}<br>Composite Gamma=%{y:.1f}<extra></extra>'
      }], {
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', margin: { l: 46, r: 20, t: 12, b: 40 },
        xaxis: { title: 'Year', gridcolor: 'rgba(255,255,255,0.08)' },
        yaxis: { title: 'Composite Gamma', gridcolor: 'rgba(255,255,255,0.08)' }
      }, { displayModeBar: false, responsive: true });

            Plotly.newPlot('invariant', [{
                x: data.invariants.series.year,
                y: data.invariants.series.gamma_1,
                mode: 'lines+markers',
                name: 'Γ₁',
                line: { color: '#67d4ff', width: 2 },
                marker: { size: 7 },
                hovertemplate: '%{x}<br>Γ₁=%{y:.1f}<extra></extra>'
            }, {
                x: data.invariants.series.year,
                y: data.invariants.series.gamma_2,
                mode: 'lines+markers',
                name: 'Γ₂',
                line: { color: '#8ee38a', width: 2 },
                marker: { size: 7 },
                hovertemplate: '%{x}<br>Γ₂=%{y:.1f}<extra></extra>'
            }, {
                x: data.invariants.series.year,
                y: data.invariants.series.invariance,
                mode: 'lines+markers',
                name: 'Invariance',
                line: { color: '#ffb36b', width: 2 },
                marker: { size: 7 },
                hovertemplate: '%{x}<br>Invariance=%{y:.1f}<extra></extra>'
            }], {
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', margin: { l: 46, r: 20, t: 12, b: 40 },
                xaxis: { title: 'Year', gridcolor: 'rgba(255,255,255,0.08)' },
                yaxis: { title: 'Invariant Structure', gridcolor: 'rgba(255,255,255,0.08)', range: [0, 100] },
                legend: { orientation: 'h', x: 0, y: 1.15 }
            }, { displayModeBar: false, responsive: true });

            Plotly.newPlot('lifecycle', [{
                x: data.lifecycle.states.map(row => row.state),
                y: data.lifecycle.states.map(row => row.share),
                type: 'bar',
                marker: { color: ['#67d4ff', '#8ee38a', '#b57cff', '#ffb36b', '#ff6b8b'] },
                hovertemplate: '%{x}<br>Share=%{y:.1f}%<extra></extra>'
            }], {
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', margin: { l: 46, r: 20, t: 12, b: 80 },
                xaxis: { title: 'Lifecycle state', tickangle: -20, gridcolor: 'rgba(255,255,255,0.08)' },
                yaxis: { title: 'Share', gridcolor: 'rgba(255,255,255,0.08)', range: [0, 100] }
            }, { displayModeBar: false, responsive: true });

      document.getElementById('thesis').innerHTML = data.thesis.records.map(row => `
        <div class="watch-item">
          <span>${row.year} · ${row.status}</span>
          <span class="tiny">${row.health_score.toFixed(1)}</span>
        </div>`).join('');

      document.getElementById('validation').innerHTML = data.validation.rows.map(row => `
        <div class="watch-item">
          <span>${row.year} · ${row.prediction}</span>
          <span class="tiny">Hit ${row.hit_rate.toFixed(1)}%</span>
        </div>`).join('');
    }

    async function loadAttractor() {
      const payload = await fetch(`/api/attractor-field?year=${appState.year}`).then(r => r.json());
      Plotly.newPlot('attractor', [{
        z: payload.z,
        x: payload.x,
        y: payload.y,
        type: 'heatmap',
        colorscale: [
          [0, '#051018'], [0.25, '#0f2b45'], [0.5, '#165d7d'], [0.75, '#4ab4d1'], [1, '#9bf3ff']
        ],
        hovertemplate: 'x=%{x:.1f}<br>y=%{y:.1f}<br>potential=%{z:.3f}<extra></extra>'
      }], {
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', margin: { l: 46, r: 20, t: 12, b: 40 },
        xaxis: { title: 'Γ₂ Reachability Expansion', gridcolor: 'rgba(255,255,255,0.08)' },
        yaxis: { title: 'Structural Gravity', gridcolor: 'rgba(255,255,255,0.08)' }
      }, { displayModeBar: false, responsive: true });
    }

    async function refreshAll() {
      document.getElementById('yearLabel').textContent = String(appState.year);
      await Promise.all([loadStateSpace(), loadEntity(appState.ticker), loadAttractor()]);
    }

    document.getElementById('timeline').addEventListener('input', async event => {
      appState.year = Number(event.target.value);
      document.getElementById('yearSelect').value = String(appState.year);
      await refreshAll();
    });

    document.getElementById('yearSelect').addEventListener('change', async event => {
      appState.year = Number(event.target.value);
      document.getElementById('timeline').value = String(appState.year);
      await refreshAll();
    });

    document.getElementById('searchBtn').addEventListener('click', async () => {
      const q = document.getElementById('query').value.trim();
      if (!q) return;
      const result = await fetch(`/api/search?q=${encodeURIComponent(q)}`).then(r => r.json());
      if (result.matches.length > 0) {
        appState.ticker = result.matches[0].ticker;
        await loadEntity(appState.ticker);
      }
    });

    loadSummary().then(loadYears).then(refreshAll);
    setInterval(refreshAll, 15000);
  </script>
</body>
</html>"""


def build_state_space_payload(engine: GammaEngine, year: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    views = engine.active_views(year, filters)
    active_snapshots = engine.active_snapshots(year)
    x_values = [view.x for view in views]
    y_values = [view.y for view in views]
    if not views:
        return {"items": [], "zones": [], "x_range": [0, 100], "y_range": [0, 100]}

    x_low, x_high, y_low, y_high = engine._zone_thresholds(active_snapshots)
    zones = [
        {"label": "Legacy Anchors", "x0": min(x_values) - 10, "x1": x_low, "y0": y_high, "y1": max(y_values) + 10, "label_x": x_low - 4, "label_y": y_high + 5, "color": "#8ea0b8", "fillcolor": "rgba(142,160,184,0.08)"},
        {"label": "Substrate Core", "x0": x_high, "x1": max(x_values) + 10, "y0": y_high, "y1": max(y_values) + 10, "label_x": x_high + 4, "label_y": y_high + 5, "color": "#78d4ff", "fillcolor": "rgba(103,212,255,0.09)"},
        {"label": "Expansion Frontier", "x0": x_high, "x1": max(x_values) + 10, "y0": min(y_values) - 10, "y1": y_low, "label_x": x_high + 4, "label_y": y_low - 5, "color": "#8ee38a", "fillcolor": "rgba(142,227,138,0.09)"},
        {"label": "Extraction Endpoints", "x0": min(x_values) - 10, "x1": x_low, "y0": min(y_values) - 10, "y1": y_low, "label_x": x_low - 4, "label_y": y_low - 5, "color": "#ffb36b", "fillcolor": "rgba(255,179,107,0.08)"},
        {"label": "Competitive Basin", "x0": x_low, "x1": x_high, "y0": y_low, "y1": y_high, "label_x": (x_low + x_high) / 2, "label_y": (y_low + y_high) / 2, "color": "#b57cff", "fillcolor": "rgba(181,124,255,0.06)"},
    ]

    items = []
    for view in views:
        payload = view.to_dict()
        payload.update(
            {
                "ticker": view.snapshot.ticker,
                "name": view.snapshot.name,
                "sector": view.snapshot.sector,
                "fill_color": _fill_color(view.snapshot.lifecycle_state),
                "border_color": _border_color(view.snapshot.classification),
                "customdata": view.snapshot.ticker,
            }
        )
        items.append(payload)

    return {
        "items": items,
        "zones": zones,
        "x_range": [min(x_values) - 10, max(x_values) + 10],
        "y_range": [min(y_values) - 10, max(y_values) + 10],
    }


def build_architecture_contract(engine: GammaEngine) -> Dict[str, Any]:
    return {
        "system": APP_TITLE,
        "layers": {
            "presentation": ["Top bar", "Search command bar", "Timeline slider", "State-space map", "Entity drilldown", "Invariant monitor", "Thesis layer", "Validation layer"],
            "analytics": ["Gamma feature engine", "State classifier", "Attractor field engine", "Reachability engine", "Thesis scorer", "Validation evaluator"],
            "data": ["PostgreSQL snapshots", "Dependency edges", "Thesis logs", "Blind test results", "Watchlists", "Saved layouts"],
            "streaming": ["WebSocket/SSE live refresh", "Snapshot ingestion", "Search and crossfilter updates"],
        },
        "entities": {
            "companies": len({snapshot.ticker for snapshot in engine.snapshots}),
            "snapshots": len(engine.snapshots),
            "edges": len(engine.dependency_edges),
        },
        "api": [
            "/api/live",
            "/api/state-space",
            "/api/company/{ticker}",
            "/api/company/{ticker}/trajectory",
            "/api/company/{ticker}/thesis",
            "/api/company/{ticker}/invariants",
            "/api/company/{ticker}/dependencies",
            "/api/reachability",
            "/api/attractor-field",
            "/api/validation",
            "/api/search",
            "/api/watchlists",
            "/api/snapshot",
        ],
        "visualizations": [
            "Gamma State-Space Map",
            "Invariant Structure Monitor",
            "Historical Trajectory",
            "Attractor Landscape",
            "Dependency Network",
            "Lifecycle Observatory",
            "Thesis Intelligence",
            "Validation Rankings",
        ],
    }


def _fill_color(lifecycle_state: str) -> str:
    palette = {
        "Expansion State": "#67d4ff",
        "Stable Regime": "#8ee38a",
        "Substrate State": "#8f9fb4",
        "Extraction Spiral": "#ff8b8b",
        "Frontier State": "#ffb36b",
    }
    return palette.get(lifecycle_state, "#d7e7fb")


def _border_color(classification: str) -> str:
    palette = {
        "Substrate": "#d7fbff",
        "Extractor": "#ff8b8b",
        "Platform": "#67d4ff",
        "Bottleneck": "#ffb36b",
        "Frontier": "#8ee38a",
    }
    return palette.get(classification, "#d7e7fb")


def build_app(engine: GammaEngine) -> Any:
    if FastAPI is None:
        return None

    app = FastAPI(title=APP_TITLE, version="3.0.0")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return build_dashboard_html()

    @app.get("/api/live")
    def live() -> Dict[str, Any]:
        return engine.summary()

    @app.get("/api/architecture")
    def architecture() -> Dict[str, Any]:
        return build_architecture_contract(engine)

    @app.get("/api/state-space")
    def state_space(year: Optional[int] = Query(default=None), sector: Optional[str] = Query(default=None), classification: Optional[str] = Query(default=None), lifecycle_state: Optional[str] = Query(default=None), ticker: Optional[str] = Query(default=None)) -> Dict[str, Any]:
        filters = {"sector": sector, "classification": classification, "lifecycle_state": lifecycle_state, "ticker": ticker}
        return build_state_space_payload(engine, year=year, filters=filters)

    @app.get("/api/company/{ticker}")
    def company(ticker: str) -> Dict[str, Any]:
        try:
            return engine.company_detail(ticker)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=f"Unknown ticker: {exc.args[0]}")

    @app.get("/api/company/{ticker}/trajectory")
    def company_trajectory(ticker: str) -> Dict[str, Any]:
        return {"items": engine.trajectory(ticker)}

    @app.get("/api/company/{ticker}/thesis")
    def company_thesis(ticker: str) -> Dict[str, Any]:
        return engine.thesis_tracker(ticker)

    @app.get("/api/company/{ticker}/invariants")
    def company_invariants(ticker: str) -> Dict[str, Any]:
        return engine.invariant_profile(ticker)

    @app.get("/api/company/{ticker}/lifecycle")
    def company_lifecycle(ticker: str) -> Dict[str, Any]:
        return engine.lifecycle_observatory(ticker)

    @app.get("/api/company/{ticker}/dependencies")
    def company_dependencies(ticker: str) -> Dict[str, Any]:
        return engine.dependency_network(ticker)

    @app.get("/api/reachability")
    def reachability(ticker: Optional[str] = Query(default=None)) -> Dict[str, Any]:
        return engine.reachability_field(ticker)

    @app.get("/api/attractor-field")
    def attractor_field(year: Optional[int] = Query(default=None), grid_size: int = Query(default=36, ge=16, le=72)) -> Dict[str, Any]:
        return engine.attractor_field(year=year, grid_size=grid_size)

    @app.get("/api/validation")
    def validation(ticker: Optional[str] = Query(default=None)) -> Dict[str, Any]:
        return engine.validation_report(ticker)

    @app.get("/api/lifecycle-observatory")
    def lifecycle_observatory(ticker: Optional[str] = Query(default=None)) -> Dict[str, Any]:
        return engine.lifecycle_observatory(ticker)

    @app.get("/api/search")
    def search(q: str = Query(min_length=1)) -> Dict[str, Any]:
        return {"matches": engine.search(q)}

    @app.get("/api/watchlists")
    def watchlists() -> Dict[str, Any]:
        return engine.watchlists

    @app.post("/api/snapshot")
    def snapshot(payload: Dict[str, Any]) -> Dict[str, Any]:
        snapshot = engine.ingest_snapshot(payload)
        return snapshot.to_dict()

    return app


app = build_app(ENGINE)


def main() -> None:
    if app is None:
        print(json.dumps(ENGINE.summary(), indent=2))
        return

    try:
        import uvicorn
    except Exception:
        print(json.dumps(ENGINE.summary(), indent=2))
        return

    uvicorn.run(app, host="127.0.0.1", port=DEFAULT_PORT, reload=False)


if __name__ == "__main__":
    main()