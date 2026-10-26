---
name: brand-domain-research
description: Brainstorm brand, product, or project names, suggest matching domain names, and check domain registration records. Trigger when the user asks for naming ideas, domain suggestions, a domain availability check, or a combination.
---

# Brand and domain research

Use this skill for naming and domain discovery. Reuse the product brief and preferences already in the conversation. Ask one concise question only when a missing constraint would materially change the candidates; otherwise state a reasonable assumption and proceed.

## Naming and domain suggestions

- Generate a focused shortlist of names that fits the product, audience, tone, and market. Add a brief reason for each candidate.
- Suggest matching domains only when requested or when the user asks for names and available domains together. Respect their preferred TLDs; otherwise choose a small set of sensible options rather than listing many extensions.
- When checking availability, verify the shortlisted domains before presenting them as likely unregistered. If the user asked only to brainstorm, mark domain status as unchecked.
- Search exact candidate names on the web when the user asks to vet them or when an obvious existing-brand collision could mislead the shortlist. Report visible conflicts, but do not claim this is legal or trademark clearance.

## RDAP lookup

Use RDAP for a read-only registration-record check. Normalize each candidate to a bare domain hostname: remove any scheme, path, query, or fragment, lowercase it, and convert internationalized names to their ASCII IDNA form for the request while preserving the user's spelling in the answer. Reject malformed hostnames. Never place unvalidated user text into shell syntax.

When shell access and `curl` are available, make one request per shortlisted domain, following redirects and setting a short timeout:

```sh
curl -sS -L --max-time 15 \
  -w '\nHTTP %{http_code}\n' \
  "https://rdap.org/domain/${domain}"
```

Interpret the HTTP status together with the JSON body:

- HTTP 200 with `objectClassName: "domain"` means RDAP returned a registration record.
- HTTP 404 with a not-found/no-data response means no registration record was returned and the name is likely unregistered. It does not prove that a registrar will let the user register it or what it will cost; names can be reserved or premium-priced.
- Timeouts, rate limits, malformed responses, and other errors are inconclusive. Do not call those domains available.

If shell access is unavailable, use the public RDAP lookup URL in a browser when available. Check only the candidate shortlist; do not bulk-scan names. Include the lookup date and label results as RDAP checks, not guaranteed purchase availability. Recommend a registrar lookup before the user acts on a promising name.

## Output

For a naming request, return a concise table with the candidate name, matching domain, RDAP status when checked, and a short rationale. Separate verified lookup results from unchecked ideas. Do not register, purchase, or submit a domain checkout.
