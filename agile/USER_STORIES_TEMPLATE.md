# 📝 User Story Template

## User Story Format

```
As a [type of user],
I want [to perform some action],
So that [I can achieve some goal/benefit].
```

---

## Example User Stories (Portfolio)

### US-001: Vulnerability Report Export
**As a** security analyst,  
**I want** to export scan results to CSV sorted by severity,  
**So that** I can quickly prioritise remediation efforts.

**Story Points:** 5  
**Priority:** High  
**Sprint:** Sprint 2  

**Acceptance Criteria:**
- Given a valid OpenVAS XML file, when I run the scanner, then a CSV file is produced
- CSV rows are sorted by CVSS score descending
- All fields (host, port, severity, CVE, name, description, solution) are present
- A `--min-severity` flag filters out lower severity findings

**Tasks:**
- [ ] Implement `CSVExporter.export()` method
- [ ] Add severity-sorting logic to `ScanReport`
- [ ] Write unit tests for exporter
- [ ] Update README with usage example

---

### US-002: Sprint Board Display
**As a** developer,  
**I want** to view the current sprint board in the terminal,  
**So that** I can see what is in progress and what is done.

**Story Points:** 3  
**Priority:** High  
**Sprint:** Sprint 2  

**Acceptance Criteria:**
- Sprint name, goal, dates, and velocity are displayed
- Stories are grouped by status column
- Story ID, points, priority, and assignee are visible

---

## Estimation Reference (Planning Poker)

| Points | Complexity |
|--------|------------|
| 1 | Trivial — config change, typo fix |
| 2 | Very simple — small isolated change |
| 3 | Simple — clear path, minor effort |
| 5 | Medium — some design decisions needed |
| 8 | Complex — significant work, some unknowns |
| 13 | Very complex — large scope, many unknowns |
| 21 | Epic — needs breakdown into smaller stories |
