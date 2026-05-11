# providers layer

Cross-cutting concerns: auth, telemetry, connectors, flags.

This layer provides reusable functionality that cuts across multiple
other layers. Providers should be stateless when possible.

May import from: `types`, `config`, `utils`, `providers` (self-imports allowed)
