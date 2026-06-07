# Rhino Plugin

`plugin/` will contain the future Rhino plugin that becomes the final user-facing UI.

The plugin should show preview results produced by the sandbox runner and display logs and errors clearly. It should provide an Import or Commit button for approved geometry.

Import or Commit is the only step that writes approved geometry into the active Rhino document. Preview results must remain non-destructive until a human user explicitly approves them through the plugin.
