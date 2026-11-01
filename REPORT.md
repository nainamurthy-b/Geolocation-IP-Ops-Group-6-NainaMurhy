# TP 2 — Student Report: Modern Python Tooling & Live API Systems

**Student Name:** Naina Murthy Bandari  
**EPITA Login:** naina-murthy.bandari  
**Assigned API Group:** Group 6 — Geolocation & IP Ops (IPInfo.io)  
**Date:** 01/11/2026  
**TestPyPI Live Package URL:** https://test.pypi.org/project/epita-naina-murthy/

---

## Step 0: Assigned Group Verification

- **Group Command Output:** [Paste the output of your group verification command here]
- **Assigned Domain:** Group 6 - Geolocation & IP Ops (IPInfo.io)
- **Project Directory Name:** `epita_naina_murthy`

---

## Part 1: Environment Isolation with `uv`

### 1. Comparison of `sys.executable` & `sys.prefix`

```text
[Global sys.executable]:
/Library/Developer/CommandLineTools/usr/bin/python3

[uv sys.executable]:
/Users/nainamurthyb/epita_naina_murthy/.venv/bin/python

[Global sys.prefix]:
/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9

[uv sys.prefix]:
/Users/nainamurthyb/epita_naina_murthy/.venv
```

**Analysis:**

The global Python version is 3.9.6, while the project uses Python 3.14.8 through `uv`. `uv run` automatically uses the project's virtual environment without manual activation. This keeps project dependencies separate from global Python.

---

## Part 2: Live API Connection & 12-Factor Secret Hygiene

### 1. Git Status Output

```bash
$ git status

On branch main
Changes not staged for commit:
    modified: REPORT.md

no changes added to commit
```

**Additional verification:**

```text
$ git check-ignore .env
.env

$ git ls-files .env.template
.env.template
```

This shows that `.env` is ignored by Git and `.env.template` is tracked. This helps protect my API token from being shared accidentally.

### 2. Live API Response (Redacted)

```json
{
  "status": "LIVE_SUCCESS",
  "city": "Vitry-sur-Seine",
  "region": "Île-de-France",
  "country": "FR",
  "org": "AS12322 Free SAS",
  "postal": "94400",
  "timezone": "Europe/Paris"
}
```

### 3. Security Analysis

- **Why is storing secrets in environment variables superior to putting them in configuration files like `config.json` or `settings.yaml`? Give 2 reasons:**

  1. Environment variables keep API keys separate from the source code.
  2. They help prevent secrets from being accidentally shared when uploading code.

- **Why are default fallbacks like `os.getenv("API_KEY", "default")` dangerous for production secrets?**

  They can hide missing configuration and allow the application to run with an invalid or insecure API key.

---

## Part 3: Dependency Hygiene & Semantic Versioning

### 1. Dependency Tree (`uv tree`)

**Direct dependencies:**
- `requests`
- `python-dotenv`
- `rich`

**Development dependency:**
- `pytest`

**Transitive dependencies pulled in by `requests` / `rich`:**

- Requests: `certifi`, `charset-normalizer`, `idna`, `urllib3`
- Rich: `markdown-it-py`, `mdurl`, `pygments`

### 2. Lockfile & SemVer Analysis

1. **Meaning of version specifiers:**
   - `requests = "^2.31.0"`: Allows compatible versions below `3.0.0`.
   - `urllib3 = "~=2.2.1"`: Allows versions from `2.2.1` up to, but not including, `2.3.0`.
   - `rich = "==13.7.1"`: Allows only version `13.7.1`.

2. **If an upstream author releases `3.0.0`, will `^2.31.0` install it? Why or why not?**

   No. It does not allow version `3.0.0` because it restricts the major version to 2.

3. **What is the fundamental difference between `pyproject.toml` (declaration) and `uv.lock` (pinning)?**

   `pyproject.toml` declares the project dependencies, while `uv.lock` stores the exact resolved versions for installation.

4. **How do the SHA-256 cryptographic hashes in `uv.lock` protect against supply chain attacks?**

   They help verify that downloaded packages match the expected files and have not been modified.

---

## Part 4: Package Build & TestPyPI Deployment

### 1. TestPyPI Deployment Details

- **TestPyPI Package Name:** `epita-naina-murthy`
- **Public URL:** https://test.pypi.org/project/epita-naina-murthy/
- **CLI installation and execution output:**

```bash
$ uv run --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ epita-naina-murthy-cli

[Paste your fresh installation and execution output here]
```

The package was successfully published to TestPyPI. The local CLI successfully displayed live IPInfo data.

### 2. Packaging Theory

- **What is the difference between an `sdist` (.tar.gz) and a Wheel (.whl)?**

  An sdist contains the source code and build information, while a Wheel is a built package ready for installation.

- **Why are Wheels significantly faster and safer to install on client machines?**

  Wheels generally install faster because they do not need to be built from source on the client's machine.

---

## Part 5: Professional Debugging Challenge (No `print()`!)

### 1. Root Cause Analysis

- **Observed types in the debugger:**
  - Runtime type of `record['volume']`: `str`
  - Runtime type of `record['weight']`: `str`

- **Why did Python fail or miscalculate without crashing initially?**

  Python read the values as strings instead of numbers. This caused incorrect calculations because the values were not converted before mathematical operations.

### 2. Call Stack Inspection

The debugger was used in VS Code with a breakpoint inside `aggregate_telemetry()`.

```text
Frame 1: <module>
Frame 2: aggregate_telemetry()
Frame 3: compute_weighted_metric()
```

### 3. The Fix (Code Diff / Snippet)

I converted the values into floating-point numbers while parsing the records.

```python
"volume": float(parts[2]),
"weight": float(parts[4])
```

### 4. Verified Execution Output

```text
$ uv run python scripts/debug_challenge.py

Aggregate Result: {'successful_entries': 3, 'total_volume': 650.0, 'avg_volume': 216.66666666666666, 'high_impact_count': 1}
```


