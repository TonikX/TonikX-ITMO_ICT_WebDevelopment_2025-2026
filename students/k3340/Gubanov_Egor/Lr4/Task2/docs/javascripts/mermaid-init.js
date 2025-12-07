document$.subscribe(function() {
  mermaid.initialize({ startOnLoad: false });
  mermaid.init(undefined, ".language-mermaid");
})

