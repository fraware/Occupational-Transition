# Security

This project is a public research codebase. It is not a deployed service and does not collect user credentials in the repository.

If you discover a security issue (for example accidental committed secrets, or unsafe handling of downloaded data in scripts), please report it responsibly:

- Open a **private** security advisory on GitHub if the platform supports it for this repository, or
- Contact the repository maintainers directly with a clear description and steps to reproduce.

Do not post exploit details in public issues before a fix or maintainer response.

## Secrets

Do not commit API keys, passwords, or personal microdata. The [`.gitignore`](.gitignore) ignores common env files; verify with `git status` before every commit.
