# HTTP Service

Bugs that escape often sit at the running service: request decoding, routing,
authentication scope, and response shape. Tests that build the handler in
process are a strong base. They still skip the real binary's composition,
configuration, and auth wiring.

## Launch

- Boot the production entry point with local configuration. Avoid a test-only
  router.
- Bind it to loopback on a dynamic port, and record the port in the `up` state
  file.
- Turn off workers that send external messages unless they point at local
  sinks. See [external-services.md](external-services.md).
- **Readiness:**
  1. a liveness route responds;
  2. an unauthenticated call to a protected route returns 401;
  3. an authenticated call returns 200.

  Only all three together mean the service is ready.

## Drive

Call the service as a real client would: the real token, the real headers, and
request bodies shaped like the ones the client sends. Write journeys as tests
in the project's language, behind a build tag or separate target so normal test
runs skip them. They then run again exactly the same way, and the test runner's
structured output gives the verdict. Each journey checks:

- **The response.** Status, body, and shape. Validate the shape against the
  contract; see [contracts.md](contracts.md).
- **Denials.** A user with the wrong role or wrong tenant gets the denial, and
  no state changes. See [identity.md](identity.md).
- **Durable effects.** Read them after the call. A 2xx response is acceptance,
  not completion; work that was enqueued still has to run and finish.

## Gotchas

- Listeners that bind `0.0.0.0` expose the service. Prefer loopback.
- Client dev-server proxies, for example `proxy.conf.json` in Angular or
  Vite's `server.proxy`, may point at a shared or production API. Check them
  before you drive a browser against the local service.
- A deploy can ship code ahead of its migrations. After a deploy, run the
  journey checks against the deployed revision. See
  [post-deploy.md](post-deploy.md).
