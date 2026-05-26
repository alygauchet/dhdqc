# DQC Module – Epic Prioritisation

## Document Information

| Field | Value |
|-------|-------|
| **Owner** | Aminata Ly-Gauchet|
| **Version** | 1.1 |
| **Date** | 2026-03-17 |
| **Status** | Final |
| **Category** | DQC – Planning |

---

## 1. Purpose

This document tracks and prioritises epics for the DQC (Data Quality Control) module. Use it to:

- Maintain a single view of all epics and their priority
- Support planning and roadmap decisions
- Align stakeholders on what to deliver first

---

## 2. Prioritisation Criteria

| Criterion | Description |
|-----------|-------------|
| **Business value** | Impact on data quality, user workflows, and compliance |
| **Dependencies** | Blocking or enabling other epics |
| **Effort** | Rough size/complexity (XS/S/M/L) |
| **Risk** | Technical or organisational risk |

---

## 3. Epic Register

| # | Epic ID | Epic Name | Description | Priority | Effort | Target Datahub | Status | Notes |
|---|---------|------------|-------------|----------|--------|----------------|--------|------|
| 1 | DHRD-117880 | Business rule based control type | DQC - Configure and execute control with business rule based control type - Date/String/Numeric | Critical | L | 7.5.2-0 | Done | Initial Requirement for S&P POC|
| 2 | DHRD-116411 | In List / Not In List Operators | DQC - Configure and execute control with in List / Not In List Operators | Critical | L | 7.6.0-0 | Done |Only for thick client|
| 3 | DHRD-118291 | Relative date operators | DQC - Configure and execute control with relative date operators | Critical | M | 7.6.0-0 | Done | Only for thick client |
| 4 | DHRD-119051 | Business rule based control type - Reference | DQC - Configure and execute control with business rule based control type for reference data type SMARTCLASS and SMARTLIST | High | S | 7.6.0-0 | Done  
| 5 | DHRD-117146 | Clause evaluation algorithm enhancement | DQC - Update clause evaluation algorithm to remove the unecessary clause evaluation | Medium | M | 7.6.0-0 | Done | |
| 6 | DHRD-119209 | Enhancement of executeBusinessQualityRules()| DQC - Enhancement of executeBusinessQualityRules to allow specific rules execution by adding argument ; update result format and add error details in control execution result | Low  | M | 7.7.0-0| Done | Remaining work from 7.6 |
| 7 | DHRD-119736 | Tracking activation/deactivation for control execution rule | DQC - Add tracking activation/deactivation on control execution rule positive results | Low | S | 7.7.0-0 | Done | Remaining work from 7.6 |
| 8 | DHRD-119233 | InList/NotInList and relative date in web client | DQC - Configure InList/Not in List and relative date operator in the web client using the new component| Critical | XS | 7.6.1-0 ; 7.7.0-0  | Done | Dependent from DHRD-117874 & DHRD-119111 handled by Front Squad|
| 9 | DHRD-119739 | Trigger object saved enhancement | DQC - Trigger object saved enhancement to only triggers controls for updated data only | Low | M | 7.7.0-0 | In Progress | Remaining work from 7.6 |
| 10 | DHRD-112665 | Trigger control rule upon field changed | DQC - Trigger control rule execution upon field changed | High | L | 7.7.0-0  | Planned | Review with Squad Front Done no impact on web ui - synchronise with Squad Front sev team|
| 11 | DHRD-113776 | Trigger control rule upon object to be saved | DQC - Trigger control on object to be saved - Not Interactive| High | M | 7.7.0-0 | Planned | Review the existing code to fix and enable the feature for import only 
| 12 | DHRD-92538 | Field from linked business class | DQC - Configure and execute control with field from linked business class | Critical | | 7.8.0-0 | Planned | Analysis and solution design to complete Ex. Equity data to be compared to the Equity Issuer's data |
| 13 | DHRD-110155 | Control Builder | DQC Control Builder - Configure control clause through a specific component in the web client | High | L | 7.8.0-0 | Planned | Analysis and solution design to complete Ex. Equity data to be compared to the Equity Issuer's data | Read Only and  Edit Mode using the API |
| 14 | DHRD-119182 | Execute control on historical time series data | DQC - Execute control on historical time series data | High| | | Backlog | Depend on approach validation for business dictionnary configuration|
| 15 | DHRD-117146 | Trigger control rule upon object to be saved | DQC - Trigger control on object to be saved - Interactive| Medium | L | 7.8.0-0  | Planned | Revieww the need to adapt to visage|
| 16 | DHRD-119182 | Execute control on historical time series data | DQC - Execute control on historical time series data | High| | | Backlog | Depend on approach validation for business dictionnary configuration|
| 17 | DHRD-119240 | Scope based control | DQC - Scope based control clause configuration and execution | Low | | | Backlog | To be used only with in List / not in List operators |
| 18 | DHRD-119182 | Execute control on historical time series data | DQC - Execute control on historical time series data | High|  | 7.X | Planned | Depend on approach validation for business dictionnary configuration|
| 19 | DHRD-112667 | Trigger control rule upon field to be changed | DQC - Trigger control rule execution upon field to be changed |Low | | | Backlog | |

**Priority scale:** Critical | High | Medium | Low  
**Effort scale:** XS (Extra Small) S (Small) | M (Medium) | L (Large)  
**Status:** Backlog | Planned | In Progress | Done

---

## 4. Notes

_Add any context, assumptions, or decisions here._
