// Keep track of scripts that are already dynamically imported to save CPU cycles
const loadedScripts = new Set();

async function router(pageName) {
  try {
    // Get layout data from Python
    const response = await window.pywebview.api.changePage(pageName);

    if (response.status === "success") {
      const { content, script_url } = response;

      // If the browser hasn't executed this component file yet, import it.
      if (!loadedScripts.has(script_url)) {
        console.log(`Auto-importing script payload: ${script_url}`);
        await import(script_url);
        loadedScripts.add(script_url);
      }

      // Inject the element wrapper. The Web Component's lifecycle boots instantly
      document.getElementById("app-viewport").innerHTML = content;
    } else if (response.status === "unauthorized") {
      alert("Access Denied. Redirecting to login...");
      router("login");
    }
  } catch (error) {
    console.error("Autopilot router encountered an issue:", error);
  }
}

window.router = router;

// Global scope expose for view changes
window.addEventListener("pywebviewready", async () => {
  try {
    const assets = await window.pywebview.api.get_boot_assets();

    assets.css_files.forEach((cssUrl) => {
      if (!document.querySelector(`link[href="${cssUrl}"]`)) {
        console.log(`Auto-loading style sheet ruleset: ${cssUrl}`);

        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = cssUrl;

        document.head.appendChild(link);
      }
    });
  } catch (error) {
    console.error("Failed to parse and inject automated asset headers:", error);
  }

  router("homepage");
});
