# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 3.1.x   | :white_check_mark: |
| 3.0.x   | :white_check_mark: |
| < 3.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability within Reversi42, please send an email to:

**luca.amore@gmail.com**

### What to Include

Please include the following information in your report:

- **Type of vulnerability** (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- **Full paths of source file(s)** related to the vulnerability
- **Location** of the affected source code (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact** of the vulnerability, including how an attacker might exploit it

### Response Timeline

- **Within 48 hours**: We will acknowledge receipt of your vulnerability report
- **Within 7 days**: We will provide an initial assessment of the report
- **Within 30 days**: We will work to release a fix or provide a remediation timeline

### What to Expect

1. We will confirm the receipt of your vulnerability report
2. We will confirm the vulnerability and determine its impact
3. We will release a fix as soon as possible, depending on complexity
4. We will publicly acknowledge your responsible disclosure (unless you prefer to remain anonymous)

## Security Considerations for Users

### Safe Installation

1. **Download only from official sources**:
   - Official GitHub repository: https://github.com/lucaamore/reversi42
   - PyPI (if/when published)

2. **Verify dependencies**:
   ```bash
   pip install -r requirements.txt --require-hashes
   ```

3. **Use virtual environments**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Saved Game Files

- XOT files are **plain text** and safe to open
- Never execute `.xot` files directly
- Only load game files from trusted sources
- Saved games are stored in `saves/` directory by default

### Network Play (Future Feature)

Currently, Reversi42 does not support network play. When network features are added:

- They will use encryption (TLS/SSL)
- Authentication will be implemented
- Input validation will be enforced
- Rate limiting will be applied

### AI Safety

The AI engines in Reversi42:

- Do **not** execute arbitrary code
- Do **not** access files outside the project directory
- Do **not** make network connections
- Are **deterministic** and predictable
- Use bounded memory and CPU time

### Configuration Files

- Configuration files are JSON/text format
- Never execute configuration files
- Validate all user inputs
- Use safe parsing (no `eval()` or similar)

## Known Security Considerations

### 1. Resource Exhaustion

**Issue**: Deep AI searches (depth 12+) can consume significant CPU and memory.

**Mitigation**:
- Default depth limits are set conservatively (depth 9)
- Time limits can be configured
- Memory usage is bounded by transposition table size

### 2. File System Access

**Issue**: The application reads/writes saved games.

**Mitigation**:
- Saved games are restricted to `saves/` directory
- Path traversal is prevented
- File permissions are validated

### 3. Input Validation

**Issue**: User inputs (coordinates, file names) need validation.

**Mitigation**:
- All inputs are validated before processing
- Type checking is enforced
- Range checking is applied
- Malformed inputs are rejected gracefully

## Security Best Practices for Contributors

When contributing code:

1. **Never commit sensitive data**:
   - No API keys, passwords, or tokens
   - No personal information
   - Use `.gitignore` for local config files

2. **Validate all inputs**:
   - Check types and ranges
   - Sanitize file paths
   - Validate game states

3. **Use safe APIs**:
   - Avoid `eval()`, `exec()`, `__import__()`
   - Use `json.loads()` instead of `eval()`
   - Use `pathlib` for safe path handling

4. **Follow principle of least privilege**:
   - Don't request unnecessary permissions
   - Limit file system access
   - Minimize external dependencies

5. **Keep dependencies updated**:
   - Regularly update `requirements.txt`
   - Monitor for security advisories
   - Use `pip-audit` to check for vulnerabilities

## Security Tools

We recommend using these tools for security analysis:

```bash
# Check for known vulnerabilities in dependencies
pip install pip-audit
pip-audit

# Static security analysis
pip install bandit
bandit -r src/

# Dependency vulnerability checking
pip install safety
safety check
```

## Disclosure Policy

When a security issue is fixed:

1. A security advisory will be published on GitHub
2. The fix will be released as soon as possible
3. CVE will be requested for high-severity issues
4. Users will be notified through release notes
5. The reporter will be credited (if desired)

## Hall of Fame

We maintain a list of security researchers who have responsibly disclosed vulnerabilities:

*No security vulnerabilities have been reported yet.*

## Contact

For security concerns:
- **Email**: luca.amore@gmail.com
- **Subject**: `[SECURITY] Reversi42 - <brief description>`

For general questions:
- GitHub Issues: https://github.com/lucaamore/reversi42/issues
- GitHub Discussions: https://github.com/lucaamore/reversi42/discussions

---

**Thank you for helping keep Reversi42 and its users safe!** 🔒

