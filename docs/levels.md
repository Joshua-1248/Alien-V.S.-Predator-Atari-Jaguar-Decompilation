# Levels

Level/maze data supplies geometry/traversal, object placement and gameplay state to the runtime.

For the future SDK:

1. extract native user-owned level/resource data from the supplied `.jag`;
2. decode it into an editable intermediate representation;
3. preserve every native field required for a lossless round trip;
4. rebuild the native resource before cartridge packing;
5. structurally verify the rebuilt output.

Extracted retail level payloads must not be committed to this source repository.
