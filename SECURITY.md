# Security Policy

## Supported Versions

We actively support the following versions of Reversi42 with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 6.3.x   | :white_check_mark: |
| 6.2.x   | :white_check_mark: |
| < 6.2   | :x:                |

## Security Updates

### Version 6.3.0 and later

All security vulnerabilities in dependencies have been resolved:

- **fastapi**: Updated to >=0.115.0 (resolves CVE vulnerabilities in older versions)
- **uvicorn**: Updated to >=0.32.0 (includes security patches)
- **websockets**: Updated to >=13.0 (fixes security issues in <12.0)
- **PyYAML**: Updated to >=6.0.2 (resolves CVE-2020-14343 and related issues)
- **python-multipart**: Updated to >=0.0.20 (security improvements)

### Previous Versions

Versions prior to 6.3.0 may contain known security vulnerabilities in dependencies. We strongly recommend upgrading to the latest version.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email security concerns to: luca.amore@gmail.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to resolve the issue before public disclosure.

## Security Best Practices

When using Reversi42:

- Always use the latest version
- Keep your Python environment updated
- Review dependency updates regularly
- Run security scans on your deployments
- Use HTTPS in production environments

## Dependency Security

We use automated tools to monitor dependencies:

- **Dependabot**: Weekly automated dependency updates
- **Safety**: Known vulnerability database scanning
- **pip-audit**: CVE database scanning
- **CodeQL**: Semantic code analysis

All security scans run automatically on:
- Every push to master
- Every pull request
- Weekly scheduled scans

## Security Advisories

For the latest security information, check:
- GitHub Security tab: https://github.com/lucaamore/reversi42/security
- CHANGELOG.md for security-related updates

