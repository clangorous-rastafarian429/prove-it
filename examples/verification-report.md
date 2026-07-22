# ProveIt verification report

Status: **PARTIALLY VERIFIED**

| Claim | Evidence | Result |
| --- | --- | --- |
| Invalid sessions return 401 | `python -m pytest tests/test_auth.py -k invalid_session -q` | Pass |
| Existing login flow still works | `python -m pytest tests/test_auth.py -q` | Pass, 18 tests |
| Application compiles | `npm run typecheck` | Pass |
| Production bundle builds | `npm run build` | Pass |
| Real OAuth callback succeeds | Provider sandbox exercise | Unavailable: credentials not present |

Unverified:

- The real OAuth callback remains unverified because the provider sandbox was unavailable.

Caveat:

- Local tests use the repository's OAuth fixture rather than the provider service.
