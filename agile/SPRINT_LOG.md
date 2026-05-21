# 📋 Sprint Log

This file documents sprint goals, deliverables, and retrospectives for all portfolio projects.

---

## Sprint 1 — Foundation
**Dates:** 2026-04-01 → 2026-04-14  
**Goal:** Set up all project scaffolding and core data models  
**Team:** Remigiusz Ungeheuer (Solo)

### Delivered
| Story | Points | Status |
|-------|--------|--------|
| Set up repository structure | 1 | ✅ Done |
| Vulnerability Scanner: XML parser + data models | 5 | ✅ Done |
| Scrum Task Manager: SQLite schema + models | 5 | ✅ Done |
| Password Vault: Crypto engine + key derivation | 8 | ✅ Done |

**Velocity:** 19 story points  
**Sprint Review:** All acceptance criteria met. Data models are robust and well-tested.

### Retrospective
- ✅ **What went well:** TDD approach caught 3 bugs early in the crypto engine
- 🔧 **Improve:** Start documentation earlier (moved to Sprint 2 DoD)
- 🎯 **Action:** Add README template to project scaffolding

---

## Sprint 2 — Core Features
**Dates:** 2026-04-15 → 2026-04-28  
**Goal:** Implement core functionality for all four projects  
**Team:** Remigiusz Ungeheuer (Solo)

### Delivered
| Story | Points | Status |
|-------|--------|--------|
| Vulnerability Scanner: CSV exporter + severity filter | 5 | ✅ Done |
| Scrum Manager: Board display + story CRUD | 8 | ✅ Done |
| Password Vault: CRUD operations | 5 | ✅ Done |
| API Monitor: HTTP checker + threading | 8 | ✅ Done |

**Velocity:** 26 story points  
**Sprint Review:** Core features complete. Demo given to mentor — positive feedback.

### Retrospective
- ✅ **What went well:** Velocity increased from Sprint 1 (19→26 pts)
- 🔧 **Improve:** Thread safety in API monitor needs more testing
- 🎯 **Action:** Add `threading.Lock` for shared state in Sprint 3

---

## Sprint 3 — CLI & Polish
**Dates:** 2026-04-29 → 2026-05-12  
**Goal:** CLI interfaces, documentation, CI/CD pipeline  
**Team:** Remigiusz Ungeheuer (Solo)

### Delivered
| Story | Points | Status |
|-------|--------|--------|
| All projects: CLI with argparse | 8 | ✅ Done |
| GitHub Actions CI pipeline | 5 | ✅ Done |
| README.md for all projects | 3 | ✅ Done |
| Unit tests (pytest) | 5 | ✅ Done |
| Portfolio README | 3 | ✅ Done |

**Velocity:** 24 story points  
**Total Portfolio Velocity:** 69 story points across 3 sprints

### Retrospective
- ✅ **What went well:** CI pipeline automated testing from day 1 of this sprint
- 🔧 **Improve:** Could have written more integration tests
- 🎯 **Action:** Add integration tests as Sprint 4 backlog items

---

## 📊 Velocity Chart

```
Sprint 1: ██████████████████░ 19 pts
Sprint 2: ██████████████████████████ 26 pts  
Sprint 3: ████████████████████████ 24 pts
Average:  23 pts/sprint
```
