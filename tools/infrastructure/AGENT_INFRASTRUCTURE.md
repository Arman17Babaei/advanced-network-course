# Agent Infrastructure

## Goal

Provide each student team with a shared AI coding environment that can use subscription-backed coding agents such as Codex while keeping usage controlled, observable, private to the team and teaching staff, and maintainable by the course staff.

## Requirements

- Works with **Codex CLI** and preferably the official Codex IDE extension.
- Supports **pooling multiple Codex/ChatGPT subscription accounts**.
- Supports **one isolated agent/access credential per team**.
- Records enough **request/response and usage information** to study how teams use coding agents.
- Can be deployed securely behind infrastructure controlled by the course.
- Does not require substantial course-specific maintenance.

## Nice to have

- Individual student API keys and attribution.
- Per-user or per-key quotas.
- Upstream subscription quota monitoring.
- Compatibility with other agents such as Claude Code, Cline, Cursor, etc.
- Easy export of logs for research and assessment.
- Automatic failover between equivalent upstream accounts.

Per-user quotas are **not currently required**. The acceptable fallback is one shared agent/quota pool per team.

## Tools considered

| Tool | Codex / IDE support | Account pooling | Per-key quota | Request / response logging | Assessment |
|---|---|---|---|---|---|
| **9Router** | **Excellent** | **Yes** | Not yet; requested | **Strong logging infrastructure** | **Selected** |
| **Sub2API** | Excellent | Yes | **Yes** | Mostly usage/accounting | Strong alternative |
| **CLIProxyAPI** | Excellent | Yes | No | Basic/usage logs | Good proxy, weak controls |
| **codex-pool** | Good | **Yes** | No | Usage-oriented | Simple pooling |
| **Code Proxy** | Good for OpenAI-compatible IDEs | Yes | **Yes** | Request history | Interesting but less mature |
| **codex-proxy** | **Excellent native Codex Responses support** | Yes | No | Metadata only by design | Good reference/building block |

## Selected solution: 9Router

9Router is currently the preferred base because it appears to be the most mature and broadly exercised option we examined for subscription-backed coding-agent routing. It supports Codex subscriptions through OAuth, multiple provider accounts, Codex CLI and other coding clients, usage tracking, account pooling, and quota-aware upstream routing.

### Proposed architecture

```text
Students / team
      |
      | team credential
      v
Reverse proxy
  - TLS
  - authentication
  - rate limiting
  - header sanitization
      |
      v
9Router
  - Codex protocol handling
  - subscription OAuth
  - account pooling
  - upstream quota tracking
  - usage / agent logging
      |
      v
Pooled Codex subscriptions
```

9Router should **not be directly exposed to students or the Internet**. Only the reverse proxy should reach it. The administrative dashboard should be restricted to the teaching team.

A reverse proxy also gives us an independent security boundary and leaves room to add course-specific authentication or quota enforcement later without maintaining a 9Router fork. This follows the standard API-gateway pattern of centralizing authentication, rate limiting, and access control at the gateway boundary.

## Current limitations

### Per-user quotas

9Router does not currently provide the per-key quota controls we originally considered. There is an upstream feature request for API-token limits. This is not blocking because the course can assign **one shared agent/quota pool per team**.

### Logging

9Router has request/usage logging and deep request-detail infrastructure, but before relying on it for research instrumentation we must verify that it captures the exact data we need for modern Codex sessions, including prompts, responses, tool calls, tool results, streaming, and session continuity.

### Security

9Router has had authentication/reverse-proxy security fixes in the past. Deployment should therefore:

- run a current pinned version;
- place 9Router behind a hardened reverse proxy;
- prevent direct network access to the 9Router port;
- sanitize forwarded/client-IP headers;
- keep the dashboard private;
- disable unnecessary exposed features; and
- review upgrades before deployment during the semester.

## Decision

Start with:

**one 9Router deployment + reverse proxy + one shared credential/agent allocation per student team.**

Do **not** initially build a custom per-user quota service.

The main remaining technical validation is whether 9Router's logging gives sufficiently complete and reliable agent-session data for course assessment and research.

## References

- 9Router: https://github.com/decolua/9router
- Sub2API: https://github.com/Wei-Shaw/sub2api
- CLIProxyAPI: https://github.com/router-for-me/CLIProxyAPI
- codex-pool: https://github.com/darvell/codex-pool
- Code Proxy: https://github.com/rodrigorodriguescosta/code-proxy
- codex-proxy: https://github.com/thezillo/codex-proxy
- OWASP Secure API Gateway Blueprint: https://owasp.org/www-project-secure-api-gateway-blueprint/
