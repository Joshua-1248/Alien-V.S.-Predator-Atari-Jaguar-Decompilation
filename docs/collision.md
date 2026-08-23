# Collision

Collision belongs to the 68000 gameplay domain and is tied to the native level/maze and actor-state representations.

The decompilation preserves original comparison/order behavior rather than replacing it with a modern physics abstraction. Integer/fixed-point edge cases are therefore part of retail behavior.

Future SDK editors should expose native collision data losslessly and preserve every field required for a round trip back to the Jaguar format.
