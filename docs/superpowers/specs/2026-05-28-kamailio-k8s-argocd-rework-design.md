# kamailio-k8s-argocd — Rework Design

**Date:** 2026-05-28
**Scope:** Full rework of the lab project: README rewrite, manifest cleanup, ArgoCD fixes, Python bug fixes.
**Target:** Learning / demo (optimize for clarity, not production hardening).

## Goals

1. README that explains the project at a glance, with a colored-badges row.
2. Working ArgoCD app-of-apps setup that syncs cleanly on a fresh Minikube.
3. Kamailio Deployment with sane defaults (resources, probes, securityContext, UDP+TCP).
4. Remove dead code (unused `statefulset.yaml`, unused `kamailio3s.py`).
5. Fix Python bugs that would crash request routing (`requests` not imported, `sys.exit()` in route).
6. sipexer CronJob targets the new UDP/TCP service.

## Non-goals

- HPA, NetworkPolicy, PodDisruptionBudget (lab scope).
- Image digest pinning.
- TLS / SIPS, authentication, registrar.

## Target architecture

```
ArgoCD (argocd ns)
  └─ root Application → application/
        ├─ Application: kamailio  → kamailio/overlays/  (Kustomize)
        └─ Application: sipexer   → sipexer/            (Kustomize)
                                        │
                                        ▼  namespace: kamailio
            Deployment kamailio (×2)
              └─ ghcr.io/kamailio/kamailio:5.8.4-bookworm
                 + ConfigMap (kamailio.cfg + kamailio3.py)
            Service kamailio-svc  (UDP 5060, TCP 5060)  LoadBalancer
            CronJob sipexer       (every 1m → kamailio-svc)
```

## File-level changes

| File | Action | Notes |
|---|---|---|
| `README.md` | Rewrite | Badges row, overview, architecture (Mermaid), quick start, testing, troubleshooting, cleanup |
| `LICENSE` | New | MIT |
| `application/root.yaml` | New | App-of-apps Application pointing at `application/` |
| `application/kamailio.yaml` | Edit | Drop broken `destination.name`, add `CreateNamespace=true`, ignore `root.yaml` via directory recurse=false |
| `application/sipexer.yaml` | Edit | Same fixes |
| `kamailio/base/deployment.yaml` | Rewrite | Resources, probes, securityContext, UDP+TCP ports |
| `kamailio/base/statefulset.yaml` | Delete | Dead (commented in kustomization) |
| `kamailio/base/service.yaml` | Edit | Expose UDP 5060 + TCP 5060, LoadBalancer |
| `kamailio/base/kamailio.cfg` | Edit | Listen UDP+TCP, real `request_route` via Python |
| `kamailio/base/kamailio3.py` | Rewrite | Drop `requests.get` (unimported), drop `sys.exit()`, proper OO routing |
| `kamailio/base/kamailio3s.py` | Delete | Dead (cfg uses `app_python3`, not `app_python3s`) |
| `kamailio/base/kustomization.yaml` | Edit | Switch resource to `deployment.yaml`, drop dead python file |
| `kamailio/overlays/kustomization.yaml` | Edit | Cleanup commented blocks; keep replicas=2 |
| `sipexer/kustomization.yaml` | New | Consistency with kamailio overlay |
| `sipexer/cronjob.yaml` | Edit | UDP target now that service supports it |

## README structure

```
# Kamailio on Kubernetes with ArgoCD
[badges row: Kubernetes, ArgoCD, Kamailio, Kustomize, SIP, License MIT]

> One-line tagline

## Overview
## Architecture (Mermaid)
## Repository Layout
## Prerequisites
## Quick Start
## How It Works (cfg + KSR Python)
## Load Testing with sipexer
## Troubleshooting
## Cleanup
## License
```

Badges use shields.io with `logo=` query param for colored icons.

## Validation

- `kubectl kustomize kamailio/overlays/` renders without error.
- `kubectl kustomize sipexer/` renders without error.
- `yamllint` (best-effort) on all YAML files.
- Manual review of README rendering.
