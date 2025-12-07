# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Personal Expense Tracker seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: [security@example.com](mailto:security@example.com)

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

- Type of issue (e.g., SQL injection, cross-site scripting, authentication bypass, etc.)
- Full paths of source file(s) related to the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours.
- **Updates**: We will keep you informed of the progress towards a fix and full announcement.
- **Credit**: We will credit you in our security advisory if you wish (unless you prefer to remain anonymous).

## Security Best Practices for Users

### Development Environment

1. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Use Virtual Environments**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Never Commit Sensitive Data**
   - Keep `.env` files out of version control
   - Use environment variables for secrets

### Production Deployment

1. **Database Security**
   - Use a production-grade database (PostgreSQL, MySQL)
   - Enable encryption at rest
   - Use strong, unique passwords
   - Limit database user permissions

2. **HTTPS/TLS**
   - Always use HTTPS in production
   - Use a reverse proxy (nginx, Caddy) for SSL termination
   - Enable HSTS headers

3. **Authentication & Authorization**
   - Implement user authentication before production use
   - Use secure session management
   - Implement rate limiting

4. **Input Validation**
   - The application uses Pydantic for input validation
   - Always validate and sanitize user inputs
   - Use parameterized queries (handled by SQLAlchemy)

5. **CORS Configuration**
   - Configure CORS appropriately for your domain
   - Do not use wildcard (`*`) in production

6. **Error Handling**
   - Do not expose stack traces in production
   - Log errors securely without sensitive data

## Known Security Considerations

### Current Implementation Notes

1. **No Authentication**: This is a demo/training application and does not include user authentication. For production use, implement authentication using:
   - FastAPI Security utilities
   - OAuth2 / JWT tokens
   - Session-based authentication

2. **CSRF Protection**: Form submissions should include CSRF tokens in production. Consider using:
   - `starlette-csrf` package
   - Custom CSRF middleware

3. **SQLite Limitations**: SQLite is used for development convenience. For production:
   - Migrate to PostgreSQL or MySQL
   - Enable connection encryption
   - Use connection pooling

4. **Rate Limiting**: No rate limiting is implemented. Consider:
   - `slowapi` package for FastAPI
   - Reverse proxy rate limiting

### Dependency Security

We regularly monitor dependencies for known vulnerabilities. To check your installation:

```bash
# Install safety checker
pip install safety

# Check for vulnerabilities
safety check -r requirements.txt
```

## Security Checklist for Production

Before deploying to production, ensure:

- [ ] Authentication system implemented
- [ ] HTTPS enabled with valid certificates
- [ ] Database credentials secured (not in code)
- [ ] Environment variables used for all secrets
- [ ] CORS configured for specific domains
- [ ] Rate limiting enabled
- [ ] Error pages don't expose sensitive info
- [ ] Logging configured without sensitive data
- [ ] Dependencies updated and scanned
- [ ] Input validation on all endpoints
- [ ] CSRF protection on forms
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified

## Contact

For any security-related questions, contact: [security@example.com](mailto:security@example.com)

---

Thank you for helping keep Personal Expense Tracker and its users safe!
